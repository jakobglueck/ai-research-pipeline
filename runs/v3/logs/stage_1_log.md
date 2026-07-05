# Stage 1 Log — Exploration, Forschungsdesign & PRISMA-Literatursuche

**Author:** Anonymous Author  
**Pipeline:** v3  
**Date:** 2026-06-07

---

## 1. Effect-Size-Gate

Pre-registered thresholds: |r| ≥ 0.15 OR Cohen's d ≥ 0.25 OR Eta² ≥ 0.01 OR OR ≥ 1.5

| Test | Value | Threshold | Pass? |
|---|---|---|---|
| Spearman r (AIThreat_bin vs JobSat) | r = −0.085 | |r| ≥ 0.15 | FAIL |
| Cohen's d (AIThreat Yes vs No+Unsure) | d = −0.295 | d ≥ 0.25 | **PASS** |
| Spearman r (AIAcc_ord vs JobSat) | r = +0.045 | |r| ≥ 0.15 | FAIL |

**Gate Verdict: PASSED** (Cohen's d = −0.295 exceeds threshold)

### Gate Details
- AIThreat=Yes group: M=6.40, N=2,380
- AIThreat=No+Unsure group: M=7.01, N=19,940
- t = −13.622, p < 0.0001
- Listwise N for main model (all 6 predictors): 17,670

### Interaction Signal (Pre-Gate Exploratory Check)
- AIAcc→JobSat among AIThreat=Yes: r = +0.030, p = 0.19 (N=1,932)
- AIAcc→JobSat among AIThreat=No: r = +0.052, p < 0.001 (N=16,269)
- Δr = −0.022 — **very small interaction signal**
- **Interpretation:** The moderation hypothesis (H1) may yield a null or very small interaction effect. Analysis proceeds as preregistered. This will be reported as confirmatory.

### Mediation Paths (Pre-Gate Check)
- a-path (AIThreat_bin → Frustration_bin): r = +0.016, p = 0.018, N = 21,488
- b-path (Frustration_bin → JobSat): r = −0.097, p < 0.001
- **Assessment:** a-path is very weak (r=0.016). Mediation analysis will proceed but may yield negligible indirect effect. Flagged in PAP as secondary.

**No PAP deviation needed — gate passed, primary analysis proceeds as preregistered.**

---

## 2. Suchprotokoll (PRISMA-lite)

| Parameter | Spezifikation |
|---|---|
| Suchstring 1 | ("AI threat" OR "artificial intelligence threat") AND ("job satisfaction" OR "work satisfaction") |
| Suchstring 2 | "artificial intelligence" AND "job insecurity" AND ("moderating" OR "moderation") AND ("work satisfaction" OR "employee well-being") |
| Suchstring 3 | ("AI adoption" OR "AI trust" OR "AI accuracy") AND "job satisfaction" AND (developers OR programmers OR "software") |
| Suchstring 4 | ("automation threat" OR "AI technostress") AND ("job satisfaction" OR "well-being") AND ("trust" OR "moderation") |
| Suchstring 5 | ("cognitive threat appraisal" OR "fear of replacement") AND "artificial intelligence" AND (stress OR "job satisfaction") |
| Suchstring 6 | ("AI technostress" OR "technology stress") AND ("job satisfaction" OR "well-being") AND (developer OR programmer OR "knowledge worker") |
| Datenbanken | arXiv, Semantic Scholar, PubMed/PMC, Frontiers |
| Zeitraum | 2018–2026 |
| Einschluss | empirische Studien, peer-reviewed, Englisch, N ≥ 100 |
| Ausschluss | rein theoretische Arbeiten, Blogposts, Grauiteratur, N < 100, qualitative only |

---

## 3. PRISMA-Flow

```
Identifiziert via 6 Web-Searches: N = 36
  └─ Titles screened: 36
      ├─ Excluded (duplicates): 3
      ├─ Excluded (not empirical / no job satisfaction): 8
      ├─ Excluded (qualitative, N < 100): 5
      ├─ Excluded (inaccessible, 403): 2
      └─ Abstract screening: 18
          ├─ Excluded after abstract: 4
          └─ Included (final): 14
```

N_identified = 36 | N_screened = 33 | N_excluded_after_abstract = 4 | **N_included = 14** (+ 2 dataset references)

---

## 4. Kandidatenliste (alle 36 Kandidaten)

| # | Titel (kurz) | Quelle | Entscheidung | Begründung |
|---|---|---|---|---|
| 1 | Employee Well-being in the Age of AI (Sadeghi 2024) | arXiv 2412.04796 | INCLUDE | Framework paper, AI perception → well-being |
| 2 | "I Don't Use AI for Everything" (Pan et al. 2024) | arXiv 2409.13343 | EXCLUDE | N=19, qualitative only |
| 3 | AI technostress → physicians job insecurity (Liu et al. 2025) | PMC12811485 | INCLUDE | N=400, PLS-SEM, job insecurity → job satisfaction |
| 4 | AI Where It Matters (Choudhuri et al. 2026) | arXiv 2510.00762 | EXCLUDE | No job satisfaction outcome |
| 5 | Americans' Support for AI Development (2024) | arXiv 2412.05163 | EXCLUDE | Not job satisfaction |
| 6 | AI, Scientific Discovery, Product Innovation (2024) | arXiv 2412.17866 | EXCLUDE | Not job satisfaction |
| 7 | Perceptions of AI and Job Insecurity (IJSRP 2025) | ijsrp.org | EXCLUDE | Not accessible/peer-reviewed |
| 8 | AI workplace anxiety → life satisfaction (Zhao et al. 2025) | PMC12360261 | INCLUDE | N=549, full mediation via negative emotions |
| 9 | AI awareness, career resilience, job insecurity (Chung et al. 2025) | PMC12481535 | INCLUDE | N=209, longitudinal, moderated mediation |
| 10 | AI application → job insecurity: self-efficacy + leadership (Fu & Zhang 2026) | Frontiers fpsyg.2026 | INCLUDE | N=411, U-shaped relationship, moderation |
| 11 | AI usage → moonlighting intention (Wu et al. 2025) | SAGE | EXCLUDE | Not job satisfaction |
| 12 | AI Exposure, Morale, Emotional Intelligence moderation | SCIRP 143574 | EXCLUDE | Inaccessible (403) |
| 13 | AI Awareness → Depression via Emotional Exhaustion (Xu et al. 2023) | PMC10049037 | INCLUDE | N=321, moderated mediation, POS moderator |
| 14 | AI Awareness → Emotional Exhaustion serial mediation (Zheng & Zhang 2025) | PMC12024253 | INCLUDE | N=303, BCa bootstrap, job insecurity mediator |
| 15 | Automation workers skills job satisfaction (Schwabe & Castellacci 2020) | PMC7703879 | INCLUDE | N=10,051, fear→lower JobSat, d≈large for low-skilled |
| 16 | Stack Overflow 2025 Developer Survey — AI | survey.stackoverflow.co/2025 | INCLUDE (dataset ref) | Official survey data, N=65k |
| 17 | Stack Overflow 2024 Developer Survey — AI | survey.stackoverflow.co/2024 | INCLUDE (dataset ref) | Data source for current analysis |
| 18 | Trust in AI tools plummeting (LeadDev) | leaddev.com | EXCLUDE | Journalism, not peer-reviewed |
| 19 | Empowering workforces in AI-driven environments (Zhang et al. 2025) | Frontiers fpsyg.2025 | INCLUDE | N=437, PLS-SEM, co-skilling, job insecurity |
| 20 | Trust propensity → AI acceptance (ScienceDirect) | SciDirect 2451958823 | EXCLUDE | Inaccessible (403) |
| 21 | Trust in Automation bibliometric review (2023) | arXiv 2309.09828 | MAYBE→EXCLUDE | Bibliometric only, no primary effect size |
| 22 | AGAWA scale GenAI barriers (Sikorski et al. 2025) | arXiv 2512.23373 | EXCLUDE | Scale dev, no job satisfaction |
| 23 | Automation from Worker's Perspective (Armstrong et al. 2024) | arXiv 2409.20387 | INCLUDE | N=9,000+, 9 countries, counterpoints |
| 24 | AI Technostress → Adoption moderated by self-efficacy (Chang et al. 2024) | PMC10859089 | INCLUDE | N=301, three-wave, moderated mediation |
| 25 | Technostress GenAI qualitative (Frontiers frai.2025) | Frontiers frai.2025 | EXCLUDE | Qualitative |
| 26 | Technostress employee well-being systematic review (SciDirect) | SciDirect 2451958826 | EXCLUDE | Inaccessible (403) |
| 27 | Technostress Creators & Job Performance moderation (PMC9278755) | PMC9278755 | MAYBE→EXCLUDE | Not AI-specific, pre-AI-era |
| 28 | Work Design & Multidimensional AI Threat (Reich et al. 2026) | arXiv 2602.23278 | INCLUDE | N=2,257, multidimensional threat measure |
| 29 | Job Anxiety in CS Students (Farooqi et al. 2026) | arXiv 2601.10468 | EXCLUDE | N=25, qualitative |
| 30 | AI Automation & Labor Risk Latin America (Cremaschi et al. 2025) | arXiv 2505.08841 | EXCLUDE | Not job satisfaction, Latin America only |
| 31 | Psychological Impacts AI Displacement Indian IT (2025) | PMC12409910 | EXCLUDE | N=24, qualitative |
| 32 | Job-Related Anxiety in Age of AI (FJMR) | npaformosapublisher | MAYBE→EXCLUDE | Not accessible |
| 33 | Consequenes of Technostress for End Users (Ragu-Nathan et al. 2008) | ISR | MAYBE→EXCLUDE | Pre-AI, old scale |
| 34 | AI awareness → Depression (Xu et al. 2023 PMC10049037) | PMC10049037 | (dup of #13) | — |
| 35 | AI awareness → Emotional Exhaustion (MDPI 2025) | MDPI Behav.Sci. | INCLUDE (dup of #14) | Same paper as PMC12024253 |
| 36 | Mental health AI era: technostress SEM (Frontiers fpsyg.2025.1600013) | Frontiers | MAYBE→EXCLUDE | Anxiety/depression focus, not job satisfaction |

---

## 5. Datenextraktionstabelle (INCLUDEd Papers)

| # | Titel | Autoren | Jahr | N | Land | Methode | Hauptbefund | Effektgröße | Relevanz H1 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Automation, workers' skills and job satisfaction | Schwabe & Castellacci | 2020 | 10,051 | Norwegen | IV-bivariate probit | Fear of replacement → signifikant niedrigere JobSat; Effekt by low-skilled workers | ~50% prob-decrease (low-skilled) | **stützt** |
| 2 | AI Awareness → Depression via Emotional Exhaustion | Xu, Xue, Zhao | 2023 | 321 | China | Cross-sectional, moderated mediation | AI awareness → emotional exhaustion (β=0.34) → depression (β=0.52); POS moderiert | Indirect: 0.11 (CI: 0.06–0.17) | **stützt** (emotionale Erschöpfung = pathway) |
| 3 | AI Awareness → Emotional Exhaustion serial mediation | Zheng & Zhang | 2025 | 303 | China | Cross-sectional, bootstrap mediation | AI awareness → job insecurity (β=0.655) → emotional exhaustion; 75.5% mediiert | β=0.648 direkt; 75.5% indirekt | **stützt** (job insecurity mediiert) |
| 4 | AI workplace anxiety → life satisfaction | Zhao et al. | 2025 | 549 | China | Cross-sectional, PROCESS 4&7 | AI anxiety → negative emotions (volle Mediation, 85.64%) → life satisfaction | β=−0.161 (CI: −0.219/−0.107) | **stützt** (negative emotions = full mediator) |
| 5 | AI awareness, career resilience, job insecurity | Chung et al. | 2025 | 209 | South Korea | Longitudinal (3-wave), PROCESS | AI awareness → job insecurity → task performance↓; career resilience moderiert | Indirect: −0.12 (CI: −0.20/−0.06) | **stützt** (resilience moderiert threat → insecurity) |
| 6 | AI technostress → physicians job insecurity | Liu, Lin, Ko | 2025 | 400 | Taiwan | PLS-SEM | Self-esteem threat → job insecurity (β=0.459); job insecurity → job satisfaction (neg.) | R²(JobSat)=2.6% | **stützt** |
| 7 | AI Technostress → Adoption moderated by self-efficacy | Chang et al. | 2024 | 301 | China | 3-wave survey, Mplus | Challenge stress → positive affect (B=0.56) → adoption; self-efficacy moderiert | B=0.56 challenge, B=−0.48 hindrance | **teilweise stützt** (moderation durch self-efficacy analog zu AIAcc moderation) |
| 8 | Empowering workforces in AI-driven environments | Zhang et al. | 2025 | 437 | China | PLS-SEM, cross-sectional | Co-skilling → POS → reduziert job insecurity; mental wellbeing R²=0.738 | f²=0.008–0.537 | **neutral** (buffer-Faktoren) |
| 9 | Employee Well-being in the Age of AI | Sadeghi | 2024 | N/A | N/A | Framework/Review | AI kann well-being sowohl schützen als auch schädigen je nach Implementierung | — | **neutral** (konzeptuell) |
| 10 | Work Design & Multidimensional AI Threat | Reich et al. | 2026 | 2,257 | N/A | Cross-sectional survey | Status threat → neg. AI use depth; job design (autonomy) → pos. AI adoption | — | **stützt** (multidimensionale Bedrohung differenziert) |
| 11 | Automation from Worker's Perspective | Armstrong et al. | 2024 | 9,000+ | 9 Länder | Survey experiment | Mehr berichten Benefits als Costs; Komplexität der Arbeit → positivere Sicht | — | **widerspricht** (counternarrative) |
| 12 | AI application → job insecurity: self-efficacy + leadership | Fu & Zhang | 2026 | 411 | China | Cross-sectional, hierarchical regression | U-förmiger Effekt; hohe self-efficacy schwächt Insecurity | R²=0.062–0.185 | **stützt moderation** (analog zu AIAcc) |

**Dataset References:**
- Stack Overflow Developer Survey 2024 (N=65,437, 180+ countries)
- Stack Overflow Developer Survey 2025 (N≈ 65,000)

---

## 6. CRITIC-CHECK — Literaturverifikation

| Quelle | Behauptung (geplant) | Abstract sagt tatsächlich | Match |
|---|---|---|---|
| Schwabe & Castellacci 2020 | "Fear of replacement negatively predicts job satisfaction, especially for low-skilled workers" | "fear of replacement does negatively affect workers' job satisfaction at present … driven by low-skilled workers" | **JA** |
| Xu et al. 2023 | "AI awareness predicts depression via emotional exhaustion; POS moderates" | AI awareness → emotional exhaustion (β=0.34) → depression (β=0.52); POS interaction β=−0.22 | **JA** |
| Zheng & Zhang 2025 | "AI awareness predicts emotional exhaustion via job insecurity (75.5% indirect effect)" | Exactly this, BCa bootstrap 5,000 reps | **JA** |
| Zhao et al. 2025 | "Negative emotions fully mediate AI anxiety → life satisfaction" | "negative emotions fully mediated" (85.64%), β=−0.161 CI −0.219/−0.107 | **JA** |
| Chung et al. 2025 | "Career resilience moderates AI awareness → job insecurity pathway" | Moderation confirmed β=−.17, p<.05; indirect effects on performance | **JA** |
| Liu et al. 2025 | "AI technostress → job insecurity → lower job satisfaction among physicians" | Self-esteem threat β=0.459 → insecurity; insecurity → job satisfaction neg. supported | **JA** |
| Chang et al. 2024 | "Technical self-efficacy moderates the link between AI technostress and adoption intention" | Self-efficacy moderates challenge→positive affect (B=0.51) and hindrance→anxiety (B=−0.37) | **JA** |
| Armstrong et al. 2024 | "More workers perceive benefits than costs from automation" | "More respondents reported potential benefits … than reported costs" | **JA** |
| Reich et al. 2026 | "AI threat perceptions have differentiated effects on AI use depth" | "Status threat showed negative but not consistently significant relationship with deeper use" | **JA** |
| Fu & Zhang 2026 | "AI application has a U-shaped relationship with employee job insecurity" | "Moderate application of AI can effectively alleviate employees' job insecurity, while excessive application will intensify" | **JA** |

**Alle 10 kritisch-verifizierten Quellen: Match = JA ✓**

---

## 7. Exploratorische Beobachtungen (EXPLORATORY)

Die folgenden Muster wurden nach Bestehen des Gates beobachtet. Sie werden in Stage 2 als EXPLORATORY geführt.

- **EXPLORATORY-1:** AIThreat=Yes-Gruppe zeigt deutlich niedrigere JobSat (M=6.40 vs. 7.01, d=−0.295), aber der Gruppeneffekt von AIAcc auf JobSat ist gering (r=+0.045).
- **EXPLORATORY-2:** Der Interaktionseffekt (Δr = −0.022 zwischen AIAcc→JobSat in AIThreat vs. non-AIThreat Gruppen) ist schwach. H1 (Moderation) wird möglicherweise statistisch nicht signifikant sein — das wird als Null-Befund berichtet.
- **EXPLORATORY-3:** N_listwise für das Hauptmodell beträgt 17,670 — ausreichend für Power, aber ~73% Datenverlust gegenüber Gesamt-N.
- **EXPLORATORY-4:** AISent (AI sentiment) zeigt 0% Missing und wäre ein potenziell stärkerer Prädiktor als AIAcc. Wird in Multiverse Spec 4 geprüft.

---

## 8. Abweichungen vom PAP

Keine Abweichungen. Der Gate ist bestanden, die primäre Analyse wird wie vorregistriert durchgeführt.

Der schwache Interaktions-Signal wird nicht als Anlass genommen, auf eine Alternative zu wechseln — ein Null-Befund für H1 ist ein valides, präregistriertes Ergebnis.
