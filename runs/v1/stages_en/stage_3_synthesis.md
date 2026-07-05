# STAGE 3 — Synthesis & Paper Writing

## PRIVACY
Author = `Anonymous Author`. Never use real names, email addresses, or personal data
from the context — including in the \author{} field of the LaTeX document.

## Task
Write a complete, compilable scientific paper based on the validated results from Stage 1 and Stage 2.

## Context (read before writing)
- Research question, H0/H1, method, sources: `logs/stage_1_log.md`
- All statistical results: `logs/stage_2_log.md`
- Figures: `experiment/figures/`

## LaTeX header (always use)
```latex
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{natbib}
\usepackage{geometry}
\usepackage{hyperref}
\graphicspath{{../experiment/figures/}}
```

## Structure — exactly 6 pages (11pt, 2.5cm margins)
1. **Abstract** — 150 words
2. **Introduction** — motivation, research question, related work with all sources from Stage 1
3. **Methodology** — dataset description with correct missing data information, analysis method
4. **Results** — all numbers from Stage 2, tables, figures via `\includegraphics`
5. **Discussion & Conclusion** — interpretation, limitations, implications
6. **References** — only real sources retrieved in Stage 1

## Constraints
- **Exactly 6 pages** — actively shorten if too long, add if too short
- **Author: Anonymous Author** — no real name, no email
- No estimated numbers — every number from `logs/stage_2_log.md`
- Represent missing data fully and correctly
- Explain sign changes between correlation and regression coefficient if present
- SE values never as "0.000" — use `< 0.001` or more decimal places for small SE
- LaTeX must compile

## LOG
Create `logs/stage_3_log.md`:
- Which numbers were taken from which log
- Structural decisions
- Problems encountered while writing

---

## NEXT
Stage complete → read and execute: `stages_en/stage_4_export.md`
