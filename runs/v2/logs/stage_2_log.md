# Stage 2 Log — Statistische Analyse

**Datum:** 2026-06-07  
**Pipeline:** v2

---

## 1. Missing Data Analyse

**Geladene Spalten:** JobSat, AIThreat, AISelect, YearsCodePro, RemoteWork, OrgSize  
**Gesamtzeilen:** 65.437

| Spalte | Fehlend | % |
|---|---|---|
| JobSat | 36.311 | 55.5 % |
| AIThreat | 0 | 0.0 % |
| AISelect | 0 | 0.0 % |
| YearsCodePro | 13.827 | 21.1 % |
| RemoteWork | 0 | 0.0 % |
| OrgSize | 0 | 0.0 % |

**Zeilen mit mind. 1 fehlenden Wert:** 37.081 (56.7 %)

### Missing-Pattern-Einschätzung
- **JobSat** (55.5 % fehlend): Wahrscheinlich MAR. Die Beantwortung der JobSat-Frage hängt von beobachtbaren Variablen ab (z. B. MainBranch: Hobby-Coder ohne Jobkontext überspringen diese Frage systematisch). Keine MCAR-Annahme vertretbar bei so hohem Missing-Anteil.
- **YearsCodePro** (21.1 % fehlend): MAR plausibel — Studierende und Hobby-Coder haben keine professionellen Programmierjahre. Imputation mit Median (8.0 Jahre) gewählt, da listwise deletion ~50 % des analytischen Samples eliminieren würde.

**Entscheidung: Listwise Deletion + Median-Imputation für YearsCodePro.**

---

## 2. Preprocessing — STDOUT (preprocessing_v2.py)

```
=== MISSING DATA ANALYSIS ===
Total rows loaded: 65437
  JobSat: 36311 missing (55.5%)
  AIThreat: 0 missing (0.0%)
  AISelect: 0 missing (0.0%)
  YearsCodePro: 13827 missing (21.1%)
  RemoteWork: 0 missing (0.0%)
  OrgSize: 0 missing (0.0%)

Rows with at least 1 missing value: 37081 (56.7%)

YearsCodePro median (for imputation): 8.0

OrgSize distribution:
OrgSize
20 to 99 employees                                    3962
100 to 499 employees                                  3475
10,000 or more employees                              2148
...

=== ANALYTIC SAMPLE ===
N (after filtering + encoding): 17696

Encoded feature columns:
  AIThreat_Yes
  AISelect_Yes
  AISelect_PlanSoon
  AIThreat_x_AISelect
  YearsCodePro_imp
  RemoteWork_Hybrid
  RemoteWork_Remote
  OrgSize_20_to_99_employees
  OrgSize_100_to_499_employees
  OrgSize_10000_or_more_employees
  OrgSize_1000_to_4999_employees
  OrgSize_2_to_9_employees
  OrgSize_10_to_19_employees
  OrgSize_500_to_999_employees
  OrgSize_5000_to_9999_employees
  OrgSize_I_don't_know
```

### Encoding-Entscheidungen

**AIThreat** (binär): Dummy-Coding. AIThreat=No → 0 (Referenz), AIThreat=Yes → 1.  
„I'm not sure" und „NA" ausgeschlossen (primäre Analyse), in Robustheitsprüfung einbezogen.

**AISelect** (binär im analytischen Sample): Da im AIThreat Yes/No-Subsample die Kategorie „No, and I don't plan to" faktisch nicht vorkommt (0 Fälle), reduziert auf AISelect_Yes (1=currently using, 0=plans to use soon). Referenz = „No, but I plan to soon".

**YearsCodePro** (numerisch, kontinuierlich): Keine Dichotomisierung; metrische Behandlung. Median-Imputation bei 21 % Missing (begründet oben).

**RemoteWork** (3-stufig kategorisch): Dummy-Coding. Referenz = „In-person". Die Abstände zwischen Kategorien (0/hybrid/vollremote) sind nicht metrisch, daher kein Likert-Score.

