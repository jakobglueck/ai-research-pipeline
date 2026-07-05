import sqlite3
import math
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "db", "survey.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def mean_sd_by_group(numeric_col, group_col):
    """Return mean and SD for numeric_col grouped by group_col."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        f'SELECT "{group_col}", "{numeric_col}" FROM survey '
        f'WHERE "{numeric_col}" IS NOT NULL AND "{group_col}" IS NOT NULL'
    )
    rows = cur.fetchall()
    conn.close()

    groups = {}
    for r in rows:
        g, v = r[0], r[1]
        groups.setdefault(g, []).append(float(v))

    result = {}
    for g, vals in sorted(groups.items()):
        n = len(vals)
        mean = sum(vals) / n
        variance = sum((x - mean) ** 2 for x in vals) / (n - 1) if n > 1 else 0.0
        sd = math.sqrt(variance)
        result[g] = {"n": n, "mean": round(mean, 4), "sd": round(sd, 4)}
    return result


def pearson_correlation(col_a, col_b):
    """Compute Pearson r between two numeric columns."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        f'SELECT "{col_a}", "{col_b}" FROM survey '
        f'WHERE "{col_a}" IS NOT NULL AND "{col_b}" IS NOT NULL'
    )
    rows = cur.fetchall()
    conn.close()

    if len(rows) < 2:
        return None, 0

    xs = [float(r[0]) for r in rows]
    ys = [float(r[1]) for r in rows]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denom_x = math.sqrt(sum((x - mx) ** 2 for x in xs))
    denom_y = math.sqrt(sum((y - my) ** 2 for y in ys))
    if denom_x == 0 or denom_y == 0:
        return 0.0, n
    r = num / (denom_x * denom_y)
    return round(r, 6), n


def missing_value_count():
    """Return missing value count and percent for every column."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM survey")
    total = cur.fetchone()[0]
    cur.execute("PRAGMA table_info(survey)")
    cols = [row[1] for row in cur.fetchall()]
    result = {}
    for col in cols:
        cur.execute(f'SELECT COUNT(*) FROM survey WHERE "{col}" IS NULL')
        missing = cur.fetchone()[0]
        result[col] = {"missing": missing, "pct": round(100 * missing / total, 2)}
    conn.close()
    return total, result


def value_distribution(col, limit=20):
    """Return value counts for a categorical column."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        f'SELECT "{col}", COUNT(*) as cnt FROM survey '
        f'WHERE "{col}" IS NOT NULL GROUP BY "{col}" ORDER BY cnt DESC LIMIT {limit}'
    )
    rows = cur.fetchall()
    conn.close()
    return [(r[0], r[1]) for r in rows]


def cohens_d(col, group_col, group_a, group_b):
    """Compute Cohen's d for col between two groups."""
    conn = get_conn()
    cur = conn.cursor()
    def fetch(g):
        cur.execute(
            f'SELECT "{col}" FROM survey WHERE "{group_col}"=? AND "{col}" IS NOT NULL',
            (g,)
        )
        return [float(r[0]) for r in cur.fetchall()]
    a_vals = fetch(group_a)
    b_vals = fetch(group_b)
    conn.close()

    if not a_vals or not b_vals:
        return None

    def stats(vals):
        n = len(vals)
        mean = sum(vals) / n
        var = sum((x - mean) ** 2 for x in vals) / (n - 1) if n > 1 else 0.0
        return mean, math.sqrt(var), n

    ma, sa, na = stats(a_vals)
    mb, sb, nb = stats(b_vals)
    pooled_sd = math.sqrt(((na - 1) * sa ** 2 + (nb - 1) * sb ** 2) / (na + nb - 2))
    if pooled_sd == 0:
        return 0.0
    d = (ma - mb) / pooled_sd
    return round(d, 4)


def eta_squared(numeric_col, group_col):
    """Compute eta-squared for numeric_col ~ group_col."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        f'SELECT "{group_col}", "{numeric_col}" FROM survey '
        f'WHERE "{numeric_col}" IS NOT NULL AND "{group_col}" IS NOT NULL'
    )
    rows = cur.fetchall()
    conn.close()

    all_vals = [float(r[1]) for r in rows]
    grand_mean = sum(all_vals) / len(all_vals)
    ss_total = sum((v - grand_mean) ** 2 for v in all_vals)

    groups = {}
    for r in rows:
        groups.setdefault(r[0], []).append(float(r[1]))

    ss_between = sum(
        len(v) * (sum(v) / len(v) - grand_mean) ** 2 for v in groups.values()
    )
    return round(ss_between / ss_total, 6) if ss_total > 0 else 0.0


if __name__ == "__main__":
    total, mv = missing_value_count()
    print(f"Total rows: {total}")
    print("\nMissing values per column:")
    for col, info in mv.items():
        if info["missing"] > 0:
            print(f"  {col}: {info['missing']} ({info['pct']}%)")
