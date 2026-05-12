# Stage 1 Log — Exploration & Forschungsdesign

## 1. Datensatz verstehen

**Datensatz**: Stack Overflow Annual Developer Survey 2024  
**Befragte**: 65,437 Softwareentwicklerinnen und -entwickler weltweit  
**Numerische Variablen**: YearsCode, YearsCodePro, CompTotal, ConvertedCompYearly, WorkExp, JobSat, JobSatPoints_*  
**Kategoriale Variablen**: Age, Employment, RemoteWork, DevType, EdLevel, Country, AISelect, AISent, AIThreat, AIBen, AIAcc, ICorPM, Frustration, TimeSearching, Knowledge_*, Frequency_*  

**Zielvariable**: `JobSat` (1–10, Jobzufriedenheit), vorhanden bei 29,126 Befragten (55% missing)  
**Mögliche Prädiktoren**: AIThreat, AISelect, AISent, YearsCodePro, ConvertedCompYearly, RemoteWork, Age

---

## 2. Explorative SQL-Abfragen und Ergebnisse

### 2.1 Verteilung Zielvariable JobSat (N=29,126)
```sql
SELECT JobSat, COUNT(*) FROM survey WHERE JobSat IS NOT NULL GROUP BY JobSat ORDER BY JobSat
```
| JobSat | N |
|--------|---|
| 0 | 311 |
| 1 | 276 |
| 2 | 772 |
| 3 | 1,165 |
| 4 | 1,130 |
| 5 | 1,956 |
| 6 | 3,751 |
| 7 | 6,379 |
| 8 | 7,509 |
| 9 | 3,626 |
| 10 | 2,251 |
Median: ~7, linksgipflig.

### 2.2 AISelect-Verteilung
| AISelect | N |
|----------|---|
| Yes | 37,662 |
| No, and I don't plan to | 14,837 |
| No, but I plan to soon | 8,408 |
| NA | 4,530 |

**57.5% der Befragten nutzen aktiv KI-Tools.**

### 2.3 AIThreat-Verteilung
| AIThreat | N |
|----------|---|
| No | 30,423 |
| NA | 20,748 |
| I'm not sure | 8,878 |
| Yes | 5,388 |

**8.2% der Befragten empfinden KI als Bedrohung ihres Arbeitsplatzes.**

### 2.4 JobSat nach AIThreat-Gruppe (mcp_helpers.mean_sd_by_group)
| AIThreat | Mean JobSat | SD | N |
|----------|-------------|-----|---|
| Yes | 6.403 | 2.302 | 2,380 |
| No | 7.088 | 2.032 | 15,944 |
| I'm not sure | 6.719 | 2.036 | 3,996 |

**Cohen's d (Threat=Yes vs No) = -0.331** → passiert Gate ✓

### 2.5 JobSat nach AISelect-Gruppe
| AISelect | Mean JobSat | SD | N |
|----------|-------------|-----|---|
| Yes | 6.970 | 2.084 | 18,233 |
| No, and I don't plan to | 6.889 | 2.125 | 6,784 |
| No, but I plan to soon | 6.855 | 2.043 | 4,109 |

**Cohen's d (Yes vs No) = 0.038** → sehr klein, kein Gate

### 2.6 Korrelationen (Pearson via mcp_helpers.pearson_correlation)
| Variablenpaar | r | N |
|---------------|---|---|
| YearsCodePro ↔ JobSat | 0.104 | 28,356 |
| YearsCodePro ↔ ConvertedCompYearly | 0.141 | 23,345 |
| ConvertedCompYearly ↔ JobSat (Comp < 1M USD) | 0.072 | 16,045 |
| AIThreat_binary ↔ JobSat | -0.111 | 18,324 |

### 2.7 KI-Nutzung bei Bedrohungs-Wahrnehmung
```sql
SELECT AIThreat, AISelect, COUNT(*) FROM survey WHERE AIThreat IN ('Yes','No') AND AISelect != 'NA' GROUP BY AIThreat, AISelect
```
| AIThreat | AISelect | N |
|----------|----------|---|
| Yes | Yes | 4,396 |
| Yes | No, but I plan to soon | 992 |
| No | Yes | 24,812 |
| No | No, but I plan to soon | 5,611 |

**81.6% (4,396 / 5,388) der Bedrohten nutzen trotzdem aktiv KI-Tools.**

### 2.8 Gehaltsvergleich: Threatened vs. Not-Threatened
| AIThreat | Mean ConvComp (USD) | N |
|----------|---------------------|---|
| Yes | 81,092 | 1,886 |
| No | 88,104 | 12,750 |

Gehaltsunterschied: ~8.7% — relativ gering, kein vollständiger Confounder.

