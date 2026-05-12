# EXPERIMENT PIPELINE — Vollständiger Durchlauf

Führe alle fünf Stages **ohne Unterbrechung** durch. Warte nicht auf User-Input zwischen den Stages.
Arbeite Stage 0 → 1 → 2 → 3 → 4 sequentiell ab. Erst wenn Stage 4 vollständig abgeschlossen
ist (alle Logs geschrieben, LaTeX kompiliert), ist die Pipeline fertig.

## PRIVACY — gilt für alle Stages
Verwende niemals persönliche Daten aus dem Kontext (Name, E-Mail etc.) in Output-Dokumenten.
Author = immer `Anonymous Author`. Auch nicht im `\author{}` Feld des LaTeX-Dokuments.

---

# STAGE 0 — Setup & Datenbank

## Aufgabe
Finde den Datensatz in `data/`, verstehe seine Struktur und importiere ihn in eine SQLite-Datenbank.

## Schritte

1. Erstelle folgende Verzeichnisse:
   - `db/`, `scripts/`, `experiment/figures/`, `logs/`

2. Schau in `data/` — finde die CSV-Datei (egal wie sie heißt)

3. Analysiere die CSV:
   - Spaltenanzahl, Spaltennamen, Datentypen
   - Erste Zeilen lesen um den Inhalt zu verstehen
   - Mögliche Zielvariablen identifizieren

4. Schreibe `scripts/setup_db.py` das:
   - Die CSV in `db/survey.db` importiert (DB-Name immer `survey.db`)
   - Numerische Spalten als REAL, Text als TEXT importiert
   - Fehlende Werte als NULL behandelt (nicht als leere Strings)

5. Führe das Script aus

6. Schreibe `scripts/mcp_helpers.py` mit Hilfsfunktionen für:
   - Mittelwert/SD pro Gruppe (SQLite hat kein STDDEV)
   - Pearson-Korrelation zwischen zwei Spalten
   - Missing-Value-Count pro Spalte
   - Wertverteilung einer Spalte

7. Prüfe via SQLite-MCP (DB-Pfad: `./db/survey.db`):
   - Zeilenanzahl, Spaltennamen, Schema
   - Fehlende Werte pro Spalte

## LOG
Erstelle `logs/stage_0_log.md`:
- Dateiname und Größe des gefundenen Datensatzes
- Kurze Beschreibung: Worum geht es in den Daten?
- Schema (Spalten + Typen)
- Fehlende Werte pro Spalte
- Identifizierte mögliche Zielvariablen
- Aufgetretene Fehler

---

# STAGE 1 — Exploration & Forschungsdesign

## Aufgabe
Exploriere den Datensatz via SQLite-MCP und Python, und entwickle eine überraschende,
kontra-intuitive Forschungsfrage die auf echten Datenmustern basiert.

## MCP-Nutzung
Nutze `scripts/mcp_helpers.py` für Berechnungen die SQL alleine nicht leisten kann.
Erweitere die Helferklassen wenn nötig. SQLite-MCP Pfad: `./db/survey.db`.

## Schritte

### 1. Datensatz verstehen
- Was misst dieser Datensatz? Wer sind die Befragten?
- Welche Variablen sind numerisch, welche kategorial?
- Welche Variable eignet sich als Zielvariable?
- Welche Variablen könnten interessante Prädiktoren sein?

### 2. Explorative SQL-Abfragen
- Verteilung der Zielvariable
- Mittelwerte/SD aller numerischen Variablen
- Korrelationen via Python-Hilfsfunktion
- Unerwartete Muster, Ausreißer, Subgruppen
- Interaktionseffekte zwischen je zwei Variablen

### 3. Forschungsfrage — Out of the Box mit Effect-Size-Gate

**Schritt A — Kandidaten sammeln:**
Suche aktiv nach überraschenden oder kontra-intuitiven Mustern:
- Gibt es eine Subgruppe die sich entgegen der Erwartung verhält?
- Widerspricht der Datensatz einer etablierten Annahme?
- Welche Variable hat überraschend keinen oder den stärksten Zusammenhang?
- Gibt es einen Interaktionseffekt der erst durch Kombination zweier Variablen entsteht?

