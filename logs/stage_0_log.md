# Stage 0 Log — Setup & Database

## Dataset
- **Dateiname:** `data/survey_results_public.csv`
- **Größe:** 155,786 KB (≈ 152 MB)
- **Zeilen:** 65,437 Befragte
- **Spalten:** 114

## Beschreibung
Stack Overflow Annual Developer Survey (2024). Befragt werden Softwareentwicklerinnen und -entwickler weltweit zu ihrer beruflichen Situation, verwendeten Technologien, Lernerfahrungen, KI-Nutzung und Arbeitszufriedenheit. Die Daten umfassen demografische Angaben, Berufserfahrung, Gehalt, Technologie-Stacks sowie Einstellungen zu KI-Tools und Stack Overflow.

## Schema (Spalten + Typen)

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| ResponseId | REAL | Eindeutige Befragten-ID |
| MainBranch | TEXT | Entwickler-Status (Beruf/Hobby/lernt gerade) |
| Age | TEXT | Altersgruppe |
| Employment | TEXT | Beschäftigungsstatus |
| RemoteWork | TEXT | Remote/Hybrid/Vor-Ort |
| EdLevel | TEXT | Ausbildungsniveau |
| YearsCode | REAL | Gesamtjahre Coding (inkl. Ausbildung) |
| YearsCodePro | REAL | Berufliche Coding-Jahre |
| DevType | TEXT | Jobbezeichnung |
| OrgSize | TEXT | Unternehmensgröße |
| Country | TEXT | Wohnland |
| CompTotal | REAL | Jahresgehalt (Landeswährung) |
| ConvertedCompYearly | REAL | Jahresgehalt (USD, normalisiert) |
| AISelect | TEXT | Verwendet KI-Tools aktiv |
| AISent | TEXT | Einstellung zu KI |
| AIBen | TEXT | Erwarteter KI-Nutzen |
| AIAcc | TEXT | Vertrauen in KI-Ausgaben |
| AIComplex | TEXT | Komplexitätslimit von KI |
| AIThreat | TEXT | Empfindet KI als Bedrohung |
| Knowledge_1–9 | TEXT | Likert-Skala (Stimme zu/nicht zu) |
| Frequency_1–3 | TEXT | Stack Overflow Nutzungsfrequenz |
| JobSat | REAL | Jobzufriedenheit (1–10) |
| JobSatPoints_1–11 | REAL | Zufriedenheitspunkte pro Dimension |
| WorkExp | REAL | Berufserfahrung (Jahre) |
| ICorPM | TEXT | Individual Contributor vs. Project Manager |
| Frustration | TEXT | Frustrationslevel (Zeitsuche) |
| TimeSearching | TEXT | Zeit für Informationssuche |
| TimeAnswering | TEXT | Zeit für Antwortbeantwortung |

## Fehlende Werte pro Spalte

| Spalte | Fehlend | % |
|--------|---------|---|
| YearsCode | 5,568 | 8.51% |
| YearsCodePro | 13,827 | 21.13% |
| CompTotal | 31,697 | 48.44% |
| ConvertedCompYearly | 42,002 | 64.19% |
| WorkExp | 35,779 | 54.68% |
| JobSat | 36,311 | 55.49% |
| JobSatPoints_* | ~36,000 | ~55% |
| AINextMuch more integrated | 20,730 | 31.68% |
| AINextMuch less integrated | 33,020 | 50.46% |
| OpSysPersonal use | 402 | 0.61% |
| AIToolCurrently Using | 905 | 1.38% |

Die meisten Kernspalten (Employment, Age, Country, AISelect, DevType) haben keine fehlenden Werte.

## Identifizierte Zielvariablen (potenzielle Ziele)

1. **JobSat** (REAL, 1–10) — Jobzufriedenheit. Geeignet für Regression; 55% missing.
2. **ConvertedCompYearly** (REAL) — Jahresgehalt USD. Schief verteilt; 64% missing.
3. **AISelect** (TEXT: Yes/No/Unsure) — KI-Nutzung. Geeignet als binäre Zielvariable.
4. **AIThreat** (TEXT: Yes/No) — Empfindet KI als Bedrohung.

## Aufgetretene Fehler
- Knowledge_1–9 und Frequency_1–3 waren initial fälschlicherweise als REAL deklariert (100% NULL-Rate), da sie Likert-Text-Werte enthalten. Korrektur auf TEXT in zweitem DB-Import.
- WorkExp: 54.68% fehlend, da nur für nicht-selbstständige Befragte erhoben.
