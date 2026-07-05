# STAGE 4 — Export & Qualitätskontrolle

## PRIVACY
Prüfe: Enthält das Paper echte Namen oder E-Mails? → Ersetzen durch `Anonymous Author`.

## Aufgabe
QC-Check, LaTeX-Kompilierung, Reproducibility-Artifacts exportieren.

## Schritt 1 — Automatisierter QC (PFLICHT)

Schreibe `scripts/qc_check_v3.py`:
- Lese `experiment_v3/experiment_v3_output.tex` + `logs/v3/stage_2_log.md`
- Prüfe via Regex alle zentralen Zahlen (N, Cohen's d, Bootstrap-CI, p-Werte, R², β)
- Führe das Script aus und kopiere vollständigen STDOUT in `logs/v3/stage_4_log.md`

**Erweiterte QC-Checks (neu in v3):**
- [ ] Citation Count ≥ 15 (zähle `\bibitem` oder `\cite` im .tex)
- [ ] Citation Recency: mind. 50% der Quellen aus 2020–2025 (Jahreszahlen prüfen)
- [ ] Bootstrap-CI vorhanden im Paper?
- [ ] Power Statement vorhanden?
- [ ] PRISMA-Flow im Methodenteil erwähnt?
- [ ] Counter-Narrative Absatz vorhanden?
- [ ] Mindestens 1 Absatz zu Limitations?
- [ ] PAP-Verweis im Methodenteil?
- [ ] Data Availability Statement vorhanden?
- [ ] Exploratorische Analysen als EXPLORATORY markiert?
- [ ] Author = Anonymous Author?
- [ ] Alle Abbildungen eingebunden?

Kein PASS ohne STDOUT-Beweis.

## Schritt 2 — Reproducibility Artifacts exportieren (neu in v3)

Exportiere folgende Dateien für maximale Reproduzierbarkeit:
1. `logs/v3/analysis_queries.sql` — alle sqlite3-Queries aus Stage 2 als SQL-Script
2. `logs/v3/prisma_flow.md` — PRISMA-Flow aus Stage 1 als eigenständiges Dokument
3. `logs/v3/preanalysis_plan.json` — bereits aus Stage 0b vorhanden, bestätigen

## Schritt 3 — LaTeX kompilieren
```bash
tectonic experiment_v3/experiment_v3_output.tex
```
Fehler korrigieren, nochmal kompilieren. Alle Fehler im Log dokumentieren.

## Schritt 4 — Speichern
Finales Paper: `experiment_v3/experiment_v3_output.tex` + `.pdf`

## LOG
Erstelle `logs/v3/stage_4_log.md`:
- Vollständiger QC-STDOUT
- Ergebnis aller erweiterten Checks (✓/✗)
- LaTeX-Fehler und Korrekturen
- Gesamtdauer (geschätzt)
- Anzahl menschlicher Eingriffe

Erstelle `logs/v3/experiment_v3_summary.md`:

### Pipeline-Statistik
- SQL-Abfragen gesamt
- Python-Script-Ausführungen
- Fetch-MCP Aufrufe
- Critic-Check-Durchläufe gesamt: Stage 1 / Stage 2 / Stage 2b / Stage 3
- Adversarial-Critic HOCH-Bewertungen + wie adressiert
- Counter-Narrative Quellen gefunden
- Menschliche Eingriffe (Anzahl + Art)

### Qualitäts-Selbstcheck
- Pre-Analysis Plan eingehalten?
- PAP-Abweichungen dokumentiert?
- Citation count und Recency bestanden?
- Bootstrap-CIs berichtet?
- Mediation getestet?
- Adversarial Critic vollständig abgearbeitet?
- Counter-Narrative in Discussion?
- Reproducibility Artifacts exportiert?

---

## PIPELINE V3 ABGESCHLOSSEN
Alle Outputs in `experiment_v3/`, Logs in `logs/v3/`.
