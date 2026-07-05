# Stage 0b Log — Pre-Analysis Plan

**Author:** Anonymous Author  
**Pipeline:** v3  
**Date:** 2026-06-07  
**Status:** LOCKED

---

## Primary Research Question

**"Does trust in AI accuracy (AIAcc) moderate the negative relationship between AI job threat perception (AIThreat) and developer job satisfaction (JobSat)?"**

### Rationale for this RQ

Derived from Cognitive Threat Appraisal Theory (Lazarus & Folkman 1984): a threat is psychologically damaging in proportion to its perceived credibility. Developers who trust AI accuracy believe AI can genuinely do their job; those who distrust AI accuracy can rationalize the threat away. Therefore, the threat-satisfaction link should be stronger among high-trust respondents.

This is a moderation (interaction) question — structurally distinct from v1 (main-effect comparison with salary) and v2 (main-effect comparison with AISelect).

---

## Novelty Assessment

| Comparison | Score | Reason |
|---|---|---|
| vs. v1 | LOW overlap | v1 tested AIThreat main effect vs. compensation; v3 tests AIThreat × AIAcc interaction |
| vs. v2 | MEDIUM overlap | Both use AIThreat, but v2 compared main effects while v3 tests conditional amplification |

**Combined novelty score: MEDIUM** — No redesign required per protocol (only HIGH triggers rejection).

---

## Key Design Decisions & Justifications

### 1. AIThreat coding: Binary (Yes vs. No+Unsure)
- 'I'm not sure' collapsed with 'No' as conservative reference group
- Alternative: three-level ordinal (tested in Multiverse Spec 2)
- Preregistered to avoid post-hoc recoding bias

### 2. AIAcc coding: Ordinal 1–5
- Highly distrust=1, Somewhat distrust=2, Neither=3, Somewhat trust=4, Highly trust=5
- Treated as continuous for interaction term (standard in moderation analysis)
- Binary version tested in Multiverse Spec 3

### 3. Mediator: Frustration (binary)
- Frustration is multi-select free-form; operationalized as any-vs-none
- Expected partial mediation via JD-R theory (Bakker & Demerouti 2017)
- Flagged secondary: if N drops below 5,000 after listwise, labeled EXPLORATORY

### 4. Missing data: Listwise deletion
- Conservative, transparent, avoids model-dependency assumptions
- MICE sensitivity check preregistered as EXPLORATORY (Multiverse Spec 5)

### 5. Multiple comparison correction
- BH-FDR applied across all hypothesis tests in Stage 2
- Primary test (interaction term) evaluated before correction; correction applied to full test family

---

## DAG Summary

```
WorkExp → AIThreat (confound: experienced devs feel less threatened)
WorkExp → JobSat (confound: experience → seniority → satisfaction)
YearsCodePro → JobSat (confound: coding seniority → satisfaction)
AISelect → AIThreat (possible confounder, direction ambiguous)
AIThreat → JobSat (direct negative effect — primary path)
AIAcc × AIThreat → JobSat (moderation — primary test)
AIThreat → Frustration → JobSat (indirect path — secondary)
```

All causal arrows are theoretically justified and preregistered before any data access.

---

## Exploratory Analyses (will be clearly labeled EXPLORATORY in Stage 2)

1. AIEthics concern count → JobSat (beyond AIThreat)
2. DevType heterogeneity of main interaction
3. AISent as mediator/moderator
4. Salary-controlled replication (ConvertedCompYearly subset)
5. Country-level clustering

---

## PAP Lock

This file and `preanalysis_plan.json` constitute the pre-registered analysis plan.  
All analyses in Stage 2 will be compared against this plan.  
Deviations → labeled EXPLORATORY in the report.
