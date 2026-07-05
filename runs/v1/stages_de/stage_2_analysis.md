# STAGE 2 — Statistische Analyse

## PRIVACY
Verwende niemals persönliche Daten aus dem Kontext in Output-Dokumenten. Author = `Anonymous Author`.

## Aufgabe
Führe die vollständige statistische Analyse durch. Alle Zahlen direkt aus den Daten — keine Schätzungen.

## MCP-Nutzung
Kombiniere SQLite-MCP (`./db/survey.db`) mit Python. Erlaubte Bibliotheken: `pandas`, `numpy`, `scipy`, `scikit-learn`, `matplotlib`, `seaborn`, `statsmodels`. Speichere alle Scripts unter `scripts/`.

## Schritte

### 1. Missing-Data-Analyse (vollständig)
- Fehlende Werte pro Spalte (absolut + Prozent)
- Zeilen mit mindestens 1 fehlenden Wert (Gesamtanzahl)
- Missing-Pattern: MCAR / MAR / MNAR einschätzen
- Entscheide: Listwise Deletion oder Imputation (MICE/KNN) — begründe die Wahl

### 2. Deskriptive Statistik
- Mittelwert, SD, Min, Median, Max für alle relevanten Variablen
- Stratifiziert nach Zielvariable
- Stichprobengröße für jede Analyse explizit angeben

### 3a. Pre-Processing — PFLICHTSCHRITT, darf nicht übersprungen werden
Schreibe `scripts/preprocessing.py`:
- Identifiziere alle kategorialen und ordinalen Variablen im Modell
- Für Likert-Skalen (1–5): Begründe **schriftlich im Log** ob ordinale oder
  kategoriale Behandlung (Dummies) gewählt wird. Eine Annahme ohne Begründung
  ist ein Fehler — die Wahl muss vertretbar sein.
- Kategoriale Variablen → Dummy-Coding (One-Hot-Encoding), Referenzkategorie benennen
- Führe das Script aus und kopiere den **rohen STDOUT** (Spaltennamen der
  kodierten Variablen) vollständig in `logs/stage_2_log.md`
- **Erst wenn der STDOUT im Log steht, darf Schritt 3b beginnen.**

### 3b. Hauptanalyse
Führe die in Stage 1 gewählte Methode durch:
- Alle Berechnungen dokumentieren und via SQL gegenchecken
- Effektgrößen berechnen (nicht nur p-Werte)
- VIF berechnen falls Regression

### 3c. Praktische Signifikanz — PFLICHTINTERPRETATION

**Statistische Signifikanz ≠ Praktische Relevanz.** Für den Hauptbefund gilt:

Bewerte nach Cohen-Konventionen:
- Cohen's f² < 0.02 → kleiner Effekt (praktisch irrelevant)
- Cohen's f² 0.02–0.14 → mittlerer Effekt
- Cohen's f² ≥ 0.15 → großer Effekt
- Pearson |r| < 0.10 → vernachlässigbar
- Pearson |r| 0.10–0.29 → schwach
- Pearson |r| ≥ 0.30 → moderat bis stark

**Wenn der Hauptbefund einen kleinen oder vernachlässigbaren Effekt hat:**
- Formuliere das explizit als Null-Ergebnis: *"Es gibt keinen bedeutsamen Zusammenhang zwischen X und Y."*
- Ein Null-Ergebnis ist eine wissenschaftliche Aussage — nicht ein Misserfolg.
- p<0.05 bei kleinem Effekt bedeutet: statistisch nachweisbar, aber praktisch ohne Bedeutung.
- Berichte beides im Paper: den p-Wert UND die inhaltliche Einordnung.
- Erkläre im Discussion warum der Effekt trotz Signifikanz nicht relevant ist.

Dokumentiere im Log: gemessene Effektgröße + Cohen-Kategorie + praktische Interpretation.

### 4. Visualisierungen
Wähle selbstständig geeignete Grafiken die die zentralen Ergebnisse am klarsten kommunizieren. Entscheide eigenständig welche Darstellungsform (Boxplot, Heatmap, Scatterplot etc.) am besten passt. Speichere als PNG in `experiment/figures/`. Begründe die Wahl im Log. Speichere Plot-Code als `scripts/generate_figures.py`.

### 5. Robustheitsprüfung
- Voraussetzungen der gewählten Methode prüfen
- Vorzeichenwechsel zwischen bivariater Korrelation und Regressionskoeffizienten erklären falls vorhanden

## Erfolgskriterium
- Alle Kennzahlen aus DB berechnet und belegbar
- Vollständige Missing-Data-Analyse
- Mindestens 2 Visualisierungen
- VIF oder Intercorrelation-Matrix falls Regression

## LOG
Erstelle `logs/stage_2_log.md`:
- Alle SQL-Abfragen und Ergebnisse
- Vollständige Ergebnistabellen
- Missing-Data-Statistik komplett
- Grafik-Auswahl und Begründung
- Unerwartete Befunde

---

## WEITER
Stage abgeschlossen → lies und führe aus: `stages/stage_3_synthesis.md`
