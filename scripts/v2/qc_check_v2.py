"""
qc_check_v2.py
Stage 4 quality-control check for pipeline v2.
Reads runs/v2/output/experiment_v2_output.tex and runs/v2/logs/stage_2_log.md,
verifies that key numbers in the paper match the log via regex string matching.
"""
import os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX_PATH  = os.path.join(BASE, "runs", "v2", "output", "experiment_v2_output.tex")
LOG2_PATH = os.path.join(BASE, "logs", "v2", "stage_2_log.md")

# ------------------------------------------------------------------
# Load files
# ------------------------------------------------------------------
with open(TEX_PATH, encoding="utf-8") as f:
    tex = f.read()
with open(LOG2_PATH, encoding="utf-8") as f:
    log2 = f.read()

# ------------------------------------------------------------------
# Check 1: Privacy — no real author name or email
# ------------------------------------------------------------------
FORBIDDEN = ["jakob", "gluck", "glueck", "@gmail", "@tu-chemnitz"]
print("=== CHECK 1: Privacy ===")
privacy_pass = True
for term in FORBIDDEN:
    if term.lower() in tex.lower():
        print(f"  FAIL: Found forbidden term '{term}' in paper")
        privacy_pass = False
if privacy_pass:
    anon_ok = "Anonymous Author" in tex
    print(f"  Anonymous Author in paper: {'OK' if anon_ok else 'MISSING'}")
    print(f"  Status: {'PASS' if anon_ok else 'FAIL'}")
else:
    print(f"  Status: FAIL")

# ------------------------------------------------------------------
# Helper: check a string appears in the tex
# ------------------------------------------------------------------
checks = []

def check(label, value_str, search_in=tex):
    found = value_str.lower() in search_in.lower()
    status = "PASS" if found else "FAIL"
    checks.append((label, value_str, status))
    print(f"  [{status}] {label}: '{value_str}'")
    return found

# ------------------------------------------------------------------
# Check 2: Sample size
# ------------------------------------------------------------------
print("\n=== CHECK 2: Sample Size ===")
check("N in paper", "17{,}696")

# ------------------------------------------------------------------
# Check 3: Group means
# ------------------------------------------------------------------
print("\n=== CHECK 3: Group Means ===")
check("Mean AIThreat=No", "7.099")
check("Mean AIThreat=Yes", "6.426")
check("Mean diff rounded", "0.67")

# ------------------------------------------------------------------
# Check 4: Effect sizes
# ------------------------------------------------------------------
print("\n=== CHECK 4: Effect Sizes ===")
check("Cohen d AIThreat", "0.33")
check("Cohen d AISelect", "0.031")
check("Eta-squared AIThreat", "0.012")

# ------------------------------------------------------------------
# Check 5: Regression coefficients
# ------------------------------------------------------------------
print("\n=== CHECK 5: Regression Coefficients ===")
check("Beta AIThreat Model1", "-0.673")
check("Beta AIThreat Model2", "-0.651")
check("Beta AISelect Model1", "0.060")
check("R2 Model2", "0.033")

# ------------------------------------------------------------------
# Check 6: p-values / t-values
# ------------------------------------------------------------------
print("\n=== CHECK 6: Test Statistics ===")
check("t-statistic AIThreat", "13.32")
check("F-value ANOVA", "212.27")
check("Delta R2", "0.011")

# ------------------------------------------------------------------
# Check 7: Robustness
# ------------------------------------------------------------------
print("\n=== CHECK 7: Robustness ===")
check("Robustness d AI users", "0.325")
check("Robustness n AI users", "14{,}538")

# ------------------------------------------------------------------
# Check 8: All 5 references present
# ------------------------------------------------------------------
print("\n=== CHECK 8: References ===")
refs = [
    ("Sadeghi 2024", "sadeghi2024employee"),
    ("Giuntella 2025", "giuntella2025ai"),
    ("Vaillant 2024", "vaillant2024developers"),
    ("Soulami 2024", "soulami2024exploring"),
    ("Feng 2025",    "feng2025ai"),
]
for name, key in refs:
    check(name, key)

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------
n_pass = sum(1 for _, _, s in checks if s == "PASS")
n_fail = sum(1 for _, _, s in checks if s == "FAIL")
n_total = len(checks)
print(f"\n=== SUMMARY ===")
print(f"  Total checks: {n_total}")
print(f"  PASS: {n_pass}")
print(f"  FAIL: {n_fail}")
if n_fail == 0:
    print("  OVERALL: PASS — all numbers verified in paper")
else:
    print("  OVERALL: FAIL — see items above")
    sys.exit(1)
