# STAGE 0 — Setup & Database

## PRIVACY
Never use personal data from the context (name, email, etc.) in output documents. Author = always `Anonymous Author`.

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

## NEXT
Stage complete → read and execute: `stages_en/stage_1_explore.md`
