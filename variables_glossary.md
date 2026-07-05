# Variablen- und Metriken-Glossar
## Alle Begriffe aus den vier Pipeline-Runs erklärt

---

## Teil 1 — Survey-Variablen (Stack Overflow Developer Survey 2024)

Diese Variablen kommen direkt aus dem Datensatz. Sie sind Antworten von
65.437 Entwicklern auf konkrete Survey-Fragen.

---

### JobSat — Job Satisfaction (Zielvariable)

**Survey-Frage:** "How satisfied are you in your current job?"  
**Skala:** 0–10 (kontinuierlich, 0 = sehr unzufrieden, 10 = sehr zufrieden)  
**Fehlende Werte:** 55.5% — nur aktiv beschäftigte Entwickler wurden gefragt  
**Warum Zielvariable:** Das Konstrukt das alle drei Pipeline-Runs zu erklären versuchen.
In v1: wird JobSat durch AIThreat vs. Gehalt vorhergesagt.
In v2: durch AIThreat vs. AISelect.
In v3: ist JobSat das Outcome einer Moderation und Mediation.

---

### AIThreat — Perceived AI Job Threat (Hauptprädiktor)

**Survey-Frage:** "Do you believe that AI is a threat to your current job?"  
**Antwortoptionen:** Yes / No / I'm not sure  
**Kodierung in den Analysen:**
- Baseline & v1: "Yes" = 1, "No" = 0 (I'm not sure ausgeschlossen)
- v2/v3 `AIThreat_bin`: "Yes" = 1, "No + I'm not sure" = 0
- v3 `AIThreat_3`: "Yes" = 2, "I'm not sure" = 1, "No" = 0 (ordinale Spec)

**Was es misst:** Subjektive Wahrnehmung ob KI den eigenen Job gefährdet —
kein objektives Maß der tatsächlichen Gefährdung, sondern psychologische
Bedrohungswahrnehmung.

**Befund über alle Runs:** Entwickler die AIThreat = Yes angeben haben
konsistent niedrigere Jobzufriedenheit (d ≈ −0.30 bis −0.36, dreifach repliziert).

---

### AISelect — AI Tool Adoption

**Survey-Frage:** "Do you currently use AI tools in your development process?"  
**Antwortoptionen:** Yes / No, but I plan to / No, and I don't plan to  
**Kodierung:** `AISelect_bin` = 1 (Yes), 0 (sonst)  
**Warum relevant:** In v2 der direkte Vergleich: Prediziert *Bedrohungswahrnehmung*
oder *tatsächliche Nutzung* die Jobzufriedenheit stärker? Ergebnis: AIThreat
(d = 0.327) >> AISelect (d = 0.031, nicht signifikant).

---

### AIAcc — Trust in AI Output Accuracy

**Survey-Frage:** "How much do you trust the accuracy of the output from AI
tools as part of your development workflow?"  
**Skala:** 5-Punkte-Ordinalskala:
1 = Highly distrust, 2 = Somewhat distrust, 3 = Neither, 4 = Somewhat trust, 5 = Highly trust  
**Nur sichtbar für:** Entwickler die AISelect = Yes angegeben haben  
**Warum wichtig:** In v3 der Moderator — verstärkt AIAcc den negativen Effekt
von AIThreat auf JobSat? Antwort: Nein (Null-Ergebnis, β = −0.009, p = .856).
Außerdem eigenständiger Prädiktor: höheres Vertrauen → höhere Jobzufriedenheit
(exploratorisch, β = +0.141, p = 10⁻¹⁹).

**Wichtige Einschränkung:** Weil AIAcc nur für AISelect = Yes beantwortet wird,
ist das v3-Sample nach Listwise Deletion ausschließlich aktive KI-Tool-Nutzer.

---

### YearsCodePro — Professional Coding Experience

**Survey-Frage:** "NOT including education, how many years have you coded
professionally?"  
**Format:** Binned (< 1 Jahr → 0, danach integer bis 50+)  
**Verwendung:** In der Baseline Hauptprädiktor (→ AIAcc). In v1 Kovariate.
In v2/v3 Kovariate für Erfahrungs-Effekte auf Jobzufriedenheit.

---

### ConvertedCompYearly — Jahresgehalt (USD)

**Survey-Frage:** Selbstberichtetes Gehalt, von Stack Overflow in USD umgerechnet  
**Problem:** 64.2% fehlende Werte — nur Entwickler die ihr Gehalt angaben  
**Verwendung:** Nur in v1 als log1p-transformierter Kovariate (log-Transformation
wegen starker Rechtsschiefe der Gehaltsverteilung)  
**Befund v1:** Log-Kompensation ist schwächerer Prädiktor für JobSat als AIThreat
(standardized β = 0.054 vs. β = −0.111)

---

### Frustration_bin — Work Frustration (Mediator in v3)

**Survey-Frage:** Indirekt abgeleitet aus Fragen zu negativen Arbeitsgefühlen  
**Kodierung:** Binary 0/1 — Frustration erwähnt = 1, "None of these" = 0  
**Verwendung:** In v3 als Mediator getestet: AIThreat → Frustration → JobSat  
**Befund:** Null-Mediation — indirekter Effekt CI [−0.289, +0.021] enthält 0

---

### WorkExp — Gesamte Arbeitserfahrung (Jahre)

**Survey-Frage:** Jahre Berufserfahrung insgesamt (inkl. Nicht-Coding-Arbeit)  
**Kodierung:** Ordinale Binning → numerisch umkodiert  
**Verwendung:** Kovariate in v2/v3 zur Kontrolle von Erfahrungseffekten

---

## Teil 2 — Statistische Kennzahlen

---

### Cohen's d — Standardisierte Mittelwertdifferenz

**Was es misst:** Wie groß ist der Unterschied zwischen zwei Gruppen in
Standardabweichungs-Einheiten? Unabhängig von der Stichprobengröße.

**Formel:**
```
d = (M₁ - M₂) / SD_pooled
```

**Interpretation (Cohen 1988):**
- |d| < 0.20 → vernachlässigbar
- |d| = 0.20–0.49 → klein
- |d| = 0.50–0.79 → mittel
- |d| ≥ 0.80 → groß

**In den Papers:**
- Baseline: nicht direkt als d berichtet
- v1: d = −0.36 (AIThreat Yes vs. No für JobSat) → kleiner bis mittlerer Effekt
- v2: d = −0.327
- v3: d = −0.303, 95% BCa CI [−0.350, −0.250]

**Wichtig:** Cohen's d ist robust gegenüber Stichprobengröße — er zeigt ob
ein Effekt *praktisch* bedeutsam ist, nicht nur statistisch.

---

### BCa Bootstrap Confidence Interval (neu in v3)

**Was es ist:** Ein Konfidenzintervall das nicht normalverteilt sein muss —
es "resampled" die Daten 1.000 Mal mit Zurücklegen und berechnet die
Verteilung des Schätzers empirisch.

**BCa** = Bias-Corrected and Accelerated: korrigiert für systematische
Verzerrungen im Bootstrap-Prozess.

**Warum besser als parametrisches CI:** JobSat-Daten sind nicht perfekt
normalverteilt, und Cohen's d ist ein komplexer Schätzer. BCa ist robuster.

**Interpretation:**
- d = −0.303, 95% BCa CI [−0.350, −0.250]
- → Mit 95% Konfidenz liegt der wahre Effekt zwischen d = −0.35 und d = −0.25
- → Das Intervall schließt 0 aus → Effekt ist signifikant
- → Das Intervall schließt auch d = −0.20 aus → praktisch bedeutsam

---

### Eta² (Eta-Quadrat)

**Was es misst:** Welcher Anteil der Gesamtvarianz in der AV wird durch die
Gruppenzugehörigkeit (UV) erklärt? Verwandt mit R² bei kontinuierlichen UVs.

**Formel:**
```
Eta² = SS_between / SS_total
```

**Interpretation:**
- Eta² < 0.01 → klein
- Eta² 0.01–0.06 → mittel
- Eta² > 0.14 → groß

**In den Papers:**
- Baseline: Eta² = 0.003 (sehr klein — 0.3% erklärte Varianz)
- v2: Eta² = 0.012 (AIThreat erklärt 1.2% der Varianz in JobSat)
- v3: Eta² = 0.011 (ähnlich)

**Unterschied zu Cohen's d:** Eta² funktioniert auch für mehr als zwei Gruppen
(ANOVA), Cohen's d nur für Zwei-Gruppen-Vergleiche.

---

### OLS-Regression (Ordinary Least Squares)

**Was es ist:** Die Standard-Regressionsmethode — findet die Gerade (oder
Hyperebene bei mehreren Prädiktoren) die die Abstände zu allen Datenpunkten
minimiert.

**In den Papers:**
```
JobSat = β₀ + β₁·AIThreat + β₂·Kovariate₁ + ... + ε
```

**Was die Koeffizienten sagen:**
- β₀ = Intercept (Wert wenn alle Prädiktoren = 0)
- β₁ = Wie ändert sich JobSat wenn AIThreat um 1 steigt, alles andere gleich?
- Standardisiertes β = Koeffizient wenn alle Variablen z-standardisiert → direkt vergleichbar

**Beispiel v1:** Standardisiertes β(AIThreat) = −0.111, β(LogComp) = +0.054
→ AIThreat hat etwa doppelt so starken Einfluss wie Gehalt

---

### p-Wert

**Was er aussagt:** Unter der Annahme dass kein Effekt existiert (H0 = wahr):
Wie wahrscheinlich ist es, einen Effekt dieser Stärke oder stärker zu finden?

**Wichtig:** Der p-Wert sagt **nicht** wie wahrscheinlich H1 ist.

**Bei großem N (wie hier N ≈ 17.000):** Fast alles wird signifikant, auch
winzige, praktisch bedeutungslose Effekte. Deshalb sind Cohen's d und f²
wichtiger als der p-Wert allein.

**Beispiel v3:** AIAcc Haupteffekt: p = 4.44×10⁻¹⁹ (hochsignifikant),
aber β = +0.141 — der Effekt ist statistisch klar, aber klein.

---

### BH-FDR (Benjamini-Hochberg False Discovery Rate) — neu in v3

**Problem:** Wenn man viele Tests durchführt (mehrere Hypothesen, mehrere
Koeffizienten), steigt die Wahrscheinlichkeit zufällig ein "signifikantes"
Ergebnis zu finden (Multiple Comparisons Problem).

**BH-FDR-Lösung:** Passt die p-Werte so an, dass im Erwartungswert maximal
5% der als signifikant deklarierten Ergebnisse falsch-positiv sind.

**Formel (konzeptuell):**
```
p_adj(i) = p(i) × (Anzahl Tests / Rang von p(i))
```

**Unterschied zu Bonferroni:** Bonferroni ist konservativer (teilt α durch
Anzahl Tests). BH-FDR ist weniger streng aber kontrolliert die Rate der
Falschentdeckungen — empfohlen für explorative Analysen.

**In v3:** Alle 5 Hypothesentests (AIThreat, AIAcc, Interaktion, WorkExp,
YearsCodePro) wurden BH-korrigiert. Kernergebnisse blieben stabil.

---

### f² (Cohen's f-Quadrat)

**Was es misst:** Effektgröße für den *inkrementellen* Beitrag eines Prädiktors
in einer Regression, nach Kontrolle anderer Variablen.

**Formel:**
```
f² = (R²_voll - R²_ohne_Prädiktor) / (1 - R²_voll)
```

**Interpretation:**
- f² < 0.02 → kleiner Effekt (praktisch irrelevant)
- f² 0.02–0.14 → mittlerer Effekt
- f² ≥ 0.15 → großer Effekt

**In v3:** f² für den Interaktionsterm AIThreat × AIAcc = 0.000002 → absolut
vernachlässigbar. Das Null-Ergebnis ist nicht nur nicht-signifikant, sondern
auch praktisch = 0.

---

### VIF (Variance Inflation Factor)

**Was er misst:** Multikollinearität — wie stark korrelieren die Prädiktoren
untereinander? Hohe Korrelation zwischen Prädiktoren macht Regressionskoeffizienten
instabil und schwer interpretierbar.

**Interpretation:**
- VIF < 5 → unproblematisch
- VIF 5–10 → moderat, diskutieren
- VIF > 10 → problematisch, Modell überdenken

**In v3:** Max VIF = 5.53 (AISelect_Yes) — knapp über 5, dokumentiert aber
akzeptabel. In v2 wurde ein Multikollinearitätsproblem (konstante AISelect_bin
im Listwise-Sample) vom Critic erkannt und behoben.

---

### R² und Adjusted R²

**Was sie messen:** Welcher Anteil der Gesamtvarianz in der AV wird durch
das Modell erklärt?

**R²:** Steigt immer wenn eine Variable hinzugefügt wird, auch wenn sie
irrelevant ist.

**Adjusted R²:** Bestraft für unnötige Prädiktoren — besser für Modellvergleich.

**In den Papers:**
- v1: R² ≈ 0.015 (full model) — das Modell erklärt ~1.5% der JobSat-Varianz
- v3: R² = 0.027 — ähnlich klein, was typisch für Survey-Daten ist

**Interpretation:** Kleine R² sind bei Survey-Forschung normal — JobSat hängt
von hunderten Faktoren ab die nicht gemessen wurden.

---

### ΔR² (Delta R-Quadrat)

**Was es misst:** Wie viel zusätzliche Varianz erklärt eine Variable über
das Basismodell hinaus?

**In v1:**
- Modell 1 (Erfahrung + Gehalt): R² = Basiswert
- Modell 2 (+AIThreat): ΔR² = 0.012
- → AIThreat erklärt 1.2% zusätzliche Varianz jenseits Erfahrung und Gehalt

---

### Spearman's r_s (Rangkorrelation)

**Was es ist:** Wie linear korrelieren zwei Variablen, gemessen über ihre
Ränge statt die Rohwerte? Robuster als Pearson r für ordinale Daten
und nicht-normale Verteilungen.

**Interpretation:** Wie Pearson r: −1 = perfekt negativ, 0 = kein Zusammenhang,
+1 = perfekt positiv.

**In der Baseline:** r_s = 0.10 (YearsCodePro → AIAcc)
→ Sehr schwacher positiver Zusammenhang: mehr Erfahrung → leicht mehr Misstrauen

---

### Kruskal-Wallis Test

**Was es ist:** Nicht-parametrisches Äquivalent zur ANOVA — vergleicht
Verteilungen mehrerer Gruppen ohne Normalverteilungsannahme.

**Geeignet für:** Ordinale AV (wie AIAcc mit 5 Stufen), wenn keine
Normalverteilung angenommen werden kann.

**In der Baseline:** H(4) = 127.78, p < .001
→ Die Erfahrungs-Verteilung unterscheidet sich signifikant über die 5
AIAcc-Gruppen.

---

### Welch t-Test

**Was es ist:** t-Test für zwei Gruppen der **keine** gleichen Varianzen
voraussetzt (Welch's Korrektur). Geeignet wenn eine Gruppe viel größer
oder varianzreicher ist als die andere.

**In v2/v3:** Vergleich JobSat(AIThreat=Yes) vs. JobSat(AIThreat=No)
mit stark ungleichen Gruppengrößen (n=2.282 vs. n=15.414 in v3).

---

## Teil 3 — Methoden der v3-Pipeline (neu gegenüber v1/v2)

---

### Mediation (Mediationsanalyse)

**Fragestellung:** Wird der Effekt von X auf Y durch eine dritte Variable M
vermittelt? (X → M → Y)

**Pfade:**
- **a-Pfad:** X → M (wirkt X auf den Mediator?)
- **b-Pfad:** M → Y (wirkt der Mediator auf Y, kontrolliert für X?)
- **c-Pfad:** X → Y (totaler Effekt, ohne M kontrolliert)
- **c'-Pfad:** X → Y (direkter Effekt, M kontrolliert)
- **Indirekter Effekt:** a × b (der durch M vermittelte Anteil)

**In v3:** AIThreat → Frustration → JobSat
- a-Pfad: β = +0.161, p = .106 → **nicht signifikant**
- b-Pfad: β = −0.778, p < .001 → signifikant
- Indirekter Effekt a×b: −0.124, 95% BCa CI [−0.289, +0.021] → CI enthält 0
- **Ergebnis: Null-Mediation** — Frustration ist kein signifikanter Mediator

**Tool:** `pingouin.mediation_analysis()` mit n_boot=1000, Seed=42

---

### Moderation (Moderationsanalyse)

**Fragestellung:** Hängt der Effekt von X auf Y davon ab wie stark M ist?
(= Interaktionseffekt: X × M → Y)

**Formel:**
```
Y = β₀ + β₁X + β₂M + β₃(X×M) + ε
```

**β₃ ist der Moderationseffekt.** Wenn β₃ signifikant: der Effekt von X
auf Y ist bei verschiedenen M-Werten verschieden stark.

**In v3:** AIThreat × AIAcc → JobSat
- β₃ = −0.009, p = .856, f² = 0.000002
- → **Null-Moderation**: AIAcc moderiert den AIThreat→JobSat Effekt nicht

---

### Multiverse-Analyse / Specification Curve

**Was es ist:** Das Hauptmodell wird in mehreren "vernünftigen" Varianten
wiederholt — verschiedene Kovariaten, Operationalisierungen, SE-Schätzungen.
Wenn das Ergebnis über alle Varianten stabil ist, ist es robust.

**In v3 — 5 Spezifikationen:**

| Spec | Was verändert | Interaktionsterm β | p |
|---|---|---|---|
| 1 | Hauptmodell (PAP) | −0.009 | .856 |
| 2 | AIThreat 3-stufig ordinale | −0.011 | .618 |
| 3 | AIAcc binär (trust vs. distrust) | −0.106 | .375 |
| 4 | HC3 Robust Standard Errors | −0.009 | .879 |
| 5 | Mean-centered predictors | −0.009 | .856 |

**Fazit:** 0/5 Specs signifikant → Null-Ergebnis ist **sehr robust**, kein Spec-Artefakt.

---

### Pre-Analysis Plan (PAP)

**Was es ist:** Eine schriftliche Festlegung der Hypothesen, Methoden und
Analysestrategie *bevor* die Daten analysiert werden.

**Warum wichtig:** Verhindert HARKing (Hypothesizing After Results Known) —
wenn die Hypothese erst nach Datensichtung formuliert wird, steigt die
Wahrscheinlichkeit falsch-positiver Ergebnisse massiv (p-Hacking).

**In v3:** Gespeichert als `logs/v3/preanalysis_plan.json` vor Stage 1.
Enthält: primäre Hypothese, Methode, Kovariaten, Mindest-Effektgröße,
Mediationshypothese, DAG, Novelty-Score vs. v1/v2.

**Einschränkung:** Lokale Datei, nicht auf OSF.io zeitgestempelt — nicht
extern verifizierbar.

---

### PRISMA-lite (Systematic Literature Search)

**Was es ist:** Vereinfachte Version des PRISMA-Protokolls für systematische
Literaturübersichten — dokumentiert den vollständigen Suchprozess.

**In v3:**
- 8 Web-Searches mit definierten Suchstrings
- 36 Kandidaten identifiziert (N_identified)
- 33 Abstracts gescreent gegen Inclusion-Kriterien (empirisch, peer-reviewed, N≥100, Englisch)
- 14 Papers eingeschlossen (N_included)
- Alle 14 per Fetch-MCP verifiziert (Claim gegen Abstract)

**Warum wichtig:** Macht die Literaturauswahl transparent und reproduzierbar —
ein Reviewer kann nachvollziehen warum welche Papers drin sind und welche nicht.

---

### Adversarial Critic

**Was es ist:** Eine separate Agenten-Instanz die das Paper aktiv zu rejecten
versucht — feindlicher Gutachter-Modus.

**6 Review-Punkte in v3:**
1. Steelman der Nullhypothese
2. Nicht kontrollierte Konfundierungen
3. P-Hacking-Risiko
4. Fehlende Vergleichsgruppen
5. Messprobleme (Single-Item, Common Method Bias)
6. Generalisierbarkeit

**Ergebnis v3:** Alle 6 als HOCH bewertet, 2 Zusatzanalysen durchgeführt
(DevType-Kontrolle, Country-Kontrolle) — AIThreat-Effekt blieb robust.

---

### Behavioral Uncertainty (vs. Selbstauskunft)

**Problem:** Wenn man ein LLM fragt "Wie sicher bist du?", ist die Antwort
systematisch zu optimistisch (+30 Prozentpunkte Overestimation, laut
arxiv:2601.11956).

**Lösung in v3:** Konfidenz wird nicht selbst berichtet sondern aus
Verhalten abgeleitet:
- Konsistenz über 3 Bootstrap-Seeds (Varianz = 0.000 → sehr stabil)
- Breite des BCa-Intervalls (schmal = präzise)
- Abstand des p-Werts von der Schwelle (p = 10⁻³⁴ vs. p = 0.04 → sehr verschiedene Evidenz)

---

## Schnellreferenz: Alle Effektgrößen der drei Hauptruns

| Kennzahl | v1 | v2 | v3 |
|---|---|---|---|
| AIThreat Cohen's d | −0.36 | −0.327 | −0.303 |
| AIThreat BCa CI | — | — | [−0.350, −0.250] |
| AIThreat β (OLS) | −0.673 | −0.651 | −0.609 |
| AIThreat p-Wert | < 10⁻⁴⁴ | < 10⁻⁴⁴ | 1.03×10⁻³⁴ |
| Modell R² | ~0.015 | 0.033 | 0.027 |
| N analytisches Sample | 10.112 | 17.696 | 17.670 |
| Interaktionsterm f² | — | — | 0.000002 |
| Mediations-CI | — | — | [−0.289, +0.021] |
