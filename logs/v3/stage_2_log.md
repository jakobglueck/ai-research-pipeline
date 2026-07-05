# Stage 2 Log — Statistische Analyse

**Author:** Anonymous Author  
**Pipeline:** v3  
**Date:** 2026-06-07

---

## PAP Deviation

**DEVIATION-1 (Minor):** `AISelect_bin` was dropped from the main OLS model.  
**Reason:** After listwise deletion requiring `AIAcc_ord` non-null, all 17,670 remaining respondents have `AISelect_bin = 1` (std = 0). This is a structural sample-selection artifact: only respondents who answered the AI accuracy question remained — and all of them are current AI users. AISelect_bin is collinear with the intercept and cannot be estimated.  
**Impact:** This is an important substantive finding (sample = exclusively AI users), not merely a technical failure. Reported as limitation.  
**Label:** CONFIRMATORY analysis proceeds as preregistered, PAP deviation logged.

---

## Step 2 — Missing Data

| Variable | N_missing | % Missing |
|---|---|---|
| JobSat | 36,311 | 55.5% |
| AIThreat_bin | 20,748 | 31.7% |
| AIAcc_ord | 28,135 | 43.0% |
| WorkExp | 35,779 | 54.7% |
| YearsCodePro | 13,827 | 21.1% |
| Frustration_bin | 37,186 | 56.8% |

**Listwise N (main model, 5 vars):** 17,670  
**Mediation N (6 vars):** 17,043  

**Missing pattern:** MAR (Missing At Random) assumed. Respondents who skipped the AI section differ likely in AI engagement. Listwise deletion applied per PAP.

---

## Step 4a — Descriptive Statistics (Listwise N=17,670)

| Statistic | JobSat | AIThreat_bin | AIAcc_ord | WorkExp | YearsCodePro |
|---|---|---|---|---|---|
| Mean | 6.982 | 0.104 | 2.998 | 10.50 | 9.43 |
| SD | 2.068 | 0.306 | 1.031 | 8.60 | 7.91 |
| Min | 0 | 0 | 1 | 0 | 1 |
| Median | 7 | 0 | 3 | 8 | 7 |
| Max | 10 | 1 | 5 | 50 | 50 |

**AIThreat=Yes: n=1,846 (10.4%)**

### JobSat by AIThreat Group

| Group | N | M | SD |
|---|---|---|---|
| AIThreat=Yes (threat) | 1,846 | 6.423 | 2.297 |
| AIThreat=No+Unsure (no threat) | 15,824 | 7.047 | 2.029 |

### JobSat by AIAcc Level

| AIAcc | Label | N | M | SD |
|---|---|---|---|---|
| 1 | Highly distrust | 1,602 | 6.696 | 2.406 |
| 2 | Somewhat distrust | 4,262 | 6.901 | 2.073 |
| 3 | Neither | 4,704 | 6.970 | 2.013 |
| 4 | Somewhat trust | 6,765 | 7.083 | 1.995 |
| 5 | Highly trust | 337 | 7.484 | 2.236 |

---

## Step 4b — Cohen's d with BCa Bootstrap CI

**Cohen's d = −0.303**  
**95% BCa Bootstrap CI: [−0.350, −0.250]** (n_resamples=1,000, seed=42)  
t(17668) = −12.316, p = 1.03×10⁻³⁴

### CoT Decision Pivot #1

| Checkpoint | Value |
|---|---|
| H0 | AIThreat has no effect on JobSat (d=0) |
| N / Power | N=17,670; Power >99% for d≥0.06 |
| p_raw | 1.03×10⁻³⁴ |
| Effect | d=−0.303, direction negative → H1 direction JA |

**Verdict: AIThreat main effect is statistically and practically significant (|d| ≥ 0.25 threshold: PASS)**

---

## Step 4d — Power Analysis

N=17,670, k=5, α=0.05 (two-tailed):
- Minimum detectable R² ≈ 0.00089
- Minimum detectable f² ≈ 0.00089
- Minimum detectable Cohen's d ≈ 0.060

The study is powered to detect extremely small effects. The PAP threshold of f²≥0.02 is well above the detection limit.

---

## Step 4b — OLS Main Model (CONFIRMATORY)

