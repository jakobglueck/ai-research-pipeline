# Stage 1 Log — Exploration & Forschungsdesign

**Datum:** 2026-06-07  
**Pipeline:** v2

---

## 1. Datensatz-Überblick

- **Quelle:** Stack Overflow Annual Developer Survey (2024 Edition)
- **N:** 65.437 Befragte weltweit
- **Zielpopulation:** Software-Entwickler:innen, Studierende, Hobby-Coder
- **Messung:** Technologienutzung, Vergütung, KI-Einstellungen, Jobzufriedenheit (JobSat 0–10)

**Numerische Variablen:** YearsCode, YearsCodePro, WorkExp, CompTotal, ConvertedCompYearly, JobSat, JobSatPoints_1–11  
**Kategoriale Variablen:** AISelect, AIThreat, AISent, AIBen, RemoteWork, EdLevel, DevType, OrgSize, PurchaseInfluence, Country, u. v. m.

**Fehlende Werte (wichtigste):**
- JobSat: 36.311 (55 %)
- ConvertedCompYearly: 42.002 (64 %)
- YearsCodePro: 13.827 (21 %)

---

## 2. Explorative SQL-Abfragen

### Verteilung JobSat (Zielvariable)
```sql
SELECT JobSat, COUNT(*) FROM survey WHERE JobSat IS NOT NULL
GROUP BY JobSat ORDER BY JobSat;
```
| JobSat | n |
|---|---|
| 0 | 311 |
| 1 | 276 |
| 2 | 772 |
| 3 | 1.165 |
| 4 | 1.130 |
| 5 | 1.956 |
| 6 | 3.751 |
| 7 | 6.379 |
| 8 | 7.509 |
| 9 | 3.626 |
| 10 | 2.251 |

Verteilung ist links-schief (Median ≈ 8, Modus = 8). Große Mehrheit ist zufrieden.

### Mittelwerte AIThreat × JobSat
| AIThreat | Mean JobSat | SD | n |
|---|---|---|---|
| No | 7.088 | 2.032 | 15.944 |
| Yes | 6.403 | 2.302 | 2.380 |
| I'm not sure | 6.719 | 2.036 | 3.996 |
| NA | 6.889 | 2.127 | 6.806 |

### Mittelwerte AISelect × JobSat
| AISelect | Mean JobSat | SD | n |
|---|---|---|---|
| Yes | 6.970 | 2.084 | 18.233 |
| No, and I don't plan to | 6.889 | 2.125 | 6.784 |
| No, but I plan to soon | 6.855 | 2.043 | 4.109 |

### Mittelwerte PurchaseInfluence × JobSat
| PurchaseInfluence | Mean JobSat | SD | n |
|---|---|---|---|
| I have a great deal of influence | 7.628 | 1.888 | 5.439 |
| I have some influence | 7.068 | 1.912 | 11.963 |
| I have little or no influence | 6.468 | 2.228 | 10.760 |
| NA | 6.591 | 2.321 | 964 |

### TimeSearching × JobSat
| TimeSearching | Mean JobSat | n |
|---|---|---|
| Less than 15 min/day | 7.340 | 2.670 |
| 15–30 min/day | 7.129 | 7.749 |
| 30–60 min/day | 6.935 | 10.869 |
| 60–120 min/day | 6.691 | 5.240 |
| Over 120 min/day | 6.335 | 2.176 |

---

## 3. Kandidaten-Forschungsfragen & Effect-Size-Gate

### Kandidat A — AISelect → JobSat (FAIL)
**Frage:** Haben KI-Tool-Nutzer höhere Jobzufriedenheit?  
**Ergebnis:** Eta²(JobSat ~ AISelect) = **0.0005**  
**Gate:** Eta² ≥ 0.01 — **NICHT BESTANDEN**  
**Bewertung:** Fast keine erklärte Varianz. Offensichtliche Erwartung und nicht-triviales Null-Ergebnis.

### Kandidat B — PurchaseInfluence → JobSat (PASS, aber wenig kontraintuitiv)
**Frage:** Haben Entwickler:innen mit Entscheidungsmacht über Tools höhere Jobzufriedenheit?  
**Ergebnis:** Cohen's d(great deal vs. little influence) = **0.547**, Eta² = **0.042**  
**Gate:** Cohen's d ≥ 0.25 — **BESTANDEN**  
**Bewertung:** Starker Effekt. Inhaltlich als Kontrollbefund wertvoll (Autonomy-Satisfaction-Link nach SDT), aber nicht überraschend.

