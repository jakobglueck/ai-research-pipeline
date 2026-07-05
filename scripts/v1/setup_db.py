import csv
import sqlite3
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE, "data", "survey_results_public.csv")
DB_PATH = os.path.join(BASE, "db", "survey.db")

NUMERIC_COLS = {
    "ResponseId", "YearsCode", "YearsCodePro", "CompTotal",
    "ConvertedCompYearly", "WorkExp", "JobSat",
    "JobSatPoints_1", "JobSatPoints_4", "JobSatPoints_5", "JobSatPoints_6",
    "JobSatPoints_7", "JobSatPoints_8", "JobSatPoints_9", "JobSatPoints_10",
    "JobSatPoints_11",
}

def infer_type(col_name):
    return "REAL" if col_name in NUMERIC_COLS else "TEXT"

def coerce(value, col_type):
    if value == "" or value is None:
        return None
    if col_type == "REAL":
        try:
            return float(re.sub(r"[^\d.\-]", "", value)) if re.search(r"\d", value) else None
        except (ValueError, TypeError):
            return None
    return value

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

with open(CSV_PATH, newline="", encoding="utf-8") as fp:
    reader = csv.reader(fp)
    header = next(reader)
    col_types = [infer_type(c) for c in header]

    col_defs = ", ".join(f'"{c}" {t}' for c, t in zip(header, col_types))
    cur.execute(f"CREATE TABLE survey ({col_defs})")

    placeholders = ", ".join("?" * len(header))
    insert_sql = f"INSERT INTO survey VALUES ({placeholders})"

    batch = []
    for row in reader:
        coerced = [coerce(v, t) for v, t in zip(row, col_types)]
        batch.append(coerced)
        if len(batch) >= 5000:
            cur.executemany(insert_sql, batch)
            batch = []
    if batch:
        cur.executemany(insert_sql, batch)

conn.commit()

row_count = cur.execute("SELECT COUNT(*) FROM survey").fetchone()[0]
print(f"Imported {row_count} rows into survey.db")
print(f"Columns: {len(header)}")
for c, t in zip(header, col_types):
    print(f"  {c}: {t}")

conn.close()