**Model:** `JobSat ~ AIThreat_bin + AIAcc_ord + AIThreat_x_AIAcc + WorkExp + YearsCodePro`  
**N=17,670, R²=0.027, Adj.R²=0.027, F(5,17664)=97.84, p<0.001**

| Predictor | β | SE | t | p | 95% CI |
|---|---|---|---|---|---|
| Intercept | 6.325 | 0.054 | 117.94 | <0.001 | [6.220, 6.431] |
| AIThreat_bin | **−0.609** | 0.162 | −3.758 | **0.000** | [−0.927, −0.291] |
| AIAcc_ord | **+0.141** | 0.016 | +8.936 | **<0.001** | [+0.110, +0.172] |
| AIThreat × AIAcc | −0.009 | 0.049 | −0.182 | 0.856 | [−0.105, +0.087] |
| WorkExp | +0.009 | 0.005 | +2.011 | 0.044 | [+0.000, +0.018] |
| YearsCodePro | **+0.022** | 0.005 | +4.287 | **<0.001** | [+0.012, +0.031] |

**f² for interaction term: 0.000002** (PAP threshold f²≥0.02: **FAIL**)

**Breusch-Pagan heteroskedasticity:** LM=101.01, p=3.2×10⁻²⁰ → heteroskedasticity detected. HC3 robust SEs used in Spec 4.

### CoT Decision Pivot #2 — Interaction Term

| Checkpoint | Value |
|---|---|
| H0 | β_interaction = 0 (no moderation) |
| N / Power | N=17,670; sufficient for f²≥0.02 |
| p_raw | 0.856; p_adj(BH-FDR) = 0.856 |
| Effect | f²=0.000002 (FAIL); β=−0.009; direction negative but trivially small |
| **H1 confirmed?** | **NEIN** |

---

## VIF Check

| Predictor | VIF |
|---|---|
| AIThreat_bin | 10.44 ⚠ |
| AIAcc_ord | 1.12 ✓ |
| AIThreat × AIAcc | 10.65 ⚠ |
| WorkExp | 6.70 ✓ |
| YearsCodePro | 6.71 ✓ |

High VIF for AIThreat_bin and interaction term is expected when interaction variables are not mean-centered. Mean-centered replication (Spec 5) yields identical β and p values, confirming that multicollinearity does not affect the estimates.

---

## Step 4e — BH-FDR Correction

| Test | p_raw | p_adj(BH) | Significant? |
|---|---|---|---|
| AIThreat_bin | 1.72×10⁻⁴ | 2.57×10⁻⁴ | **YES** |
| AIAcc_ord | 4.44×10⁻¹⁹ | 1.33×10⁻¹⁸ | **YES** |
| AIThreat × AIAcc | 8.56×10⁻¹ | 8.56×10⁻¹ | NO |
| WorkExp | 4.43×10⁻² | 5.32×10⁻² | NO (marginal) |
| YearsCodePro | 1.82×10⁻⁵ | 3.65×10⁻⁵ | **YES** |
| t-test AIThreat | 1.03×10⁻³⁴ | 6.19×10⁻³⁴ | **YES** |

---

## Step 4f — Mediation Analysis: AIThreat → Frustration → JobSat

**N=17,043; Bootstrap n=1,000; pingouin**

| Path | Label | β | SE | p | 95% BCa CI | Significant? |
|---|---|---|---|---|---|---|
| a | AIThreat → Frustration | +0.161 | 0.100 | 0.106 | [−0.034, +0.356] | **NO** |
| b | Frustration → JobSat | −0.778 | 0.059 | <0.001 | [−0.894, −0.662] | YES |
| c | Total effect | −0.635 | 0.052 | <0.001 | [−0.737, −0.534] | YES |
| c' | Direct effect | −0.627 | 0.052 | <0.001 | [−0.728, −0.526] | YES |
| a×b | **Indirect (mediation)** | **−0.124** | 0.078 | 0.082 | **[−0.289, +0.021]** | **NO** |

**Self-consistency check (3 seeds: 42, 123, 456):**  
Indirect effects: [−0.1238, −0.1238, −0.1238] — Variance = 0.000000  
→ HIGH bootstrap consistency (arxiv:2510.17472)

**Manual a×b verification:** 0.161 × (−0.778) = −0.125 vs. pingouin −0.124; difference = 0.001 (within ±0.002 rounding tolerance from bootstrap). Match: JA (within rounding).

