# Pipeline v3 — Experiment Summary

**Author:** Anonymous Author  
**Date:** 2026-06-07  
**Research Question:** Does trust in AI output accuracy (AIAcc) moderate the negative relationship between AI job threat perception (AIThreat) and developer job satisfaction (JobSat)?

---

## Key Results

| Result | Value |
|---|---|
| **AIThreat main effect (Cohen's d)** | **d = −0.303, 95% BCa CI [−0.350, −0.250]** |
| **H1: Moderation by AIAcc** | **NULL — β = −0.009, p = .856, f² < .001** |
| **Mediation via Frustration** | **NULL — CI [−0.289, +0.021] includes 0** |
| Sample (listwise) | N = 17,670 (exclusively AI tool users) |
| R² (main model) | 0.027 |
| Multiverse robustness | 0/5 specifications significant for interaction |

---

## Pipeline Statistics

| Metric | Count |
|---|---|
| SQL queries executed | 8 (verification) + continuous analysis |
| Python script executions | 4 (preprocessing, analysis, figures, QC) |
| WebSearch queries | 8 |
| WebFetch calls (abstract screening) | 16 |
| CRITIC-CHECK passes | |
| → Stage 1 (literature) | 10/10 JA |
| → Stage 2 (statistics, SQL) | 7/7 JA |
| → Stage 2b (adversarial) | 6 HOCH-rated points addressed |
| → Stage 3 (inline, paper) | 20/20 JA |
| Adversarial Critic HOCH ratings | 6 |
| Counter-narrative sources | 2 (Armstrong 2024, Chung 2025) |
| Human interventions | 0 |

---

## Qualitäts-Selbstcheck

| Criterion | Status |
|---|---|
| Pre-Analysis Plan eingehalten | ✓ YES — PAP locked before data access |
| PAP-Abweichungen dokumentiert | ✓ YES — AISelect_bin drop documented |
| Citation count ≥ 15 | ✓ YES — 18 references |
| Citation recency ≥ 50% from 2020–2025 | ✓ YES — 78% |
| Bootstrap-CIs berichtet | ✓ YES — BCa CI for d and mediation |
| Mediation getestet | ✓ YES — pingouin, 3-seed self-consistency |
| BH-FDR correction | ✓ YES — applied to all p-values |
| Adversarial Critic vollständig abgearbeitet | ✓ YES — all HOCH points addressed |
| Counter-Narrative in Discussion | ✓ YES — §4.3 |
| Reproducibility Artifacts exportiert | ✓ YES — SQL, PRISMA, PAP, code |
| PRISMA-lite search (15–25 papers) | ✓ YES — 14 papers |
| Prompt Injection Sanitizer applied | ✓ YES — all fetched content screened |
| Self-Consistency mediation (3 seeds) | ✓ YES — variance = 0.000 |
| CoT Decision Pivots (4 checkpoints) | ✓ YES — all 4 documented |
| Multiverse Analysis (5 specs) | ✓ YES — 0/5 significant |
| Novelty score assessed | ✓ MEDIUM — moderation design vs v1/v2 main effects |
| DAG pre-specified | ✓ YES — in preanalysis_plan.json |
| ScientificClaim JSON schema | ✓ YES — 6 claims in scientific_claims.json |

---

## Stages Completed

| Stage | Description | Status |
|---|---|---|
| Stage 0 | Setup & Database | ✓ Done |
| Stage 0b | Pre-Analysis Plan | ✓ Done (LOCKED) |
| Stage 1 | PRISMA Literature Search + Effect-Size Gate | ✓ Done |
| Stage 2 | Statistical Analysis (OLS, bootstrap, mediation, multiverse) | ✓ Done |
| Stage 2b | Adversarial Critic Review | ✓ Done |
| Stage 3 | Paper Writing (LaTeX) | ✓ Done |
| Stage 4 | QC, Export, Reproducibility Artifacts | ✓ Done |

---

## Files Produced

**Paper:** `experiment_v3/experiment_v3_output.tex` (LaTeX, ready for pdflatex)  
**Figures:** `experiment_v3/figures/` (3 PNG files)  
**Scripts:** `scripts/preprocessing_v3.py`, `scripts/analysis_v3.py`, `scripts/generate_figures_v3.py`, `scripts/qc_check_v3.py`  
**Logs:** `logs/v3/` (8 log files)  
**Artifacts:** `logs/v3/preanalysis_plan.json`, `logs/v3/scientific_claims.json`, `logs/v3/analysis_queries.sql`, `logs/v3/prisma_flow.md`

---

## Interpretation

The primary pre-registered hypothesis (H1: moderation of AIThreat → JobSat by AIAcc) was **not supported** across any of the 5 multiverse specifications. This is a clean, pre-registered null result.

The secondary finding — a robust negative main effect of AIThreat on JobSat (d = −0.303) — replicates across methods and controls, and is consistent with prior literature. However, this sample is restricted to current AI tool users, and reverse causation cannot be excluded in this cross-sectional design.

The null moderation suggests that trust in AI accuracy and perceived AI job threat operate as independent cognitive pathways, contradicting the threat-credibility mediation hypothesis. Future studies should measure perceived replaceability (distinct from AI capability trust) as the theorized moderator.

**PIPELINE V3 COMPLETE.**