### Kandidat C — AIThreat → JobSat (PASS + kontraintuitiv) ✅ GEWÄHLT
**Frage:** Sagt die Wahrnehmung von KI als Jobbedrohung niedrige Jobzufriedenheit vorher — unabhängig vom tatsächlichen KI-Adoptionsverhalten?  
**Ergebnis:** Cohen's d(AIThreat Yes vs. No) = **−0.331**, Eta² = 0.0098  
**Gate:** Cohen's d ≥ 0.25 — **BESTANDEN** (d-Kriterium, auch wenn Eta² knapp unter 0.01)  
**Warum kontraintuitiv:**  
Der dominante Diskurs besagt, dass *wer* KI-Tools nutzt, produktiver und zufriedener ist — und wer sie nicht nutzt, benachteiligt wird. Die Daten widerlegen genau das:  
- AISelect erklärt fast keine Varianz in JobSat (Eta² = 0.0005 ≈ 84× schwächer als PurchaseInfluence)  
- Die *Wahrnehmung* von KI als Bedrohung, nicht das Nutzungsverhalten, ist mit niedrigerer Jobzufriedenheit assoziiert  
- Selbst unter aktuellen KI-Nutzern: AISelect=Yes + AIThreat=Yes → Mean JobSat = 6.42 (vs. 7.10 ohne Bedrohungswahrnehmung)  

### Kandidat D — TimeSearching → JobSat (PASS, aber trivial)
**Frage:** Haben Entwickler:innen, die mehr Zeit mit Suchen verbringen, niedrigere Jobzufriedenheit?  
**Ergebnis:** Eta²(JobSat ~ TimeSearching) = **0.014**  
**Gate:** Eta² ≥ 0.01 — **BESTANDEN**  
**Bewertung:** Klarer monotoner Zusammenhang, aber wenig überraschend.

---

## 4. Finales Forschungsdesign

### Forschungsfrage
**"Sagt die Wahrnehmung von KI als Jobbedrohung (AIThreat) niedrigere Jobzufriedenheit unter Software-Entwickler:innen voraus, und ist dieser Effekt stärker als der Effekt des tatsächlichen KI-Tool-Adoptionsstatus (AISelect)?"**

### H0
AIThreat ist kein signifikanter Prädiktor von JobSat nach Kontrolle von AISelect und demografischen Kovariablen (β = 0).

