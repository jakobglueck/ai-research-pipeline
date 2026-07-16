# From Prompt to Pipeline: Autonomous AI Research with Claude Code

A controlled empirical study on autonomous scientific paper writing using
Claude Code (Sonnet 4.6) on the Stack Overflow Developer Survey 2024 (N = 65,437).
Four conditions — one baseline and three iteratively improved pipeline versions —
were compared with zero human interventions per run.

---

## What this project is

The central question: can a large language model autonomously traverse the full
scientific research process — from exploratory data analysis to a publication-ready
paper — and does **pipeline architecture** make a measurable difference in quality?

**Condition A — Baseline:** A single prompt instructs the agent to find a CSV,
devise a research question, analyse the data, and produce a six-page LaTeX paper.
No tools, no verification, no structure.

**Condition B — Pipeline v1:** A five-stage instruction chain with two MCP tools:
`sqlite-mcp` for structured SQL access and `fetch-mcp` for live literature retrieval.

**Condition C — Pipeline v2:** Same five stages as v1, plus embedded Critic-Loops
in each stage: every source re-fetched and verified, every key statistic independently
re-computed via SQL.

**Condition D — Pipeline v3:** Seven stages, adding a locked Pre-Analysis Plan
(Stage 0b) before any data access, an Adversarial Critic agent (Stage 2b),
Bootstrap BCa CIs, BH-FDR correction, multiverse analysis (5 specifications),
and a full PRISMA-lite literature search.

The same model, the same dataset, and zero human interventions across all runs.

---

## Results

### Quality evaluation

Assessed on a five-dimension matrix (1–5 points each):

| Criterion | Baseline | v1 | v2 | v3 |
|---|:---:|:---:|:---:|:---:|
| Literature & citation quality | 2 | 3 | 4 | **5** |
| Methodological robustness | 2 | 3 | 4 | **5** |
| Scientific integrity | 1 | 2 | 3 | **5** |
| Depth of insight | 3 | 4 | 3 | **4** |
| Verification & reproducibility | 1 | 4 | 4 | **5** |
| **Total** | **9/25** | **16/25** | **18/25** | **24/25** |

### Empirical findings across conditions

Each pipeline version independently formulated and tested a research question on
the same dataset. The AIThreat → JobSat effect replicated across all three pipeline runs:

| Condition | Research question | Key finding |
|---|---|---|
| Baseline | Coding experience → AI distrust? | r_s = 0.10, d < 0.25 — trivial effect |
| v1 — *Fear Over Pay* | Is AI job threat a stronger predictor of job satisfaction than salary? | Cohen's d = −0.36, β_AIThreat > β_logComp, 29/29 QC checks |
| v2 — *Perception Over Adoption* | Is AI threat perception stronger than actual AI adoption for job satisfaction? | d = −0.33 (AIThreat), d = 0.03 n.s. (AISelect), 21/21 QC checks |
| v3 — *Trust Does Not Moderate Threat* | Does trust in AI accuracy moderate the AIThreat → JobSat link? | **H1 pre-registered null** — β = −0.009, p = .856, f² < .001, 0/5 multiverse specs; AIThreat main effect d = −0.303, BCa 95% CI [−0.350, −0.250], 31/32 QC checks |

The v3 null result for the moderation hypothesis is a clean pre-registered finding:
the hypothesis was locked as JSON before any data query was issued, and the null
replicates across all five multiverse specifications.

---

## Engineering lessons

Each run exposed a failure mode that required a structural fix:

| Run | Failure mode | Fix applied | General lesson |
|---|---|---|---|
| 1 | Real email injected into `\author{}` from system context | Anonymous Author constraint in pipeline instructions | System context bypasses prompt instructions |
| 2 | QC declared PASS without executing the script | STDOUT proof required — no PASS without console output | Self-declared PASS is unverifiable |
| 2 | 7 citations, 0 abstracts actually read | fetch-mcp mandatory before every citation | No citation without prior fetch |
| 3 | f² = 0.00033 reported as main finding | Effect-Size Hard-Stop: f² ≥ 0.02 for interaction terms | p < .05 ≠ scientifically relevant |
| 3 | **Reasoned Non-Compliance** — method instruction overridden | Code assertions instead of text rules | Models override text rules with correct arguments |
| **4** | — | 31/32 PASS, 0 interventions, 3.5 h runtime | Quality requires iteration |

**On Reasoned Non-Compliance:** In Run 3, the pipeline explicitly instructed
dummy-coding for ordinal variables. The model substituted ordinal treatment for
AIAcc (1–5 Likert) and justified it with a statistically correct argument about
interval assumptions and multicollinearity. The argument was right. The finding
was stable. But a text instruction had been silently broken.

