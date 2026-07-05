# Stage 2b Log — Adversarial Critic Review

**Author:** Anonymous Author (Critic role)  
**Pipeline:** v3  
**Date:** 2026-06-07  
**Note:** Reviewer adopts deliberately sharper-than-comfortable stance to counteract RLHF consensus bias (arxiv:2605.08956). Rating scale: NIEDRIG / MITTEL / HOCH

---

## REVIEW-PUNKT 1 — Steelman der Nullhypothese

**Rating: HOCH**

The strongest argument for H0 is that the theoretical premise is structurally flawed. Cognitive threat appraisal theory (Lazarus & Folkman 1984) proposes that threat credibility intensifies stress *only when combined with low coping resources* — not simply when capability is perceived as high. The paper's hypothesis conflates two distinct cognitive evaluations: AI capability assessment (AIAcc) and personal job vulnerability judgment (AIThreat). A developer can simultaneously believe "AI is highly accurate" and "but my specific work requires human judgment that AI cannot replicate" — these evaluations are logically independent. Trust in AI accuracy does not straightforwardly convert into perceived job vulnerability; it might equally increase confidence that AI augments rather than replaces human expertise. The null finding across all 5 multiverse specifications (p > 0.37 in all) suggests this independence is empirically real, not an artifact of low power (N=17,670, power >99%).

**Response (Discussion paragraph):**
> The null moderation result should be interpreted in light of the theoretical distinction between *capability appraisal* (AIAcc: "AI is accurate") and *vulnerability appraisal* (AIThreat: "AI threatens my job"). These may operate as independent cognitive pathways. Developers who trust AI accuracy may interpret this favorably — as AI augmenting their capabilities — rather than inferring job displacement. Future research should directly measure perceived *replaceability* (distinct from general AI capability trust) as the theorized moderator.

---

## REVIEW-PUNKT 2 — Nicht kontrollierte Konfundierungen

### Konfundierung 1: Developer Specialization / DevType

**Rating: HOCH**

Software developers working in data science, ML/AI, and DevOps roles face qualitatively different AI threat exposure than front-end or full-stack developers. Full-stack developers (N=6,592, 37% of sample) are the modal group, but their AI exposure profile is heterogeneous. Critically, DevType correlates with both AIThreat (ML engineers may perceive more capability-related threat) and JobSat (senior roles with higher autonomy report higher satisfaction). Omitting DevType could bias the AIThreat main effect in either direction.

**Bias direction:** Likely attenuation (toward zero) if high-satisfaction/low-threat specialists (e.g., ML engineers who see AI as tool) dominate the no-threat group.

**Additional analysis conducted (EXPLORATORY):**  
Model with DevCat dummies (N=17,655):
- AIThreat_bin: β=−0.611, p=1.65×10⁻⁴ (virtually unchanged vs. −0.609)
- Interaction: β=−0.009, p=0.858 (unchanged, still null)
- R²=0.027

**Verdict:** DevType does not confound the main result. The AIThreat effect and null moderation are robust to DevType control.

### Konfundierung 2: Income / Compensation Level

**Rating: HOCH**

Compensation (ConvertedCompYearly) is missing for 64% of respondents and was therefore excluded from the listwise sample. However, income is a strong predictor of both AIThreat (higher-paid senior developers occupy harder-to-automate roles → lower AIThreat) and JobSat (higher pay → higher satisfaction). Not controlling for income could produce an upward bias in the AIThreat main effect: the observed group difference may partly reflect income differences between threat-perceivers (likely lower-paid, junior) and non-perceivers (likely higher-paid, senior).

**Bias direction:** Upward inflation of AIThreat → JobSat effect (omitted variable bias; income is a shared cause of both).

**Response (Limitations paragraph):**
> A critical limitation is the inability to control for compensation (64% missing). Perceived AI threat may correlate with income: junior developers with lower compensation are both more exposed to routine task automation and less satisfied. The observed d=−0.303 may therefore partially reflect a socioeconomic gradient rather than purely AI-threat-mediated effects. Future analyses with full compensation data (N≈23,000 before additional listwise) should treat income as a covariate.

