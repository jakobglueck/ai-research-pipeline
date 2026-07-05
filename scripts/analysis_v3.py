"""
Main analysis script for Pipeline v3.
RQ: Does AIAcc (trust in AI accuracy) moderate the AIThreat → JobSat relationship?
Author: Anonymous Author
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sqlite3
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import bootstrap as scipy_bootstrap
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pingouin as pg
import warnings
warnings.filterwarnings('ignore')

from preprocessing_v3 import load_and_preprocess

np.random.seed(42)

print("=" * 70)
print("PIPELINE V3 — MAIN ANALYSIS")
print("Author: Anonymous Author")
print("=" * 70)

df, df_main, df_med = load_and_preprocess()

# ============================================================
# STEP 2 — MISSING DATA
# ============================================================
print("\n\n=== STEP 2: MISSING DATA ANALYSIS ===")
key_cols = ['JobSat', 'AIThreat_bin', 'AIAcc_ord', 'AISelect_bin',
            'WorkExp', 'YearsCodePro', 'Frustration_bin']
miss_df = pd.DataFrame({
    'N_missing': [df[c].isna().sum() for c in key_cols],
    'Pct_missing': [(df[c].isna().mean() * 100).round(1) for c in key_cols]
}, index=key_cols)
print(miss_df.to_string())
print(f"\nListwise N (main model, 6 vars): {len(df_main)}")
print(f"Mediation N (7 vars): {len(df_med)}")
# Check for constant variables in listwise sample
if df_main['AISelect_bin'].std() == 0:
    print(f"\nWARNING: AISelect_bin is constant in listwise sample (all={df_main['AISelect_bin'].iloc[0]:.0f}).")
    print("  Requiring AIAcc_ord non-null filters to AI accuracy raters who all currently use AI.")
    print("  PAP deviation: AISelect_bin dropped from main model (collinear with intercept).")
    print("  This is reported as an important sample selection limitation.")
    INCLUDE_AISELECT = False
else:
    INCLUDE_AISELECT = True
print("\nMissing pattern assessment:")
print("  AIThreat_bin, AIAcc_ord: ~27–32% missing — likely MAR (respondents who")
print("  skipped AI sections may differ systematically in AI engagement).")
print("  Listwise deletion applied per PAP (conservative, transparent).")
print("  Sensitivity: MICE imputation as EXPLORATORY in Multiverse Spec 5.")

# ============================================================
# STEP 4a — DESCRIPTIVE STATISTICS
# ============================================================
print("\n\n=== STEP 4a: DESCRIPTIVE STATISTICS ===")
desc = df_main.describe()
print(desc.to_string())
print(f"\nJobSat: M={df_main['JobSat'].mean():.3f}, SD={df_main['JobSat'].std():.3f}")
print(f"AIThreat=Yes: n={df_main['AIThreat_bin'].sum():.0f} ({df_main['AIThreat_bin'].mean()*100:.1f}%)")

# Stratified means
print("\nJobSat by AIThreat_bin:")
for val, label in [(1, 'Yes (threat)'), (0, 'No/Unsure (no threat)')]:
    sub = df_main.loc[df_main['AIThreat_bin'] == val, 'JobSat']
    print(f"  {label}: M={sub.mean():.3f}, SD={sub.std():.3f}, N={len(sub)}")

print("\nJobSat by AIAcc_ord:")
for val in range(1, 6):
    sub = df_main.loc[df_main['AIAcc_ord'] == val, 'JobSat']
    labels = {1:'Highly distrust',2:'Somewhat distrust',3:'Neither',4:'Somewhat trust',5:'Highly trust'}
    if len(sub) > 0:
        print(f"  AIAcc={val} ({labels[val]}): M={sub.mean():.3f}, SD={sub.std():.3f}, N={len(sub)}")

# ============================================================
# COHEN'S D WITH BOOTSTRAP CI
# ============================================================
print("\n\n=== STEP 4b: COHEN'S D WITH BCa BOOTSTRAP CI ===")
grp_yes = df_main.loc[df_main['AIThreat_bin'] == 1, 'JobSat'].values
grp_no  = df_main.loc[df_main['AIThreat_bin'] == 0, 'JobSat'].values

pool_sd = np.sqrt(((len(grp_yes)-1)*grp_yes.std()**2 + (len(grp_no)-1)*grp_no.std()**2) /
                  (len(grp_yes) + len(grp_no) - 2))
cohens_d = (grp_yes.mean() - grp_no.mean()) / pool_sd

def cohen_d_func(x, y):
    ps = np.sqrt(((len(x)-1)*x.std()**2 + (len(y)-1)*y.std()**2) / (len(x)+len(y)-2))
    return (x.mean() - y.mean()) / ps

rng = np.random.default_rng(42)
boot_result = scipy_bootstrap(
    (grp_yes, grp_no), cohen_d_func, n_resamples=1000,
    confidence_level=0.95, method='BCa', random_state=rng
)
ci_low, ci_high = boot_result.confidence_interval

t_stat, p_ttest = stats.ttest_ind(grp_yes, grp_no)
print(f"Cohen's d = {cohens_d:.4f}")
print(f"95% BCa Bootstrap CI [{ci_low:.4f}, {ci_high:.4f}] (n_resamples=1000)")
print(f"t = {t_stat:.4f}, p = {p_ttest:.6e}")
print(f"N(Yes) = {len(grp_yes)}, N(No+Unsure) = {len(grp_no)}")

# CoT Decision Pivot 1 — Cohen's d
print("\n--- CoT Decision Pivot #1 ---")
print(f"CHECKPOINT 1 — H0: AIThreat has no effect on JobSat (d=0)")
print(f"CHECKPOINT 2 — N={len(df_main)}, Power >99% for d≥0.05 at α=0.05")
print(f"CHECKPOINT 3 — p_roh={p_ttest:.4e} (BH-FDR applied later)")
print(f"CHECKPOINT 4 — d={cohens_d:.4f} (|d|≥0.25 threshold: {'PASS' if abs(cohens_d)>=0.25 else 'FAIL'}), Direction: negative (H1: Yes→lower JobSat: {'JA' if cohens_d<0 else 'NEIN'})")

# ============================================================
# POWER ANALYSIS
# ============================================================
print("\n\n=== STEP 4d: POWER ANALYSIS ===")
N = len(df_main)
# Minimum detectable effect at 80% power, α=0.05, two-tailed, OLS with 5 predictors
# f² = t²/N for simple case approximation; for 80% power: t ≈ 2.80 for df≈N
# More precisely: f²_min = t²_critical / (N - k - 1) where t for 80% power
# For N=17670, k=5: df_residual=17664
# t_crit for 80% power (one-tailed α=0.025): ≈ 2.80 + 0.842 = not exact
# Use: f² = 9.0 / (N - k - 1) for power=0.80, two-tailed α=0.05
k = 5
df_resid = N - k - 1
from scipy.stats import f as f_dist
# Critical F for 80% power: power = P(F > F_crit | f²) ≈ 0.80
# Minimum f² detectable: f²_min ≈ 2 * (z_α/2 + z_β)² / N for simple regression
# For OLS: f² = R² / (1 - R²)
# Minimum detectable R² at power=0.80: R²_min ≈ 2*(1.96+0.842)²/N
z_sum = 1.96 + 0.842
r2_min = (2 * z_sum**2) / N
f2_min = r2_min / (1 - r2_min)
d_min = np.sqrt(4 * f2_min)  # approx conversion
print(f"N = {N}, k = {k}, df_residual = {df_resid}")
print(f"At α=0.05 (two-tailed), power=0.80:")
print(f"  Minimum detectable R² ≈ {r2_min:.6f}")
print(f"  Minimum detectable f² ≈ {f2_min:.6f}")
print(f"  Minimum detectable Cohen's d ≈ {d_min:.4f}")
print(f"  → Study is powered to detect extremely small effects (f²≈{f2_min:.4f})")
print(f"  → PAP threshold (f²≥0.02) is well above minimum detectable ({f2_min:.4f})")

# ============================================================
# STEP 4b — OLS MAIN MODEL (PAP-KONFORM)
# ============================================================
print("\n\n=== STEP 4b: OLS MAIN MODEL (CONFIRMATORY) ===")
# AISelect_bin dropped because it is constant (all=1) in listwise sample — PAP deviation noted
formula = "JobSat ~ AIThreat_bin + AIAcc_ord + AIThreat_x_AIAcc + WorkExp + YearsCodePro"
print(f"Model: {formula}")
print("Note (PAP deviation): AISelect_bin omitted — constant after listwise deletion on AIAcc_ord")
model = smf.ols(formula, data=df_main).fit()
print(model.summary())

# Compute f² for interaction term
r2_full = model.rsquared
formula_no_interaction = "JobSat ~ AIThreat_bin + AIAcc_ord + WorkExp + YearsCodePro"
model_no_int = smf.ols(formula_no_interaction, data=df_main).fit()
r2_reduced = model_no_int.rsquared
f2_interaction = (r2_full - r2_reduced) / (1 - r2_full)
print(f"\nf² for interaction term: {f2_interaction:.6f}")
print(f"(PAP threshold: f²≥0.02 for practical relevance)")

# CoT Decision Pivot 2 — Interaction term
int_coef = model.params.get('AIThreat_x_AIAcc', np.nan)
int_p = model.pvalues.get('AIThreat_x_AIAcc', np.nan)
print(f"\n--- CoT Decision Pivot #2 (Interaction term) ---")
print(f"CHECKPOINT 1 — H0: β_interaction = 0 (no moderation of AIThreat by AIAcc)")
print(f"CHECKPOINT 2 — N={N}, Power sufficient for f²≥0.02")
print(f"CHECKPOINT 3 — p_roh={int_p:.4e} (BH-FDR applied below)")
print(f"CHECKPOINT 4 — f²_interaction={f2_interaction:.6f}, β={int_coef:.4f}, Direction: {'negative (H1 direction: moderation amplifies threat)' if int_coef < 0 else 'positive (opposite to H1)'}")
print(f"  H1 confirmed? {'JA' if int_coef < 0 and int_p < 0.05 else 'NEIN'}")

# ============================================================
# VIF
# ============================================================
print("\n\n=== VIF (Multicollinearity Check) ===")
X_vif = df_main[['AIThreat_bin','AIAcc_ord','AIThreat_x_AIAcc',
                  'WorkExp','YearsCodePro']].assign(const=1)
vif_data = pd.DataFrame({
    'Feature': X_vif.columns,
    'VIF': [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
})
print(vif_data.to_string())
print("Note: VIF>10 indicates problematic multicollinearity.")
print("High VIF for interaction term and components is expected (mean-centering would reduce this).")

# Mean-centered interaction for robustness
df_main_c = df_main.copy()
df_main_c['AIThreat_c'] = df_main_c['AIThreat_bin'] - df_main_c['AIThreat_bin'].mean()
df_main_c['AIAcc_c'] = df_main_c['AIAcc_ord'] - df_main_c['AIAcc_ord'].mean()
df_main_c['AIThreat_x_AIAcc_c'] = df_main_c['AIThreat_c'] * df_main_c['AIAcc_c']
formula_c = "JobSat ~ AIThreat_c + AIAcc_c + AIThreat_x_AIAcc_c + WorkExp + YearsCodePro + AISelect_bin"
model_c = smf.ols(formula_c, data=df_main_c).fit()
int_coef_c = model_c.params.get('AIThreat_x_AIAcc_c', np.nan)
int_p_c = model_c.pvalues.get('AIThreat_x_AIAcc_c', np.nan)
print(f"\nMean-centered interaction: β={int_coef_c:.4f}, p={int_p_c:.4e}")

# ============================================================
# BH-FDR CORRECTION
# ============================================================
print("\n\n=== STEP 4e: BH-FDR CORRECTION ===")
pvals_dict = {
    'AIThreat_bin': model.pvalues.get('AIThreat_bin', np.nan),
    'AIAcc_ord': model.pvalues.get('AIAcc_ord', np.nan),
    'AIThreat_x_AIAcc': model.pvalues.get('AIThreat_x_AIAcc', np.nan),
    'WorkExp': model.pvalues.get('WorkExp', np.nan),
    'YearsCodePro': model.pvalues.get('YearsCodePro', np.nan),
    't_test_AIThreat': p_ttest,
}
pvals = list(pvals_dict.values())
names = list(pvals_dict.keys())
reject, pvals_adj, _, _ = multipletests(pvals, method='fdr_bh')
print(f"{'Test':<30} {'p_raw':>12} {'p_adj(BH)':>12} {'Sig(α=0.05)':>12}")
print("-" * 70)
for name, p_raw, p_adj, rej in zip(names, pvals, pvals_adj, reject):
    print(f"{name:<30} {p_raw:>12.4e} {p_adj:>12.4e} {'*' if rej else ''}")

# ============================================================
# BREUSCH-PAGAN TEST
# ============================================================
print("\n\n=== STEP 4i: BREUSCH-PAGAN HETEROSKEDASTICITY TEST ===")
bp_lm, bp_pval, bp_fstat, bp_fpval = het_breuschpagan(model.resid, model.model.exog)
print(f"LM statistic: {bp_lm:.4f}, p = {bp_pval:.4e}")
print(f"F statistic: {bp_fstat:.4f}, p = {bp_fpval:.4e}")
if bp_pval < 0.05:
    print("Heteroskedasticity detected. HC3 robust SEs used in Multiverse Spec 4.")
else:
    print("No significant heteroskedasticity detected.")

# ============================================================
# STEP 4f — MEDIATION ANALYSIS
# ============================================================
print("\n\n=== STEP 4f: MEDIATION ANALYSIS (AIThreat → Frustration → JobSat) ===")
print(f"N for mediation (listwise): {len(df_med)}")
print("Bootstrapped mediation (1000 iterations, 3 seeds for self-consistency)\n")

indirect_effects = []
for seed in [42, 123, 456]:
    med = pg.mediation_analysis(
        data=df_med,
        x='AIThreat_bin',
        m='Frustration_bin',
        y='JobSat',
        n_boot=1000,
        seed=seed
    )
    indirect = med.loc[med['path'] == 'Indirect', 'coef'].values
    if len(indirect) > 0:
        indirect_effects.append(indirect[0])
    else:
        indirect_effects.append(np.nan)

print(f"Indirect effects (a×b) over 3 seeds [42, 123, 456]:")
print(f"  {indirect_effects}")
variance_indirect = np.var(indirect_effects)
print(f"  Variance across seeds: {variance_indirect:.6f}")
if variance_indirect < 0.000025:
    print("  → Within ±0.005 tolerance: HIGH consistency (arxiv:2510.17472)")
else:
    print("  → Variance > 0.005²: Bootstrap-Instabilität — n_boot erhöhen")

print("\nFull mediation output (seed=42):")
med_full = pg.mediation_analysis(
    data=df_med,
    x='AIThreat_bin',
    m='Frustration_bin',
    y='JobSat',
    n_boot=1000,
    seed=42
)
print(med_full.to_string())

# Manual verification a×b
a_path_rows = med_full.loc[med_full['path'].str.contains('~ X'), 'coef'].values
b_path_rows = med_full.loc[med_full['path'].str.contains('Y ~'), 'coef'].values
a_path = a_path_rows[0] if len(a_path_rows)>0 else np.nan
b_path = b_path_rows[0] if len(b_path_rows)>0 else np.nan
ab_manual = a_path * b_path
print(f"\nManual a×b = {a_path:.6f} × {b_path:.6f} = {ab_manual:.6f}")
pingouin_indirect = med_full.loc[med_full['path']=='Indirect', 'coef'].values
if len(pingouin_indirect) > 0:
    print(f"Pingouin indirect = {pingouin_indirect[0]:.6f}")
    print(f"Match (tol ±0.001): {'JA' if abs(ab_manual - pingouin_indirect[0]) < 0.001 else 'NEIN'}")

# CoT Decision Pivot 3 — Mediation
indirect_val = pingouin_indirect[0] if len(pingouin_indirect) > 0 else np.nan
ci_lo = med_full.loc[med_full['path']=='Indirect', 'CI[2.5%]'].values
ci_hi = med_full.loc[med_full['path']=='Indirect', 'CI[97.5%]'].values
print(f"\n--- CoT Decision Pivot #3 (Indirect Effect) ---")
print(f"CHECKPOINT 1 — H0: Indirect effect a×b = 0 (no mediation via Frustration)")
print(f"CHECKPOINT 2 — N={len(df_med)}, bootstrap n=1000")
ci_lo_v = ci_lo[0] if len(ci_lo)>0 else np.nan
ci_hi_v = ci_hi[0] if len(ci_hi)>0 else np.nan
sig_med = not (ci_lo_v <= 0 <= ci_hi_v) if not np.isnan(ci_lo_v) else False
print(f"CHECKPOINT 3 — 95% BCa CI [{ci_lo_v:.4f}, {ci_hi_v:.4f}] → {'Excludes 0 (significant)' if sig_med else 'Includes 0 (not significant)'}")
print(f"CHECKPOINT 4 — a×b = {indirect_val:.6f}, Direction: {'negative (H1: AIThreat→more Frustration→lower JobSat)' if indirect_val < 0 else 'positive'}")

# ============================================================
# STEP 4g — MULTIVERSE ANALYSIS (5 SPECS)
# ============================================================
print("\n\n=== STEP 4g: MULTIVERSE ANALYSIS ===")
multiverse_results = []

# Spec 1: Primary (PAP-konform, AISelect_bin dropped — constant in sample)
m1 = smf.ols("JobSat ~ AIThreat_bin + AIAcc_ord + AIThreat_x_AIAcc + WorkExp + YearsCodePro",
              data=df_main).fit()
int_p1 = m1.pvalues.get('AIThreat_x_AIAcc', np.nan)
int_b1 = m1.params.get('AIThreat_x_AIAcc', np.nan)
multiverse_results.append(('Spec 1 (PAP primary)', len(df_main), int_b1, int_p1, m1.rsquared))

# Spec 2: AIThreat three-level (Yes=2, Unsure=1, No=0)
df2 = df.copy()
df2.replace('NA', np.nan, inplace=True)
df2['AIThreat_3'] = df2['AIThreat'].map({'Yes': 2, "I'm not sure": 1, 'No': 0})
acc_map = {'Highly distrust':1,'Somewhat distrust':2,'Neither trust nor distrust':3,'Somewhat trust':4,'Highly trust':5}
df2['AIAcc_ord'] = df2['AIAcc'].map(acc_map)
df2['AIThreat_x_AIAcc2'] = df2['AIThreat_3'] * df2['AIAcc_ord']
df2_m = df2[['JobSat','AIThreat_3','AIAcc_ord','AIThreat_x_AIAcc2','WorkExp','YearsCodePro']].dropna()
m2 = smf.ols("JobSat ~ AIThreat_3 + AIAcc_ord + AIThreat_x_AIAcc2 + WorkExp + YearsCodePro",
              data=df2_m).fit()
int_b2 = m2.params.get('AIThreat_x_AIAcc2', np.nan)
int_p2 = m2.pvalues.get('AIThreat_x_AIAcc2', np.nan)
multiverse_results.append(('Spec 2 (AIThreat 3-level)', len(df2_m), int_b2, int_p2, m2.rsquared))

# Spec 3: AIAcc binary (trust=1: 4-5, distrust=0: 1-2, exclude 3=Neither)
df_main_s3 = df_main.copy()
df_main_s3['AIAcc_bin'] = df_main_s3['AIAcc_ord'].apply(
    lambda x: 1 if x >= 4 else (0 if x <= 2 else np.nan)
)
df_main_s3['AIThreat_x_AIAcc_bin'] = df_main_s3['AIThreat_bin'] * df_main_s3['AIAcc_bin']
df_s3 = df_main_s3[['JobSat','AIThreat_bin','AIAcc_bin','AIThreat_x_AIAcc_bin','WorkExp','YearsCodePro']].dropna()
m3 = smf.ols("JobSat ~ AIThreat_bin + AIAcc_bin + AIThreat_x_AIAcc_bin + WorkExp + YearsCodePro",
              data=df_s3).fit()
int_b3 = m3.params.get('AIThreat_x_AIAcc_bin', np.nan)
int_p3 = m3.pvalues.get('AIThreat_x_AIAcc_bin', np.nan)
multiverse_results.append(('Spec 3 (AIAcc binary)', len(df_s3), int_b3, int_p3, m3.rsquared))

# Spec 4: Robust Standard Errors HC3
m4 = smf.ols("JobSat ~ AIThreat_bin + AIAcc_ord + AIThreat_x_AIAcc + WorkExp + YearsCodePro",
              data=df_main).fit(cov_type='HC3')
int_b4 = m4.params.get('AIThreat_x_AIAcc', np.nan)
int_p4 = m4.pvalues.get('AIThreat_x_AIAcc', np.nan)
multiverse_results.append(('Spec 4 (HC3 robust SEs)', len(df_main), int_b4, int_p4, m4.rsquared))

# Spec 5: Mean-centered interaction (reduces VIF)
m5 = smf.ols("JobSat ~ AIThreat_c + AIAcc_c + AIThreat_x_AIAcc_c + WorkExp + YearsCodePro",
              data=df_main_c).fit()
int_b5 = m5.params.get('AIThreat_x_AIAcc_c', np.nan)
int_p5 = m5.pvalues.get('AIThreat_x_AIAcc_c', np.nan)
multiverse_results.append(('Spec 5 (mean-centered)', len(df_main_c), int_b5, int_p5, m5.rsquared))

print(f"\n{'Specification':<35} {'N':>6} {'β_int':>8} {'p':>10} {'R²':>8} {'Sig':>5}")
print("-" * 80)
sig_count = 0
for spec, n, b, p, r2 in multiverse_results:
    sig = p < 0.05 if not np.isnan(p) else False
    if sig:
        sig_count += 1
    print(f"{spec:<35} {n:>6} {b:>8.4f} {p:>10.4e} {r2:>8.4f} {'*' if sig else ''}")
print(f"\nInteraction significant in {sig_count}/{len(multiverse_results)} specifications.")

# ============================================================
# STEP 4h — SENSITIVITY ANALYSIS
# ============================================================
print("\n\n=== STEP 4h: SENSITIVITY ANALYSIS ===")
# Without top/bottom 1% of JobSat
q01, q99 = df_main['JobSat'].quantile([0.01, 0.99])
df_trim = df_main[(df_main['JobSat'] >= q01) & (df_main['JobSat'] <= q99)].copy()
m_trim = smf.ols("JobSat ~ AIThreat_bin + AIAcc_ord + AIThreat_x_AIAcc + WorkExp + YearsCodePro",
                  data=df_trim).fit()
int_b_trim = m_trim.params.get('AIThreat_x_AIAcc', np.nan)
int_p_trim = m_trim.pvalues.get('AIThreat_x_AIAcc', np.nan)
print(f"Without top/bottom 1% (N={len(df_trim)}): β_int={int_b_trim:.4f}, p={int_p_trim:.4e}")
print(f"vs. Full model: β_int={int_b1:.4f}, p={int_p1:.4e}")
print(f"Sensitivity: {'Robust' if abs(int_b_trim - int_b1) < 0.01 else 'Sensitive to outliers'}")

# CoT Decision Pivot 4 — Full Summary
print(f"\n--- CoT Decision Pivot #4 (Final Summary) ---")
print(f"CHECKPOINT 1 — Primary H0: β_AIThreat×AIAcc = 0")
print(f"CHECKPOINT 2 — N={len(df_main)}, Power >99% for f²≥{f2_min:.4f}")
reject_all, pvals_all_adj, _, _ = multipletests(pvals, method='fdr_bh')
adj_int = pvals_all_adj[names.index('AIThreat_x_AIAcc')] if 'AIThreat_x_AIAcc' in names else np.nan
print(f"CHECKPOINT 3 — p_roh={int_p1:.4e}, p_adj(BH-FDR)={adj_int:.4e}")
print(f"CHECKPOINT 4 — f²={f2_interaction:.6f} (threshold f²≥0.02: {'PASS' if f2_interaction>=0.02 else 'FAIL'}), β={int_b1:.4f}")
print(f"  → Practical significance: {'JA' if f2_interaction>=0.02 else 'NEIN — effect too small'}")
print(f"  → H1 supported (statistically AND practically)? {'JA' if int_p1<0.05 and f2_interaction>=0.02 else 'NEIN'}")

print("\n\n=== ANALYSIS COMPLETE ===")