The fix: methodological decisions must be enforced by code assertions, not prose.
`assert pd.api.types.is_dummy_encoded(X)` in the script beats any prompt instruction.

---

## Repository structure

```
runs/
  baseline/
    prompt.md                  Single-prompt baseline instruction
    output/
      baseline_output.tex      The baseline paper (LaTeX source)
  v1/
    run_en.md                  Trigger file (English)
    run_de.md                  Trigger file (German)
    stages_en/                 Stage 0–4 instructions (English)
    stages_de/                 Stage 0–4 instructions (German)
    logs/                      Stage logs, experiment summary
    output/
      experiment_output.tex    v1 paper (LaTeX source)
  v2/
    run.md                     Trigger file
    stages/                    Stage 0–4 instructions
    logs/                      Stage logs, experiment summary
    output/
      experiment_v2_output.tex v2 paper (LaTeX source)
      paper_v2.tex
      analytic_sample_v2.csv   Analytic sample (N = 17,696)
  v3/
    run.md                     Trigger file
    stages/                    Stage 0–0b–1–2–2b–3–4 instructions
    logs/
      preanalysis_plan.json    Pre-registered hypotheses (locked before data access)
      scientific_claims.json   Structured claims (6 entries with evidence + caveats)
      analysis_queries.sql     All SQL queries for independent verification
      prisma_flow.md           PRISMA-lite search protocol (36 → 14 sources)
      adversarial_critic_log.md
      stage_*_log.md
    output/
      experiment_v3_output.tex v3 paper (LaTeX source)
      paper_v3.tex

scripts/
  v1/    setup_db.py, preprocessing.py, analysis.py, generate_figures.py, qc_check.py, mcp_helpers.py
  v2/    preprocessing_v2.py, analysis_v2.py, generate_figures_v2.py, qc_check_v2.py
  v3/    preprocessing_v3.py, analysis_v3.py, generate_figures_v3.py, qc_check_v3.py

data/
  survey_results_schema.csv   Column schema (114 variables, public metadata)
  survey_results_public.csv   NOT INCLUDED — download separately (see below)

db/
  survey.db                   SQLite database (65,437 rows, generated by setup_db.py)

metareport/
  metareport.tex              Meta-report: full engineering journey as a paper
  metareport.pdf              Compiled PDF
  references.bib              BibTeX entries
```

---

## Dataset

The Stack Overflow Developer Survey 2024 is publicly available at:
[https://survey.stackoverflow.co/2024/](https://survey.stackoverflow.co/2024/)

Download `survey_results_public.csv` and place it in `data/` before running v1
(which imports it into `db/survey.db`). Subsequent runs reuse the existing database.

---

## Running the pipeline

### Requirements

- [Claude Code](https://claude.ai/code) with Sonnet 4.6
- [uvx](https://docs.astral.sh/uv/) for MCP server execution
- Python 3.10+ with `pandas`, `scipy`, `statsmodels`, `matplotlib`, `seaborn`, `pingouin`
- [tectonic](https://tectonic-typesetting.github.io/) for LaTeX compilation

### MCP configuration

Create `.claude/settings.json` in this directory:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/absolute/path/to/db/survey.db"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  },
  "permissions": {
    "allow": ["Bash(*)", "Read(*)", "Write(*)", "Edit(*)", "mcp__sqlite__*", "mcp__fetch__*"]
  }
}
```

**Note:** Use the absolute path for `--db-path`. A relative path silently falls back
to Bash (v2 failure mode #3).

### Trigger

Open Claude Code in this directory and send the corresponding trigger command:

| Version | Trigger |
|---|---|
| Baseline | `Read and execute completely: runs/baseline/prompt.md` |
| v1 (English) | `Read and execute completely: runs/v1/run_en.md` |
| v2 | `Read and execute completely: runs/v2/run.md` |
| v3 | `Read and execute completely: runs/v3/run.md` |

Each pipeline runs all stages autonomously from that single command.
No further user input is required or expected.

---

## Meta-report

`metareport/metareport.tex` is a peer-review-style paper (TU Chemnitz Hauptseminar
Medieninformatik 2026) documenting the full engineering journey: architecture decisions,
observed failure modes, the Reasoned Non-Compliance phenomenon, and a systematic
quality evaluation of all four conditions.

Compile with:

```bash
cd metareport && tectonic metareport.tex
```

---

## License

MIT — code and pipeline instructions are free to reuse.
The survey data belongs to Stack Overflow and is not included in this repository.
Download it directly from [survey.stackoverflow.co/2024](https://survey.stackoverflow.co/2024/).