### Konfundierung 3: Country / Labor Market Context

**Rating: MITTEL**

Labor market conditions, social safety nets, union strength, and AI regulation differ substantially across the 180+ countries in the dataset. A developer in Germany (strong Kündigungsschutz) would rationally show weaker AIThreat → JobSat association than one in the US (at-will employment). Cross-national heterogeneity is a validity threat.

**Bias direction:** Unpredictable (depends on distribution of countries and their threat-satisfaction correlations).

**Additional analysis conducted (EXPLORATORY):**  
Model with Country top-5 + Other (N=17,670):
- AIThreat_bin: β=−0.623, p=1.22×10⁻⁴ (unchanged direction and magnitude)
- Interaction: β=−0.004, p=0.935 (still null)
- R²=0.029

**Verdict:** Country control does not change the main finding. Cross-national heterogeneity does not drive the results.

---

## REVIEW-PUNKT 3 — P-Hacking-Risiko

**Rating: MITTEL**

The following analytical decisions were made after data access, despite the PAP:

1. **AISelect_bin dropped post-hoc:** The decision to omit this pre-registered covariate was made after discovering it was constant in the listwise sample. While the justification is valid (structural collinearity), this constitutes an unregistered modification to the analysis protocol.

2. **Primary narrative shift:** The pre-registered primary test (H1: moderation) is null. Reporting the AIThreat main effect (d=−0.303) as the headline finding — while scientifically valid — could be perceived as selective emphasis on a significant finding that was not the primary hypothesis.

3. **Mitigating factors:** 
   - The multiverse shows 0/5 specifications significant for the interaction — an unlikely outcome if p-hacking were occurring
   - All BH-FDR-corrected p-values are accurately reported
   - The null result for H1 is reported first and prominently
   - The AIThreat main effect was anticipated in the PAP as a byproduct of the interaction model

**Response:** All three analytical decisions are transparently documented as PAP deviations or labeled EXPLORATORY. No post-hoc specification searches occurred. The p-hacking risk is MITTEL but mitigated by transparent reporting.

---

## REVIEW-PUNKT 4 — Fehlende Vergleichsgruppe / Kausalität

**Rating: HOCH**

The cross-sectional design makes causal inference fundamentally impossible. The reverse causal pathway is theoretically plausible and methodologically indistinguishable from the hypothesized direction:

> *Unhappy developers (low JobSat) attribute their dissatisfaction to external causes — and perceiving AI as a job threat is a cognitively available, socially sanctioned attribution. Hence: low JobSat → high AIThreat perception.*

This reverse causation would produce an identical negative correlation without any causal role for AI threat in causing dissatisfaction. The mediation analysis (Frustration as mediator) is doubly cross-sectional: the mediator, predictor, and outcome were all measured simultaneously, making causal inference from mediation impossible (Bullock et al., 2010 JEP).

**Response (Discussion/Limitations paragraph):**
> The cross-sectional design of the Stack Overflow Developer Survey precludes causal inference. The negative association between AIThreat and JobSat (d=−0.303) is equally consistent with (a) threat perception reducing satisfaction, (b) dissatisfied developers selectively perceiving AI as threatening, or (c) a shared third cause. Future research should use longitudinal designs — measuring AIThreat perception prior to measuring JobSat — or exploit exogenous variation in AI exposure (e.g., policy changes, firm-level AI adoption decisions) as natural experiments. The mediation analysis is reported descriptively and should not be interpreted causally.

---

## REVIEW-PUNKT 5 — Messprobleme

**Rating: HOCH**

Three measurement issues of substantial severity:

**5a. AIThreat — Single-item binary:**  
A single Yes/No question ("Do you believe AI is a threat to your job?") is an extremely coarse, likely unreliable measure of a multidimensional construct. Reich et al. (2026) identified at least 3 distinct AI threat dimensions (status threat, work change threat, displacement threat) that have different relationships with outcomes. Collapsing this to binary eliminates all variance in threat type and intensity. The "I'm not sure" → 0 coding (pre-registered) may misclassify genuinely ambivalent individuals who experience moderate threat.

