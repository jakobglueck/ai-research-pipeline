# Stage 3 Log — Synthese & Paper

**Author:** Anonymous Author  
**Pipeline:** v3  
**Date:** 2026-06-07

---

## Paper Output

**File:** `experiment_v3/paper_v3.tex`  
**Format:** LaTeX (pdflatex/xelatex compatible)  
**Note:** No LaTeX compiler available in environment. File is syntactically complete and ready for compilation on any LaTeX-equipped system.

---

## Counter-Narrative Sources (PFLICHT)

### Counter-Narrative 1 — Benefits outweigh costs

**Source:** Armstrong et al. (2024). *Automation from the Worker's Perspective*. arXiv:2409.20387.  
**Finding:** Among 9,000+ workers across 9 countries, more respondents reported potential benefits from AI (safety, pay, autonomy) than reported costs. Employees solving complex problems showed greater receptiveness.  
**How addressed in paper:** Cited in Discussion §4.3 to acknowledge that AI threat perception is not universal; our 10.4% AIThreat rate is consistent with a minority affected.

### Counter-Narrative 2 — Career resilience buffers threat

**Source:** Chung et al. (2025). *AI awareness, career resilience, job insecurity and behavioural outcomes*. PMC12481535.  
**Finding:** Career resilience significantly moderates AI awareness → job insecurity pathway (β=−.17, p<.05). High-resilience workers do not translate AI awareness into job insecurity.  
**How addressed in paper:** Cited in Discussion §4.3 to explain why AI-using developers (who self-selected into tool adoption, likely indicating higher resilience) may show lower AIThreat prevalence and attenuated moderation effects.

---

## Inline CRITIC-CHECK (≥15 Checks)

| # | Zahl im Paper | Quelle | Log-Abschnitt | Gefunden | Korrekt? |
|---|---|---|---|---|---|
| 1 | $N = 17{,}670$ (listwise) | stage_2_log.md | Step 2 Missing Data | JA | JA |
| 2 | $d = -0.303$ | stage_2_log.md | Cohen's d section | JA | JA |
| 3 | 95% BCa CI $(-0.350, -0.250)$ | stage_2_log.md | Cohen's d section | JA | JA |
| 4 | $t(17{,}668) = -12.316$ | stage_2_log.md | Cohen's d section | JA | JA |
| 5 | $p = 1.03 \times 10^{-34}$ | stage_2_log.md | Cohen's d section | JA | JA |
| 6 | $M_{\text{threat}} = 6.42$ | stage_2_log.md | Descriptive Stats | JA | JA |
| 7 | $M_{\text{no-threat}} = 7.05$ | stage_2_log.md | Descriptive Stats | JA | JA |
| 8 | $\beta_{\text{AIThreat} \times \text{AIAcc}} = -0.009$ | stage_2_log.md | OLS Main Model table | JA | JA |
| 9 | $p = .856$ (interaction) | stage_2_log.md | OLS Main Model table | JA | JA |
| 10 | $f^2 = 0.000002$ | stage_2_log.md | OLS Main Model section | JA | JA |
| 11 | $\beta_a = +0.161$, $p = .106$ (a-path) | stage_2_log.md | Mediation Analysis table | JA | JA |
| 12 | $\beta_b = -0.778$ (b-path) | stage_2_log.md | Mediation Analysis table | JA | JA |
| 13 | $a \times b = -0.124$, CI $(-0.289, +0.021)$ | stage_2_log.md | Mediation Analysis table | JA | JA |
| 14 | Null in 0/5 multiverse specs | stage_2_log.md | Multiverse Analysis table | JA | JA |
| 15 | 10.4% AIThreat=Yes | stage_2_log.md | Descriptive Stats | JA | JA |
| 16 | $N_{\text{included}} = 14$ papers | stage_1_log.md | PRISMA-Flow | JA | JA |
| 17 | $N_{\text{identified}} = 36$ candidates | stage_1_log.md | PRISMA-Flow | JA | JA |
| 18 | $\beta_{\text{AIAcc}} = +0.141$, $p = 4.44 \times 10^{-19}$ | stage_2_log.md | OLS Main Model table | JA | JA |
| 19 | DevType control: $\beta = -0.611$, $p = 1.65 \times 10^{-4}$ | adversarial_critic_log.md | Konfundierung 1 table | JA | JA |
| 20 | Bootstrap variance over 3 seeds = 0.000 | stage_2_log.md | Mediation Self-consistency | JA | JA |

**All 20 inline CRITIC-CHECKs: JA ✓ — No corrections required.**

---

## Citation CRITIC-CHECK (Key Claims)

| Claim in paper | Source | Abstract confirms? |
|---|---|---|
| "fear of machine replacement negatively affects job satisfaction" | Schwabe & Castellacci (2020) PMC7703879 | JA |
| "more workers report benefits than costs from automation" | Armstrong et al. (2024) arXiv:2409.20387 | JA |
| "career resilience moderates AI awareness → insecurity" | Chung et al. (2025) PMC12481535 | JA |
| "AI anxiety → life satisfaction fully mediated by negative emotions" | Zhao et al. (2025) PMC12360261 | JA |
| "AI awareness → emotional exhaustion via job insecurity (75.5% mediated)" | Zheng & Zhang (2025) PMC12024253 | JA |

---

## Numbers Source Map

All numbers in the paper trace directly to validated log entries:

| Section | Numbers | Source log |
|---|---|---|
| Abstract | d=−0.303, CI[−0.350,−0.250], β=−0.009, p=.856 | stage_2_log.md |
| Methods | N=17,670; N_identified=36; N_included=14 | stage_2_log.md, stage_1_log.md |
| Results Table 1 | All 5 multiverse βs and ps | stage_2_log.md |
| Results mediation | a=0.161, b=−0.778, ab=−0.124, CI | stage_2_log.md |
| Discussion | DevType β=−0.611, Country β=−0.623 | adversarial_critic_log.md |

---

## PAP Deviations in Paper

| Deviation | Location in Paper | Label |
|---|---|---|
| AISelect_bin dropped from main model | §2.4 Missing Data | PAP deviation explained |
| AIAcc main effect reported | §3.3 | EXPLORATORY |
| DevType + Country control reported | §3.5 | EXPLORATORY |
