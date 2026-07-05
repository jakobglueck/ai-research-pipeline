"""
preprocessing_v2.py
Stage 2 preprocessing for pipeline v2.
Research question: Does AIThreat predict JobSat beyond AISelect?
"""
import sqlite3, os, sys
import pandas as pd
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "db", "survey.db")


def load_raw():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        """SELECT JobSat, AIThreat, AISelect, YearsCodePro, RemoteWork, OrgSize
           FROM survey""",
        conn,
    )
    conn.close()
    return df


def missing_analysis(df):
    total = len(df)
    print("=== MISSING DATA ANALYSIS ===")
    print(f"Total rows loaded: {total}")
    for col in df.columns:
        n_miss = df[col].isna().sum()
        pct = 100 * n_miss / total
        print(f"  {col}: {n_miss} missing ({pct:.1f}%)")
    rows_any_missing = df.isna().any(axis=1).sum()
    print(f"\nRows with at least 1 missing value: {rows_any_missing} ({100*rows_any_missing/total:.1f}%)")


def filter_and_encode(df):
    # -----------------------------------------------------------------------
    # Filter: keep only rows with valid AIThreat (Yes/No) and non-null JobSat
    # "I'm not sure" and "NA" are excluded from primary analysis;
    # they are used in robustness check.
    # -----------------------------------------------------------------------
    df_core = df[
        df["JobSat"].notna() &
        df["AIThreat"].isin(["Yes", "No"])
    ].copy()

    # -----------------------------------------------------------------------
    # AIThreat: binary dummy
    #   1 = "Yes" (perceives AI as job threat)
    #   0 = "No"  <- reference category
    # -----------------------------------------------------------------------
    df_core["AIThreat_Yes"] = (df_core["AIThreat"] == "Yes").astype(int)

    # -----------------------------------------------------------------------
    # AISelect: one-hot, reference = "No, and I don't plan to"
    # -----------------------------------------------------------------------
    aiselect_map = {
        "Yes": "AISelect_Yes",
        "No, but I plan to soon": "AISelect_PlanSoon",
        "No, and I don't plan to": None,   # reference
        "NA": None,
    }
    df_core["AISelect_Yes"] = (df_core["AISelect"] == "Yes").astype(int)
    df_core["AISelect_PlanSoon"] = (df_core["AISelect"] == "No, but I plan to soon").astype(int)

    # -----------------------------------------------------------------------
    # Interaction term
    # -----------------------------------------------------------------------
    df_core["AIThreat_x_AISelect"] = df_core["AIThreat_Yes"] * df_core["AISelect_Yes"]

    # -----------------------------------------------------------------------
    # YearsCodePro: continuous numeric covariate.
    # Missing values (13,827 rows) → impute with median (MAR assumption plausible:
    # missingness partly explained by MainBranch/EdLevel which are observed).
    # Listwise deletion would remove ~50% of the analytic sample; median imputation
    # is conservative and preserves power.
    # -----------------------------------------------------------------------
    median_ycp = df_core["YearsCodePro"].median()
    df_core["YearsCodePro_imp"] = df_core["YearsCodePro"].fillna(median_ycp)
    print(f"\nYearsCodePro median (for imputation): {median_ycp}")

    # -----------------------------------------------------------------------
    # RemoteWork: categorical, 3 levels.
    # Reference = "In-person"
    # Note: "NA" rows excluded (n=9 in JobSat-complete sample, negligible).
    # -----------------------------------------------------------------------
    df_core = df_core[df_core["RemoteWork"].isin(["In-person", "Hybrid (some remote, some in-person)", "Remote"])]
    df_core["RemoteWork_Hybrid"] = (df_core["RemoteWork"] == "Hybrid (some remote, some in-person)").astype(int)
    df_core["RemoteWork_Remote"] = (df_core["RemoteWork"] == "Remote").astype(int)

    # -----------------------------------------------------------------------
    # OrgSize: ordinal (company size categories).
    # Encoding choice: dummy coding (not ordinal) because the distances between
    # categories are unequal (e.g., "2-9" vs "10-19" vs "1000-4999" employees).
    # Reference = "Just me - I am a freelancer, sole proprietor, etc."
    # -----------------------------------------------------------------------
    valid_orgsizes = df_core["OrgSize"].value_counts()
    print(f"\nOrgSize distribution:")
    print(valid_orgsizes.to_string())

    top_orgsizes = [s for s in valid_orgsizes.index if s not in ["Just me - I am a freelancer, sole proprietor, etc.", "NA"]]
    for val in top_orgsizes:
        col_name = "OrgSize_" + val.replace(" ", "_").replace(",", "").replace("-", "_").replace("+", "plus")[:30]
        df_core[col_name] = (df_core["OrgSize"] == val).astype(int)

    df_core = df_core[df_core["OrgSize"] != "NA"]

    # Final analytic sample
    feature_cols = (
        ["AIThreat_Yes", "AISelect_Yes", "AISelect_PlanSoon", "AIThreat_x_AISelect",
         "YearsCodePro_imp", "RemoteWork_Hybrid", "RemoteWork_Remote"]
        + [c for c in df_core.columns if c.startswith("OrgSize_")]
    )
    df_out = df_core[["JobSat"] + feature_cols].dropna()

    print(f"\n=== ANALYTIC SAMPLE ===")
    print(f"N (after filtering + encoding): {len(df_out)}")
    print(f"\nEncoded feature columns:")
    for c in feature_cols:
        print(f"  {c}")
    print(f"\nJobSat stats:")
    print(df_out["JobSat"].describe().to_string())

    return df_out, feature_cols


if __name__ == "__main__":
    df_raw = load_raw()
    missing_analysis(df_raw)
    df_clean, features = filter_and_encode(df_raw)
    out_path = os.path.join(BASE, "experiment_v2", "analytic_sample_v2.csv")
    df_clean.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")
