# Stage 3 Log — Synthese & Paper-Schreiben

## Übernommene Zahlen aus Stage 2 Log

| Zahl | Quelle | Verwendung im Paper |
|------|--------|---------------------|
| N = 10,112 | stage_2_log.md | Methodology, Abstract, Table 1 |
| N = 65,437 | stage_2_log.md | Introduction, Methodology |
| M(Threat=Yes) = 6.3349, SD = 2.3103 | stage_2_log.md | Table 1, Results |
| M(Threat=No) = 7.0778, SD = 2.0347 | stage_2_log.md | Table 1, Results |
| β_AIThreat = -0.1115 | stage_2_log.md | Abstract, Results, Fig. 2 |
| β_YearsCodePro = 0.0942 | stage_2_log.md | Results, Fig. 2 |
| β_logComp = 0.0538 | stage_2_log.md | Results, Fig. 2 |
| b(AIThreat) = -0.7049, SE = 0.062, t = -11.36 | stage_2_log.md | Table 2 |
| b(YearsCodePro) = 0.0244, SE = 0.003, t = 9.04 | stage_2_log.md | Table 2 |
| b(log1p_Comp) = 0.0809, SE = 0.016, t = 5.16 | stage_2_log.md | Table 2 |
| R²(Model1) = 0.016589 | stage_2_log.md | Table 2, Fig. 3 |
| R²(Model2) = 0.028975 | stage_2_log.md | Table 2, Fig. 3, Abstract |
| ΔR² = 0.012386 | stage_2_log.md | Table 2, Abstract, Discussion |
| F(3,10108) = 100.54 | stage_2_log.md | Table 2 |
| Cohen's d = 0.3587 (rounded 0.36) | stage_2_log.md | Abstract, Discussion |
| Cohen's f² = 0.01276 | stage_2_log.md | Discussion |
| VIF < 1.14 | stage_2_log.md | Results text |
| 81.6% der Bedrohten nutzen AI | stage_1_log.md | Abstract, Discussion |
| 55.5% JobSat missing | stage_2_log.md | Methodology |
| 64.2% Comp missing | stage_2_log.md | Methodology |
| Ausreißer ≥1M USD: 47 | stage_2_log.md | Methodology |

## Strukturentscheidungen

1. **Seitenziel: ~6 Seiten** bei 11pt, 2.5cm Margins, parskip.
   - Abstract: ~150 Wörter ✓
   - Introduction + Related Work: ca. 1.5 Seiten
   - Methodology: ca. 1 Seite
   - Results: ca. 1.5 Seiten (3 Figuren + 2 Tabellen)
   - Discussion: ca. 1 Seite
   - References: ~0.5 Seite

2. **Related Work inline in Introduction**: Kein separater Abschnitt, da bei 6 Seiten platzsparend.

3. **Figures**: 3 Figuren (Boxplot, Betas, R²-Dekomposition) sind ausreichend und kommunizieren die Kernbotschaft klar.

4. **SE-Werte**: Alle SE > 0.001 (z.B. 0.062, 0.003, 0.016) — kein Problem mit "0.000"-Formatierung.

5. **Vorzeichenwechsel**: Kein Vorzeichenwechsel zwischen bivariater Korrelation und Regressionskoeffizienten (r(logComp,JobSat) = 0.093 > 0, b = 0.081 > 0). Daher keine Erklärung nötig.

6. **Missing Data**: Als MAR klassifiziert für JobSat und AIThreat; MNAR möglich für CompYearly. Listwise Deletion mit Begründung.

7. **Author**: Anonymous Author ✓ (kein echter Name)

## Entscheidungen zur Darstellung

- Für Table 2: Beide Modelle nebeneinander (kompakt, ermöglicht direkten Vergleich)
- Formel im Abstract vermieden; stattdessen klare Sprachformulierung
- Cohen's d wird auf 2 Nachkommastellen gerundet (0.36)
- Sternchen-Notation: *** für p < .001

## Probleme beim Schreiben

- LaTeX-Formatierung für Table 2 (beide Modelle in einer Tabelle) benötigt 6 Spalten → booktabs + Midrule gelöst
- \bibitem manuell geschrieben (kein .bib-File für experiment_output.tex), da BibTeX hier nicht verlangt wurde
- \graphicspath gesetzt auf `../experiment/figures/` gemäß Pipeline-Vorgabe
- Seitenlimit wird durch pdflatex-Kompilierung in Stage 4 verifiziert
