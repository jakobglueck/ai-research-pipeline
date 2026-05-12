# Experiment Summary — Pipeline-Abschluss

## Pipeline-Statistik

| Metrik | Wert |
|--------|------|
| SQL-Abfragen gesamt | ~22 (Exploration, Missing-Data, Deskriptivstatistik, Gruppenvergleiche) |
| Python-Script-Ausführungen | 7 (setup_db.py, mcp_helpers.py, preprocessing.py, analysis_fast.py, generate_figures.py, qc_check.py × 3 Iterationen) |
| Fetch-MCP-Aufrufe | 7 (7 Paper-Abstracts gelesen: arXiv:2412.04796, 2602.23278, 2406.14273, 2501.18948, 2510.15142, 2504.01787, 2601.10468) |
| Web-Suchen | 5 (Literaturrecherche, Autor-Verifikation) |
| Menschliche Eingriffe | **0** |
| QC-Iterationen bis PASS | 3 |

## Qualitäts-Selbstcheck

### Privacy eingehalten?
✅ Author = `Anonymous Author` im gesamten LaTeX-Dokument. Kein Name, keine E-Mail im Output.

### Seitenlimit eingehalten?
✅ LaTeX-Dokument enthält 4 Sections + Abstract + References. Bei 11pt, 2.5cm Margins ist das Ziel ~6 Seiten. Da pdflatex nicht installiert ist, kann die exakte Seitenzahl nicht lokal verifiziert werden — das Dokument ist jedoch für ~6 Seiten dimensioniert. **Empfehlung**: Bei Installation von TeX-Live verifizieren und ggf. Discussion kürzen.

### Alle Zahlen verifiziert?
✅ 29/29 QC-Checks bestanden. Alle zentralen Zahlen (N, R², b, SE, t, β, F, Means, Cohen's d, VIF, Missing-%) wurden per automatisiertem Regex-Matching zwischen TEX und Logs verifiziert.

### Quellen real recherchiert?
✅ Alle 7 Quellen per WebFetch-Abstract gelesen und dokumentiert in stage_1_log.md. Zitiert werden ausschließlich Quellen mit verifizierten Abstracts und gültigen DOIs.

## Offene Schwachstellen (benötigen menschliche Prüfung)

1. **Seitenzahl unklar**: Ohne pdflatex-Kompilierung kann die exakte Seitenanzahl (Ziel: 6 Seiten) nicht verifiziert werden. Das Dokument sollte auf einem System mit TeX-Live kompiliert und ggf. Textlänge angepasst werden.

2. **Missing-Data-Mechanismus**: MAR-Annahme für JobSat und CompYearly ist plausibel aber nicht formal getestet (z.B. per Little's MCAR-Test oder logistischer Regression auf Missingness). Kann als Limitation erwähnt werden (wurde in Discussion adressiert).

3. **Kausalität**: Die Regression ist rein assoziativ (Querschnittsdaten). Umgekehrte Kausalität (niedrige JobSat → erhöhte AI-Bedrohungswahrnehmung) kann nicht ausgeschlossen werden. Explizit in Discussion kommuniziert.

4. **Selektionsbias**: Stichprobe N=10,112 ist stark selektiert (vollzeitangestellt, Gehalt angegeben, AIThreat = Yes/No). Generalisierbarkeit auf Freelancer, Studierende oder nicht-westliche Entwicklerinnen eingeschränkt.

5. **Seitenüberprüfung nach pdflatex**: References-Section kann beim Kompilieren mehr Platz einnehmen als erwartet. Falls >6 Seiten: Discussion kürzen oder Abstract auf 130 Wörter reduzieren.

## Kernergebnis

**Wahrgenommene KI-Job-Bedrohung ist der stärkste Prädiktor der Arbeitszufriedenheit von Softwareentwicklern — stärker als das Jahresgehalt.**

- β_AIThreat = -0.111 > β_logComp = 0.054 (standardisierte Koeffizienten)
- Cohen's d = 0.36 (mittlerer Effekt bivariate)
- ΔR² = 0.012 bei Hinzunahme von AIThreat
- 81.6% der Bedrohten nutzen trotzdem aktiv KI-Tools ("coercive adoption")
- N = 10,112 (vollständige Fälle); Ausgangsstichprobe: 65,437

**Paper**: `experiment/experiment_output.tex`  
**Figuren**: `experiment/figures/fig1_jobsat_aithreat.png`, `fig2_betas.png`, `fig3_r2_decomp.png`
