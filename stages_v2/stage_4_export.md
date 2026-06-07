# STAGE 4 — Export & Qualitätskontrolle

## PRIVACY
Prüfe explizit: Enthält das Paper echte Namen oder E-Mail-Adressen? Falls ja, ersetze durch `Anonymous Author`.

## Aufgabe
Konsistenzprüfung, LaTeX kompilieren, finalen Output speichern.

## Schritte

### 1. Konsistenzprüfung — QC muss Beweis liefern, keine Selbstbehauptung

**Automatisierter Beweis (Pflicht):**
Schreibe `scripts/qc_check_v2.py`:
- Lese `experiment_v2/experiment_v2_output.tex` und `logs/v2/stage_2_log.md` ein
- Prüfe per Regex/String-Matching ob die zentralen Zahlen (N, p-Werte, R²,
  b-Koeffizienten, SE-Werte) exakt übereinstimmen
- Führe das Script aus
- Kopiere den **vollständigen rohen STDOUT** in `logs/v2/stage_4_log.md`
- Kein „PASS" ohne Terminal-Output. Ein „PASS" ohne Beweis ist kein QC.

**Manuelle Prüfliste (danach):**
- Abbildungen vorhanden und korrekt eingebunden?
- Alle Quellen aus Stage 1 in References — keine dazugekommen, keine weggefallen?
- Quellenscodes im Log stimmen mit References im Paper überein?
- Author = `Anonymous Author`?
- Genau 6 Seiten?
- Critic-Check-Einträge in logs/v2/stage_1_log.md, stage_2_log.md, stage_3_log.md vorhanden?

### 2. LaTeX kompilieren
```bash
pdflatex -interaction=nonstopmode experiment_v2/experiment_v2_output.tex
```

Fehler korrigieren und erneut kompilieren. Alle Fehler im Log dokumentieren.

### 3. Speichern
Finales Paper: `experiment_v2/experiment_v2_output.tex`

## LOG
Erstelle `logs/v2/stage_4_log.md`:
- Gefundene und korrigierte Inkonsistenzen
- LaTeX-Fehler und Korrekturen
- Gesamtdauer (geschätzt)
- Anzahl menschlicher Eingriffe

Erstelle `logs/v2/experiment_v2_summary.md`:

### Pipeline-Statistik
- SQL-Abfragen gesamt
- Python-Script-Ausführungen
- Fetch-MCP-Aufrufe
- Critic-Check-Durchläufe: gesamt / davon FAIL (+ was korrigiert wurde)
- Menschliche Eingriffe (Anzahl + Art)

### Qualitäts-Selbstcheck
- Privacy eingehalten?
- Seitenlimit eingehalten?
- Alle Zahlen verifiziert?
- Quellen real recherchiert und semantisch geprüft?
- Offene Schwachstellen die menschliche Prüfung benötigen

---

## PIPELINE V2 ABGESCHLOSSEN
Alle Outputs in `experiment_v2/`, Logs in `logs/v2/`.