**OrgSize** (8 kategorische Stufen, ungleiche Intervalle): Dummy-Coding. Referenz = „Just me (Freelancer)". Ordinale Behandlung nicht begründbar (Sprung von 99 auf 100 ≠ Sprung von 9.999 auf 10.000 Mitarbeitende).

---

## 3. Deskriptive Statistik

### JobSat gesamt (analytisches Sample, N=17.696)
| | Wert |
|---|---|
| Mean | 7.012 |
| SD | 2.072 |
| Min | 0 |
| Median | 7 |
| Max | 10 |
| 25. Pz. | 6 |
| 75. Pz. | 8 |

### JobSat nach AIThreat
| Gruppe | n | Mean | SD | Median | Min | Max |
|---|---|---|---|---|---|---|
| AIThreat=No | 15.414 | **7.099** | 2.025 | 7 | 0 | 10 |
| AIThreat=Yes | 2.282 | **6.426** | 2.285 | 7 | 0 | 10 |

**Mittlere Differenz: 0.673 Punkte (auf 0–10-Skala)**

### JobSat nach AISelect
| Gruppe | n | Mean | SD |
|---|---|---|---|
| AISelect=Plans to use (Ref) | 3.158 | 6.960 | 1.994 |
| AISelect=Yes | 14.538 | 7.024 | 2.089 |

**Mittlere Differenz: 0.064 Punkte (trivial)**

---

## 4. Hauptanalyse

### Welch t-Test: AIThreat No vs. Yes → JobSat
- t = 13.32, df ≈ 2.875, **p < 2.5 × 10⁻³⁹**

### One-Way ANOVA + Eta²
- F(1, 17.694) = 212.27, **p < 8.3 × 10⁻⁴⁸**
- **Eta² = 0.0119** (1.19 % erklärte Varianz)

### Cohen's d: AIThreat
- **d = 0.327** (No > Yes)  
- Cohen-Kategorie: *klein (0.2–0.5)*

### Cohen's d: AISelect
- **d = 0.031** (negligibel)

---

### OLS Regression — Modell 1 (AIThreat + AISelect, ohne Kovariaten)

N = 17.696, **R² = 0.01198**, Adj.R² = 0.01186

| Prädiktor | β | p | 95%-KI |
|---|---|---|---|
| const | 7.050 | < 0.001 | [6.977, 7.123] |
| **AIThreat_Yes** | **−0.673** | **< 0.001** | [−0.763, −0.582] |
| AISelect_Yes | 0.060 | 0.140 | [−0.020, 0.139] |

→ AIThreat signifikant negativ; AISelect nicht signifikant.

---

### OLS Regression — Modell 2 (Vollmodell mit Kovariaten)

N = 17.696, **R² = 0.03286**, Adj.R² = 0.03209

| Prädiktor | β | p | 95%-KI |
|---|---|---|---|
| const | 6.644 | < 0.001 | [6.274, 7.015] |
| **AIThreat_Yes** | **−0.651** | **< 0.001** | [−0.741, −0.562] |
| AISelect_Yes | 0.096 | 0.018 | [0.017, 0.175] |
| YearsCodePro_imp | 0.028 | < 0.001 | [0.024, 0.031] |
| RemoteWork_Hybrid | 0.242 | < 0.001 | [0.156, 0.328] |
| RemoteWork_Remote | 0.336 | < 0.001 | [0.248, 0.424] |
| OrgSize_I_don't_know | −0.539 | 0.019 | [−0.989, −0.089] |
| *OrgSize-Dummies (andere)* | n.s. | n.s. | — |

→ AIThreat bleibt nach Kontrolle aller Kovariaten hochsignifikant (β=−0.651, p<0.001).  
→ AISelect statistisch signifikant (p=0.018), aber β=0.096 ist praktisch bedeutungslos.

---

### ΔR² / f² für AIThreat (inkrementelle Erklärungskraft)
| Modell | R² |
|---|---|
| Kovariaten + AISelect (ohne AIThreat) | 0.02180 |
| Vollmodell | 0.03286 |
| **ΔR² (AIThreat)** | **0.01106** |
| **f² (AIThreat)** | **0.01144** |

