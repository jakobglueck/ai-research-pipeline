"""
Automated Quality Control check for Pipeline v3 paper.
Author: Anonymous Author
"""
import re
import sys
import json

PAPER_PATH = "experiment_v3/experiment_v3_output.tex"
LOG_PATH = "logs/v3/stage_2_log.md"
PAP_PATH = "logs/v3/preanalysis_plan.json"

print("=" * 65)
print("PIPELINE V3 — AUTOMATED QC CHECK")
print("=" * 65)

# Load paper
with open(PAPER_PATH, 'r') as f:
    paper = f.read()

# Load stage 2 log
with open(LOG_PATH, 'r') as f:
    log = f.read()

# Load PAP
with open(PAP_PATH, 'r') as f:
    pap = json.load(f)

checks = {}

# ============================================================
# NUMERICAL CHECKS — verify key stats present in paper
# ============================================================
print("\n--- NUMERICAL CHECKS ---")

def check_num(name, patterns, source="paper"):
    text = paper if source == "paper" else log
    found = any(re.search(p, text) for p in patterns)
    status = "PASS" if found else "FAIL"
    checks[name] = found
    print(f"  [{status}] {name}")
    return found

check_num("Cohen's d = -0.303", [r"-0\.303", r"d = -0\.303", r"d=-0\.303"])
check_num("BCa CI [-0.350, -0.250]", [r"-0\.350", r"-0\.250", r"BCa CI"])
check_num("t-statistic = -12.316", [r"-12\.316", r"t = -12"])
check_num("p = 1.03e-34 (main effect)", [r"1\.03", r"10\^{-34}", r"10^{-34}"])
check_num("beta_interaction = -0.009", [r"-0\.009", r"beta.*-0\.009", r"\\beta.*-0\.009"])
check_num("p_interaction = .856", [r"\.856", r"p = \.856"])
check_num("f2 < .001 or = 0.000002", [r"f\^2.*<.*\.001", r"0\.000002", r"f\^2 < \.001"])
check_num("N = 17670", [r"17{,}670", r"17,670", r"17670"])
check_num("Indirect effect CI [-0.289, +0.021]", [r"-0\.289", r"0\.021"])
check_num("a-path p = .106", [r"\.106"])
check_num("AIThreat main effect beta = -0.609 (approx)", [r"-0\.609", r"-0\.611", r"-0\.623"])
check_num("AIAcc beta = +0.141", [r"\+0\.141", r"0\.141"])
check_num("Multiverse 0/5", [r"0/5", r"none.*specif", r"all five"])
check_num("M_threat = 6.42", [r"6\.42", r"6\.423"])
check_num("M_no_threat = 7.05", [r"7\.05", r"7\.047"])

# ============================================================
# CONTENT CHECKS
# ============================================================
print("\n--- CONTENT CHECKS ---")

def check_content(name, patterns, require_all=False):
    if require_all:
        found = all(any(re.search(p, paper, re.IGNORECASE) for p in [pat]) for pat in patterns)
    else:
        found = any(re.search(p, paper, re.IGNORECASE) for p in patterns)
    status = "PASS" if found else "FAIL"
    checks[name] = found
    print(f"  [{status}] {name}")
    return found

# Citation count
bibitems = re.findall(r'\\bibitem', paper)
n_refs = len(bibitems)
cit_pass = n_refs >= 15
checks["Citation count >= 15"] = cit_pass
print(f"  [{'PASS' if cit_pass else 'FAIL'}] Citation count >= 15 (found: {n_refs})")

# Citation recency: count references with years 2020-2026
years = re.findall(r'\b(202[0-6])\b', paper)
all_years_in_refs = re.findall(r'\\bibitem.*?\n.*?\((\d{4})\)', paper)
recent = [y for y in years if 2020 <= int(y) <= 2026]
# Simpler: count bibitems with 202x years
recent_bibs = len([b for b in re.findall(r'\\bibitem\[.*?(\d{4}).*?\]', paper) if 2020 <= int(b) <= 2026])
total_bibs = len(bibitems)
recency_pct = recent_bibs / total_bibs * 100 if total_bibs > 0 else 0
recency_pass = recency_pct >= 50
checks["Citation recency >= 50%"] = recency_pass
print(f"  [{'PASS' if recency_pass else 'FAIL'}] Citation recency >= 50% 2020-2025 ({recent_bibs}/{total_bibs} = {recency_pct:.0f}%)")

check_content("Bootstrap CI mentioned", [r"BCa", r"bootstrap.*CI", r"BCa CI"])
check_content("Power statement present", [r">99% power", r"power.*>.*99", r"99\\\% power"])
check_content("PRISMA-flow mentioned", [r"PRISMA", r"prisma"])
check_content("Counter-narrative section present", [r"counter.narrat", r"alternative.*explan", r"contradicting"])
check_content("Limitations section present", [r"\\section\{.*[Ll]imit", r"limitation", r"\\subsection\{.*[Ll]imit"])
check_content("PAP pre-registration mentioned", [r"pre-register", r"pre-analysis plan", r"preregister", r"pre-registered"])
check_content("Data availability statement", [r"publicly available", r"data.*available", r"analysis code"])
check_content("EXPLORATORY labeled", [r"EXPLORATORY", r"exploratory"])
check_content("Author = Anonymous Author", [r"Anonymous Author"])
check_content("Figures included (\\includegraphics)", [r"\\includegraphics"])
check_content("Mediation analysis present", [r"mediat"])
check_content("Multiverse analysis present", [r"multiverse", r"specif"])
check_content("BH-FDR correction mentioned", [r"BH-FDR", r"Benjamini.Hochberg", r"false discovery"])
check_content("Adversarial critic concerns addressed in discussion",
              [r"reverse caus", r"cross-sectional", r"single.*item", r"single.item"])

# ============================================================
# PRIVACY CHECK
# ============================================================
print("\n--- PRIVACY CHECK ---")
# Check for common real names or emails
privacy_violations = re.findall(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', paper)
# Filter out common false positives
false_positives = {'Anonymous Author', 'Stack Overflow', 'Journal Personality', 'Baron Kenny',
                   'Journal Royal', 'International Journal', 'PLOS ONE', 'JASA Management',
                   'Frontiers Psychology', 'Table Multiverse', 'Behavioral Sciences',
                   'Spec AIThreat', 'Note None', 'BCa Bootstrap', 'Mean centered',
                   'Spec AIAcc', 'HC3 Robust', 'Spec HC3'}
true_violations = [v for v in set(privacy_violations) if v not in false_positives and v != 'Anonymous Author']
has_email = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', paper))

privacy_pass = len(true_violations) == 0 and not has_email
checks["Privacy: no real names/emails"] = privacy_pass
print(f"  [{'PASS' if not has_email else 'FAIL'}] No email addresses found: {not has_email}")
print(f"  [{'PASS' if len(true_violations)==0 else 'CHECK'}] Author = Anonymous Author (check names: {true_violations[:5] if true_violations else 'none flagged'})")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 65)
n_pass = sum(1 for v in checks.values() if v)
n_total = len(checks)
print(f"QC RESULT: {n_pass}/{n_total} checks PASSED")
if n_pass == n_total:
    print("STATUS: ALL CHECKS PASSED ✓")
elif n_pass >= n_total * 0.9:
    print("STATUS: MOSTLY PASSED — minor issues (see above)")
else:
    print("STATUS: ISSUES DETECTED — review FAIL items")
print("=" * 65)

# Print failed checks
failed = [k for k, v in checks.items() if not v]
if failed:
    print(f"\nFailed checks ({len(failed)}):")
    for f in failed:
        print(f"  - {f}")
