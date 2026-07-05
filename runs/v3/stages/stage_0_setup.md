# STAGE 0 — Setup & Datenbank

## PRIVACY
Verwende niemals persönliche Daten aus dem Kontext. Author = `Anonymous Author`.

## Aufgabe
Verzeichnisse anlegen, DB prüfen, Existenz bestehender Scripts bestätigen.

## Schritte

1. Erstelle folgende Verzeichnisse falls nicht vorhanden:
   - `runs/v3/output/figures/`, `runs/v3/logs/`
   - `db/` und `scripts/` existieren bereits — nicht neu anlegen

2. **Datenbank prüfen (nicht neu importieren):**
   - `db/survey.db` existiert bereits von Pipeline v1/v2
   - Prüfe via sqlite3 Bash:
     - Zeilenanzahl, Spaltennamen, Schema
     - Fehlende Werte pro Spalte
   - Wenn DB leer oder nicht vorhanden: `scripts/v1/setup_db.py` ausführen

3. Datensatz via sqlite3 verstehen:
   - Welche Variablen sind numerisch, welche kategorial?
   - Welche Variable eignet sich als Zielvariable?
   - Welche Variablen könnten Mediatoren sein (z.B. JobInsecurity, Autonomy, Stress)?

4. **Script-Regel:** Alle neuen Scripts bekommen `_v3`-Suffix.
   Niemals bestehende Scripts (v1/v2) überschreiben.

## LOG
Erstelle `runs/v3/logs/stage_0_log.md`:
- DB-Status (Zeilenanzahl, Schema-Check)
- Identifizierte Zielvariablen
- Identifizierte mögliche Mediator-Variablen

---

## WEITER
Stage abgeschlossen → lies und führe aus: `runs/v3/stages/stage_0b_preanalysis_plan.md`
