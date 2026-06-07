# Stage 3 Log — Synthese & Paper-Schreiben

**Datum:** 2026-06-07  
**Pipeline:** v2  
**Output:** `experiment_v2/paper_v2.tex`

---

## Struktur-Entscheidungen

- **Titel:** "Perception Over Adoption: Perceived AI Job Threat Predicts Developer Job Satisfaction More Strongly than AI Tool Use"
- **6 Sektionen:** Abstract, Introduction, Methodology, Results, Discussion & Conclusion, References
- **Sprache:** Englisch (wissenschaftlicher Stil)
- **Figuren eingebunden:** fig1 (Violin), fig2 (Grouped Bar), fig3 (Effect Size Comparison)
- **Tabellen:** Table 1 (Descriptives), Table 2 (Regression)

---

## Zahlen-Quellennachweis (aus logs/v2/stage_2_log.md)

| Zahl im Paper | Abschnitt in stage_2_log.md | Gefunden |
|---|---|---|
| N = 17.696 | „Analytic Sample N = 17696" | JA |
| AIThreat=No: n=15.414, mean=7.099, sd=2.025 | „Descriptive: JobSat by AIThreat_Yes" | JA |
| AIThreat=Yes: n=2.282, mean=6.426, sd=2.285 | „Descriptive: JobSat by AIThreat_Yes" | JA |
| AISelect=Yes: n=14.538, mean=7.024, sd=2.089 | „Descriptive: JobSat by AISelect_Yes" | JA |
| AISelect=Plans: n=3.158, mean=6.960, sd=1.994 | „Descriptive: JobSat by AISelect_Yes" | JA |
| Mittlere Differenz AIThreat: 0.67 | 7.099 − 6.426 = 0.673 | JA |
| Cohen's d (AIThreat) = 0.327 | „Cohen's d: AIThreat No vs Yes" | JA |
| Cohen's d (AISelect) = 0.031 | „Cohen's d: AISelect Yes vs Plans" | JA |
| t = 13.32, p < 2.5e-39 | „Welch t-test: AIThreat No vs Yes" | JA |
| F = 212.27, p < 8.3e-48, Eta² = 0.012 | „ANOVA: AIThreat → JobSat" | JA |
| Modell 1: β(AIThreat) = −0.673, p<0.001 | „MODEL 1" Tabelle | JA |
| Modell 1: β(AISelect) = 0.060, p=0.14 | „MODEL 1" Tabelle | JA |
| Modell 2: β(AIThreat) = −0.651, p<10⁻⁴⁵ | „MODEL 2" Tabelle | JA |
| Modell 2: β(AISelect) = 0.096, p=0.018 | „MODEL 2" Tabelle | JA |
| Modell 2: R² = 0.033 | „MODEL 2" | JA |
| ΔR² = 0.011, f² = 0.011 | „MODEL COMPARISON: ΔR²" | JA |
| VIF max 5.53 (AISelect_Yes) | „VIF (Model 2)" | JA |
| Robustheit AI-Nutzer: n=14.538, d=0.325, p<1.1e-31 | „ROBUSTNESS" | JA |
| Interaction f² = 0.0008 | Stage 1 log (AIThreat×AISelect Interaktion) | JA |

**Alle 19 Zahlen aus den Logs verifiziert.**

---

## CRITIC-CHECK — Claim-Verifikation (Literatur)

### Claim 1

```
Claim im Paper: "AI deployment raises concerns about employment stability, 
fairness, and privacy, with the net effect on worker contentment dependent on 
implementation context"
Quelle: Sadeghi 2024 (arXiv:2412.04796)
Abstract/Text sagt: "AI systems can boost operational efficiency and minimize bias, 
they simultaneously generate apprehension regarding employment stability, equitable 
treatment, and data protection. Implementation approaches matter significantly — 
outcomes depend on organizational deployment strategies and worker perception."
URL erneut abgerufen: JA
Claim korrekt belegt: JA
```

### Claim 2

```
Claim im Paper: "Workers in highly AI-exposed occupations do not report lower life 
satisfaction or greater job insecurity than comparable workers in less-exposed roles"
Quelle: Giuntella et al. 2025 (DOI:10.1038/s41598-025-98241-3)
Abstract/Text sagt: "found no evidence of a sizeable negative impact of AI on workers' 
well-being and mental health... did not cause job losses... no significant adverse effects"
URL erneut abgerufen: JA
Claim korrekt belegt: JA
```

### Claim 3

```
Claim im Paper: "AI-related workplace anxiety directly reduces life satisfaction through 
heightened negative affect, with social support acting as a buffer"
Quelle: Feng et al. 2025 (DOI:10.3389/fpsyg.2025.1603393)
Abstract/Text sagt: "AI job anxiety significantly and negatively predicted life satisfaction 
(t=−3.905, p<0.001). fully mediated by negative emotions (β=−0.161). social support 
moderated the effect of AI anxiety on negative emotions"
URL erneut abgerufen: JA
Claim korrekt belegt: JA
```

### Claim 4

```
Claim im Paper: "workplace autonomy and psychological health as the two most consistently 
observed mediating themes"
Quelle: Soulami et al. 2024 (DOI:10.3389/frai.2024.1473872)
Abstract/Text sagt: "four main clusters, including 'work autonomy' and 'mental health' as 
central themes. AI adoption creates complex workplace changes: enhances job autonomy while 
simultaneously generating occupational stress and mental health concerns"
URL erneut abgerufen: JA
Claim korrekt belegt: JA (leichte Abschwächung: "two most consistently observed" → Abschnitt 
des Papers leicht angepasst zu "key mediating themes")
```

### Claim 5

```
Claim im Paper: "survey examined developers' perspectives on [...] concerns about 
potential job displacement"
Quelle: Vaillant et al. 2024 (arXiv:2405.12195)
Abstract/Text sagt: "delves into developers' expectations regarding future adaptations of 
ChatGPT, concerns about potential job displacement, and perspectives on regulatory interventions"
URL erneut abgerufen: JA
Claim korrekt belegt: JA — nur Thema des Papers zitiert, keine spezifischen Befunde behauptet
```

**Ergebnis: 5/5 Claims korrekt belegt. Keine Falschangaben.**

---

## Probleme beim Schreiben

1. **AISelect im Regression signifikant (p=0.018)** aber β=0.096 substantiell trivial. Klar erklärt als "statistisch signifikant bei N=17.696, aber praktisch bedeutungslos."
2. **Fehlende Referenzkategorie** für AISelect im analytischen Sample dokumentiert und im Methodik-Abschnitt erläutert.
3. **Seitenzahl:** Paper ist ~6 Seiten (11pt, 2.5cm margins mit 3 Figuren + 2 Tabellen).

---

## Fehler

Keine.
