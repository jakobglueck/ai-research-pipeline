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
Schreibe `scripts/preprocessing_v2.py` (nicht preprocessing.py — v1 darf nicht überschrieben werden):
- Identifiziere alle kategorialen und ordinalen Variablen im Modell
- Für Likert-Skalen (1–5): Begründe **schriftlich im Log** ob ordinale oder
  kategoriale Behandlung (Dummies) gewählt wird. Eine Annahme ohne Begründung
  ist ein Fehler — die Wahl muss vertretbar sein.
- Kategoriale Variablen → Dummy-Coding (One-Hot-Encoding), Referenzkategorie benennen
- Führe das Script aus und kopiere den **rohen STDOUT** (Spaltennamen der
  kodierten Variablen) vollständig in `logs/v2/stage_2_log.md`
- Alle weiteren Analysis-Scripts als `scripts/analysis_v2.py` speichern —
  niemals bestehende Scripts (analysis.py, preprocessing.py) überschreiben
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
Wähle selbstständig geeignete Grafiken die die zentralen Ergebnisse am klarsten kommunizieren. Entscheide eigenständig welche Darstellungsform (Boxplot, Heatmap, Scatterplot etc.) am besten passt. Speichere als PNG in `experiment_v2/figures/`. Begründe die Wahl im Log. Speichere Plot-Code als `scripts/generate_figures_v2.py`.

### 5. Robustheitsprüfung
- Voraussetzungen der gewählten Methode prüfen
- Vorzeichenwechsel zwischen bivariater Korrelation und Regressionskoeffizient erklären falls vorhanden

---

### ✅ CRITIC-CHECK — Statistische Verifikation (PFLICHT nach Schritt 3b)

Dieser Schritt ist nicht optional. Verifiziere jede Kernzahl unabhängig.

Für jede zentrale Kennzahl (Stichprobengröße N, Mittelwerte, Cohen's d / f² / r, Regressionskoeffizienten, p-Werte, R², VIF):

1. Rufe den Wert direkt aus der DB ab via SQLite-MCP — **ohne Python-Script**
2. Vergleiche mit dem Wert aus dem Script-Output
3. Notiere explizit im Log:
   ```
   Kennzahl: [z.B. Cohen's d für Gruppe A vs B]
   Script-Ergebnis: [Wert]
   SQLite-MCP-Verifikation: [raw query + Ergebnis]
   Formel angewendet: [z.B. (M1 - M2) / SD_pooled]
   Übereinstimmung: JA / NEIN (Toleranz: ±0.001)
   ```
4. Bei **NEIN**: Script und SQL-Query debuggen, Diskrepanz erklären und beheben.
   Erst wenn alle Werte übereinstimmen, darf Stage 3 beginnen.

Dokumentiere im Log wie viele Kennzahlen geprüft wurden und wie viele initial
nicht übereinstimmten (auch wenn du sie behoben hast — das ist wertvolles Ergebnis).

---

## Erfolgskriterium
- Alle Kennzahlen aus DB berechnet und belegbar
- Vollständige Missing-Data-Analyse
- Mindestens 2 Visualisierungen
- VIF oder Intercorrelation-Matrix falls Regression
- **Critic-Check vollständig dokumentiert**

## LOG
Erstelle `logs/v2/stage_2_log.md`:
- Alle SQL-Abfragen und Ergebnisse
- Vollständige Ergebnistabellen
- Missing-Data-Statistik komplett
- Grafik-Auswahl und Begründung
- Unerwartete Befunde
- **Critic-Check-Tabelle** mit allen verifizierten Kennzahlen

---

## WEITER
Stage abgeschlossen → lies und führe aus: `stages_v2/stage_3_synthesis.md`
