# Stage 0 Log — Setup & Database

**Author:** Anonymous Author  
**Pipeline:** v3  
**Date:** 2026-06-07

---

## DB Status

- **File:** `db/survey.db` (Stack Overflow Developer Survey)
- **Table:** `survey`
- **Rows:** 65,437
- **Columns:** 114
- **Status:** Exists and intact — not re-imported

### Schema Summary

| Type | Columns |
|---|---|
| Numeric | ResponseId, YearsCode, YearsCodePro, CompTotal, WorkExp, JobSatPoints_1/4–11, ConvertedCompYearly, JobSat |
| Categorical (TEXT) | MainBranch, Age, Employment, RemoteWork, AISelect, AISent, AIBen, AIAcc, AIComplex, AIThreat, AIEthics, Frustration, DevType, Country, … (98 text cols total) |

### Missing Values (key columns)

| Column | Missing % |
|---|---|
| ConvertedCompYearly | 64.2% |
| JobSat | 55.5% → **~29,126 usable rows** |
| WorkExp | 54.7% |
| AISelect | 0.0% |
| AISent | 0.0% |
| AIThreat | 0.0% |
| AIAcc | 0.0% |
| AIComplex | 0.0% |
| Frustration | 56.8% |

---

## Identified Target Variable

**`JobSat`** — Job Satisfaction (0–10 scale)
- N = 29,126 non-null
- Mean = 6.94, SD = 2.09, range 0–10
- Continuous numeric → suitable for regression and correlation analysis

---

## Identified Predictors

| Variable | Type | Description |
|---|---|---|
| AISelect | Categorical (3 levels) | Currently using AI tools at work: Yes / No, plan to / No, don't plan to |
| AISent | Ordinal (5 levels) | AI sentiment: Very unfavorable → Very favorable |
| YearsCode | Numeric | Years coding experience |
| YearsCodePro | Numeric | Years professional coding |
| WorkExp | Numeric | Work experience (years) |

---

## Identified Mediator Candidates

| Variable | Type | Rationale |
|---|---|---|
| AIThreat | Binary (Yes/No/Unsure) | Perceiving AI as a job threat → negative emotions → lower JobSat |
| AIAcc | Ordinal | Trust in AI accuracy → affects willingness/comfort with AI tools |
| AIComplex | Ordinal | Perceived AI capability → competence assessment |

---

## Directories Created

- `experiment_v3/figures/` ✓
- `logs/v3/` ✓
- `db/` — pre-existing ✓
- `scripts/` — pre-existing ✓
