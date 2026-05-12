import sqlite3, os, math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "db", "survey.db")
FIG_DIR = os.path.join(BASE, "experiment", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'figure.dpi': 150,
})

conn = sqlite3.connect(DB_PATH)

# -------------------------------------------------------
# Figure 1: BoxPlot — JobSat by AIThreat group
# -------------------------------------------------------
df1 = pd.read_sql_query("""
    SELECT AIThreat, JobSat FROM survey
    WHERE AIThreat IN ('Yes','No') AND JobSat IS NOT NULL
""", conn)

fig, ax = plt.subplots(figsize=(7, 5))
order = ['No', 'Yes']
labels = ['No AI threat\n(N=15,944)', 'AI threat perceived\n(N=2,380)']
colors = ['#4C9BE8', '#E8614C']

data_by_group = [df1[df1['AIThreat'] == g]['JobSat'].values for g in order]
bp = ax.boxplot(data_by_group, patch_artist=True, widths=0.5,
                medianprops=dict(color='white', linewidth=2.5),
                flierprops=dict(marker='o', markersize=2, alpha=0.3),
                whiskerprops=dict(linewidth=1.5),
                capprops=dict(linewidth=1.5))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)

means = [df1[df1['AIThreat'] == g]['JobSat'].mean() for g in order]
ax.scatter([1, 2], means, marker='D', s=60, color='white', zorder=5, label='Mean')

ax.set_xticks([1, 2])
ax.set_xticklabels(labels)
ax.set_ylabel('Job Satisfaction (0–10)')
ax.set_title('Job Satisfaction by Perceived AI Job Threat\n'
             "(Cohen's d = 0.36, Eta² = 0.012)", pad=12)
ax.set_ylim(-0.5, 11)
ax.axhline(y=df1['JobSat'].mean(), color='gray', linestyle='--', alpha=0.5,
           label=f"Overall mean ({df1['JobSat'].mean():.2f})")
ax.legend(fontsize=9)
ax.text(1.5, 10.3, '***', ha='center', va='bottom', fontsize=14, fontweight='bold')
ax.annotate('', xy=(2, 10.1), xytext=(1, 10.1),
            arrowprops=dict(arrowstyle='-', color='black', lw=1.2))

# Annotate means
for i, (m, g) in enumerate(zip(means, order), 1):
    ax.text(i, m + 0.25, f'M={m:.2f}', ha='center', va='bottom', fontsize=9, color='white',
            fontweight='bold', bbox=dict(boxstyle='round,pad=0.2', facecolor=colors[i-1], alpha=0.9))

plt.tight_layout()
path1 = os.path.join(FIG_DIR, 'fig1_jobsat_aithreat.png')
plt.savefig(path1, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {path1}")

# -------------------------------------------------------
# Figure 2: Standardized Beta Coefficients (Model 2)
# -------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 4.5))

predictors = ['AI Threat\n(Perceived)', 'Professional\nExperience', 'Annual\nCompensation\n(log)']
betas = [-0.1115, 0.0942, 0.0538]
errors = [0.062 * 0.3299 / 2.0853, 0.003 * 8.0428 / 2.0853, 0.016 * 1.3877 / 2.0853]

colors_bar = ['#E8614C' if b < 0 else '#4C9BE8' for b in betas]

bars = ax.barh(predictors, betas, xerr=errors, color=colors_bar, alpha=0.85,
               height=0.5, error_kw=dict(elinewidth=1.5, ecolor='gray', capsize=4))

ax.axvline(x=0, color='black', linewidth=0.8)
ax.set_xlabel('Standardized Beta Coefficient (β)')
ax.set_title('Standardized Regression Coefficients\nPredicting Developer Job Satisfaction (N = 10,112)', pad=10)
ax.set_xlim(-0.16, 0.16)

for bar, beta in zip(bars, betas):
    x_pos = beta + (0.006 if beta >= 0 else -0.006)
    ha = 'left' if beta >= 0 else 'right'
    ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
            f'β = {beta:.3f}***', va='center', ha=ha, fontsize=10, fontweight='bold')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
path2 = os.path.join(FIG_DIR, 'fig2_betas.png')
plt.savefig(path2, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {path2}")

# -------------------------------------------------------
# Figure 3: R² decomposition — model comparison
# -------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 4))

models = ['Baseline\n(Experience +\nCompensation)', 'Full Model\n(+ AI Threat)']
r2_vals = [0.016589, 0.028975]
delta = 0.028975 - 0.016589

ax.bar([0], [0.016589], color='#4C9BE8', alpha=0.8, label='YearsCodePro + log(Comp)', width=0.5)
ax.bar([0], [delta], bottom=[0.016589], color='#E8614C', alpha=0.8, label='AIThreat unique (ΔR²=0.012)', width=0.5)
ax.bar([1], [0.028975], color='#4C9BE8', alpha=0.5, width=0.5)
ax.bar([1], [delta], bottom=[0.016589], color='#E8614C', alpha=0.8, width=0.5)

ax.set_xticks([0, 1])
ax.set_xticklabels(models)
ax.set_ylabel('R²')
ax.set_title('Model R² Comparison\n(AI Threat uniquely adds ΔR² = 0.012)', pad=10)
ax.legend(fontsize=9, loc='upper left')
ax.set_ylim(0, 0.05)

for i, r2 in enumerate(r2_vals):
    ax.text(i, r2 + 0.001, f'R²={r2:.4f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
path3 = os.path.join(FIG_DIR, 'fig3_r2_decomp.png')
plt.savefig(path3, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {path3}")

conn.close()
print("All figures generated.")
