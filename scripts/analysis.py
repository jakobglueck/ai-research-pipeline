import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocessing import load_regression_data

cols, js, at, ycp, lc = load_regression_data()
n = len(js)

# --- Helper functions ---

def mean(v): return sum(v) / len(v)

def std(v, ddof=1):
    m = mean(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - ddof))

def cov(a, b):
    ma, mb = mean(a), mean(b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (len(a) - 1)

def pearson(a, b):
    return cov(a, b) / (std(a) * std(b))

def dot(a, b): return sum(x * y for x, y in zip(a, b))

def mat_vec_mult(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]

def transpose(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

def mat_mult(A, B):
    n, m, p = len(A), len(A[0]), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]

def mat_inv_3x3(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    if abs(det) < 1e-12:
        raise ValueError("Singular matrix")
    inv = [
        [(e*i - f*h)/det, (c*h - b*i)/det, (b*f - c*e)/det],
        [(f*g - d*i)/det, (a*i - c*g)/det, (c*d - a*f)/det],
        [(d*h - e*g)/det, (b*g - a*h)/det, (a*e - b*d)/det],
    ]
    return inv

def mat_inv_4x4(M):
    import functools
    # Use Gaussian elimination
    n = len(M)
    aug = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(M)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        if abs(aug[col][col]) < 1e-15:
            raise ValueError("Singular matrix")
        factor = aug[col][col]
        aug[col] = [x / factor for x in aug[col]]
        for row in range(n):
            if row != col:
                mult = aug[row][col]
                aug[row] = [aug[row][k] - mult * aug[col][k] for k in range(2 * n)]
    return [row[n:] for row in aug]


# --- OLS Regression via Normal Equations ---

def ols(X_cols, y):
    """X_cols: list of lists (each list is one predictor, length n).
    Returns b (coefficients), se, t, r2, r2adj, F."""
    n = len(y)
    k = len(X_cols)
    # Design matrix: [1, x1, x2, ...]
    X = [[1.0] + [X_cols[j][i] for j in range(k)] for i in range(n)]
    p = k + 1  # num params

    Xt = transpose(X)
    XtX = mat_mult(Xt, X)
    Xty = [dot(Xt[i], y) for i in range(p)]

    XtX_inv = mat_inv_4x4(XtX) if p == 4 else mat_inv_3x3(XtX)

    b = mat_vec_mult(XtX_inv, Xty)

    yhat = [dot(X[i], b) for i in range(n)]
    res = [y[i] - yhat[i] for i in range(n)]

    ss_res = sum(r ** 2 for r in res)
    y_mean = mean(y)
    ss_tot = sum((yi - y_mean) ** 2 for yi in y)
    r2 = 1 - ss_res / ss_tot
    r2adj = 1 - (1 - r2) * (n - 1) / (n - p)

    sigma2 = ss_res / (n - p)
    se = [math.sqrt(XtX_inv[j][j] * sigma2) for j in range(p)]
    t = [b[j] / se[j] for j in range(p)]

    # F-statistic
    ss_reg = ss_tot - ss_res
    df_reg, df_res = p - 1, n - p
    F = (ss_reg / df_reg) / (ss_res / df_res)

    return b, se, t, r2, r2adj, F, df_reg, df_res


# --- VIF ---

def compute_vif(X_cols):
    vifs = []
    for i, col_i in enumerate(X_cols):
        others = [X_cols[j] for j in range(len(X_cols)) if j != i]
        _, _, _, r2, _, _, _, _ = ols(others, col_i)
        vifs.append(1 / (1 - r2) if r2 < 1 else float('inf'))
    return vifs


# --- Descriptive statistics ---

print("=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)
print(f"N = {n}")

variables = [('JobSat', js), ('AIThreat_binary', at), ('YearsCodePro', ycp),
             ('log1p_ConvertedCompYearly', lc)]

print(f"\n{'Variable':<30} {'Mean':>8} {'SD':>8} {'Min':>8} {'Max':>8}")
print("-" * 66)
for name, v in variables:
    print(f"{name:<30} {mean(v):>8.4f} {std(v):>8.4f} {min(v):>8.4f} {max(v):>8.4f}")

print()
print("Correlation matrix:")
var_names = [n for n, _ in variables]
vals = [v for _, v in variables]
header = f"{'':30}" + "".join(f"{n[:8]:>10}" for n in var_names)
print(header)
for i, (ni, vi) in enumerate(variables):
    row = f"{ni:<30}"
    for j, (nj, vj) in enumerate(variables):
        row += f"{pearson(vi, vj):>10.4f}"
    print(row)

# --- Model 1: baseline (YearsCodePro + log_comp) ---
print()
print("=" * 60)
print("MODEL 1: YearsCodePro + log1p_Comp → JobSat (baseline)")
print("=" * 60)
b1, se1, t1, r2_1, r2adj_1, F1, df1, dfr1 = ols([ycp, lc], js)
labels1 = ['Intercept', 'YearsCodePro', 'log1p_Comp']
print(f"\n{'Predictor':<30} {'b':>10} {'SE':>10} {'t':>10}")
print("-" * 62)
for lab, bi, si, ti in zip(labels1, b1, se1, t1):
    print(f"{lab:<30} {bi:>10.4f} {si:>10.4f} {ti:>10.4f}")
print(f"\nR² = {r2_1:.6f}, R²adj = {r2adj_1:.6f}, F({df1},{dfr1}) = {F1:.4f}")

# --- Model 2: full (AIThreat + YearsCodePro + log_comp) ---
print()
print("=" * 60)
print("MODEL 2: AIThreat + YearsCodePro + log1p_Comp → JobSat")
print("=" * 60)
b2, se2, t2, r2_2, r2adj_2, F2, df2, dfr2 = ols([at, ycp, lc], js)
labels2 = ['Intercept', 'AIThreat_binary', 'YearsCodePro', 'log1p_Comp']
print(f"\n{'Predictor':<30} {'b':>10} {'SE':>10} {'t':>10}")
print("-" * 62)
for lab, bi, si, ti in zip(labels2, b2, se2, t2):
    print(f"{lab:<30} {bi:>10.6f} {si:>10.6f} {ti:>10.4f}")
print(f"\nR² = {r2_2:.6f}, R²adj = {r2adj_2:.6f}, F({df2},{dfr2}) = {F2:.4f}")

delta_r2 = r2_2 - r2_1
print(f"\nΔR² (adding AIThreat) = {delta_r2:.6f}")

# Standardized betas
sd_y = std(js)
sd_at = std(at)
sd_ycp = std(ycp)
sd_lc = std(lc)
print(f"\nStandardized betas (Model 2):")
print(f"  β_AIThreat  = {b2[1] * sd_at / sd_y:.4f}")
print(f"  β_YearsCode = {b2[2] * sd_ycp / sd_y:.4f}")
print(f"  β_logComp   = {b2[3] * sd_lc / sd_y:.4f}")

# VIF
print()
print("VIF (Model 2):")
vifs = compute_vif([at, ycp, lc])
vif_names = ['AIThreat_binary', 'YearsCodePro', 'log1p_Comp']
for name, v in zip(vif_names, vifs):
    print(f"  {name}: VIF = {v:.4f}")

# Cohen's f² for AIThreat in full model
# f² = (R²_full - R²_baseline) / (1 - R²_full)
f2_ai = delta_r2 / (1 - r2_2)
print(f"\nCohen's f² (AIThreat unique contribution) = {f2_ai:.6f}")

# Eta² (from bivariate ANOVA for comparison)
print(f"\nBivariate Eta²(AIThreat→JobSat) = 0.0122 [from Stage 1]")
print(f"Bivariate r(Comp, JobSat) = 0.0718 [from Stage 1]")
print(f"Bivariate r(AIThreat_bin, JobSat) = -0.1106 [from Stage 1]")

# Descriptive: mean JobSat by AIThreat
import sqlite3
BASE2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conn = sqlite3.connect(os.path.join(BASE2, 'db', 'survey.db'))
cur = conn.cursor()

print()
print("=" * 60)
print("DESCRIPTIVE: Mean JobSat by AIThreat (full sample, no listwise)")
print("=" * 60)
cur.execute("""
    SELECT AIThreat, AVG(JobSat), COUNT(*),
           SUM((JobSat - (SELECT AVG(JobSat) FROM survey WHERE AIThreat=s.AIThreat AND JobSat IS NOT NULL)) *
               (JobSat - (SELECT AVG(JobSat) FROM survey WHERE AIThreat=s.AIThreat AND JobSat IS NOT NULL)))
    FROM survey s
    WHERE AIThreat IN ('Yes','No') AND JobSat IS NOT NULL
    GROUP BY AIThreat
""")
for row in cur.fetchall():
    sd_val = math.sqrt(row[3] / (row[2] - 1)) if row[2] > 1 else 0
    print(f"  AIThreat={row[0]}: M={row[1]:.4f}, SD={sd_val:.4f}, N={row[2]}")

conn.close()
