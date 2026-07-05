# Stage 0 Log — Setup & Datenbank

**Datum:** 2026-06-07  
**Pipeline:** v2

---

## DB-Status

- Datei: `db/survey.db`
- Status: vorhanden und korrekt befüllt (kein Neuimport notwendig)
- Zeilen: **65.437**
- Tabelle: `survey`

---

## Datensatz-Beschreibung

Stack Overflow Developer Survey (Stack Overflow Annual Developer Survey).  
Befragt werden Software-Entwickler:innen weltweit zu Berufsbild, Technologie-Nutzung, Vergütung, KI-Tools und Arbeitszufriedenheit.

---

## Schema (Spalten + Typen)

| Spalte | Typ | Beschreibung |
|---|---|---|
| ResponseId | REAL | Eindeutige Befragten-ID |
| MainBranch | TEXT | Hauptberuf (Developer / Hobby / Lernend …) |
| Age | TEXT | Altersgruppe |
| Employment | TEXT | Beschäftigungsstatus |
| RemoteWork | TEXT | Remote-Anteil |
| EdLevel | TEXT | Bildungsabschluss |
| YearsCode | REAL | Jahre seit erstem Code schreiben |
| YearsCodePro | REAL | Jahre professionelle Entwicklung |
| DevType | TEXT | Entwickler-Typ (mehrfach) |
| OrgSize | TEXT | Unternehmensgröße |
| Country | TEXT | Land |
| CompTotal | REAL | Bruttogehalt (lokale Währung) |
| ConvertedCompYearly | REAL | Jahresvergütung (USD, normiert) |
| LanguageHaveWorkedWith | TEXT | Genutzte Sprachen |
| AISelect | TEXT | KI-Tool aktuell genutzt (Yes/No/Plan) |
| AISent | TEXT | KI-Sentiment |
| AIBen | TEXT | KI-Nutzen wahrgenommen |
| AIAcc | TEXT | KI-Genauigkeitseinschätzung |
| AIComplex | TEXT | KI für komplexe Aufgaben |
| AIThreat | TEXT | KI als Jobgefahr wahrgenommen |
| AIEthics | TEXT | KI-Ethik-Einschätzung |
| WorkExp | REAL | Arbeitserfahrung in Jahren |
| JobSat | REAL | Jobzufriedenheit (0–10) ← Zielvariable |
| JobSatPoints_1–11 | REAL | Subdimensionen der Jobzufriedenheit |
| SurveyLength | TEXT | Bewertung Umfragelänge |
| SurveyEase | TEXT | Bewertung Umfrageverständlichkeit |

*(weitere Technologie-Spalten: Databases, Platforms, Webframes, Embedded, MiscTech, Tools, Collab-Tools, OpSys, OfficeStack, AI-Tools)*

---

## Fehlende Werte (Schlüsselspalten)

| Spalte | NULL-Werte |
|---|---|
| ResponseId | 0 |
| MainBranch | 0 |
| Age | 0 |
| Employment | 0 |
| RemoteWork | 0 |
| EdLevel | 0 |
| YearsCode | 5.568 |
| YearsCodePro | 13.827 |
| DevType | 0 |
| Country | 0 |
| CompTotal | 31.697 |
| ConvertedCompYearly | 42.002 |
| WorkExp | 35.779 |
| AISelect | 0 |
| AISent | 0 |
| AIBen | 0 |
| **JobSat** | **36.311** |

---

## Mögliche Zielvariablen

1. **JobSat** (0–10, numerisch) — Primäre Zielvariable: Jobzufriedenheit
2. **ConvertedCompYearly** (numerisch, USD) — Alternative: Vergütung
3. **AISelect** (kategorial) — Alternativ als Zielvariable für Klassifikation (KI-Adoption)

**Empfohlene Zielvariable für v2: `JobSat`** (kontinuierlich 0–10, 29.126 gültige Werte)

---

## Interessante Prädiktoren

- `AISelect`, `AISent`, `AIBen`, `AIThreat`, `AIEthics` — KI-Einstellungen
- `YearsCode`, `YearsCodePro`, `WorkExp` — Erfahrung
- `RemoteWork` — Arbeitsmodell
- `EdLevel` — Bildung
- `DevType`, `OrgSize` — Berufskontext
- `ConvertedCompYearly` — Vergütung

---

## Fehler

Keine.

---

## Verzeichnisse erstellt

- `experiment_v2/figures/` ✓
- `logs/v2/` ✓