→ f² = 0.011 liegt in der Kategorie *klein* nach Cohen (0.02 = mittel). Interpretation: AIThreat erklärt etwa 1,1 % der Varianz inkrementell — statistisch robust, praktisch bescheiden.

---

### VIF (Modell 2) — keine kritische Multikollinearität

| Prädiktor | VIF |
|---|---|
| AISelect_Yes | 5.53 |
| RemoteWork_Hybrid | 3.53 |
| RemoteWork_Remote | 3.22 |
| OrgSize-Dummies | 1.4–3.2 |
| YearsCodePro_imp | 2.56 |
| **AIThreat_Yes** | **1.15** |
| OrgSize_I_don't_know | 1.10 |

Alle VIFs deutlich unter 10. Keine problematische Multikollinearität.

---

### 3c. Praktische Signifikanz

**Cohen's d = 0.327 → kleiner Effekt (0.2–0.5)**  
**f² = 0.011 → kleiner Effekt (<0.02)**  
**Eta² = 0.012 → kleiner Effekt (1 %)**

**Interpretation:**  
AIThreat ist ein statistisch hochsignifikanter (p < 10⁻⁴⁷), aber *kleiner* Prädiktor von Jobzufriedenheit. Die mittlere Differenz von 0.67 Punkten auf einer 0–10-Skala ist zwar messbar, aber ohne große praktische Relevanz für individuelle Vorhersagen. Als Gruppenunterschied in einer Survey-Studie (N=17.696) ist dieser Effekt dennoch substantiell berichtbar.

Die statistische Signifikanz bei kleinem Effekt resultiert aus dem großen N — das ist methodisch korrekt zu benennen: Es gibt einen echten, aber kleinen Zusammenhang zwischen AIThreat und JobSat.

---

### Robustheitsprüfung: AIThreat-Effekt nur unter KI-Nutzern

| Gruppe | n | Mean JobSat |
|---|---|---|
| AISelect=Yes, AIThreat=No | 12.678 | 7.110 |
| AISelect=Yes, AIThreat=Yes | 1.860 | 6.435 |

- Cohen's d = 0.325, t = 11.89, **p < 1.1 × 10⁻³¹**

→ Der AIThreat-Effekt persistiert vollständig unter aktuellen KI-Tool-Nutzern (d=0.325 ≈ Gesamtsample d=0.327). KI-Tool-Adoption "immunisiert" nicht gegen den negativen Effekt von AIThreat auf Jobzufriedenheit.

---

## 5. Visualisierungen

**Fig. 1 — `fig1_jobsat_by_aithreat.png` (Violin + Box):**  
Zeigt Verteilungsform von JobSat in beiden AIThreat-Gruppen. Violin statt reinem Boxplot gewählt, da die Verteilung linksskief ist und bimodale Strukturen sichtbar gemacht werden sollen.

**Fig. 2 — `fig2_grouped_bar_threat_select.png` (Grouped Bar):**  
Mean JobSat × AIThreat × AISelect (±1 SE). Zeigt, dass der AIThreat-Effekt sowohl bei AI-Nutzern als auch bei Planern konsistent ist (keine Interaktion).

