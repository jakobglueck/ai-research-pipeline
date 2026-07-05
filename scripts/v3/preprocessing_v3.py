"""
Preprocessing script for Pipeline v3.
Author: Anonymous Author
"""
import sqlite3
import pandas as pd
import numpy as np


def load_and_preprocess():
    conn = sqlite3.connect("db/survey.db")
    df = pd.read_sql(
        "SELECT JobSat, AIThreat, AIAcc, AISelect, WorkExp, YearsCodePro, Frustration FROM survey",
        conn
    )
    conn.close()

    # Replace 'NA' strings with NaN
    df.replace('NA', np.nan, inplace=True)

    # --- AIThreat binary (PAP: Yes=1, No+Unsure=0) ---
    df['AIThreat_bin'] = df['AIThreat'].map({'Yes': 1, 'No': 0, "I'm not sure": 0})

    # --- AIAcc ordinal 1-5 ---
    acc_map = {
        'Highly distrust': 1,
        'Somewhat distrust': 2,
        'Neither trust nor distrust': 3,
        'Somewhat trust': 4,
        'Highly trust': 5
    }
    df['AIAcc_ord'] = df['AIAcc'].map(acc_map)

    # --- AISelect binary (PAP: Yes=1, else=0) ---
    df['AISelect_bin'] = df['AISelect'].apply(
        lambda x: 1 if x == 'Yes' else (0 if pd.notna(x) else np.nan)
    )

    # --- Frustration binary (PAP: any=1, None of these=0, NA=NaN) ---
    def frustration_binary(val):
        if pd.isna(val) or val == 'NA':
            return np.nan
        elif val == 'None of these':
            return 0
        else:
            return 1
    df['Frustration_bin'] = df['Frustration'].apply(frustration_binary)

    # --- Interaction term ---
    df['AIThreat_x_AIAcc'] = df['AIThreat_bin'] * df['AIAcc_ord']

    # Listwise dataset for main model
    main_vars = ['JobSat', 'AIThreat_bin', 'AIAcc_ord', 'AIThreat_x_AIAcc',
                 'AISelect_bin', 'WorkExp', 'YearsCodePro']
    df_main = df[main_vars].dropna().copy()

    # Mediation dataset
    med_vars = ['JobSat', 'AIThreat_bin', 'Frustration_bin', 'AIAcc_ord',
                'AISelect_bin', 'WorkExp', 'YearsCodePro']
    df_med = df[med_vars].dropna().copy()

    return df, df_main, df_med


if __name__ == "__main__":
    df, df_main, df_med = load_and_preprocess()
    print(f"Full N: {len(df)}")
    print(f"Listwise N (main model): {len(df_main)}")
    print(f"Mediation N: {len(df_med)}")
    print(f"\nMain model columns:\n{df_main.describe()}")
