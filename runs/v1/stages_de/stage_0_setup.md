# STAGE 0 — Setup & Datenbank

## PRIVACY
Verwende niemals persönliche Daten aus dem Kontext (Name, E-Mail etc.) in Output-Dokumenten. Author = immer `Anonymous Author`.

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

## WEITER
Stage abgeschlossen → lies und führe aus: `stages/stage_1_explore.md`
