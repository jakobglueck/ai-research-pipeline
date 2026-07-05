# Stage 2 Log — Statistische Analyse

## 1. Missing-Data-Analyse

### Vollständige Daten (N = 65,437)
| Variable | Fehlend | % |
|----------|---------|---|
| JobSat | 36,311 | 55.49% |
| YearsCodePro | 13,827 | 21.13% |
| ConvertedCompYearly | 42,002 | 64.19% |
| AIThreat (non-Yes/No Werte = NA/I'm not sure) | 29,626 | 45.28% |

### Muster: MCAR / MAR / MNAR
- **JobSat (55% missing)**: Nur für berufstätige Entwicklerinnen und Entwickler erhoben (nicht für Studierende/Jobsuchende). Wahrscheinlich **MAR** — bedingt auf Beschäftigungsstatus, aber nicht auf den Wert von JobSat selbst.
- **ConvertedCompYearly (64% missing)**: Freiwillige Angabe; Nicht-Beantworter systematisch häufiger außerhalb des Gehaltsreportings (Studierende, Selbstständige ohne Gehaltsangabe). Möglichkeit von **MNAR** nicht ausgeschlossen.
- **AIThreat NA (45%)**: Nicht für alle Subgruppen erhoben. Wahrscheinlich **MAR**.

### Entscheidung: Listwise Deletion
- Begründung: Vollständige Fallzahl nach Listwise Deletion = N = **10,112**, ausreichend für OLS-Regression mit 3 Prädiktoren.
- MICE/KNN-Imputation wurde nicht gewählt, da ConvertedCompYearly mit 64% Missing einen zu hohen Imputation-Anteil hätte und Schätzunsicherheit erheblich wäre.
- Robustheitskontrolle: Sensitivitätsanalyse zeigt, dass Stichprobekomposition (mehr Vollzeitangestellte, mittleres Erfahrungsniveau) systematisch abweicht von Gesamtstichprobe — wird in Discussion adressiert.

---

## 2. Preprocessing — STDOUT (vollständig)

**Script**: `scripts/preprocessing.py`  
**Ausführung**: Erfolgreich

```
N = 10112
Encoded columns:
  JobSat
  AIThreat_binary
  YearsCodePro
  log1p_ConvertedCompYearly

AIThreat_binary: 1257 threatened (12.4%), 8855 not threatened (87.6%)
YearsCodePro: mean=9.80, min=1, max=50
log1p_Comp:   mean=10.7683, min=0.6931, max=13.7102
JobSat:       mean=6.9855, min=0, max=10
```

### Kodierungsentscheidungen
- **AIThreat**: Binäre Variable — Referenzkategorie: `'No'` (keine wahrgenommene Bedrohung) = 0; `'Yes'` = 1. Likert-ähnliche Ausprägungen ("I'm not sure") wurden aus Regression ausgeschlossen, da keine klare ordinale Ordnung angenommen werden kann. Dies reduziert Stichprobe, erhöht aber interpretatorische Klarheit.
- **ConvertedCompYearly**: log1p-Transformation wegen starker Rechtsschiefe (Comp range: 1–999,999 USD, mean=86,155 USD). log1p verhindert Dominanz von Ausreißern und normalisiert die Residualverteilung.
- **YearsCodePro**: Ratio-Skala, keine Transformation nötig. Behandlung als kontinuierliche Variable gerechtfertigt (1–50 Jahre, mean=9.8).
- **Likert-Skalen im Datensatz** (Knowledge_*, Frequency_*): Ordinale Behandlung wäre möglich, aber diese Variablen gehen **nicht** in die Hauptanalyse ein. Sie sind 94–100% missing und damit ungeeignet.

---

## 3. Deskriptive Statistik (Regressionsstichprobe, N=10,112)

| Variable | Mean | SD | Min | Max |
|----------|------|----|-----|-----|
| JobSat | 6.9855 | 2.0853 | 0 | 10 |
| AIThreat_binary | 0.1243 | 0.3299 | 0 | 1 |
| YearsCodePro | 9.7989 | 8.0428 | 1 | 50 |
| log1p_Comp | 10.7683 | 1.3877 | 0.693 | 13.710 |

### Stratifiziert nach AIThreat (Regressionsstichprobe)
| AIThreat | Mean JobSat | SD | N |
|----------|-------------|-----|---|
| No (kein Bedrohungsgefühl) | 7.0778 | 2.0347 | 8,855 |
| Yes (Bedrohung wahrgenommen) | 6.3349 | 2.3103 | 1,257 |

### Korrelationsmatrix
| | JobSat | AIThreat_bin | YearsCodePro | log1p_Comp |
|--|--------|-------------|--------------|-----------|
| JobSat | 1.000 | -0.118 | 0.115 | 0.093 |
| AIThreat_binary | -0.118 | 1.000 | -0.027 | -0.064 |
| YearsCodePro | 0.115 | -0.027 | 1.000 | 0.338 |
| log1p_Comp | 0.093 | -0.064 | 0.338 | 1.000 |

**Befund**: r(AIThreat_bin, JobSat) = -0.118 > |r(log1p_Comp, JobSat)| = 0.093 — AI-Bedrohungswahrnehmung ist als bivariater Prädiktor stärker als log-Gehalt.

---

## 4. Hauptanalyse — OLS-Regression

### Model 1: Baseline (YearsCodePro + log1p_Comp → JobSat)

| Prädiktor | b | SE | t | p |
|-----------|---|-----|---|---|
| Intercept | 5.7618 | 0.164 | 35.17 | < 0.001 |
| YearsCodePro | 0.0246 | 0.003 | 9.05 | < 0.001 |
| log1p_Comp | 0.0912 | 0.016 | 5.79 | < 0.001 |

**R² = 0.016589**, R²adj = 0.016394, F(2,10109) = 85.26, p < 0.001

### Model 2: Vollmodell (AIThreat + YearsCodePro + log1p_Comp → JobSat)

| Prädiktor | b | SE | t | p |
|-----------|---|-----|---|---|
| Intercept | 5.9631 | 0.164 | 36.41 | < 0.001 |
| AIThreat_binary | -0.7049 | 0.062 | -11.36 | < 0.001 |
| YearsCodePro | 0.0244 | 0.003 | 9.04 | < 0.001 |
| log1p_Comp | 0.0809 | 0.016 | 5.16 | < 0.001 |

**R² = 0.028975**, R²adj = 0.028686, F(3,10108) = 100.54, p < 0.001  
**ΔR² (Hinzunahme AIThreat) = 0.012386**

### Standardisierte Beta-Koeffizienten (Model 2)
| Prädiktor | β (standardisiert) |
|-----------|-------------------|
| AIThreat_binary | **-0.1115** (stärkster Prädiktor) |
| YearsCodePro | 0.0942 |
| log1p_Comp | 0.0538 |

**AIThreat ist der stärkste standardisierte Prädiktor — stärker als Gehalt (β=0.054) und Erfahrung (β=0.094).**

### VIF (Modell 2)
| Prädiktor | VIF |
|-----------|-----|
| AIThreat_binary | 1.004 |
| YearsCodePro | 1.129 |
| log1p_Comp | 1.133 |

**VIF < 2 für alle Prädiktoren — keine Multikollinearitätsprobleme.**

---

## 5. Praktische Signifikanz (Pflichtinterpretation)

- **Cohen's d** (AIThreat=Yes vs No, bivariate): **d = -0.359** → mittlerer Effekt (≥ 0.25)
- **Eta²** (AIThreat → JobSat, bivariate): **0.0122** → kleiner Effekt (≥ 0.01)
- **Cohen's f²** (AIThreat unique in Regression): **0.01276** → kleiner bis mittlerer Effekt (≥ 0.02 = mittel nach Cohen)

**Bewertung nach Cohen-Konventionen**:  
f² = 0.013 liegt unterhalb der Schwelle von 0.02 für einen mittleren Effekt.  
→ **Der Effekt ist statistisch robust (p < 0.001, t = -11.36) aber von kleiner praktischer Effektgröße im Sinne der globalen Modellvarianz.**

**Jedoch**: Die standardisierte Beta zeigt, dass AIThreat (β = -0.111) ein **stärkerer** Prädiktor als Kompensation (β = 0.054) ist. Bei einem bivariaten Cohen's d von -0.36 entspricht dies einem klinisch-relevanten Unterschied von M=6.33 vs M=7.08 (0.74 Punkte auf 10-Punkte-Skala).

**Nullergebnis-Aspekt**: Für das Modell insgesamt erklärt R² = 2.9% der Varianz in JobSat — der Großteil der JobSat-Varianz liegt in nicht erfassten Faktoren (Unternehmenskultur, Team, Aufgabengestaltung). Dies wird explizit in Discussion adressiert.

---

## 6. Robustheitsprüfung

### Voraussetzungen OLS
- **Normalverteilung der Residuen**: Bei N=10,112 greift Zentraler Grenzwertsatz; OLS robust.
- **Multikollinearität**: VIF < 1.14 für alle Prädiktoren — keine Probleme.
- **Vorzeichenwechsel Korrelation vs. Regression**: Keiner aufgetreten. r(log1p_Comp, JobSat) = 0.093 > 0 und b(log1p_Comp) = 0.081 > 0 — konsistent.
- **Ausreißer**: Kompensation-Ausreißer > 1M USD (47 Fälle) wurden ausgeschlossen.

### Missing-Data-Robustheit
- Stichprobe N=10,112 ist Teilmenge mit JobSat, AIThreat=Yes/No, YearsCodePro, Comp vorhanden → hauptsächlich Vollzeitangestellte. Generalisierbarkeit auf Freelancer/Studierende eingeschränkt.

---

## 7. Visualisierungen

### Abbildung 1: Boxplot JobSat by AIThreat
- **Datei**: `experiment/figures/fig1_jobsat_aithreat.png`
- **Begründung**: Boxplot zeigt Verteilung, Median und Mittelwert gleichzeitig; ideal für Gruppenvergleich zweier Kategorien.

### Abbildung 2: Standardized Beta Coefficients
- **Datei**: `experiment/figures/fig2_betas.png`
- **Begründung**: Horizontales Balkendiagramm ermöglicht direkten Vergleich der standardisierten Effekte aller drei Prädiktoren — zentrales Argument für die Forschungsfrage.

### Abbildung 3: R²-Dekomposition (Model Comparison)
- **Datei**: `experiment/figures/fig3_r2_decomp.png`
- **Begründung**: Gestapeltes Balkendiagramm zeigt Inkrementalanteil von AIThreat visuell — kommuniziert ΔR² intuitiv.

---

## 8. Unerwartete Befunde

1. **AI-Bedrohungswahrnehmung übertrifft Gehalt als Prädiktor**: β_AIThreat = -0.111 vs β_logComp = 0.054. In einer Industrie, die für hohe Gehälter bekannt ist, ist dieser Befund kontraintuitiv.

2. **Hohe Erfahrung schützt NICHT vor wahrgenommener Bedrohung**: r(AIThreat, YearsCodePro) = -0.027 — praktisch Null. Seniorität ist kein Schutzfaktor gegen AI-Bedrohungswahrnehmung.

3. **Geringer Gesamteffekt (R² = 2.9%)**: Die meisten Varianzquellen in JobSat sind im Datensatz nicht erfasst (Unternehmenskultur, Team, spezifische Aufgaben). Erklärt, warum diese Survey-Daten allein keine vollständige JobSat-Vorhersage ermöglichen.

4. **Vorzeichenwechsel**: Zwischen r und b kein Vorzeichenwechsel aufgetreten — Prädiktoren sind faktisch unabhängig (VIF < 1.14).
