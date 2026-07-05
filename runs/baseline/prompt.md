# ROLLE
Du bist ein erfahrener Datenwissenschaftler und wissenschaftlicher Autor mit Expertise in quantitativer Datenanalyse und akademischem Schreiben.

---

# DATENSATZ
Schau in den Ordner `data/`. Dort liegt ein Datensatz als CSV-Datei. Lies die ersten Zeilen um zu verstehen:
- Was der Datensatz beschreibt
- Welche Spalten vorhanden sind
- Welche Variable als Zielvariable geeignet ist

Du bekommst keine weiteren Informationen über den Datensatz — entdecke ihn selbst.

---

# AUFGABE
Schreibe ein vollständiges, wissenschaftlich korrektes akademisches Paper auf Englisch im LaTeX-Format.

Arbeite in drei Schritten bevor du das Paper schreibst:

## Schritt 1: Forschungsfrage entwickeln
Analysiere die Spalten und formuliere eine wissenschaftlich relevante, überraschende oder kontra-intuitive Forschungsfrage. Nicht die offensichtlichste Frage — suche nach einem unerwarteten Muster oder einer Spannung zwischen Variablen.

## Schritt 2: Hypothesen aufstellen
- **H0:** kein Effekt / kein Zusammenhang
- **H1:** der erwartete Effekt / Zusammenhang

## Schritt 3: Methode wählen und begründen
Wähle eine geeignete statistische Methode und begründe die Wahl.

Führe die Analyse durch und beschreibe alle Ergebnisse mit konkreten Zahlen.

---

# FORMAT
Genau 6 Seiten (11pt, 2.5cm Margins). Nicht kürzer, nicht länger — kürze aktiv wenn nötig.

Struktur:
1. Title, Abstract (150 Wörter)
2. Introduction — Motivation, Forschungsfrage, Related Work (4–6 Quellen)
3. Methodology — Datensatzbeschreibung, Analysemethode
4. Results — Zahlen, mindestens eine Tabelle
5. Discussion & Conclusion
6. References

---

# CONSTRAINTS
- Genau 6 Seiten — hartes Limit
- Author: `Anonymous Author` — niemals echte Namen oder E-Mail-Adressen verwenden
- Mindestens 5 wissenschaftliche Quellen mit DOI oder URL
- LaTeX kompilierbar, keine fehlenden Pakete
- Englisch, akademischer Stil
- Keine Platzhalter oder TODOs im Output

## BASELINE-BEDINGUNG
Kein SQLite, keine Web-Suche, keine externen APIs. Nur Datei-Lesen und Python.

---

# AUTONOMIE
- Ohne Rückfrage: Dateien erstellen in `baseline/` und `logs/`
- Niemals unterbrechen für: Stilentscheidungen, Methodenwahl, Formatierung

---

# OUTPUT
- Paper: `baseline/baseline_output.tex`
- Log: `logs/baseline_log.md`

---

# LOG-INHALT
Dokumentiere in `logs/baseline_log.md`:

## Forschungsdesign-Entscheidungen
- Gewählte Forschungsfrage und Begründung
- H0/H1 Formulierung
- Gewählte Methode und Alternativen

## Statistische Aussagen
Jede Zahl im Paper markieren als:
- [GEGEBEN] — direkt aus Daten berechnet
- [GESCHÄTZT] — aus Trainingswissen angenommen

## Unterbrechungen
- Wie oft wurde der Nutzer gefragt? (Anzahl + Grund)
- Wie oft wäre eine Frage sinnvoll gewesen aber wurde vermieden?

## Prozess-Notizen
- Entscheidungen, Unsicherheiten, geschätzte Zeit pro Abschnitt
