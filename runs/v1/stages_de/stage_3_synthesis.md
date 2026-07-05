# STAGE 3 — Synthese & Paper-Schreiben

## PRIVACY
Author = `Anonymous Author`. Niemals echte Namen, E-Mail-Adressen oder persönliche Daten aus dem Kontext verwenden — auch nicht im \author{} Feld des LaTeX-Dokuments.

## Aufgabe
Schreibe ein vollständiges, kompilierbares wissenschaftliches Paper auf Basis der validierten Ergebnisse aus Stage 1 und Stage 2.

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

## WEITER
Stage abgeschlossen → lies und führe aus: `stages/stage_4_export.md`