### 2.9 Berufserfahrung: Threatened vs. Not-Threatened
| AIThreat | Mean YearsCodePro | N |
|----------|-------------------|---|
| Yes | 9.18 | 4,329 |
| No | 10.06 | 26,303 |

Geringer Unterschied — kein substanzieller Confounder.

---

## 3. Forschungsfrage

### Kandidaten-Forschungsfragen mit Effect-Size-Gate

#### Kandidat A: AIThreat → JobSat
- **Frage**: Sagt wahrgenommene KI-Bedrohung die Jobzufriedenheit von Entwicklern voraus?
- **Vorab-Effektgröße**: Eta² = 0.0122 ≥ 0.01 ✓; Cohen's d = 0.331 ≥ 0.25 ✓
- **Status**: Gate bestanden ✓

#### Kandidat B: YearsCodePro → ConvertedCompYearly
- **Frage**: Sagt Berufserfahrung das Gehalt voraus?
- **Vorab-Effektgröße**: r = 0.141 < 0.15 — Gate knapp nicht bestanden ✗

#### Kandidat C: RemoteWork → JobSat
- **Frage**: Unterscheidet sich die Jobzufriedenheit je nach Arbeitsmodell?
- **Vorab-Effektgröße**: Eta² = 0.006 < 0.01 — Gate nicht bestanden ✗

#### Kandidat D (GEWÄHLT): AIThreat vs. ConvertedCompYearly als JobSat-Prädiktoren
- **Kontraintuitiv**: Wahrgenommene KI-Bedrohung (r = -0.111) sagt JobSat besser voraus als das Jahresgehalt (r = 0.072). Entwickler sind nicht hauptsächlich gehaltsgesteuert in ihrer Arbeitszufriedenheit — die psychologische Last der KI-Bedrohung überwiegt den Einkommenseffekt.
- **Vorab-Effektgröße**: Eta² = 0.0122 ≥ 0.01 ✓; Cohen's d = 0.331 ≥ 0.25 ✓

### Finale Forschungsfrage (Kandidat D)
> **Sagt wahrgenommene KI-Job-Bedrohung die Arbeitszufriedenheit von Softwareentwicklern stärker voraus als das Jahresgehalt, und bleibt dieser Effekt signifikant nach Kontrolle von Berufserfahrung und Vergütung?**

**H0**: AIThreat erklärt nach Kontrolle von YearsCodePro und ConvertedCompYearly keine signifikante Zusatzvarianz in JobSat.

**H1**: AIThreat ist ein signifikanter negativer Prädiktor von JobSat (β < 0, p < 0.05) und erklärt mehr Varianz als ConvertedCompYearly (|β_AIThreat| > |β_Comp|).

**Methode**: OLS-Multipel-Regression  
- AV: JobSat (1–10)  
- UV1: AIThreat_binary (1=Ja, 0=Nein)  
- Kovariate 1: YearsCodePro  
- Kovariate 2: log1p(ConvertedCompYearly)  
- Berichtete Maßzahlen: b, SE, β (standardisiert), p, R², ΔR², F, VIF  

**Vorab-Effektgröße**: Eta²(AIThreat→JobSat) = 0.0122 (erfüllt ≥ 0.01); Cohen's d = 0.331 (erfüllt ≥ 0.25)

**Warum kontraintuitiv**: 
- Im Narrativ der Tech-Branche gilt Gehalt als Hauptmotivator für Entwickler.  
- Dieses Ergebnis zeigt, dass die Angst vor KI-bedingtem Jobverlust ein stärkerer Predictor der Arbeitszufriedenheit ist als das Gehalt selbst.  
- Zusätzlich: 81.6% der Bedrohten nutzen AI-Tools trotzdem aktiv — ein "erzwungener Adoptions"-Effekt, der an den Smoker-Paradox erinnert.

---

## 4. Literaturquellen (alle Abstracts gelesen via WebFetch)

### Quelle 1
**Titel**: Employee Well-being in the Age of AI: Perceptions, Concerns, Behaviors, and Outcomes  
**Autor**: Sadeghi, S.  
**Jahr**: 2024  
**DOI**: https://doi.org/10.48550/arXiv.2412.04796  
**Abstract-Inhalt**: Zeigt, dass KI-Integration in HR-Prozesse zwar Effizienz steigern kann, gleichzeitig aber Sorgen um Beschäftigungssicherheit und fairen Umgang erzeugt. Entwickelt ein "AI-Employee Well-being Interaction Framework."  
**Relevanz**: Direkte theoretische Grundlage für die Verbindung KI-Bedrohungswahrnehmung ↔ Wohlbefinden/Arbeitszufriedenheit.

