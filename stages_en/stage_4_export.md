# STAGE 4 — Export & Quality Control

## PRIVACY
Check explicitly: does the paper contain real names or email addresses?
If yes, replace with `Anonymous Author`.

## Task
Consistency check, compile LaTeX, save final output.

## Steps

### 1. Consistency check — QC must provide proof, not self-assertion

**Automated proof (mandatory):**
Write `scripts/qc_check.py`:
- Read `experiment/experiment_output.tex` and `logs/stage_2_log.md`
- Check via regex/string-matching that the central numbers (N, p-values, R²,
  b-coefficients, SE values) match exactly
- Execute the script
- Paste the **complete raw STDOUT** into `logs/stage_4_log.md`
- No "PASS" without terminal output. A "PASS" without proof is not QC.

**Manual checklist (afterwards):**
- Figures present and correctly included?
- All sources from Stage 1 in References — none added, none removed?
- Source keys in the log match references in the paper?
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
