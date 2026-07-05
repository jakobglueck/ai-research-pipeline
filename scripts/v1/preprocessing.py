import sqlite3
import math
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "db", "survey.db")


def load_regression_data():
    """Load complete-case regression dataset and apply pre-processing."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            JobSat,
            AIThreat,
            YearsCodePro,
            ConvertedCompYearly
        FROM survey
        WHERE JobSat IS NOT NULL
          AND AIThreat IN ('Yes', 'No')
          AND YearsCodePro IS NOT NULL
          AND ConvertedCompYearly IS NOT NULL
          AND ConvertedCompYearly < 1000000
    """)
    rows = cur.fetchall()
    conn.close()

    # Categorical variable: AIThreat (binary dummy)
    # Reference category: 'No' (does not perceive AI as threat) → coded 0
    # Treatment:          'Yes' (perceives AI as threat)         → coded 1
    # Justification: binary variable, dummy coding is standard.

    # Continuous variables:
    # YearsCodePro: kept as-is (years, ratio scale)
    # ConvertedCompYearly: log1p-transformed to address right skew

    jobsat = []
    ai_threat = []
    years_code_pro = []
    log_comp = []

    for row in rows:
        jobsat.append(float(row[0]))
        ai_threat.append(1.0 if row[1] == 'Yes' else 0.0)
        years_code_pro.append(float(row[2]))
        log_comp.append(math.log1p(float(row[3])))

    col_names = ['JobSat', 'AIThreat_binary', 'YearsCodePro', 'log1p_ConvertedCompYearly']
    return col_names, jobsat, ai_threat, years_code_pro, log_comp


if __name__ == "__main__":
    cols, js, at, ycp, lc = load_regression_data()
    n = len(js)
    print(f"N = {n}")
    print("Encoded columns:")
    for c in cols:
        print(f"  {c}")
    print(f"\nAIThreat_binary: {sum(at):.0f} threatened ({100*sum(at)/n:.1f}%), "
          f"{n - sum(at):.0f} not threatened ({100*(n-sum(at))/n:.1f}%)")
    print(f"YearsCodePro: mean={sum(ycp)/n:.2f}, min={min(ycp):.0f}, max={max(ycp):.0f}")
    print(f"log1p_Comp:   mean={sum(lc)/n:.4f}, min={min(lc):.4f}, max={max(lc):.4f}")
    print(f"JobSat:       mean={sum(js)/n:.4f}, min={min(js):.0f}, max={max(js):.0f}")
