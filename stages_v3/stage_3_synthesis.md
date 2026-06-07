# STAGE 3 — Synthese & Paper-Schreiben

## PRIVACY
Author = `Anonymous Author`. Kein echter Name, keine E-Mail.

## Aufgabe
Schreibe ein vollständiges wissenschaftliches Paper auf Basis aller validierten
Ergebnisse. Lies zuerst alle vorherigen Logs.

## Kontext (lies vor dem Schreiben)
- Pre-Analysis Plan: `logs/v3/preanalysis_plan.json`
- Forschungsfrage, Quellen: `logs/v3/stage_1_log.md`
- Statistische Ergebnisse: `logs/v3/stage_2_log.md`
- Adversarial Critic Einwände + Reaktionen: `logs/v3/adversarial_critic_log.md`
- Grafiken: `experiment_v3/figures/`

## LaTeX-Header
```latex
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{natbib}
\usepackage{geometry}
\usepackage{hyperref}
\graphicspath{{../experiment_v3/figures/}}
```

## Struktur — genau 6 Seiten (11pt, 2.5cm Margins)

### 1. Abstract (150 Wörter)

### 2. Introduction
- Motivation, Forschungsfrage
- Verweis auf Pre-Analysis Plan: "This study follows a pre-registered analysis plan
  (Stage 0b artifact) to minimize researcher degrees of freedom."

### 3. Methodology
- Datensatzbeschreibung mit Missing-Data-Angabe
- PRISMA-Flow: "We identified N papers via systematic search [string], screened N
  abstracts against inclusion criteria [X, Y, Z], and retained N papers."
- Analysemethode, Kovariaten (wie im PAP spezifiziert)
- Mediationsmodell falls vorhanden
- Data Availability Statement:
  "Data: Stack Overflow Developer Survey 2024 (public). Analysis code:
  available as supplementary material (scripts/analysis_v3.py)."

### 4. Results
- Alle Zahlen aus `logs/v3/stage_2_log.md`
- Bootstrap-CIs für Hauptbefund: "d = X.XX, 95% BCa CI [X.XX, X.XX]"
- Power-Statement: "The analytic sample provides >99% power to detect d ≥ 0.05"
- Mediationsergebnis falls vorhanden (Pfade a, b, c, c', indirekter Effekt)
- Multiverse-Ergebnis: "Robust in X/5 Spezifikationen"
- Exploratorische Analysen klar als EXPLORATORY markiert

### 5. Discussion & Conclusion
- Interpretation des Hauptbefunds
- **Counter-Narrative Sektion (PFLICHT, neu in v3):**
  Suche vor dem Schreiben via Fetch-MCP nach mindestens 2 Papers die das
  Gegenteil finden oder den Befund kritisieren:
  - Search: "[topic] null result job satisfaction"
  - Search: "[topic] measurement critique self-report"
  - Search: "[topic] no significant effect"
  Schreibe einen Absatz "Alternative Explanations and Contradicting Evidence"
  der diese Gegenbelege fair zusammenfasst und erklärt warum H1 trotzdem gestützt wird.
- Adversarial Critic Einwände (alle HOCH-bewerteten Punkte adressieren)
- Limitationen (Kausalität, Cross-Sectional Design, Selbstbericht-Bias, Generalisierbarkeit)
- Implikationen für Forschung und Praxis

### 6. References
- Nur real recherchierte Quellen aus Stage 1 (PRISMA-verifizierten Quellen)
- Mindestens 15 Quellen
- Mindestens 50% aus den letzten 5 Jahren (2020–2025)
- Keine Quelle die den CRITIC-CHECK nicht bestanden hat

---

## INLINE CRITIC-CHECK — Semantic Verification (PFLICHT während des Schreibens)

Für jede Zahl im Paper:
```
Zahl: [z.B. d = 0.327]
Quelle: logs/v3/stage_2_log.md, Abschnitt: [Name]
Gefunden: JA / NEIN
```

Für jede Citation:
1. URL via Fetch-MCP nochmals abrufen
2. Prüfe: Stützt der Abstract genau diese Behauptung?
```
Claim: "[der Satz]"
Quelle: [Titel, URL]
Abstract sagt: "[relevante Textstelle]"
Korrekt belegt: JA / NEIN
```
Bei NEIN: Formulierung anpassen oder Quelle ersetzen. Mindestens 15 Checks dokumentieren.

---

## Constraints
- Genau 6 Seiten
- Author: Anonymous Author
- Keine geschätzten Zahlen — jede Zahl aus `logs/v3/stage_2_log.md`
- Exploratorische Analysen explizit als EXPLORATORY markiert
- PAP-Abweichungen im Methodenteil erwähnt

## LOG
Erstelle `logs/v3/stage_3_log.md`:
- Zahlen-Quellennachweis (alle Zahlen aus welchem Log-Abschnitt)
- Counter-Narrative-Quellen (URLs + wie adressiert)
- Inline Critic-Check-Tabelle (≥15 Checks, alle JA/NEIN)
- PAP-Abweichungen falls vorhanden

---

## WEITER
Stage abgeschlossen → lies und führe aus: `stages_v3/stage_4_export.md`
