# STAGE 0b — Pre-Analysis Plan (PAP) — DATENZUGRIFF VERBOTEN

## Zweck
Dieser Stage eliminiert strukturelles HARKing (Hypothesizing After Results Known).
Du spezifizierst die vollständige Analysestrategie **bevor** du auch nur eine SQL-Query
auf die Inhaltsdaten läufst. Der Plan wird als JSON-Artifact gespeichert und ist danach
LOCKED — jede Abweichung in Stage 2 muss als EXPLORATORY markiert werden.

## WICHTIG: Keine Daten ansehen
- Kein `SELECT ... FROM survey` auf inhaltliche Variablen
- Kein Lesen von stage_1_log.md aus früheren Runs
- Nur erlaubt: Spaltennamen und Datentypen (`PRAGMA table_info`) — kein Inhalt

## Aufgabe
Erstelle den Pre-Analysis Plan auf Basis von:
1. Theoretischem Wissen über KI, Arbeit, Jobzufriedenheit
2. Den Spaltennamen aus dem Schema (kein inhaltlicher Zugriff)
3. Eigenem Weltwissen über die Stack Overflow Developer Survey

## Der Plan muss enthalten

### 1. Primäre Forschungsfrage + Hypothese
- Formuliere eine kontraintuitive, nicht-triviale Forschungsfrage
- Die Frage DARF NICHT identisch oder sehr ähnlich zu diesen bisherigen Runs sein:
  - v1: "Fear Over Pay" — AIThreat stärker als Gehalt für JobSat
  - v2: "Perception Over Adoption" — AIThreat stärker als AISelect für JobSat
- H0 (Nullhypothese), H1 (gerichtete Alternativhypothese)
- Erwartete Richtung des Effekts und Begründung (theoretisch, nicht datengetrieben)

### 2. Mediationshypothese (falls plausibel)
- Gibt es eine Variable die AIThreat → JobSat theoretisch vermittelt?
  - z.B. Jobinsicherheit, Autonomieverlust, emotionale Erschöpfung
- Falls ja: Spezifiziere den Mediator und die erwartete Mediationsstruktur
  (total effect c, direct effect c', indirect effect a×b)

### 3. Geplante statistische Methode
- Haupttest (OLS, t-Test, ANOVA, Mediation?)
- Kovariaten (welche und warum — theoretisch begründet)
- Behandlung fehlender Werte (Listwise Deletion vs. Imputation — begründet)
- Signifikanzschwelle: α = 0.05 (zweiseitig)
- Mindest-Effektgröße für praktische Relevanz: Cohen's d ≥ 0.25 ODER f² ≥ 0.02

### 4. Novelty-Check
- Formuliere 2 alternative Forschungsfragen falls die primäre zu ähnlich zu v1/v2 ist
- Bewerte Ähnlichkeit zu v1/v2: HOCH / MITTEL / NIEDRIG
- Falls HOCH: Primäre Frage verwerfen, Alternative wählen

### 5. Exploratorische Analysen (klar gelabelt)
- Was wäre interessant aber NICHT primär hypothetisiert?
- Diese müssen im Paper als EXPLORATORY markiert werden

## Novelty-Score (PFLICHT, neu in v3)
Nach Formulierung der primären Forschungsfrage:

1. Berechne manuell eine Ähnlichkeitsschätzung zur Forschungsfrage gegenüber:
   - v1-Kernaussage: "AIThreat stärker als Gehalt für JobSat unter Entwicklern"
   - v2-Kernaussage: "AIThreat stärker als AISelect für JobSat unter Entwicklern"
2. Beurteile für die eigene Frage: Überlappung HOCH (>70%) / MITTEL (40-70%) / NIEDRIG (<40%)
3. Schreibe in den PAP: `"novelty_score": "LOW/MEDIUM/HIGH"` mit Begründung
4. Bei HOCH-Überlappung: Frage verwerfen, Alternative aus Punkt 4 wählen

## DAG — Kausale Annahmen explizit machen (neu in v3)
Bevor Daten angeschaut werden, zeichne den kausalen Graphen als Text-DAG:
```
Kausalpfade (Pfeile = angenommene Kausalrichtung):
AIThreat → JobSat
AIThreat → [Mediator?] → JobSat
[Konfundierung?] → AIThreat, [Konfundierung?] → JobSat
```
Begründe jede Pfeilrichtung theoretisch (1 Satz pro Pfad).
Speichere als `"causal_dag"` Feld im PAP-JSON.

## Output
Speichere den Plan als `logs/v3/preanalysis_plan.json`:
```json
{
  "pipeline_version": "v3",
  "date": "2026-06-XX",
  "primary_rq": "...",
  "h0": "...",
  "h1": "...",
  "expected_direction": "...",
  "theoretical_basis": "...",
  "mediation_hypothesis": {
    "mediator": "...",
    "expected": "partial / full / none"
  },
  "planned_method": "...",
  "covariates": ["...", "..."],
  "missing_data_strategy": "...",
  "alpha": 0.05,
  "minimum_effect_size": "d >= 0.25",
  "novelty_vs_v1": "LOW/MEDIUM/HIGH",
  "novelty_vs_v2": "LOW/MEDIUM/HIGH",
  "exploratory": ["...", "..."]
}
```

Schreibe außerdem `logs/v3/stage_0b_log.md` mit Begründungen für alle Entscheidungen.

---

## WEITER
Stage abgeschlossen → lies und führe aus: `stages_v3/stage_1_explore.md`
