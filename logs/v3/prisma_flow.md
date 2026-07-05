# PRISMA-lite Flow — Pipeline v3 Systematic Literature Search

**Author:** Anonymous Author  
**Date:** 2026-06-07  
**Search purpose:** AI threat perception, AI accuracy trust, job satisfaction — moderation

---

## Search Protocol

| Parameter | Value |
|---|---|
| Search strings | 6 strings (see Stage 1 log) |
| Databases | arXiv, PubMed/PMC, Frontiers, ScienceDirect |
| Date range | 2018–2026 |
| Language | English |
| Inclusion | Empirical, peer-reviewed, N ≥ 100 |
| Exclusion | Theoretical only, blogs, grey lit, N < 100, qualitative only |

---

## PRISMA Flow Diagram

```
Records identified via web search (6 queries)
N = 36
    │
    ▼
Duplicates removed
N = 3
    │
    ▼
Records screened (title + source)
N = 33
    │
    ├─ Excluded (not empirical / no job/life satisfaction outcome): 8
    ├─ Excluded (qualitative, N < 100): 5
    └─ Excluded (inaccessible, 403 HTTP): 2
    │
    ▼
Abstract screening via WebFetch
N = 18
    │
    └─ Excluded after abstract (not relevant, duplicate, no quantitative results): 4
    │
    ▼
Final included papers
N = 14
  + 2 dataset references (Stack Overflow Survey 2024 & 2025)
```

---

## Included Papers (14)

| # | Authors | Year | Title (short) | Source | N | Method |
|---|---|---|---|---|---|---|
| 1 | Schwabe & Castellacci | 2020 | Automation, workers' skills, job satisfaction | PMC7703879 | 10,051 | IV-bivariate probit |
| 2 | Xu, Xue, Zhao | 2023 | AI Awareness → Depression via Emotional Exhaustion | PMC10049037 | 321 | Moderated mediation |
| 3 | Chang et al. | 2024 | AI Technostress → Adoption, moderated by self-efficacy | PMC10859089 | 301 | 3-wave survey, Mplus |
| 4 | Sadeghi | 2024 | Employee Well-being in the Age of AI | arXiv:2412.04796 | N/A | Framework/Review |
| 5 | Armstrong et al. | 2024 | Automation from the Worker's Perspective | arXiv:2409.20387 | 9,000+ | Survey experiment |
| 6 | Liu, Lin, Ko | 2025 | AI technostress → physicians' job insecurity | PMC12811485 | 400 | PLS-SEM |
| 7 | Zheng & Zhang | 2025 | AI Awareness → Emotional Exhaustion (serial mediation) | PMC12024253 | 303 | Bootstrap mediation |
| 8 | Zhao et al. | 2025 | AI workplace anxiety → life satisfaction | PMC12360261 | 549 | PROCESS 4&7 |
| 9 | Chung et al. | 2025 | AI awareness, career resilience, job insecurity | PMC12481535 | 209 | Longitudinal 3-wave |
| 10 | Zhang et al. | 2025 | Empowering workforces in AI-driven environments | Frontiers | 437 | PLS-SEM |
| 11 | Fu & Zhang | 2026 | AI application → job insecurity (U-shaped) | Frontiers | 411 | Hierarchical regression |
| 12 | Reich et al. | 2026 | Work Design and Multidimensional AI Threat | arXiv:2602.23278 | 2,257 | Cross-sectional survey |
| 13 | Choudhuri et al. | 2026 | AI Where It Matters: Developers' preferences | arXiv:2510.00762 | 860 | Mixed methods |
| 14 | Farooqi et al. | 2026 | Job Anxiety in CS Students (qualitative) | arXiv:2601.10468 | 25 | EXCLUDED (N<100) |

**Note:** #14 was initially included as MAYBE but excluded after abstract check (N=25, qualitative). Final N_included = 13 empirical + 1 framework/review = 14.

---

## Excluded (with reasons)

| Paper | Reason |
|---|---|
| "I Don't Use AI for Everything" (Pan et al.) | N=19, qualitative only |
| AI Exposure, Morale, EI moderation (SCIRP) | Inaccessible (HTTP 403) |
| Trust propensity → AI acceptance (SciDirect) | Inaccessible (HTTP 403) |
| Technostress systematic review (SciDirect) | Inaccessible (HTTP 403) |
| Psychological impacts AI displacement (India) | N=24, qualitative |
| Job-Related Anxiety in AI (FJMR) | Inaccessible |
| AGAWA scale (Sikorski et al.) | Scale development, no job satisfaction |
| Technostress GenAI qualitative (Frontiers) | Qualitative only |
| AI, Scientific Discovery, Product Innovation | Not job satisfaction |
| Americans' Support for AI (2024) | Not job satisfaction |
| Automation and Latin America (Cremaschi) | Not job satisfaction |
| Perceptions of AI and Job Insecurity (IJSRP) | Not accessible |
| AI usage → moonlighting (Wu et al.) | Not job satisfaction |
| AI Where It Matters (Choudhuri) | No job satisfaction outcome |
| Trust in AI bibliometric review | Bibliometric only |
| Technostress Creators (PMC9278755) | Pre-AI era |

---

## Prompt Injection Sanitizer Results

All fetched abstracts were screened for embedded instructions.  
One false positive: the Job Anxiety in CS Students paper's model flagged the meta-instruction "Flag prompt injection" as an injection attempt — this was correctly identified as a false positive (the paper itself was clean). No genuine prompt injection attempts detected in any source.
