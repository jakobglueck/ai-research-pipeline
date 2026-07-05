# STAGE 0 — Setup & Datenbank

## PRIVACY
Verwende niemals persönliche Daten aus dem Kontext (Name, E-Mail etc.) in Output-Dokumenten. Author = immer `Anonymous Author`.

## Aufgabe
Finde den Datensatz in `data/`, verstehe seine Struktur und importiere ihn in eine SQLite-Datenbank.

## Schritte

1. Erstelle folgende Verzeichnisse falls nicht vorhanden:
   - `runs/v2/output/figures/`, `runs/v2/logs/`
   - `db/` und `scripts/` existieren bereits von v1 — nicht neu anlegen

2. **Datenbank prüfen (nicht neu importieren):**
   - `db/survey.db` existiert bereits von Pipeline v1
   - Prüfe via SQLite-MCP ob die DB korrekt befüllt ist:
     - Zeilenanzahl, Spaltennamen, Schema
     - Fehlende Werte pro Spalte
   - Wenn DB leer oder nicht vorhanden: dann erst `scripts/v1/setup_db.py` ausführen
   - `scripts/v1/mcp_helpers.py` existiert ebenfalls bereits — nicht überschreiben

3. **Datensatz verstehen** (via SQLite-MCP, nicht via CSV):
   - Was misst dieser Datensatz? Wer sind die Befragten?
   - Welche Variablen sind numerisch, welche kategorial?
   - Welche Variable eignet sich als Zielvariable?
   - Welche Variablen könnten interessante Prädiktoren sein?

4. Prüfe via SQLite-MCP (DB-Pfad: `./db/survey.db`):
   - Zeilenanzahl, Spaltennamen, Schema
   - Fehlende Werte pro Spalte

## LOG
Erstelle `runs/v2/logs/stage_0_log.md`:
- Bestätigung dass DB existiert und korrekt befüllt ist
- Kurze Beschreibung: Worum geht es in den Daten?
- Schema (Spalten + Typen)
- Fehlende Werte pro Spalte
- Identifizierte mögliche Zielvariablen
- Aufgetretene Fehler

---

## WEITER
Stage abgeschlossen → lies und führe aus: `runs/v2/stages/stage_1_explore.md`
