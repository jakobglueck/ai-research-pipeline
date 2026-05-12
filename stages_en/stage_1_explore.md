# STAGE 1 — Exploration & Research Design

## PRIVACY
Never use personal data from the context in output documents. Author = `Anonymous Author`.

## Task
Explore the dataset via SQLite-MCP and Python, and develop a surprising, counter-intuitive research question based on real data patterns.

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
- Eta² ≥ 0.01 (at least 1% explained variance)
- Odds Ratio ≥ 1.5 or ≤ 0.67

If no candidate passes the gate: search for more variable combinations.
Document all tested candidates with measured effects in the log.

**Step C — Final selection:**
Choose the question that is **both** counter-intuitive **and** passes the gate.
With multiple candidates: choose the more interesting one, not the strongest.
**Note:** Passing the gate with an obvious question (e.g. "more experience = higher salary")
does not count — the question must still be surprising or non-trivial.

**Note on interaction effects:** If the research question examines an interaction
(moderation), the **interaction term itself** (not just the main effect) must have
a medium or large effect: f² ≥ 0.02. A significant main effect passing the gate
with a trivial interaction term f²<0.01 does **not** count — that would be a
statistically significant null result. Search further in that case.

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
- **Fallback loop:** If the first search query yields too few results, iteratively
  adjust the search terms (broaden, use synonyms, related concepts).
- **Abstract required:** Read the abstract of every paper via Fetch-MCP
  BEFORE it is added to the log. Citing by title alone is forbidden.
- **Relevance note (1–2 sentences):** For each source, the log must state
  why it is relevant to the specific hypothesis — not just what it is about.
  No paper without relevance justification in the paper.
- For each source: title, authors, year, DOI/URL, abstract content, relevance

## LOG
Create `logs/stage_1_log.md`:
- All SQL queries and results
- Found patterns and anomalies
- Why this research question is more interesting than the obvious one
- Research question, H0, H1, method
- All 5+ sources with DOI/URL

---

## NEXT
Stage complete → read and execute: `stages_en/stage_2_analysis.md`
