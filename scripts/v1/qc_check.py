import re, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX_PATH = os.path.join(BASE, "experiment", "experiment_output.tex")
LOG_PATH = os.path.join(BASE, "logs", "stage_2_log.md")
LOG1_PATH = os.path.join(BASE, "logs", "stage_1_log.md")

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

tex = read(TEX_PATH)
log = read(LOG_PATH)
log1 = read(LOG1_PATH)

errors = []
warnings = []
passed = []

def check(label, expected_in_tex, expected_in_log, note=""):
    tex_ok = expected_in_tex in tex
    log_ok = expected_in_log in log
    if tex_ok and log_ok:
        passed.append(f"PASS  {label}: '{expected_in_tex}' in TEX, '{expected_in_log}' in LOG")
    else:
        errors.append(
            f"FAIL  {label}: TEX={'OK' if tex_ok else 'MISSING: '+repr(expected_in_tex)}, "
            f"LOG={'OK' if log_ok else 'MISSING: '+repr(expected_in_log)}"
        )

# N (sample size)
check("N complete cases", "10{,}112", "10,112")
check("N full survey", "65{,}437", "N = 65,437")

# R² values
check("R² Model 2", "0.0290", "0.028975")
check("R² Model 1", "0.0166", "0.016589")
check("Delta R²", "0.0124", "0.012386")

# F-statistic Model 2
check("F(3,10108)", "F(3, 10108) = 100.54", "F(3,10108) = 100.54")

# AIThreat coefficient
check("b_AIThreat", "$-$0.705", "-0.7049")
check("SE_AIThreat", "0.062", "0.062")
check("t_AIThreat", "-11.36", "t = -11.36")

# Standardized betas
check("beta_AIThreat", "0.111", "-0.1115")
check("beta_YearsCode", "0.094", "0.0942")
check("beta_logComp", "0.054", "0.0538")

# b_YearsCodePro
check("b_YearsCodePro", "0.024", "0.0244")
check("b_logComp", "0.081", "0.0809")

# Means
check("M Threat=Yes", "6.33", "6.3349")
check("M Threat=No", "7.08", "7.0778")

# Cohen's d (stored as "d = -0.359" in log)
check("Cohen's d", "0.36", "0.359")

# VIF check
check("VIF <1.14", "VIF $< 1.14$", "VIF < 1.14")

# Missing data percentages
check("JobSat missing %", "55.5\\%", "55.49%")
check("Comp missing %", "64.2\\%", "64.19%")

# 81.6% coercive adoption — this fact is in stage_1_log.md
tex_ok_81 = "81.6" in tex
log_ok_81 = "81.6%" in log1
if tex_ok_81 and log_ok_81:
    passed.append("PASS  Coercive adoption 81.6%: confirmed in TEX and stage_1_log.md")
else:
    errors.append(f"FAIL  Coercive adoption 81.6%: TEX={'OK' if tex_ok_81 else 'MISSING'}, LOG1={'OK' if log_ok_81 else 'MISSING'}")

# Author anonymity
if "Anonymous Author" in tex and "jakob" not in tex.lower() and "email" not in tex.lower():
    passed.append("PASS  Author: Anonymous Author confirmed, no real name/email in TEX")
else:
    errors.append("FAIL  Author field may contain identifying information")

# References count
bibitem_count = len(re.findall(r"\\bibitem", tex))
if bibitem_count >= 5:
    passed.append(f"PASS  References: {bibitem_count} \\bibitem entries found (≥ 5 required)")
else:
    errors.append(f"FAIL  References: only {bibitem_count} \\bibitem entries (need ≥ 5)")

# Figures included
for fig in ["fig1_jobsat_aithreat", "fig2_betas", "fig3_r2_decomp"]:
    if fig in tex:
        passed.append(f"PASS  Figure {fig} referenced in TEX")
    else:
        errors.append(f"FAIL  Figure {fig} NOT referenced in TEX")

# Figure files exist
FIG_DIR = os.path.join(BASE, "experiment", "figures")
for fig in ["fig1_jobsat_aithreat.png", "fig2_betas.png", "fig3_r2_decomp.png"]:
    path = os.path.join(FIG_DIR, fig)
    if os.path.exists(path):
        passed.append(f"PASS  Figure file {fig} exists on disk")
    else:
        errors.append(f"FAIL  Figure file {fig} NOT found on disk")

# Print results
print("=" * 65)
print("QC CHECK RESULTS")
print("=" * 65)
for p in passed:
    print(p)
if warnings:
    print()
    for w in warnings:
        print(w)
if errors:
    print()
    for e in errors:
        print(e)
print()
print("=" * 65)
print(f"SUMMARY: {len(passed)} PASS, {len(warnings)} WARN, {len(errors)} FAIL")
if not errors:
    print("OVERALL: ALL CHECKS PASSED")
else:
    print("OVERALL: SOME CHECKS FAILED — review FAIL lines above")
print("=" * 65)
sys.exit(0 if not errors else 1)
