# STAGE 2 — Statistical Analysis

## PRIVACY
Never use personal data from the context in output documents. Author = `Anonymous Author`.

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
  categorical treatment (dummies) is chosen. An assumption without justification
  is an error — the choice must be defensible.
- Categorical variables → dummy coding (one-hot encoding), name reference category
- Execute the script and paste the **raw STDOUT** (column names of the encoded
  variables) completely into `logs/stage_2_log.md`
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
- State this explicitly as a null result: *"There is no meaningful relationship between X and Y."*
- A null result is a scientific statement — not a failure.
- p<0.05 with a small effect means: statistically detectable, but practically meaningless.
- Report both in the paper: the p-value AND the substantive interpretation.
- Explain in the Discussion why the effect is not relevant despite significance.

Document in the log: measured effect size + Cohen category + practical interpretation.

### 4. Visualisations
Independently choose suitable plots that communicate the central results most clearly.
Decide autonomously which type of visualisation (boxplot, heatmap, scatterplot etc.)
fits best. Save as PNG in `experiment/figures/`. Justify the choice in the log.
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

## NEXT
Stage complete → read and execute: `stages_en/stage_3_synthesis.md`