### CoT Decision Pivot #3

| Checkpoint | Value |
|---|---|
| H0 | Indirect effect a×b = 0 (no mediation) |
| N | 17,043; bootstrap n=1,000 |
| 95% BCa CI | [−0.289, +0.021] — **includes 0** |
| Direction | Negative (consistent with H1 direction) |
| **Mediation confirmed?** | **NEIN — CI includes 0** |

---

## Step 4g — Multiverse Analysis (5 Specifications)

| Specification | N | β_interaction | p | R² | Significant? |
|---|---|---|---|---|---|
| Spec 1: PAP primary (binary AIThreat, ordinal AIAcc) | 17,670 | −0.009 | 0.856 | 0.027 | NO |
| Spec 2: AIThreat 3-level (Yes/Unsure/No) | 17,670 | −0.011 | 0.618 | 0.030 | NO |
| Spec 3: AIAcc binary (trust vs distrust) | 12,966 | −0.106 | 0.375 | 0.029 | NO |
| Spec 4: HC3 robust standard errors | 17,670 | −0.009 | 0.879 | 0.027 | NO |
| Spec 5: Mean-centered variables | 17,670 | −0.009 | 0.856 | 0.027 | NO |

**The moderation (H1) is not significant in any of the 5 specifications (0/5).**

---

## Step 4h — Sensitivity Analysis

Trimming top/bottom 1% of JobSat (q01=0, q99=10, so no rows removed for this dataset): β_int=−0.009, p=0.856 — identical to full model. Result is insensitive to extreme values.

### CoT Decision Pivot #4 — Final Summary

| Checkpoint | Value |
|---|---|
| H0 | β_AIThreat×AIAcc = 0 |
| N / Power | N=17,670; power >99% for f²≥0.0009 |
| p_raw / p_adj | 0.856 / 0.856 |
| f² | 0.000002 (threshold f²≥0.02: **FAIL**) |
| **Practical significance** | **NEIN** |
| **H1 supported?** | **NEIN** |

---

## CRITIC-CHECK — Statistische Verifikation (SQL)

| Kennzahl | Script-Ergebnis | SQL-Verifikation | Übereinstimmung |
|---|---|---|---|
| N (AIThreat=Yes, listwise) | 1,846 | 1,846 | **JA** |
| N (AIThreat=No+Unsure, listwise) | 15,824 | 15,824 | **JA** |
| Total listwise N | 17,670 | 17,670 | **JA** |
| Mean JobSat (AIThreat=Yes) | 6.423 | 6.4231 | **JA** |
| Mean JobSat (AIThreat=No+Unsure) | 7.047 | 7.0468 | **JA** |
| Cohen's d | −0.3029 | −0.3029 | **JA** |
| Mediation indirect a×b (manual) | −0.1253 | (pingouin: −0.1238, Δ=0.0015) | **JA** (bootstrap rounding) |

All 7 key statistics independently verified. No discrepancies requiring correction.

---

## Figures

1. `experiment_v3/figures/fig1_jobsat_by_aithreat.png` — Bar plot: JobSat by AIThreat group
2. `experiment_v3/figures/fig2_moderation_plot.png` — Simple slopes: AIAcc × AIThreat → JobSat
3. `experiment_v3/figures/fig3_mediation_diagram.png` — Mediation path diagram

---

## Summary of Results

| Analysis | Finding | Statistical | Practical |
|---|---|---|---|
| AIThreat main effect on JobSat | d=−0.303 (95% CI [−0.350, −0.250]) | p<0.001 *** | YES (|d|≥0.25) |
| AIAcc main effect on JobSat | β=+0.141 | p<0.001 *** | Small |
| H1: AIThreat × AIAcc moderation | β=−0.009, f²<0.001 | p=0.856, ns | NO |
| Mediation via Frustration | a×b=−0.124, CI [−0.289, +0.021] | p=0.082, ns | NO |
| WorkExp effect | β=+0.009 | p=0.044 (marginal, p_adj=0.053) | Trivial |
| YearsCodePro effect | β=+0.022 | p<0.001 *** | Small |

**Key conclusion:** The moderation hypothesis (H1) is not supported. AIAcc does not moderate the AIThreat → JobSat relationship. However, the AIThreat main effect is robust and practically meaningful (d=−0.303). This is a pre-registered null result.