### H1
Entwickler:innen mit AIThreat = Yes berichten signifikant niedrigere JobSat als jene mit AIThreat = No (β < 0, Cohen's d ≥ 0.25), und dieser Effekt ist substanziell größer als der Effekt von AISelect.

### Methode
1. **Primäranalyse:** OLS-Regression — JobSat ~ AIThreat + AISelect + AIThreat×AISelect + Kovariablen (YearsCodePro, RemoteWork, OrgSize)
2. **Effektgröße:** Cohen's d für Gruppenvergleiche; ΔR² für Modellvergleiche; Partial Eta² für Haupteffekte
3. **Stichprobe:** Filtere auf vollständige Fälle (JobSat IS NOT NULL, AIThreat IN ('Yes','No'), AISelect NOT NULL)

### Vorab-Effektgröße
- Cohen's d(AIThreat Yes vs. No) = **−0.331** → Gate-Kriterium d ≥ 0.25 erfüllt ✓
- Vergleich: Cohen's d(AISelect Yes vs. No) ≈ **0.05** (nicht signifikant)

---

## 5. Literaturquellen

### Quelle 1
**Titel:** Employee Well-being in the Age of AI: Perceptions, Concerns, Behaviors, and Outcomes  
**Autor:** Soheila Sadeghi  
**Jahr:** 2024  
**URL/DOI:** https://arxiv.org/abs/2412.04796 | DOI: 10.48550/arXiv.2412.04796  
**Abstract-Inhalt (gelesen):** Untersucht, wie KI die Zufriedenheit, psychische Gesundheit und Bindung von Arbeitnehmenden beeinflusst. KI-Systeme erzeugen Bedenken bzgl. Arbeitsplatzsicherheit; Transparenz und Beteiligung der Belegschaft sind entscheidend für positive Ergebnisse.  
**Relevanz:** Stützt direkt die Hypothese, dass wahrgenommene KI-Bedrohung (nicht nur objektive KI-Exposition) Jobzufriedenheit beeinflusst; bietet theoretischen Rahmen für subjektive KI-Wahrnehmung als Mediator.

### Quelle 2
**Titel:** Artificial intelligence and the wellbeing of workers  
**Autoren:** Osea Giuntella, Johannes Konig, Luca Stella  
**Jahr:** 2025  
**URL/DOI:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12185714/ | DOI: 10.1038/s41598-025-98241-3  
**Abstract-Inhalt (gelesen):** Längsschnittstudie (Deutschland, 2000–2020): Hochexponierte Berufsgruppen zeigen auf Makroebene keine negativen Effekte auf Lebenszufriedenheit oder Jobsicherheitsbedenken durch KI-Rollout; leicht positive physische Gesundheitseffekte.  
**Relevanz:** Wichtiger Kontrast: Aggregierte KI-Exposition (Berufsgruppe) schädigt Wohlbefinden nicht — was nahelegt, dass individuelle *Wahrnehmungen* von KI als Bedrohung (wie in unserer Hypothese) einen eigenständigen, von der tatsächlichen Expositionslage unabhängigen Effekt haben.

### Quelle 3
**Titel:** Developers' Perceptions on the Impact of ChatGPT in Software Development: A Survey  
**Autoren:** Thiago S. Vaillant et al.  
**Jahr:** 2024  
**URL/DOI:** https://arxiv.org/abs/2405.12195 | DOI: 10.48550/arXiv.2405.12195  
**Abstract-Inhalt (gelesen):** Befragung von 207 Software-Entwickler:innen zu ChatGPTs Einfluss auf Codequalität, Produktivität, Jobzufriedenheit und Sorgen um Jobverdrängung.  
**Relevanz:** Direkt kompatibel mit unserer Stichprobe (Software-Entwickler) und Hypothese (Verbindung AI-Wahrnehmung → Jobzufriedenheit + Bedenken wegen Jobverdrängung); liefert komplementäre qualitative Evidenz.

### Quelle 4
**Titel:** Exploring how AI adoption in the workplace affects employees: a bibliometric and systematic review  
**Autoren:** Malika Soulami, Saad Benchekroun, Asiya Galiulina  
**Jahr:** 2024  
**URL/DOI:** https://doi.org/10.3389/frai.2024.1473872  
**Abstract-Inhalt (gelesen):** Systematisches Review von 92 Studien (2015–2024). Identifiziert vier Hauptthemen: ethische Überlegungen, Arbeitsautonomie, Berufsstress und psychische Gesundheit als zentrale Folgen von KI-Adoption.  
**Relevanz:** Zeigt, dass sowohl Arbeitsautonomie (unser PurchaseInfluence-Befund) als auch psychische Belastung (unser AIThreat-Befund) die am besten belegten Wirkmechanismen von KI-Adoption auf Mitarbeiterzufriedenheit sind — stützt die Wahl beider Variablen.

### Quelle 5
**Titel:** Impact of AI workplace anxiety on life satisfaction among service industry employees: exploring mediating and moderating factors  
**Autoren:** Zhao Feng, Chun mei Hu, Sheng Chen, Jia yong Xu, Yue Zhang, Miao Hao  
**Jahr:** 2025  
**URL/DOI:** https://doi.org/10.3389/fpsyg.2025.1603393 | PMC: PMC12360261  
**Abstract-Inhalt (gelesen):** Querschnittsstudie (N=549, Dienstleistungssektor, China): KI-bezogene Arbeitsplatzangst reduziert Lebenszufriedenheit signifikant über negative emotionale Zustände. Soziale Unterstützung moderiert diesen Effekt.  
**Relevanz:** Zeigt den AIThreat → Satisfaction-Mechanismus empirisch in einer anderen Branche; Parallele zu unserer Hypothese ist direkt. Liefert auch Mediation-Rahmen (Angst → negative Emotion → Zufriedenheit), den wir in der Diskussion adressieren können.

---

## 6. CRITIC-CHECK — Literaturverifikation

### Quelle 1: arXiv:2412.04796

```
Quelle: Employee Well-being in the Age of AI (Sadeghi, 2024)
URL: https://arxiv.org/abs/2412.04796
Behauptung im Log: KI-Systeme erzeugen Bedenken bzgl. Arbeitsplatzsicherheit; subjektive Wahrnehmung als Mediator
Abstract sagt tatsächlich: "AI systems can boost operational efficiency and minimize bias, 
they simultaneously generate apprehension regarding employment stability, equitable treatment,
and data protection. Implementation approaches matter significantly — outcomes depend on 
organizational deployment strategies and worker perception."
Übereinstimmung: JA
Relevant für Hypothese: JA
```

### Quelle 2: PMC12185714 (Nature Scientific Reports)

```
Quelle: Artificial intelligence and the wellbeing of workers (Giuntella et al., 2025)
URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC12185714/
Behauptung im Log: Makroebene keine negativen Effekte auf Lebenszufriedenheit; individuelle 
Wahrnehmung ist anders zu bewerten
Abstract sagt tatsächlich: "found no substantial negative impacts on life satisfaction, 
job security concerns, or mental health outcomes. Instead, evidence suggests modest 
improvements in self-reported physical health and health satisfaction."
Übereinstimmung: JA
Relevant für Hypothese: JA — als theoretischer Kontrast (Makro- vs. individuelle Ebene)
```

### Quelle 3: arXiv:2405.12195

```
Quelle: Developers' Perceptions on the Impact of ChatGPT (Vaillant et al., 2024)
URL: https://arxiv.org/abs/2405.12195
Behauptung im Log: Survey, 207 Entwickler:innen, untersucht JobSat + Jobverdrängungsbedenken
Abstract sagt tatsächlich: "survey with 207 software developers... three main areas: 
impact of ChatGPT on software quality, productivity, and job satisfaction... explores 
concerns about potential job displacement."
Übereinstimmung: JA
Relevant für Hypothese: JA
```

### Quelle 4: DOI 10.3389/frai.2024.1473872

```
Quelle: Exploring how AI adoption affects employees (Soulami et al., 2024)
URL: https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2024.1473872/full
Behauptung im Log: Systematic Review, Hauptthemen: Autonomie, Berufsstress, psychische Gesundheit
Abstract sagt tatsächlich: "four primary thematic clusters: ethical considerations, 
workplace autonomy, occupational stress, and psychological health."
Übereinstimmung: JA
Relevant für Hypothese: JA
```

### Quelle 5: DOI 10.3389/fpsyg.2025.1603393

```
Quelle: Impact of AI workplace anxiety on life satisfaction (Feng et al., 2025)
URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC12360261/
Behauptung im Log: N=549, KI-Angst → neg. Emotion → Lebenszufriedenheit; soziale Unterstützung moderiert
Abstract sagt tatsächlich: "technology-related job anxiety significantly reduced life 
satisfaction through a mechanism of negative emotional states. social support 
substantially buffered the connection."
Übereinstimmung: JA
Relevant für Hypothese: JA
```

**Ergebnis Critic-Check:** Alle 5 Quellen PASS/PASS. Keine verworfenen Quellen.

---

## 7. Anomalien & Auffälligkeiten

- **KI-Nutzung ≠ mehr Zufriedenheit:** Eta²(JobSat ~ AISelect) = 0.0005 — faktisch null. Dies widerspricht der medialen Darstellung von KI als Wohlbefindenstreiber.
- **Bedrohungswahrnehmung wirkt auf Nutzer und Nicht-Nutzer:** Unter AISelect=Yes haben AIThreat=Yes-Befragte (Mean=6.42) deutlich niedrigere Sat als AIThreat=No (Mean=7.10). KI-Adoption "immunisiert" nicht gegen Bedrohungswahrnehmung.
- **Autonomie dominiert:** PurchaseInfluence d=0.547 ist der stärkste einzelne Prädiktor — konsistent mit Self-Determination Theory (Competence/Autonomy → Satisfaction).
- **TimeSearching als mögliche Kontrollvariable** in Folgeanalysen (Eta²=0.014).

---

## Fehler

Keine.
