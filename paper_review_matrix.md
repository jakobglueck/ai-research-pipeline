# Paper Review Matrix — Hauptseminar Medieninformatik
## Alle vier Pipeline-Bedingungen bewertet nach der offiziellen Review-Skala

**Bewertungsskala:**
- Excellent: 5 Punkte
- Good: 3–4 Punkte
- Needs Work: 1–2 Punkte

**Kriterien:**
1. Introduction & Literature Review
2. Methods & Results Description
3. Structure & Organization
4. Language & Clarity
5. Citation & Formatting

---

## Bedingung A — Baseline: "Experience Breeds Skepticism"

### 1. Introduction & Literature Review — 3/5 (Good)

Die Einleitung motiviert das Thema klar durch zwei konkurrierende theoretische
Vorhersagen (Competence-Trust vs. Calibration-Hypothese). Die Forschungsfrage
ist präzise formuliert und die Lücke identifiziert (keine Großstudie zur
Calibration-Hypothese). Allerdings stützt sich der gesamte Literature Review
auf nur **5 Quellen**, was für ein empirisches Paper über ein gut beforschtes
Thema (AI trust, developer behavior) deutlich zu dünn ist. Die Quellen sind
zwar relevant (Vaithilingam 2022, Ziegler 2022, Bird 2022, Liao 2023, Cai 2019),
aber alle aus dem engen Bereich Copilot-Usability — eine breitere Einbettung
in die Trust-in-AI Literatur fehlt.

### 2. Methods & Results Description — 3/5 (Good)

Variablenoperationalisierung sorgfältig (exakter Survey-Wortlaut zitiert,
Coding-Entscheidungen erklärt). Kruskal-Wallis + Spearman ist für ordinale
Daten methodisch korrekt. Jedoch: Missing Data wird kaum thematisiert (kein
Bericht wie viele Fälle ausgeschlossen wurden, keine MAR-Prüfung). Keine
Konfidenzintervalle für Effektgrößen. Reproduzierbarkeit nicht adressiert
(kein Hinweis auf Code oder Daten). Der Befund r_s = 0.10 ist praktisch
bedeutungslos — das wird im Paper nicht ausreichend problematisiert.

### 3. Structure & Organization — 4/5 (Good–Excellent)

IMRaD-Struktur konsequent eingehalten, Übergänge zwischen Sektionen fließend,
Subsektionen sinnvoll gewählt. Kleiner Abzug: keine explizite
Conclusions-Sektion, das Paper endet abrupt im Discussion-Teil.

### 4. Language & Clarity — 4/5 (Good–Excellent)

Durchgehend professionelles akademisches Englisch, formeller Ton, keine
grammatikalischen Fehler, Fachbegriffe korrekt verwendet. Kleiner Kritikpunkt:
die E-Mail-Adresse im `\author{}`-Feld (`anonymous@institution.edu`) ist
stilistisch unpassend für ein anonymisiertes Paper.

### 5. Citation & Formatting — 3/5 (Good)

Zitationsstil konsistent. Aber: Mit nur 5 Quellen ist die Bibliographie für
dieses Themengebiet nicht vollständig. Der Stack Overflow Survey selbst fehlt
als eigenständige Zitation im Literaturverzeichnis.

### Gesamtpunktzahl Baseline: **17 / 25**

---

## Bedingung B — Pipeline v1: "Fear Over Pay"

### 1. Introduction & Literature Review — 4/5 (Good)

Kontraintuitiver Ansatz gut motiviert — die Annahme dass Gehalt der zentrale
Treiber von Jobzufriedenheit ist, wird direkt herausgefordert. 7 Quellen,
alle thematisch relevant und gut integriert: Sadeghi, Ghosh, Constantinides,
Farooqi, Wolfe, Reich, Martinez decken KI-Angst, Job Insecurity und
Adoption ab. Forschungsfrage klar und beantwortbar, Lücke identifiziert
(psychologische vs. ökonomische Determinanten). Kleiner Abzug: 7 Quellen
sind für ein Survey-basiertes Paper über ein breit beforschtes Thema noch
dünn; keine systematische Suchstrategie dokumentiert.

### 2. Methods & Results Description — 4/5 (Good)

