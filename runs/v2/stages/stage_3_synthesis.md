# STAGE 3 — Synthese & Paper-Schreiben

## PRIVACY
Author = `Anonymous Author`. Niemals echte Namen, E-Mail-Adressen oder persönliche Daten aus dem Kontext verwenden — auch nicht im \author{} Feld des LaTeX-Dokuments.

## Aufgabe
Schreibe ein vollständiges, kompilierbares wissenschaftliches Paper auf Basis der validierten Ergebnisse aus Stage 1 und Stage 2.

## Kontext (lies vor dem Schreiben)
- Forschungsfrage, H0/H1, Methode, Quellen: `runs/v2/logs/stage_1_log.md`
- Alle statistischen Ergebnisse: `runs/v2/logs/stage_2_log.md`
- Grafiken: `runs/v2/output/figures/`

## LaTeX-Header (immer verwenden)
```latex
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{natbib}
\usepackage{geometry}
\usepackage{hyperref}
\graphicspath{{../runs/v2/output/figures/}}
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
- Keine geschätzten Zahlen — jede Zahl aus `runs/v2/logs/stage_2_log.md`
- Missing-Data vollständig korrekt darstellen
- Vorzeichenwechsel zwischen Korrelation und Regressionskoeffizient erklären falls vorhanden
- SE-Werte nie als "0.000" — bei kleinen SE `< 0.001` oder mehr Nachkommastellen
- LaTeX kompilierbar

---

### ✅ CRITIC-CHECK — Inline Semantic Verification (PFLICHT während des Schreibens)

Dieser Check läuft **während** des Schreibens, nicht danach. Für jeden inhaltlichen
Abschnitt bevor du ihn schreibst:

**Für jede Zahl / statistisches Ergebnis:**
1. Notiere im Log welche Zeile aus `runs/v2/logs/stage_2_log.md` diese Zahl liefert
2. Schreibe die Zahl nur wenn sie dort explizit steht — nie aus Erinnerung
   ```
   Zahl: [z.B. Cohen's d = 0.36]
   Quelle: runs/v2/logs/stage_2_log.md, Abschnitt: [Abschnittsname]
   Gefunden: JA / NEIN
   ```

**Für jede Citation / wissenschaftliche Behauptung:**
1. Rufe die URL der Quelle erneut via Fetch-MCP ab
2. Überprüfe: Stützt der Abstract/Text tatsächlich genau diese Behauptung?
3. Notiere im Log:
   ```
   Claim im Paper: "[der Satz den du schreiben willst]"
   Quelle: [Titel, URL]
   Abstract/Text sagt: "[relevante Textstelle]"
   Claim korrekt belegt: JA / NEIN
   ```
4. Bei **NEIN**: Entweder Behauptung anpassen auf das was die Quelle wirklich sagt,
   oder Quelle ersetzen. Nie eine Behauptung schreiben die die Quelle nicht stützt.

**Wichtig:** Diese Prüfung muss für **alle** Quellen im Related Work und Discussion
durchgeführt werden. Mindestens 5 Prüfungen müssen im Log dokumentiert sein.

---

## LOG
Erstelle `runs/v2/logs/stage_3_log.md`:
- Welche Zahlen aus welchem Log-Abschnitt übernommen
- Entscheidungen zur Struktur
- Probleme beim Schreiben
- **Vollständige Critic-Check-Tabelle**: alle geprüften Claims mit JA/NEIN

---

## WEITER
Stage abgeschlossen → lies und führe aus: `runs/v2/stages/stage_4_export.md`