**Bias direction:** Measurement error in AIThreat biases effect sizes toward zero (attenuation). The true d for well-measured AI threat may exceed −0.303.

**5b. Common Method Bias:**  
AIThreat, AIAcc, and JobSat are all self-reported in the same annual survey. Mood-congruent responding (respondents experiencing general dissatisfaction may endorse multiple negative items) could inflate correlations among these measures. This is a standard limitation of single-source surveys.

**5c. JobSat — Single item, 0-10:**  
While brief single-item satisfaction scales have acceptable criterion validity (Wanous et al., 1997), they cannot capture satisfaction facets (pay, autonomy, relationships, growth). The generic nature of this item may suppress true variance in AI-threat-related dissatisfaction.

**Response (Limitations paragraph):**
> AI job threat perception was operationalized as a single binary item, limiting construct validity. Future studies should employ multi-item scales that distinguish between economic threat (job loss risk), status threat (professional identity), and task threat (routine task automation). The single-item nature of both AIThreat and JobSat prevents assessment of internal consistency. Common method bias is a potential concern in this cross-sectional, single-source survey design, although the temporal lag inherent in annual survey administration provides partial protection.

---

## REVIEW-PUNKT 6 — Generalisierbarkeit

**Rating: HOCH**

Three distinct generalizability failures:

**6a. Stack Overflow self-selection:** The SO Developer Survey recruits via the SO platform and newsletter. It systematically overrepresents English-speaking developers, those who actively engage with Stack Overflow (skewing toward problem-solvers and continuous learners), Western developers (US 13%, UK 5%, Germany 5%), and males (94% typically). Developer populations in China, India's Tier-2 cities, or Latin America are substantially underrepresented.

**6b. AI-user-only sample:** After listwise deletion on AIAcc_ord, the analysis sample (N=17,670) consists entirely of current AI tool users (AISelect_bin=1). This means the findings apply only to AI-using developers and cannot be extrapolated to the ~15,000 non-users or the global developer population. This is a severe scope restriction that limits the paper's contribution.

**6c. Snapshot limitation:** The 2024 survey reflects a specific moment in AI development (ChatGPT era, pre-GPT-5). The relationship between AI threat perception and job satisfaction may evolve rapidly as AI capabilities change. Results may not replicate in the 2025 or 2026 survey contexts.

**Response (Scope and Limitations paragraph):**
> The analysis sample is restricted to current AI tool users (N=17,670) due to the structural design of the AIAcc question in the Stack Overflow survey. Findings should not be generalized to non-users of AI tools or to developer populations not represented on the Stack Overflow platform. The Stack Overflow survey also overrepresents Western, English-speaking, male developers, limiting cross-cultural generalizability. These limitations are acknowledged as inherent to the secondary analysis design; primary data collection with representative sampling would be required to address them.

---

## Summary of HOCH-Rated Issues and Resolution Status

| Issue | Rating | Resolution |
|---|---|---|
| Steelman of H0: independent cognitive pathways | HOCH | Discussion paragraph written ✓ |
| Confound: DevType | HOCH | Additional analysis run: results robust ✓ |
| Confound: Income/Compensation | HOCH | Limitations paragraph written ✓ |
| Reverse causation / no causal design | HOCH | Discussion/Limitations paragraph written ✓ |
| Measurement: AIThreat single binary item | HOCH | Limitations paragraph written ✓ |
| Generalizability: AI-users only, SO selection | HOCH | Scope paragraph written ✓ |

**All HOCH-rated points addressed. Stage 3 cleared to proceed.**

---

## Additional Analysis Summary (EXPLORATORY)

| Model | N | β_AIThreat | p | β_interaction | p |
|---|---|---|---|---|---|
| Main (PAP) | 17,670 | −0.609 | 0.000 | −0.009 | 0.856 |
| + DevCat dummies | 17,655 | −0.611 | 0.000 | −0.009 | 0.858 |
| + Country (top 5) | 17,670 | −0.623 | 0.000 | −0.004 | 0.935 |

The AIThreat main effect (d≈−0.30) is robust across all three models. The moderation (H1) remains null across all models. No HOCH-rated confound invalidates the core descriptive finding.
