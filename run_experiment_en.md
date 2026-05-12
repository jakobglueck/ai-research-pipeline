# EXPERIMENT PIPELINE — Full Run

Execute all five stages **without interruption**. Do not wait for user input between stages.
Work through Stage 0 → 1 → 2 → 3 → 4 sequentially. The pipeline is complete only when
Stage 4 is fully finished (all logs written, LaTeX compiled).

## PRIVACY — applies to all stages
Never use personal data from the context (name, email, etc.) in output documents.
Author = always `Anonymous Author`. This includes the `\author{}` field of the LaTeX document.

---

# STAGE 0 — Setup & Database

## Task
Find the dataset in `data/`, understand its structure, and import it into a SQLite database.

## Steps

1. Create the following directories:
   - `db/`, `scripts/`, `experiment/figures/`, `logs/`

2. Look in `data/` — find the CSV file (regardless of its name)

3. Analyse the CSV:
   - Number of columns, column names, data types
   - Read the first rows to understand the content
   - Identify possible target variables

4. Write `scripts/setup_db.py` that:
   - Imports the CSV into `db/survey.db` (DB name always `survey.db`)
   - Imports numeric columns as REAL, text as TEXT
   - Treats missing values as NULL (not as empty strings)

5. Execute the script

6. Write `scripts/mcp_helpers.py` with helper functions for:
   - Mean/SD per group (SQLite has no STDDEV)
   - Pearson correlation between two columns
   - Missing value count per column
   - Value distribution of a column

7. Verify via SQLite-MCP (DB path: `./db/survey.db`):
   - Row count, column names, schema
   - Missing values per column

## LOG
Create `logs/stage_0_log.md`:
- Filename and size of the found dataset
- Brief description: What is the data about?
- Schema (columns + types)
- Missing values per column
- Identified possible target variables
- Errors encountered

---

# STAGE 1 — Exploration & Research Design

## Task
Explore the dataset via SQLite-MCP and Python, and develop a surprising,
counter-intuitive research question based on real data patterns.

## MCP Usage
Use `scripts/mcp_helpers.py` for calculations that SQL alone cannot handle.
Extend the helper functions if needed. SQLite-MCP path: `./db/survey.db`.

## Steps

### 1. Understand the dataset
- What does this dataset measure? Who are the respondents?
- Which variables are numeric, which are categorical?
- Which variable is suitable as the target variable?
- Which variables could be interesting predictors?

### 2. Exploratory SQL queries
- Distribution of the target variable
- Means/SD of all numeric variables
- Correlations via Python helper function
- Unexpected patterns, outliers, subgroups
- Interaction effects between pairs of variables

### 3. Research question — Out of the box with Effect-Size Gate

**Step A — Collect candidates:**
Actively search for surprising or counter-intuitive patterns:
- Is there a subgroup that behaves contrary to expectations?
- Does the dataset contradict an established assumption?
- Which variable has a surprisingly weak or strong relationship?
- Is there an interaction effect that only emerges from combining two variables?