Operationalisierungen klar mit Survey-Wortlaut, Missing Data thematisiert
(MAR-Annahme begründet, Listwise Deletion erklärt), Ausreißer-Behandlung
dokumentiert. OLS mit standardisierten β-Koeffizienten, VIF, ΔR², Cohen's d —
methodisch solide. Der Ausschluss der "I'm not sure"-Gruppe (45.3% des Samples!)
wird nur mit "to preserve interpretive clarity" begründet — das hätte stärker
problematisiert werden müssen. Keine Bootstrap-CIs.

### 3. Structure & Organization — 4/5 (Good)

Klare IMRaD-Struktur, gute Narrative. Der "coercive adoption"-Befund (81.6%
der Bedrohten nutzen trotzdem KI) ist originell positioniert und gut integriert.
Geringfügiger Abzug: die Discussion vermischt Interpretation und Implikationen
ohne klare Trennung.

### 4. Language & Clarity — 4/5 (Good)

Professionelles akademisches Englisch, präzise Formulierungen. "Coercive or
defensive AI adoption" gut eingeführt und konsequent verwendet. Keine Sprachfehler.

### 5. Citation & Formatting — 4/5 (Good)

natbib konsistent, alle 7 Quellen vollständig und einheitlich formatiert,
Stack Overflow Survey als Datenquelle korrekt zitiert. Kleiner Abzug: 7 Quellen
ist für dieses Themenfeld eine knappe Bibliographie.

### Gesamtpunktzahl v1: **20 / 25**

---

## Bedingung C — Pipeline v2: "Perception Over Adoption"

### 1. Introduction & Literature Review — 3/5 (Good)

Die Forschungsfrage (AIThreat vs. AISelect direkt vergleichen) ist präziser als
v1, aber **inhaltlich ähnlich** — keine fundamental andere theoretische
Perspektive. Weiterhin nur 5 Quellen, keine systematische Suchstrategie.
Die Relevanz-Begründungen sind vorhanden (durch den Critic-Check erzwungen),
aber die Literaturbasis bleibt dünn. Wer beide Papers liest, fragt: Was ist
der eigenständige wissenschaftliche Beitrag gegenüber v1?

### 2. Methods & Results Description — 4/5 (Good)

Besser als v1 in einer wichtigen Dimension: der Multikollinearitätsfehler
(fehlende Referenzkategorie für AISelect) wurde erkannt und transparent als
PAP-Abweichung dokumentiert — das ist methodisch integer. VIF, Cohen's d,
Welch t-Test, ANOVA, ΔR² vorhanden. Robustness-Check für AI-Nutzer-Subgruppe
neu hinzugekommen. Kein Bootstrap-CI. Missing Data analog zu v1.

### 3. Structure & Organization — 4/5 (Good)

Klare Struktur, gute Übergänge. Die explizite Gegenüberstellung von
d = 0.031 (AISelect, nicht signifikant) vs. d = 0.327 (AIThreat, signifikant)
ist didaktisch stark präsentiert.

### 4. Language & Clarity — 4/5 (Good)

Professionelles Englisch, klare Formulierungen, formeller Ton. Keine Sprachfehler.

### 5. Citation & Formatting — 3/5 (Good)

Zitationsstil konsistent (natbib), aber nur 5 Quellen. "Bibliography complete"
ist mit 5 Quellen für dieses Themenfeld nicht erfüllt — die Bibliographie gibt
keinen ausreichenden Überblick über den Forschungsstand zu KI, Jobzufriedenheit
und Tool-Adoption.

### Gesamtpunktzahl v2: **18 / 25**

---

## Bedingung D — Pipeline v3: "Trust Does Not Moderate Threat"

### 1. Introduction & Literature Review — 5/5 (Excellent)

Theoretische Einbettung in Cognitive Threat Appraisal Theory (Lazarus & Folkman
1984) gibt dem Paper ein starkes konzeptuelles Fundament das v1 und v2 fehlt.
**14 Quellen** via dokumentierter PRISMA-Suchstrategie (36 Kandidaten → 14
eingeschlossen, Exclusion-Gründe protokolliert). Die Forschungslücke (keine
Studie zur Moderation durch AIAcc) ist klar identifiziert. Pre-Registration im
Intro explizit erwähnt. Die theoretische Begründung der Moderationshypothese
(hohes KI-Vertrauen = glaubwürdigere Bedrohung = stärkerer Negativeffekt) ist
überzeugend und klar vom Gegenteil abgegrenzt.

