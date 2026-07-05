"""
generate_figures_v2.py
Stage 2 visualizations for pipeline v2.
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_PATH = os.path.join(BASE, "runs", "v2", "output", "analytic_sample_v2.csv")
FIG_DIR = os.path.join(BASE, "runs", "v2", "output", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
PALETTE = {"AIThreat=No": "#4C72B0", "AIThreat=Yes": "#DD8452"}


def load():
    df = pd.read_csv(SAMPLE_PATH)
    df = df[df["AISelect_Yes"] + df["AISelect_PlanSoon"] > 0].copy()
    df["AIThreat_label"] = df["AIThreat_Yes"].map({0: "AIThreat=No", 1: "AIThreat=Yes"})
    df["AISelect_label"] = df["AISelect_Yes"].map({0: "Plans to use", 1: "Currently uses"})
    return df


def fig1_violin(df):
    """
    Figure 1: Violin + box plot — JobSat by AIThreat group.
    Chosen because it shows distribution shape (skew, bimodality) which a simple
    boxplot would hide. Two groups = clear side-by-side comparison.
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = [PALETTE["AIThreat=No"], PALETTE["AIThreat=Yes"]]
    groups = ["AIThreat=No", "AIThreat=Yes"]
    data_groups = [df[df["AIThreat_label"] == g]["JobSat"].values for g in groups]

    parts = ax.violinplot(data_groups, positions=[1, 2], showmedians=False,
                          showextrema=False, widths=0.7)
    for i, (pc, col) in enumerate(zip(parts["bodies"], colors)):
        pc.set_facecolor(col)
        pc.set_alpha(0.6)
        pc.set_edgecolor("grey")

    for i, (data, col) in enumerate(zip(data_groups, colors)):
        q1, med, q3 = np.percentile(data, [25, 50, 75])
        ax.plot([i+1-0.1, i+1+0.1], [med, med], color=col, lw=2.5, solid_capstyle="round")
        ax.vlines(i+1, q1, q3, color=col, lw=8, alpha=0.5)
        mean_val = np.mean(data)
        ax.scatter(i+1, mean_val, color="white", edgecolors=col, s=60, zorder=5)

    n0 = len(data_groups[0])
    n1 = len(data_groups[1])
    ax.set_xticks([1, 2])
    ax.set_xticklabels([f"AIThreat = No\n(n = {n0:,})", f"AIThreat = Yes\n(n = {n1:,})"])
    ax.set_ylabel("Job Satisfaction (0–10)")
    ax.set_title("Job Satisfaction by AI Job Threat Perception\n(d = 0.33, p < 0.001)", pad=12)
    ax.set_ylim(-0.5, 11)
    ax.annotate("Mean shown as white dot", xy=(0.02, 0.02), xycoords="axes fraction",
                fontsize=8, color="grey", style="italic")
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig1_jobsat_by_aithreat.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


def fig2_grouped_bar(df):
    """
    Figure 2: Grouped bar — Mean JobSat by AIThreat × AISelect.
    Shows that AIThreat effect persists regardless of AI adoption status.
    Bars chosen over interaction plot because small interaction effect
    makes the point clearest in simple comparisons.
    """
    table = df.groupby(["AISelect_label", "AIThreat_label"])["JobSat"].agg(
        mean="mean", sem=lambda x: x.std(ddof=1) / np.sqrt(len(x)), n="count"
    ).reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.array([0, 1])
    width = 0.35
    aiselect_vals = ["Currently uses", "Plans to use"]
    colors = [PALETTE["AIThreat=No"], PALETTE["AIThreat=Yes"]]

    for j, threat_label in enumerate(["AIThreat=No", "AIThreat=Yes"]):
        means, sems = [], []
        for sel in aiselect_vals:
            row = table[(table["AISelect_label"] == sel) & (table["AIThreat_label"] == threat_label)]
            means.append(float(row["mean"].values[0]) if len(row) else 0)
            sems.append(float(row["sem"].values[0]) if len(row) else 0)
        bars = ax.bar(x + j*width - width/2, means, width, label=threat_label,
                      color=colors[j], alpha=0.85, edgecolor="white", linewidth=0.8,
                      yerr=sems, capsize=4, error_kw={"ecolor": "black", "alpha": 0.6})
        for b, m in zip(bars, means):
            ax.text(b.get_x() + b.get_width()/2, m + 0.08, f"{m:.2f}",
                    ha="center", va="bottom", fontsize=8.5)

    ax.set_xticks(x)
    ax.set_xticklabels(aiselect_vals)
    ax.set_xlabel("AI Tool Adoption (AISelect)")
    ax.set_ylabel("Mean Job Satisfaction (0–10)")
    ax.set_title("Mean JobSat by AI Threat Perception × AI Adoption\n(Error bars = ±1 SE)", pad=12)
    ax.set_ylim(5.5, 8.0)
    ax.legend(title="AI Job Threat", framealpha=0.9)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig2_grouped_bar_threat_select.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


def fig3_effect_comparison(df):
    """
    Figure 3: Bar chart comparing effect sizes (Cohen's d) of AIThreat vs AISelect.
    Directly illustrates the core finding: perception matters, adoption does not.
    """
    import math
    def cohens_d(a, b):
        na, nb = len(a), len(b)
        sd = math.sqrt(((na-1)*np.std(a,ddof=1)**2 + (nb-1)*np.std(b,ddof=1)**2) / (na+nb-2))
        return abs((np.mean(a) - np.mean(b)) / sd)

    d_threat = cohens_d(
        df[df["AIThreat_Yes"]==0]["JobSat"].values,
        df[df["AIThreat_Yes"]==1]["JobSat"].values
    )
    d_select = cohens_d(
        df[df["AISelect_Yes"]==1]["JobSat"].values,
        df[df["AISelect_Yes"]==0]["JobSat"].values
    )

    fig, ax = plt.subplots(figsize=(6, 4.5))
    labels = ["AI Job Threat\nPerception (AIThreat)", "AI Tool\nAdoption (AISelect)"]
    vals = [d_threat, d_select]
    bar_colors = ["#DD8452", "#4C72B0"]
    bars = ax.barh(labels, vals, color=bar_colors, alpha=0.85, edgecolor="white", height=0.45)
    for b, v in zip(bars, vals):
        ax.text(v + 0.005, b.get_y() + b.get_height()/2, f"d = {v:.3f}",
                va="center", fontsize=10)
    ax.axvline(0.20, color="grey", linestyle="--", lw=1, label="Small effect threshold (d=0.2)")
    ax.set_xlabel("Cohen's d (absolute value)")
    ax.set_title("Effect Size Comparison:\nAI Threat Perception vs. AI Tool Adoption on JobSat")
    ax.set_xlim(0, 0.5)
    ax.legend(fontsize=8)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig3_effect_size_comparison.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


if __name__ == "__main__":
    df = load()
    fig1_violin(df)
    fig2_grouped_bar(df)
    fig3_effect_comparison(df)
    print("All figures saved to runs/v2/output/figures/")