Collect at least **3 candidate research questions** and calculate a quick
effect-size pre-check for each (Pearson r, Eta², Cohen's d, bivariate OR).

**Step B — Effect-Size Gate (MUST be passed):**
A research question may only be pursued if the effect exceeds at least one of:
- Pearson/Spearman |r| ≥ 0.15
- Cohen's d ≥ 0.25
- Eta² ≥ 0.01
- Odds Ratio ≥ 1.5 or ≤ 0.67

If no candidate passes the gate: search for more variable combinations.
Document all tested candidates with measured effects in the log.

**Step C — Final selection:**
Choose the question that is both counter-intuitive and passes the gate.
**Note:** Passing the gate with an obvious question does not count —
the question must still be surprising or non-trivial.

**Note on interaction effects:** If the research question examines an interaction
(moderation), the **interaction term itself** (not just the main effect) must have
a medium or large effect: f² ≥ 0.02. A significant main effect passing the gate
with a trivial interaction f²<0.01 does **not** count. Search further in that case.

Formulate:
- **Research question** — precise and answerable
- **H0** — no effect
- **H1** — expected effect
- **Method** — justified and appropriate to the question
- **Pre-effect size** — measured value + which gate criterion was met

### 4. Literature search
Use Fetch-MCP for at least **5 scientific sources** relevant to the research question:
- ArXiv: `https://arxiv.org/search/?searchtype=all&query=...`
- Semantic Scholar: `https://www.semanticscholar.org/search?q=...`
- **Fallback loop:** If the first search yields too few results, iteratively adjust
  search terms (broaden, use synonyms, related concepts).
- **Abstract required:** Read the abstract of every paper via Fetch-MCP BEFORE
  adding it to the log. Citing by title alone is forbidden.
- **Relevance note (1–2 sentences):** The log must state why each source is
  relevant to the specific hypothesis. No paper without relevance justification.
- For each source: title, authors, year, DOI/URL, abstract content, relevance

## LOG
Create `logs/stage_1_log.md`:
- All SQL queries and results
- Found patterns and anomalies
- Why this research question is more interesting than the obvious one
- Research question, H0, H1, method
- All 5+ sources with DOI/URL

---

# STAGE 2 — Statistical Analysis

## Task
Conduct the complete statistical analysis. All numbers directly from the data — no estimates.

## MCP Usage
Combine SQLite-MCP (`./db/survey.db`) with Python. Allowed libraries:
`pandas`, `numpy`, `scipy`, `scikit-learn`, `matplotlib`, `seaborn`, `statsmodels`.
Save all scripts under `scripts/`.

## Steps

### 1. Missing data analysis (complete)
- Missing values per column (absolute + percentage)
- Rows with at least 1 missing value (total count)
- Missing pattern: assess MCAR / MAR / MNAR
- Decide: listwise deletion or imputation (MICE/KNN) — justify the choice

### 2. Descriptive statistics
- Mean, SD, min, median, max for all relevant variables
- Stratified by target variable
- Sample size for each analysis stated explicitly

### 3a. Pre-processing — MANDATORY STEP, must not be skipped
Write `scripts/preprocessing.py`:
- Identify all categorical and ordinal variables in the model
- For Likert scales (1–5): justify **in writing in the log** whether ordinal or
  categorical treatment (dummies) is chosen. An assumption without justification is an error.
- Categorical variables → dummy coding, name reference category
- Execute the script and paste the **raw STDOUT** completely into `logs/stage_2_log.md`
- **Only when the STDOUT is in the log may Step 3b begin.**

### 3b. Main analysis
Conduct the method chosen in Stage 1:
- Document all calculations and cross-check via SQL
- Calculate effect sizes (not just p-values)
- Calculate VIF if regression

### 3c. Practical significance — MANDATORY INTERPRETATION

**Statistical significance ≠ practical relevance.** For the main finding:

Evaluate according to Cohen conventions:
- Cohen's f² < 0.02 → small effect (practically irrelevant)
- Cohen's f² 0.02–0.14 → medium effect
- Cohen's f² ≥ 0.15 → large effect
- Pearson |r| < 0.10 → negligible
- Pearson |r| 0.10–0.29 → weak
- Pearson |r| ≥ 0.30 → moderate to strong

**If the main finding has a small or negligible effect:**
- State explicitly as a null result: *"There is no meaningful relationship between X and Y."*
- A null result is a scientific statement — not a failure.
- Report both: the p-value AND the substantive interpretation.
- Explain in the Discussion why the effect is not relevant despite significance.

Document in the log: measured effect size + Cohen category + practical interpretation.

### 4. Visualisations
Independently choose suitable plots that communicate the central results most clearly.
Save as PNG in `experiment/figures/`. Justify the choice in the log.
Save plot code as `scripts/generate_figures.py`.

### 5. Robustness check
- Check assumptions of the chosen method
- Explain sign changes between bivariate correlation and regression coefficients if present

## Success criteria
- All metrics calculated from DB and verifiable
- Complete missing data analysis
- At least 2 visualisations
- VIF or intercorrelation matrix if regression

## LOG
Create `logs/stage_2_log.md`:
- All SQL queries and results
- Complete results tables
- Complete missing data statistics
- Visualisation selection and justification
- Unexpected findings

---

# STAGE 3 — Synthesis & Paper Writing

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

# STAGE 4 — Export & Quality Control

## Task
Consistency check, compile LaTeX, save final output.

## Steps

### 1. Consistency check — QC must provide proof, not self-assertion

**Automated proof (mandatory):**
Write `scripts/qc_check.py`:
- Read `experiment/experiment_output.tex` and `logs/stage_2_log.md`
- Check via regex/string-matching that central numbers (N, p-values, R²,
  b-coefficients, SE values) match exactly
- Execute the script
- Paste the **complete raw STDOUT** into `logs/stage_4_log.md`
- No "PASS" without terminal output. A "PASS" without proof is not QC.

**Manual checklist (afterwards):**
- Figures present and correctly included?
- All sources from Stage 1 in References?
- Author = `Anonymous Author`?
- Exactly 6 pages?

### 2. Compile LaTeX
```bash
pdflatex -interaction=nonstopmode experiment/experiment_output.tex
```
Correct errors and recompile. Document all errors in the log.

### 3. Save
Final paper: `experiment/experiment_output.tex`

## LOG
Create `logs/stage_4_log.md`:
- Found and corrected inconsistencies
- LaTeX errors and corrections
- Total duration (estimated)
- Number of human interventions

Create `logs/experiment_summary.md`:

### Pipeline statistics
- Total SQL queries
- Python script executions
- Fetch-MCP calls
- Human interventions (count + type)

### Quality self-check
- Privacy maintained?
- Page limit maintained?
- All numbers verified?
- Sources genuinely retrieved?
- Open weaknesses requiring human review

---

## PIPELINE COMPLETE
All outputs in `experiment/`, logs in `logs/`.