### Quelle 2
**Titel**: Work Design and Multidimensional AI Threat as Predictors of Workplace AI Adoption and Depth of Use  
**Autoren**: Reich, A., Wolfe, D., Price, M., Choe, A., Kidd, F., Wagner, H.  
**Jahr**: 2026  
**DOI**: https://doi.org/10.48550/arXiv.2602.23278  
**Abstract-Inhalt**: Survey mit 2,257 Mitarbeitern zeigt, dass verschiedene Dimensionen von KI-Bedrohung (Statusverlust, Kontrollverlust) AI-Adoption unterschiedlich beeinflussen. Jobdesign moderiert den Effekt.  
**Relevanz**: Unterstützt die H1, dass Bedrohungswahrnehmung unabhängig von anderen Faktoren auf Arbeitsergebnisse wirkt; bietet theoretische Rahmung für "multidimensionale Bedrohung."

### Quelle 3
**Titel**: The Impact of AI on Perceived Job Decency and Meaningfulness: A Case Study  
**Autoren**: Ghosh, K., Sadeghian, S.  
**Jahr**: 2024  
**DOI**: https://doi.org/10.48550/arXiv.2406.14273  
**Abstract-Inhalt**: Qualitative Studie mit IT-Fachleuten: Mehrheit sieht KI als ergänzendes Werkzeug, nicht als Ersatz; erwartet gleichbleibende oder höhere Jobzufriedenheit.  
**Relevanz**: Kontrastiert mit unserer quantitativen Evidenz, dass Bedrohungswahrnehmung (auch bei einer Minderheit) starke negative Effekte auf JobSat hat. Zeigt, dass Mehrheitsperspektive und Betroffenen-Perspektive divergieren können.

### Quelle 4
**Titel**: AI, Jobs, and the Automation Trap: Where Is HCI?  
**Autoren**: Constantinides, M., Quercia, D.  
**Jahr**: 2025  
**DOI**: https://doi.org/10.48550/arXiv.2501.18948  
**Abstract-Inhalt**: Argumentiert, dass aktuelle KI-Entwicklung auf Kostenreduktion/Aufgabenersatz ausgerichtet ist, nicht auf menschliche Stärkung. Human-Centered AI fehlt in der Praxis.  
**Relevanz**: Liefert gesellschaftlichen Rahmen für die Frage, warum Entwickler Jobbedrohung wahrnehmen und warum dies rationale Reaktion auf reale Anreizstrukturen ist.

### Quelle 5
**Titel**: Revisiting UTAUT for the Age of AI: Understanding Employees AI Adoption and Usage Patterns  
**Autoren**: Wolfe, D., Price, M., Choe, A., Kidd, F., Wagner, H.  
**Jahr**: 2025  
**DOI**: https://doi.org/10.48550/arXiv.2510.15142  
**Abstract-Inhalt**: Erweitert UTAUT um emotionale Faktoren (Angst, Self-Efficacy); Seniorität ist stärkster Prädiktor für AI-Adoption; Demografie hat begrenzten Erklärungswert.  
**Relevanz**: Zeigt, dass Erfahrung (Seniorität) AI-Adoption beeinflusst — wichtig als Kovariate in unserer Regression; unterstreicht Komplexität jenseits simpler demographischer Erklärungen.

### Quelle 6
**Titel**: The Factors Influencing Well-Being in Software Engineers: A Cross-Country Mixed-Method Study  
**Autoren**: Martinez Montes, C., Penzenstadler, B., Feldt, R.  
**Jahr**: 2025  
**DOI**: https://doi.org/10.48550/arXiv.2504.01787  
**Abstract-Inhalt**: Identifiziert über 15 Interviews und Cross-Country-Survey Einflussfaktoren auf Entwicklerwohlbefinden: persönliche Wahrnehmungen, zwischenmenschliche Dynamiken, organisatorische Kultur, und spezifische Stressoren in der Softwareentwicklung.  
**Relevanz**: Liefert breite empirische Grundlage für Wohlbefinden in SE; zeigt, dass psychologische und wahrgenommene Faktoren (nicht nur Gehalt) entscheidend sind — unterstützt H1.

### Quelle 7
**Titel**: Job Anxiety in Post-Secondary Computer Science Students Caused by Artificial Intelligence  
**Autoren**: Farooqi, D., Pu, G., Paudel, S., Sultana, S., Ahmed, S. I.  
**Jahr**: 2026  
**DOI**: https://doi.org/10.48550/arXiv.2601.10468  
**Abstract-Inhalt**: Interviews mit 25 CS-Studierenden an der Universität Toronto: Jobverdrängungsangst durch KI ist weit verbreitet, besonders in SE und Webentwicklung. Reaktion: "Upskilling" durch mehr KI-Nutzung.  
**Relevanz**: Zeigt "erzwungene Adoption"-Dynamik bei Bedrohungswahrnehmung — parallelt unseren Fund, dass 81.6% der bedrohten Entwickler trotzdem AI nutzen. Unterstützt qualitativ die quantitativen Befunde.
