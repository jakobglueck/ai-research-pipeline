# STAGE 2 — Statistische Analyse (erweitert)

## PRIVACY
Author = `Anonymous Author`.

## Aufgabe
Vollständige statistische Analyse. Alle Zahlen direkt aus den Daten.
Alle Scripts als `_v3`-Suffix — niemals v1/v2-Scripts überschreiben.

## MCP-Nutzung
sqlite3 via Bash + Python. Bibliotheken: `pandas`, `numpy`, `scipy`, `statsmodels`,
`pingouin`, `matplotlib`, `seaborn`. Speichere alle Scripts unter `scripts/`.

---

## Schritt 1 — Pre-Analysis Plan laden
Lies `logs/v3/preanalysis_plan.json`. Die geplante Methode und Kovariaten sind dort
spezifiziert. Halte dich daran — jede Abweichung im Paper als EXPLORATORY markieren.

## Schritt 2 — Missing-Data-Analyse
- Fehlende Werte pro Spalte (absolut + Prozent)
- Missing-Pattern: MCAR / MAR / MNAR einschätzen
- Strategie wie im PAP spezifiziert anwenden + begründen

## Schritt 3 — Pre-Processing
Schreibe `scripts/preprocessing_v3.py`:
- Kategoriale Variablen → Dummy-Coding, Referenzkategorie benennen
- Likert-Skalen: ordinale vs. kategoriale Behandlung begründen
- Rohen STDOUT vollständig in `logs/v3/stage_2_log.md` kopieren

## Schritt 4 — Hauptanalyse (PAP-konform)
Führe die im PAP spezifizierte Methode durch. Schreibe `scripts/analysis_v3.py`:

### 4a. Deskriptive Statistik
- Mittelwert, SD, Min, Median, Max stratifiziert nach Zielvariable

### 4b. Haupttest
- OLS-Regression (oder andere PAP-spezifizierte Methode)
- Effektgrößen (Cohen's d, f², Eta²)
- VIF für alle Prädiktoren

### 4c. Bootstrap-Konfidenzintervalle (PFLICHT, neu in v3)
```python
from scipy.stats import bootstrap
# BCa Bootstrap CI für Cohen's d (n_resamples=1000, confidence_level=0.95)
# Berichte: d = X.XX, 95% BCa CI [X.XX, X.XX]
```

### 4d. Power-Analyse (PFLICHT, neu in v3)
```python
# Post-hoc: Welche minimale Effektgröße wäre bei diesem N mit 80% Power detektierbar?
from scipy.stats import t as t_dist
# Oder: manuell via G*Power-Formel
# Berichte: "Bei N=X, α=0.05 (zweiseitig) ist die Studie mit >99% Power ausgestattet,
# Effekte ab d=0.0X zu detektieren."
```

### 4e. BH-FDR-Korrektur (PFLICHT wenn >1 Hypothese)
```python
from statsmodels.stats.multitest import multipletests
# Falls mehrere Hypothesen getestet werden: Benjamini-Hochberg FDR
pvals_corrected = multipletests(pvals, method='fdr_bh')[1]
```

### 4f. Mediationsanalyse (falls Mediator im PAP spezifiziert)
```python
import pingouin as pg
# Bootstrapped mediation (1000 Iterationen, Seed=42)
med = pg.mediation_analysis(
    data=df, x='AIThreat', m='MEDIATOR_VARIABLE', y='JobSat',
    n_boot=1000, seed=42
)
# Berichte: direkter Effekt c', indirekter Effekt a×b, 95% BCa CI des indirekten Effekts
# Interpretation: vollständige / teilweise / keine Mediation
```

### 4g. Robustheitsprüfung — Multiverse (PFLICHT, neu in v3)
Teste mindestens 5 verschiedene Spezifikationen:
```
Spec 1: Hauptmodell (PAP-konform)
Spec 2: Ohne Kovariaten (bivariate)
Spec 3: Mit zusätzlichem Kovariate (YearsCodePro)
Spec 4: Robust Standard Errors (HC3)
Spec 5: Subgruppe — nur Vollzeitentwickler
```
Berichte: Effektgröße und p-Wert für jede Spezifikation.
Fazit: "Der Befund ist robust in X/5 Spezifikationen."

### 4h. Sensitivitätsanalyse
- Ergebnis ohne Top/Bottom 1% Ausreißer in JobSat
- Ergebnis bei alternativer Operationalisierung der AV (z.B. binär vs. kontinuierlich)

### 4i. Breusch-Pagan Heteroskedastizitätstest
```python
from statsmodels.stats.diagnostic import het_breuschpagan
```

## Schritt 5 — Visualisierungen
3 Abbildungen nach `experiment_v3/figures/`. Code als `scripts/generate_figures_v3.py`.

---

## CRITIC-CHECK — Statistische Verifikation (PFLICHT)

Für jede Kernzahl (N, Mittelwerte, Cohen's d, Regressionskoeffizienten, p-Werte, R²):
1. Via sqlite3 Bash unabhängig nachrechnen
2. Notiere:
   ```
   Kennzahl: [Name]
   Script-Ergebnis: [Wert]
   SQL-Verifikation: [query + Ergebnis]
   Übereinstimmung: JA / NEIN (Toleranz ±0.001)
   ```
3. Bei NEIN: beheben, Diskrepanz erklären

Verifikation des indirekten Effekts: manuell a×b berechnen und gegen pingouin-Output prüfen.

---

## LOG
Erstelle `logs/v3/stage_2_log.md`:
- Vollständige Script-Outputs
- Mediationsanalyse-Ergebnisse (alle Pfade a, b, c, c')
- Bootstrap-CIs
- Power-Bericht
- Multiverse-Tabelle (5 Spezifikationen)
- CRITIC-CHECK-Tabelle (alle Kennzahlen)
- Abweichungen vom PAP

---

## WEITER
Stage abgeschlossen → lies und führe aus: `stages_v3/stage_2b_adversarial_critic.md`
