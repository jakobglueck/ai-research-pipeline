"""
Figure generation script for Pipeline v3.
Produces 3 publication-quality figures.
Author: Anonymous Author
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from preprocessing_v3 import load_and_preprocess

FIGURE_DIR = "experiment_v3/figures"
os.makedirs(FIGURE_DIR, exist_ok=True)

df, df_main, df_med = load_and_preprocess()

COLORS = {'threat': '#D62728', 'no_threat': '#1F77B4', 'neutral': '#7F7F7F'}
plt.rcParams.update({'font.size': 11, 'font.family': 'sans-serif'})

# ============================================================
# FIGURE 1 — JobSat by AIThreat group (bar + CI)
# ============================================================
fig, ax = plt.subplots(figsize=(7, 5))

groups = {
    'Perceives\nAI as\njob threat\n(Yes)': df_main.loc[df_main['AIThreat_bin']==1, 'JobSat'],
    'Does not perceive\nAI as\njob threat\n(No / Unsure)': df_main.loc[df_main['AIThreat_bin']==0, 'JobSat']
}
means = [v.mean() for v in groups.values()]
sems  = [v.sem() for v in groups.values()]
ns    = [len(v) for v in groups.values()]
colors_bars = [COLORS['threat'], COLORS['no_threat']]
bars = ax.bar(list(groups.keys()), means, yerr=[1.96*s for s in sems],
              color=colors_bars, capsize=6, alpha=0.85, edgecolor='black', linewidth=0.8)

for bar, mean, n in zip(bars, means, ns):
    ax.text(bar.get_x() + bar.get_width()/2, mean + 0.08, f'M = {mean:.2f}\nN = {n:,}',
            ha='center', va='bottom', fontsize=9.5)

ax.set_ylim(5.5, 8.0)
ax.set_ylabel('Job Satisfaction (0–10 scale)', fontsize=12)
ax.set_title('Fig. 1 — Job Satisfaction by AI Job Threat Perception\n'
             r"Cohen's $d$ = −0.303, 95% BCa CI [−0.350, −0.250]",
             fontsize=11, pad=10)
ax.axhline(df_main['JobSat'].mean(), color='gray', linestyle='--', alpha=0.6, linewidth=1)
ax.text(1.48, df_main['JobSat'].mean()+0.03, f'Overall M={df_main["JobSat"].mean():.2f}',
        ha='right', fontsize=8.5, color='gray')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/fig1_jobsat_by_aithreat.png", dpi=150, bbox_inches='tight')
plt.close()
print("Figure 1 saved.")

# ============================================================
# FIGURE 2 — Moderation Plot: AIAcc × AIThreat (simple slopes)
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5.5))

# Simple slopes: JobSat at AIAcc levels 1–5, by AIThreat group
acc_levels = [1, 2, 3, 4, 5]
acc_labels = ['Highly\ndistrust', 'Somewhat\ndistrust', 'Neither', 'Somewhat\ntrust', 'Highly\ntrust']

means_threat, means_no_threat = [], []
sems_threat, sems_no_threat = [], []
ns_threat, ns_no_threat = [], []

for acc in acc_levels:
    sub_yes = df_main.loc[(df_main['AIThreat_bin']==1) & (df_main['AIAcc_ord']==acc), 'JobSat']
    sub_no  = df_main.loc[(df_main['AIThreat_bin']==0) & (df_main['AIAcc_ord']==acc), 'JobSat']
    means_threat.append(sub_yes.mean() if len(sub_yes) > 0 else np.nan)
    means_no_threat.append(sub_no.mean() if len(sub_no) > 0 else np.nan)
    sems_threat.append(sub_yes.sem() if len(sub_yes) > 1 else np.nan)
    sems_no_threat.append(sub_no.sem() if len(sub_no) > 1 else np.nan)
    ns_threat.append(len(sub_yes))
    ns_no_threat.append(len(sub_no))

x = np.arange(len(acc_levels))
ax.errorbar(x, means_threat, yerr=[1.96*s if not np.isnan(s) else 0 for s in sems_threat],
            color=COLORS['threat'], marker='o', linewidth=2, markersize=8, label='AIThreat = Yes',
            capsize=5, capthick=1.5)
ax.errorbar(x, means_no_threat, yerr=[1.96*s if not np.isnan(s) else 0 for s in sems_no_threat],
            color=COLORS['no_threat'], marker='s', linewidth=2, markersize=8, label='AIThreat = No/Unsure',
            capsize=5, capthick=1.5)

ax.set_xticks(x)
ax.set_xticklabels(acc_labels, fontsize=9.5)
ax.set_xlabel('Trust in AI Accuracy (AIAcc)', fontsize=12)
ax.set_ylabel('Job Satisfaction (0–10 scale)', fontsize=12)
ax.set_title('Fig. 2 — Simple Slopes: AI Accuracy Trust × AI Job Threat → Job Satisfaction\n'
             r'Interaction: $\beta$ = −0.009, $p$ = .856, $f^2$ < .001 — Null Result (H1 Not Supported)',
             fontsize=10.5, pad=10)
ax.legend(fontsize=10, loc='lower right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(4.5, 9.5)
ax.annotate('Note: Parallel slopes confirm\nno moderation effect.',
            xy=(0.02, 0.04), xycoords='axes fraction', fontsize=8.5, color='gray',
            style='italic')
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/fig2_moderation_plot.png", dpi=150, bbox_inches='tight')
plt.close()
print("Figure 2 saved.")

# ============================================================
# FIGURE 3 — Mediation Path Diagram
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')

def box(ax, x, y, w, h, text, color='#AEC6CF', fontsize=10.5):
    rect = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                    boxstyle="round,pad=0.1", linewidth=1.5,
                                    edgecolor='black', facecolor=color)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight='bold')

def arrow(ax, x1, y1, x2, y2, label, color='black', lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw))
    mx, my = (x1+x2)/2, (y1+y2)/2 + 0.25
    ax.text(mx, my, label, ha='center', va='center', fontsize=9,
            color=color, style='italic',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))

# Boxes
box(ax, 1.5, 2.5, 2.4, 1.2, 'AI Job Threat\n(AIThreat_bin)', color='#FFCCCC')
box(ax, 5.0, 4.2, 2.4, 1.0, 'Work Frustration\n(Frustration_bin)', color='#FFE4B5')
box(ax, 8.5, 2.5, 2.4, 1.2, 'Job Satisfaction\n(JobSat, 0–10)', color='#CCFFCC')

# a-path (not significant)
arrow(ax, 2.7, 3.1, 3.8, 3.8, 'a = 0.161\np = .106 (n.s.)', color='#999999', lw=1.2)
# b-path (significant)
arrow(ax, 6.2, 3.8, 7.3, 3.1, 'b = −0.778\np < .001***', color='#D62728', lw=2)
# c-prime (direct, significant)
arrow(ax, 2.7, 2.5, 7.3, 2.5, "c' = −0.627, p < .001***\n(Direct effect)", color='#1F77B4', lw=2)

# Indirect effect label
ax.text(5.0, 1.3, 'Indirect effect (a × b) = −0.124\n95% BCa CI [−0.289, +0.021] — Not significant',
        ha='center', va='center', fontsize=9.5,
        bbox=dict(facecolor='#F5F5F5', edgecolor='#AAAAAA', boxstyle='round,pad=0.4'))

ax.set_title('Fig. 3 — Mediation Analysis: AIThreat → Frustration → JobSat\n'
             '(Baron-Kenny; BCa Bootstrap, n=1000; N=17,043)\n'
             'Mediation NOT confirmed: a-path non-significant (p = .106)',
             fontsize=10.5, pad=8)
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/fig3_mediation_diagram.png", dpi=150, bbox_inches='tight')
plt.close()
print("Figure 3 saved.")

print("\nAll figures saved to experiment_v3/figures/")