### 2. Methods & Results Description — 4/5 (Good–Excellent)

Herausragend in vielen Dimensionen: pre-registered PAP mit JSON-Artifact,
BCa Bootstrap CI (d = −0.303, 95% CI [−0.350, −0.250]), BH-FDR-Korrektur,
5-Spec Multiverse-Tabelle, Mediationsanalyse (pingouin, 3-Seed Self-Consistency),
Breusch-Pagan Test, Power-Statement (>99% Power für d ≥ 0.06), PAP-Abweichung
transparent dokumentiert, Code als Supplementary verfügbar. CONFIRMATORY vs.
EXPLORATORY explizit gelabelt. Kleiner Abzug: der **binäre Mediator**
(Frustration_bin als 0/1) ist methodisch problematisch — der a-Pfad sollte
mit logistischer Regression modelliert werden, nicht OLS. Das schwächt die
Mediationsaussage leicht.

### 3. Structure & Organization — 5/5 (Excellent)

Mustergültige IMRaD-Struktur mit gut gewählten Subsektionen. Der
Counter-Narrative Abschnitt in der Discussion ist eine strukturelle Stärke
die v1–v2 fehlt. Übergänge fließend, die Narrative von PAP-Formulierung über
Null-Ergebnis zu theoretischer Erklärung ist konsistent durchgehalten.
Tabelle 1 (Multiverse) klar und übersichtlich.

### 4. Language & Clarity — 5/5 (Excellent)

Durchgehend professionelles akademisches Englisch. Uncertainty korrekt
kommuniziert — nicht "wir sind sicher dass..." sondern behavioral signals
("consistent across all 5 multiverse specifications, 3-seed bootstrap stable").
Die Einschränkung "all reported results apply exclusively to developers who
currently use AI tools" ist klar, prominent und unmissverständlich platziert.
Keine Sprachfehler.

### 5. Citation & Formatting — 5/5 (Excellent)

15 Quellen, alle PRISMA-verifiziert, im apalike-Stil konsistent formatiert.
Bibliographie vollständig — deckt Theorie (Lazarus & Folkman), Methodik
(Benjamini & Hochberg), Datensatz (Stack Overflow 2024 + 2025) und empirische
Literatur (Schwabe, Zhao, Chung, Chang etc.) ab. Data Availability Statement
vorhanden. Kein Formatting-Fehler.

### Gesamtpunktzahl v3: **24 / 25**

---

## Zusammenfassung

| Kriterium | Baseline | v1 | v2 | v3 |
|---|:---:|:---:|:---:|:---:|
| Introduction & Literature Review | 3 | 4 | 3 | **5** |
| Methods & Results Description | 3 | 4 | 4 | **4** |
| Structure & Organization | 4 | 4 | 4 | **5** |
| Language & Clarity | 4 | 4 | 4 | **5** |
| Citation & Formatting | 3 | 4 | 3 | **5** |
| **Gesamt** | **17 / 25** | **20 / 25** | **18 / 25** | **24 / 25** |

---

## Wichtigste Beobachtungen

**Warum liegt v2 unter v1?**
v2 hat methodisch mehr zu bieten (Critic-Loops, verifiziertere Zahlen), aber
die Forschungsfrage ist inhaltlich ähnlich zu v1 — das kostet Punkte in
Introduction & Literature und Citation & Formatting, weil die Literaturbasis
gleich dünn bleibt (5 Quellen).

**Wo liegt der größte Sprung?**
Von v1 (20/25) zu v3 (24/25) — hauptsächlich durch:
- Pre-Registration (+Intro/Lit: HARKing eliminiert, Null-Ergebnis valide)
- PRISMA-Literatursuche (+Intro/Lit + Citation: 14 statt 5 Quellen)
- Strukturierte Null-Ergebnis-Kommunikation (+Structure + Language)

**Was hält v3 von 25/25 ab?**
Der binäre Mediator (Frustration_bin) in der Mediationsanalyse — methodisch
sollte hier logistische Regression für den a-Pfad verwendet werden.
Das ist der einzige substanzielle methodische Einwand gegen das Paper.