Sammle mindestens **3 Kandidaten-Forschungsfragen** und berechne für jeden einen
schnellen Effektgrößen-Vorabcheck (Pearson r, Eta², Cohen's d, bivariates OR).

**Schritt B — Effect-Size-Gate (MUSS bestanden werden):**
Eine Forschungsfrage darf nur weiterverfolgt werden wenn mindestens eines gilt:
- Pearson/Spearman |r| ≥ 0.15
- Cohen's d ≥ 0.25
- Eta² ≥ 0.01
- Odds Ratio ≥ 1.5 oder ≤ 0.67

Kein Kandidat besteht das Gate → weitere Variablenkombinationen suchen.
Dokumentiere alle geprüften Kandidaten mit Effekten im Log.

**Schritt C — Finale Auswahl:**
Wähle die Frage die sowohl kontraintuitiv als auch den Gate besteht.
**Achtung:** Den Gate mit einer offensichtlichen Frage zu bestehen zählt nicht —
die Frage muss trotzdem überraschend oder nicht-trivial sein.

**Achtung Interaktionseffekte:** Wenn die Forschungsfrage eine Interaktion (Moderation)
untersucht, muss der **Interaktionsterm selbst** (nicht nur der Haupteffekt) einen
mittleren oder großen Effekt haben: f² ≥ 0.02. Ein signifikanter Haupteffekt
als Gate-Erfüllung mit trivialem Interaktionsterm f²<0.01 zählt **nicht** — das
wäre ein statistisch signifikantes Null-Ergebnis. Suche in diesem Fall weiter.

Formuliere:
- **Forschungsfrage** — präzise und beantwortbar
- **H0** — kein Effekt
- **H1** — erwarteter Effekt
- **Methode** — begründet zur Frage passend
- **Vorab-Effektgröße** — Wert + erfülltes Gate-Kriterium

### 4. Literaturrecherche
Nutze Fetch-MCP für mindestens **5 wissenschaftliche Quellen** die zur Forschungsfrage passen:
- ArXiv: `https://arxiv.org/search/?searchtype=all&query=...`
- Semantic Scholar: `https://www.semanticscholar.org/search?q=...`
- **Fallback-Loop:** Wenn die erste Suchanfrage zu wenige Treffer liefert, passe
  die Suchbegriffe iterativ an (breiter fassen, Synonyme, verwandte Konzepte).
- **Abstract-Pflicht:** Lies via Fetch-MCP zwingend den Abstract jedes Papers
  BEVOR es ins Log aufgenommen wird. Zitieren nach Titel allein ist verboten.
- **Relevanz-Begründung (1–2 Sätze):** Für jede Quelle muss im Log stehen,
  warum sie für die spezifische Hypothese relevant ist.
- Für jede Quelle: Titel, Autoren, Jahr, DOI/URL, Abstract-Inhalt, Relevanz

## LOG
Erstelle `logs/stage_1_log.md`:
- Alle SQL-Abfragen und Ergebnisse
- Gefundene Muster und Anomalien
- Warum diese Forschungsfrage interessanter ist als die offensichtliche
- Forschungsfrage, H0, H1, Methode
- Alle 5+ Quellen mit DOI/URL

---

# STAGE 2 — Statistische Analyse

## Aufgabe
Führe die vollständige statistische Analyse durch. Alle Zahlen direkt aus den Daten — keine Schätzungen.

## MCP-Nutzung
Kombiniere SQLite-MCP (`./db/survey.db`) mit Python. Erlaubte Bibliotheken:
`pandas`, `numpy`, `scipy`, `scikit-learn`, `matplotlib`, `seaborn`, `statsmodels`.
Speichere alle Scripts unter `scripts/`.

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
  kategoriale Behandlung (Dummies) gewählt wird.
- Kategoriale Variablen → Dummy-Coding, Referenzkategorie benennen
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
Wähle selbstständig geeignete Grafiken die die zentralen Ergebnisse am klarsten
kommunizieren. Entscheide eigenständig welche Darstellungsform (Boxplot, Heatmap,
Scatterplot etc.) am besten passt. Speichere als PNG in `experiment/figures/`.
Begründe die Wahl im Log. Speichere Plot-Code als `scripts/generate_figures.py`.

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

# STAGE 3 — Synthese & Paper-Schreiben

## Aufgabe
Schreibe ein vollständiges, kompilierbares wissenschaftliches Paper auf Basis der
validierten Ergebnisse aus Stage 1 und Stage 2.

## Kontext (lies vor dem Schreiben)
- Forschungsfrage, H0/H1, Methode, Quellen: `logs/stage_1_log.md`
- Alle statistischen Ergebnisse: `logs/stage_2_log.md`
- Grafiken: `experiment/figures/`

## LaTeX-Header (immer verwenden)
```latex
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{natbib}
\usepackage{geometry}
\usepackage{hyperref}
\graphicspath{{../experiment/figures/}}
```

## Struktur — genau 6 Seiten (11pt, 2.5cm Margins)
1. **Abstract** — 150 Wörter
2. **Introduction** — Motivation, Forschungsfrage, Related Work mit allen Quellen aus Stage 1
3. **Methodology** — Datensatzbeschreibung mit korrekter Missing-Data-Angabe, Analysemethode
4. **Results** — alle Zahlen aus Stage 2, Tabellen, Grafiken via `\includegraphics`
5. **Discussion & Conclusion** — Interpretation, Limitationen, Implikationen
6. **References** — nur real recherchierte Quellen aus Stage 1

## Constraints
- **Genau 6 Seiten** — kürze aktiv wenn nötig, füge hinzu wenn zu kurz
- **Author: Anonymous Author** — kein echter Name, keine E-Mail
- Keine geschätzten Zahlen — jede Zahl aus `logs/stage_2_log.md`
- Missing-Data vollständig korrekt darstellen
- Vorzeichenwechsel zwischen Korrelation und Regressionskoeffizient erklären falls vorhanden
- SE-Werte nie als "0.000" — bei kleinen SE `< 0.001` oder mehr Nachkommastellen
- LaTeX kompilierbar

## LOG
Erstelle `logs/stage_3_log.md`:
- Welche Zahlen aus welchem Log übernommen
- Entscheidungen zur Struktur
- Probleme beim Schreiben

---

# STAGE 4 — Export & Qualitätskontrolle

## Aufgabe
Konsistenzprüfung, LaTeX kompilieren, finalen Output speichern.

## Schritte

### 1. Konsistenzprüfung — QC muss Beweis liefern, keine Selbstbehauptung

**Automatisierter Beweis (Pflicht):**
Schreibe `scripts/qc_check.py`:
- Lese `experiment/experiment_output.tex` und `logs/stage_2_log.md` ein
- Prüfe per Regex/String-Matching ob zentrale Zahlen (N, p-Werte, R²,
  b-Koeffizienten, SE-Werte) exakt übereinstimmen
- Führe das Script aus
- Kopiere den **vollständigen rohen STDOUT** in `logs/stage_4_log.md`
- Kein „PASS" ohne Terminal-Output.

**Manuelle Prüfliste (danach):**
- Abbildungen vorhanden und korrekt eingebunden?
- Alle Quellen aus Stage 1 in References — Quellenscodes im Log mit Paper identisch?
- Author = `Anonymous Author`?
- Genau 6 Seiten?

### 2. LaTeX kompilieren
```bash
pdflatex -interaction=nonstopmode experiment/experiment_output.tex
```
Fehler korrigieren und erneut kompilieren. Alle Fehler im Log dokumentieren.

### 3. Speichern
Finales Paper: `experiment/experiment_output.tex`

## LOG
Erstelle `logs/stage_4_log.md`:
- Gefundene und korrigierte Inkonsistenzen
- LaTeX-Fehler und Korrekturen
- Gesamtdauer (geschätzt)
- Anzahl menschlicher Eingriffe

Erstelle `logs/experiment_summary.md`:

### Pipeline-Statistik
- SQL-Abfragen gesamt
- Python-Script-Ausführungen
- Fetch-MCP-Aufrufe
- Menschliche Eingriffe (Anzahl + Art)

### Qualitäts-Selbstcheck
- Privacy eingehalten?
- Seitenlimit eingehalten?
- Alle Zahlen verifiziert?
- Quellen real recherchiert?
- Offene Schwachstellen die menschliche Prüfung benötigen

---

## PIPELINE ABGESCHLOSSEN
Alle Outputs in `experiment/`, Logs in `logs/`.