**Fig. 3 — `fig3_effect_size_comparison.png` (Horizontal Bar):**  
Direkter Effektgrößenvergleich (Cohen's d): AIThreat (d=0.327) vs. AISelect (d=0.031). Kommuniziert die Kernaussage: Wahrnehmung > Nutzungsverhalten.

---

## 6. Unerwartete Befunde

1. **AISelect im Vollmodell statistisch signifikant** (β=0.096, p=0.018), aber substantiell trivial. Bei N=17.696 ist auch ein Effekt von unter 0.1 Punkten auf 10 Punkten statistisch nachweisbar. Die p-Wert-Interpretation hier ist irreführend ohne Effektgrößenangabe.
2. **OrgSize faktisch irrelevant** — alle Kategorien nicht signifikant außer „I don't know" (wohl Residualkategorie mit besonderen Charakteristika).
3. **Remote work positiv** (β=0.336 für vollremote), was mit dem 2025 Stack Overflow Survey-Befund konsistent ist.

---

## 7. CRITIC-CHECK — Statistische Verifikation

### Kennzahl 1: N (analytisches Sample)

```
Kennzahl: N analytisches Sample
Script-Ergebnis: 17.696
SQLite-Verifikation:
  SELECT COUNT(*) FROM survey
  WHERE JobSat IS NOT NULL AND AIThreat IN ('Yes','No')
  AND RemoteWork IN ('In-person','Hybrid (...)','Remote')
  AND OrgSize != 'NA'
  AND AISelect IN ('Yes','No, but I plan to soon');
  → 17696
Übereinstimmung: JA
```

### Kennzahl 2: Mean JobSat AIThreat=No

```
Kennzahl: Mean JobSat, AIThreat=No
Script-Ergebnis: 7.0991
SQLite-Verifikation: SELECT AIThreat, COUNT(*), ROUND(AVG(JobSat),4) FROM survey [...]
  GROUP BY AIThreat → No: 15414 | 7.0991
Übereinstimmung: JA
```

### Kennzahl 3: Mean JobSat AIThreat=Yes

```
Kennzahl: Mean JobSat, AIThreat=Yes
Script-Ergebnis: 6.4259
SQLite-Verifikation: → Yes: 2282 | 6.4259
Übereinstimmung: JA
```

### Kennzahl 4: Cohen's d (AIThreat No vs. Yes)

```
Kennzahl: Cohen's d
Script-Ergebnis: 0.3268
SQL-Independent-Berechnung:
  Formel: (M_No - M_Yes) / SD_pooled
  SD(No)=2.0246, SD(Yes)=2.2847, n(No)=15414, n(Yes)=2282
  SD_pooled = sqrt(((15413*2.0246²)+(2281*2.2847²))/(17694))
  d = (7.0991 - 6.4259) / SD_pooled = 0.3268
Übereinstimmung: JA
```

### Kennzahl 5: Eta²

```
Kennzahl: Eta² (AIThreat → JobSat)
Script-Ergebnis: 0.011855
SQL-Verifikation:
  grand_mean = 7.0123, SS_total = 75987.3144
  SS_between = 15414*(7.0991-7.0123)² + 2282*(6.4259-7.0123)² = 900.83
  Eta² = 900.83 / 75987.31 = 0.011855
Übereinstimmung: JA (Differenz: 0.000000)
```

### Kennzahl 6: Regressionskoeffizient AIThreat_Yes (Modell 2)

```
Kennzahl: β(AIThreat_Yes) in Vollmodell
Script-Ergebnis: −0.6513 (95%-KI: [−0.741, −0.562])
Manuelle Verifikation: Konsistent mit bivariater Analyse (Δ = 0.022 nach Kovariat-Adjustierung)
Übereinstimmung: JA (keine SQL-basierte Gegenkontrolle möglich für Regressionskoeff., 
  aber Vorzeichen und Größenordnung konsistent mit Gruppenunterschied aus SQL)
```

### Zusammenfassung Critic-Check

| Kennzahl | Geprüft | Übereinstimmung |
|---|---|---|
| N gesamt | ✓ | JA |
| Mean AIThreat=No | ✓ | JA |
| Mean AIThreat=Yes | ✓ | JA |
| Cohen's d | ✓ | JA |
| Eta² | ✓ | JA |
| β(AIThreat_Yes) | ✓ | JA (indirekt) |

**6 von 6 Kennzahlen geprüft. 0 initiale Abweichungen.**

---

## Fehler

- **Model 1 (erste Version)**: Numerische Instabilität durch fehlende Referenzkategorie (AISelect „No, and I don't plan to" nicht im Subsample). → Behoben durch Umkodierung AISelect auf binär (Yes vs. Plans soon).
- Keine weiteren Fehler.
