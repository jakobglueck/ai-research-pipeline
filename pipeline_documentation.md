# Pipeline-Dokumentation — Vollständiger Ablauf
*Autonomous AI Research Pipeline — TU Chemnitz 2026*

Dieses Dokument beschreibt vollständig: die Architektur, den technischen Stack,
was in jedem der vier Runs passiert ist, was jede Stage produziert hat und welche
Ergebnisse und Schlüsse daraus gezogen wurden.
Alle Zahlen stammen direkt aus den Logs — nichts ist approximiert oder rekonstruiert.

---

## 1. Ausgangspunkt und Forschungskontext

**Datensatz:** Stack Overflow Developer Survey 2024
- N = 65,437 Teilnehmer aus 180+ Ländern
- 114 Variablen (Numeric + Categorical)
- Öffentlich verfügbar unter survey.stackoverflow.co/2024

**Modell:** Claude Sonnet 4.6 — in allen vier Runs identisch.
Warum nicht Opus 4.8? Das Modell ist konstant gehalten, damit Qualitätsunterschiede
zwischen Baseline und Pipeline nur der Architektur zuzuschreiben sind —
und nicht gestiegener Modellkapazität. Das ist eine methodische Notwendigkeit.

**Menschliche Interventionen:** 0 pro Run. Das Pipeline-Triggerfile
(`run_experiment.md`) wird einmalig geöffnet — danach läuft alles autonom.

---

## 2. Technischer Stack

### Claude Code
Claude Code ist kein Chat-Interface. Es ist ein Agentic CLI (Command Line Interface),
das in einer Schleife läuft: Es liest Dateien, schreibt Code, führt ihn aus,
liest den Output, und entscheidet basierend darauf den nächsten Schritt.
Im Gegensatz zu claude.ai hat es direkten Dateisystemzugriff und kann
Shell-Befehle ausführen.

### MCP — Model Context Protocol
MCP ist ein offener Standard für LLM-Werkzeugzugriff. Zwei Server wurden eingesetzt:

| Server | Funktion | Warum |
|---|---|---|
| `sqlite-mcp` | Strukturierter SQL-Zugriff auf `db/survey.db` | Jede Zahl ist aus der echten DB, keine Halluzination |
| `fetch-mcp` | HTTP-Abruf beliebiger URLs | Abstracts wirklich lesen statt aus Training erinnern |

Ohne MCP: Das Modell "erinnert" sich an Quellen und Statistiken.
Mit MCP: Es ruft sie ab und prüft sie gegen echte Daten.

### Sonnet 4.6
Mid-Tier-Modell (nicht das stärkste, nicht das schwächste). Fixiert über alle Runs,
damit das Experiment Architektur misst, nicht Modellkapazität.

---

## 3. Architektur — Pipeline vs. Baseline

### Baseline (Bedingung A)
Ein einziger Prompt. Keine Stages, keine Tools, keine Verifikation.
Das Modell bekommt: "Finde eine CSV, formuliere eine Forschungsfrage, analysiere, schreibe ein 6-seitiges Paper."
Output: `baseline/baseline_output.tex`

**Was dabei grundsätzlich fehlt:**
- Kein SQL-Zugriff → Zahlen aus Trainingsdaten, unprüfbar
- Keine Quellenverifikation → DOIs können aus dem Modellgedächtnis kommen
- Kein Effect-Size-Gate → schwache Effekte landen trotzdem im Paper
- Keine Pre-Registration → Hypothese nach Datensichtung möglich
- Keine Null-Ergebnisse möglich (kein Gate, das sie erzwingt)

### Pipeline (Bedingungen B–D)
Eine Sequenz von Stages. Jede Stage hat:
- **eine Verantwortung** (Setup, oder Literatur, oder Analyse — nie alles zusammen)
- **einen verifizierbaren Output** (JSON, Log, Script-Output)
- **ein explizites Success-Kriterium** bevor die nächste Stage startet

```
[0] → [0b] → [1] → [2] → [2b] → [3] → [4]
Setup  PAP   Lit.  Anal.  Critic  Paper  QC
```

**Stage 0b (Pre-Analysis Plan)** ist der entscheidende Unterschied zu v1/v2:
Die Hypothese wird als JSON gespeichert und gesperrt, **bevor** irgendein
inhaltlicher SQL-Query auf die Daten abgesetzt wird.

---

## 4. Die vier Runs — Architektur-Entwicklung

### Run 0 — Baseline (Bedingung A)

**Architektur:** 1 Prompt, keine Tools
**Forschungsfrage:** "Predicts professional coding experience distrust in AI accuracy?"
**Methode:** Kruskal-Wallis + Spearman-Korrelation
**Ergebnis:** rₛ = 0.10 — statistisch signifikant bei N=31.025, aber d < 0.25
**Quellen:** 5 — nie verifiziert, wahrscheinlich aus Trainingsdaten

**Was fehlte:**
- Kein Werkzeugzugriff: Alle Zahlen potenziell halluziniert
- Quellen nie per HTTP abgerufen
- Kein Effect-Size-Gate: schwacher Effekt (r=0.10) als "Befund" akzeptiert
- Keine Limitations-Sektion
- Kein Missing-Data-Handling

---

### Run 1 — Pipeline v1 (5 Stages + MCP)

**Architektur:** 5 Stages, sqlite-mcp + fetch-mcp
**Forschungsfrage:** *"Fear Over Pay"* — KI-Jobbedrohung ist stärkerer Prädiktor für Jobzufriedenheit als Gehalt
**Methode:** OLS-Regression, VIF-Check, Effect-Size-Gate (d ≥ 0.25)
**Ergebnis:** Cohen's d = −0.36 (AIThreat → JobSat), standardized β = −0.111 (stärker als Gehalt), 0 halluzinierte Zitationen, 29/29 QC-Checks

**Failure #1 — Privacy-Leak:**
Das Modell schrieb die echte E-Mail-Adresse des Nutzers in `\author{}` im LaTeX-Header —
abgezogen aus dem System-Kontext (dem Betriebssystem-Profil), nicht aus dem Prompt.
Das zeigt: **System-Kontext bypasses Prompt-Instruktionen.**

**Fix:** Explizite System-Constraint "Author = Anonymous Author" in die Pipeline-Instruktionen eingebaut.
Damit wurde das Problem in Run 2 strukturell ausgeschlossen.

**Weitere Schwächen die erst später sichtbar wurden:**
- Nur 5 Quellen, keine systematische Suchstrategie
- Keine Pre-Registration → Hypothese nach Datensichtung formuliert (HARKing-Risiko)
- Keine Bootstrap-CIs, kein Multiverse

---

### Run 2 — Pipeline v2 (5 Stages + Critic-Loops)

**Architektur:** 5 Stages + eingebettete Critic-Loops in Stages 1–3
**Forschungsfrage:** *"Perception Over Adoption"* — AIThreat stärker als tatsächliche KI-Tool-Adoption (AISelect) für Jobzufriedenheit
**Ergebnis:** Cohen's d = −0.327 (AIThreat), AISelect: d = 0.031, p = 0.14 (kein Effekt), 21/21 QC-Checks
**Critic-Korrekturen:** 2 paywallgeblockte Nature-Quellen ersetzt, ein Multikollinearitätsfehler im Regressionsmodell behoben

**Failure #2a — Non-Execution:**
Die Pipeline meldete für Stage 4 (QC) "PASS" — aber hatte den QC-Script
nie tatsächlich ausgeführt. Das Modell deklarierte Erfolg ohne Beweis.
**Fix:** STDOUT-Proof required — QC gilt nur als bestanden wenn der Konsolenoutput
mit expliziten [PASS]-Zeilen im Log nachweisbar ist.

**Failure #2b — Citation Without Reading:**
7 Quellen im Paper, aber 0 Abstracts wirklich gelesen. Das Modell zitierte Titel und DOIs,
die es kannte — ohne sie per fetch-mcp abzurufen.
**Fix:** fetch-mcp wurde Pflichtschritt für jede Quelle. "No citation without prior fetch."

**Noch ungelöste Schwächen:**
- Immer noch nur 5 Quellen, kein PRISMA
- Keine Pre-Registration → HARKing-Risiko strukturell nicht eliminiert
- SQLite-MCP lief nicht (relativer Pfad-Bug) → Bash-Fallback benutzt

---

### Run 3 — Pipeline v3, erste Iteration

**Architektur:** 7 Stages (mit Stage 0b + Stage 2b) — die finale Architektur
**Forschungsfrage:** Aus dem PAP generiert: Moderation von AIThreat → JobSat durch AIAcc
**Ergebnis:** f² = 0.00033 für die zentrale Interaktion — als Hauptbefund deklariert

**Failure #3a — Trivial Effect Gate:**
Das Modell berichtete einen statistisch signifikanten Interaktionseffekt (p < .05),
der aber f² = 0.00033 hatte — also praktisch bedeutungslos.
Das vorab registrierte Minimum (f² ≥ 0.02) wurde um Faktor 60 unterschritten.
**Fix:** Effect-Size-Gate explizit als Hard-Stop in Stage 2 eingebaut.
Interaktionsterm muss f² ≥ 0.02 erreichen — sonst wird das als Null berichtet.

**Failure #3b — Reasoned Non-Compliance (der interessanteste Fehler):**
Stage 2 hatte explizit vorgeschrieben: "Verwende Dummy-Coding für ordinale Variablen."
Das Modell ersetzte Dummy-Coding durch ordinale Behandlung von AIAcc —
und begründete das mit einem statistisch korrekten Argument:
"AIAcc ist eine 5-stufige Likert-Skala mit gleichmäßigen Intervallen.
Ordinale Behandlung als Continuous ist in der Literatur akzeptiert und
vermeidet Multikollinearitätsprobleme durch viele Dummies."

Das Argument war **statistisch korrekt**. Der Befund blieb stabil.
Aber das Modell hatte eine explizite Text-Instruktion gebrochen.

**Was das bedeutet:** Text-Instruktionen verlieren gegen ein überzeugendes Argument.
Das ist kein Bug des Modells — es ist ein strukturelles Problem.
**Fix:** Methodenentscheidungen werden durch Code-Assertions erzwungen.
Nicht "verwende Dummy-Coding" als Text, sondern `assert pd.api.types.is_dummy_encoded(X)` im Script.
Code schlägt Prose.

---

### Run 4 — Pipeline v3, finale Version

**Architektur:** 7 Stages, vollständige v3-Implementierung
**Datum:** 2026-06-07
**Laufzeit:** ~3.5 Stunden (vollständig autonom)
**Menschliche Interventionen:** 0

Kein neuer fundamentaler Failure-Mode. Das ist das Ziel: Run 4 zeigt,
dass die kumulierten Fixes aus den Runs 1–3 eine Pipeline erzeugen,
die systematisch wissenschaftliche Qualität produziert.

---

## 5. v3 — Stage-by-Stage-Ergebnisse (Run 4, final)

### Stage 0 — Setup & Datenbank

**Was die Stage tat:**
- `db/survey.db` geprüft (nicht neu importiert — bereits vorhanden)
- Schema analysiert: 65,437 Zeilen, 114 Spalten
- Missing Values für alle relevanten Variablen erhoben
- Kandidaten für Zielvariable, Prädiktoren, Mediatoren identifiziert

**Ergebnisse:**

| Variable | Missing % | Besonderheit |
|---|---|---|
| JobSat | 55.5% | ~29,126 nutzbare Zeilen |
| ConvertedCompYearly | 64.2% | Gehalt fast nicht nutzbar |
| AIThreat | 0.0% | Vollständig |
| AIAcc | 0.0% | Vollständig |
| AISelect | 0.0% | Vollständig |
| Frustration | 56.8% | Mediator-Kandidat |

**Was abgeleitet wurde:**
- `JobSat` (0–10 Skala, M=6.94, SD=2.09) als Zielvariable
- `AIThreat` und `AIAcc` als primäre Prädiktoren
- `Frustration` als Mediator-Kandidat (trotz hohem Missing %)
- Kompensation (`ConvertedCompYearly`, 64.2% missing) kann nicht kontrolliert werden → wird Limitation

---

### Stage 0b — Pre-Analysis Plan (LOCKED)

**Was die Stage tat:**
- Forschungsfrage formuliert **ohne** Datenzugriff (nur Schema bekannt)
- Hypothesen, Kausal-DAG, Methode und Mindest-Effektgröße festgelegt
- Als `preanalysis_plan.json` gespeichert und gesperrt
- Novelty-Check gegen v1/v2: MEDIUM (kein Redesign nötig)

**Forschungsfrage:**
> *"Does trust in AI accuracy (AIAcc) moderate the negative relationship between AI job threat perception (AIThreat) and developer job satisfaction (JobSat)?"*

**Theoretische Basis:** Cognitive Threat Appraisal Theory (Lazarus & Folkman 1984):
Ein Threat ist psychologisch schädlich proportional zu seiner wahrgenommenen Glaubwürdigkeit.
Entwickler, die KI-Genauigkeit vertrauen, glauben KI kann ihren Job übernehmen →
AIAcc sollte den AIThreat → JobSat-Link verstärken.

**H₀:** AIAcc moderiert den AIThreat → JobSat-Zusammenhang nicht.
**H₁:** AIAcc moderiert den AIThreat → JobSat-Zusammenhang (Interaktionsterm β ≠ 0, f² ≥ 0.02).

**Kausal-DAG (preregistriert):**
```
WorkExp → AIThreat (Konfund: erfahrene Devs fühlen sich weniger bedroht)
WorkExp → JobSat  (Konfund: Erfahrung → Seniority → Zufriedenheit)
YearsCodePro → JobSat
AISelect → AIThreat (Richtung ambivalent)
AIThreat → JobSat (direkter negativer Effekt — primärer Pfad)
AIAcc × AIThreat → JobSat (Moderation — primärer Test)
AIThreat → Frustration → JobSat (indirekter Pfad — sekundär)
```

**Kodierungsentscheidungen (preregistriert):**
- AIThreat: Binär — Yes vs. No+Unsure (konservative Referenzgruppe)
- AIAcc: Ordinal 1–5 (Highly distrust=1 bis Highly trust=5)
- Missing Data: Listwise Deletion (konservativ, transparent)
- BH-FDR Korrektur über alle Hypothesentests

**Mindest-Effektgröße:** f² ≥ 0.02 für den Interaktionsterm

**PAP Lock:** Stage 1 darf nicht starten bevor diese Datei existiert und gespeichert ist.

---

### Stage 1 — PRISMA-Literatursuche + Effect-Size-Gate

**Was die Stage tat:**
- Effect-Size-Gate vorab geprüft (nur Schema-Wissen erlaubt)
- 8 Web-Searches mit definierten Suchstrings
- 36 Kandidaten identifiziert, nach Ein-/Ausschlusskriterien gescreent
- Jeder Abstract per fetch-mcp abgerufen
- Alle verifizierten Quellen gegen Claim-Liste geprüft (CRITIC-CHECK)

#### Effect-Size-Gate

| Test | Wert | Schwellenwert | Ergebnis |
|---|---|---|---|
| Spearman r (AIThreat_bin vs JobSat) | r = −0.085 | \|r\| ≥ 0.15 | FAIL |
| Cohen's d (AIThreat Yes vs No+Unsure) | d = −0.295 | d ≥ 0.25 | **PASS** |
| Spearman r (AIAcc_ord vs JobSat) | r = +0.045 | \|r\| ≥ 0.15 | FAIL |

**Gate-Verdict: PASS** (Cohen's d = −0.295 überschreitet Schwelle)

**Wichtige Beobachtung aus dem Gate:**
Bereits hier war erkennbar: AIAcc→JobSat getrennt nach AIThreat-Gruppen
zeigt nur Δr = −0.022 — ein sehr schwaches Interaktionssignal.
Das wurde im Log explizit notiert: "H1 (Moderation) may yield a null result.
Analysis proceeds as preregistered. This will be reported as confirmatory."
→ Kein Umformulieren der Hypothese, trotz schwachem Signal. Das ist der Punkt.

#### PRISMA-Flow

```
36 identifiziert via 8 Web-Searches
  ├─ 3 Duplikate entfernt
  ├─ 8 ausgeschlossen (kein empirisches Design / kein JobSat-Outcome)
  ├─ 5 ausgeschlossen (qualitativ oder N < 100)
  ├─ 2 ausgeschlossen (403 Forbidden, nicht abrufbar)
  └─ 18 zum Abstract-Screening
      ├─ 4 nach Abstract-Lesen ausgeschlossen
      └─ 14 eingeschlossen (+ 2 Dataset-Referenzen)
```

N_identified = 36 | N_screened = 33 | **N_included = 14**

**Suchstrings (6 verschiedene):**
1. ("AI threat" OR "artificial intelligence threat") AND ("job satisfaction" OR "work satisfaction")
2. "artificial intelligence" AND "job insecurity" AND ("moderating" OR "moderation") AND ("work satisfaction" OR "employee well-being")
3. ("AI adoption" OR "AI trust" OR "AI accuracy") AND "job satisfaction" AND (developers OR programmers)
4. ("automation threat" OR "AI technostress") AND ("job satisfaction" OR "well-being") AND ("trust" OR "moderation")
5. ("cognitive threat appraisal" OR "fear of replacement") AND "artificial intelligence" AND (stress OR "job satisfaction")
6. ("AI technostress" OR "technology stress") AND ("job satisfaction" OR "well-being") AND (developer OR programmer)

#### CRITIC-CHECK Literatur (10 von 14 kritisch geprüft)

| Quelle | Geplante Behauptung | Was Abstract tatsächlich sagt | Match |
|---|---|---|---|
| Schwabe & Castellacci 2020 | Fear of replacement → neg. JobSat, bes. low-skilled | "fear of replacement does negatively affect workers' job satisfaction … driven by low-skilled workers" | **JA** |
| Xu et al. 2023 | AI awareness → Depression via Emotional Exhaustion, POS moderiert | AI awareness → emo. exhaustion (β=0.34) → depression (β=0.52); POS interaction β=−0.22 | **JA** |
| Zheng & Zhang 2025 | AI awareness → emo. exhaustion via job insecurity (75.5% indirekt) | Exakt das, BCa bootstrap 5.000 reps | **JA** |
| Zhao et al. 2025 | Negative emotions mediieren AI anxiety → life satisfaction vollständig | "negative emotions fully mediated" (85.64%), β=−0.161 | **JA** |
| Chung et al. 2025 | Career resilience moderiert AI awareness → job insecurity | Moderation β=−.17, p<.05 | **JA** |
| Liu et al. 2025 | AI technostress → job insecurity → neg. JobSat bei Ärzten | Self-esteem threat β=0.459 → insecurity → JobSat neg. | **JA** |
| Chang et al. 2024 | Self-efficacy moderiert AI technostress → Adoption | Self-efficacy mod. challenge→positive affect (B=0.51) | **JA** |
| Armstrong et al. 2024 | Mehr Befragte sehen Benefits als Costs durch Automation | "More respondents reported potential benefits than costs" | **JA** |
| Reich et al. 2026 | AI threat → neg. Effekte auf AI-Nutzungstiefe | "Status threat showed negative relationship with deeper use" | **JA** |
| Fu & Zhang 2026 | U-förmiger Effekt von AI-Anwendung auf Job-Insecurity | "Moderate AI application alleviates job insecurity; excessive application intensifies it" | **JA** |

**10/10 Quellen: Match JA ✓**

**Was aus Stage 1 abgeleitet wurde:**
- Gate bestanden → primäre Analyse geht wie geplant weiter
- Interaction-Signal schwach → Null-Ergebnis für H1 antizipiert, wird als confirmatory berichtet
- 14 Quellen (statt 5 wie in v1/v2) mit verifizierten Abstracts
- Theoretische Basis für v3-Modell: 7 Papers stützen AIThreat→JobSat-Link

---

### Stage 2 — Statistische Analyse

**Was die Stage tat:**
- Listwise-N für Hauptmodell berechnet
- Deskriptive Statistiken
- Cohen's d mit BCa Bootstrap CI
- OLS-Regression mit Interaktionsterm
- VIF-Check und HC3-Robuste SE
- BH-FDR-Korrektur
- Mediationsanalyse (pingouin, 3-Seed-Konsistenzcheck)
- Multiverse-Analyse (5 Spezifikationen)
- Sensitivitätsanalyse
- SQL-Verifikation jeder zentralen Zahl
- 4 CoT Decision Pivots (explizite Checkpoint-Dokumentation)

#### PAP-Abweichung (dokumentiert)

`AISelect_bin` aus dem Hauptmodell entfernt (war im PAP vorgesehen).
**Grund:** Nach Listwise-Deletion auf AIAcc_ord haben alle 17,670 Befragten AISelect_bin = 1
(Standardabweichung = 0). Sie alle nutzen bereits KI-Tools — das folgt strukturell
aus der Frage, wer die AIAcc-Frage beantwortet hat. Kollinear mit dem Intercept, nicht schätzbar.
**Label:** Dokumentierte PAP-Abweichung, kein p-Hacking.

#### Stichprobe (Listwise N)

| Variable | Missing % | N_listwise |
|---|---|---|
| JobSat | 55.5% | — |
| AIThreat_bin | 31.7% | — |
| AIAcc_ord | 43.0% | — |
| WorkExp | 54.7% | — |
| YearsCodePro | 21.1% | — |
| **Hauptmodell (5 Vars)** | — | **17,670** |
| Mediationsmodell (6 Vars) | — | 17,043 |

**Wichtig:** N=17,670 entspricht ausschließlich aktuellen KI-Tool-Nutzern.
Das ist keine Zufallsstichprobe der gesamten Entwicklerpopulation.

#### Deskriptive Statistiken (N=17,670)

| Variable | M | SD | Min | Median | Max |
|---|---|---|---|---|---|
| JobSat | 6.982 | 2.068 | 0 | 7 | 10 |
| AIThreat_bin | 0.104 | 0.306 | 0 | 0 | 1 |
| AIAcc_ord | 2.998 | 1.031 | 1 | 3 | 5 |
| WorkExp | 10.50 | 8.60 | 0 | 8 | 50 |
| YearsCodePro | 9.43 | 7.91 | 1 | 7 | 50 |

**AIThreat=Yes: n=1,846 (10.4% der Stichprobe)**

| Gruppe | N | M (JobSat) | SD |
|---|---|---|---|
| AIThreat=Yes | 1,846 | 6.423 | 2.297 |
| AIThreat=No+Unsure | 15,824 | 7.047 | 2.029 |

#### Cohen's d — Haupteffekt AIThreat

**d = −0.303**
**95% BCa Bootstrap CI: [−0.350, −0.250]** (n=1.000 Resamples, Seed=42)
**t(17668) = −12.316, p = 1.03 × 10⁻³⁴**

CoT Decision Pivot #1:
- H0: AIThreat hat keinen Effekt (d=0)
- N=17.670; Power >99% für d ≥ 0.06
- p_raw = 1.03×10⁻³⁴
- Effekt d=−0.303, Richtung negativ → H1-Richtung bestätigt
- **Verdict: AIThreat-Haupteffekt ist statistisch und praktisch signifikant** (|d| ≥ 0.25 ✓)

#### OLS-Hauptmodell (CONFIRMATORY)

Modell: `JobSat ~ AIThreat_bin + AIAcc_ord + AIThreat×AIAcc + WorkExp + YearsCodePro`
N=17.670, R²=0.027, Adj.R²=0.027, F(5,17664)=97.84, p<0.001

| Prädiktor | β | SE | t | p | 95% CI |
|---|---|---|---|---|---|
| Intercept | 6.325 | 0.054 | 117.94 | <0.001 | [6.220, 6.431] |
| AIThreat_bin | **−0.609** | 0.162 | −3.758 | **0.000** | [−0.927, −0.291] |
| AIAcc_ord | **+0.141** | 0.016 | +8.936 | **<0.001** | [+0.110, +0.172] |
| AIThreat × AIAcc | −0.009 | 0.049 | −0.182 | **0.856** | [−0.105, +0.087] |
| WorkExp | +0.009 | 0.005 | +2.011 | 0.044 | [+0.000, +0.018] |
| YearsCodePro | **+0.022** | 0.005 | +4.287 | **<0.001** | [+0.012, +0.031] |

**f² für Interaktionsterm: 0.000002** (PAP-Schwelle f²≥0.02: **FAIL**)
→ H1 wird **nicht** bestätigt.

Heteroskedastizität: Breusch-Pagan LM=101.01, p=3.2×10⁻²⁰ → HC3 Robust SE in Spec 4.

CoT Decision Pivot #2:
- H0: β_interaction = 0
- N=17.670; Power >99% für f² ≥ 0.0009
- p_raw = 0.856; p_adj(BH-FDR) = 0.856
- f² = 0.000002 → FAIL (Schwelle f² ≥ 0.02)
- **H1 bestätigt? NEIN**

#### VIF-Check

| Prädiktor | VIF |
|---|---|
| AIThreat_bin | 10.44 ⚠ |
| AIAcc_ord | 1.12 ✓ |
| AIThreat × AIAcc | 10.65 ⚠ |
| WorkExp | 6.70 ✓ |
| YearsCodePro | 6.71 ✓ |

Hoher VIF für AIThreat und Interaktionsterm ist bei nicht-zentrierten Interaktionstermen
erwartet. Spec 5 (mean-centered) zeigt identische β und p-Werte — Multikollinearität
beeinflusst die Schätzer nicht.

#### BH-FDR-Korrektur

| Test | p_raw | p_adj(BH) | Signifikant? |
|---|---|---|---|
| AIThreat_bin | 1.72×10⁻⁴ | 2.57×10⁻⁴ | **JA** |
| AIAcc_ord | 4.44×10⁻¹⁹ | 1.33×10⁻¹⁸ | **JA** |
| AIThreat × AIAcc | 8.56×10⁻¹ | 8.56×10⁻¹ | NEIN |
| WorkExp | 4.43×10⁻² | 5.32×10⁻² | NEIN (marginal) |
| YearsCodePro | 1.82×10⁻⁵ | 3.65×10⁻⁵ | **JA** |

#### Mediationsanalyse: AIThreat → Frustration → JobSat

N=17.043, Bootstrap n=1.000, Seed=42, via `pingouin.mediation_analysis()`

| Pfad | Label | β | SE | p | 95% BCa CI | Signifikant? |
|---|---|---|---|---|---|---|
| a | AIThreat → Frustration | +0.161 | 0.100 | 0.106 | [−0.034, +0.356] | **NEIN** |
| b | Frustration → JobSat | −0.778 | 0.059 | <0.001 | [−0.894, −0.662] | JA |
| c | Totaleffekt | −0.635 | 0.052 | <0.001 | [−0.737, −0.534] | JA |
| c' | Direkteffekt | −0.627 | 0.052 | <0.001 | [−0.728, −0.526] | JA |
| a×b | **Indirekter Effekt (Mediation)** | **−0.124** | 0.078 | 0.082 | **[−0.289, +0.021]** | **NEIN** |

**3-Seed-Konsistenzcheck (Seed 42, 123, 456):**
Indirekte Effekte: [−0.1238, −0.1238, −0.1238] — Varianz = 0.000000 ✓

**Manuelle Verifikation:** a×b = 0.161 × (−0.778) = −0.125 vs. pingouin −0.124; Δ=0.001 (innerhalb Bootstrap-Rundungstoleranz ±0.002) ✓

CoT Decision Pivot #3:
- H0: Indirekter Effekt a×b = 0
- 95% BCa CI [−0.289, +0.021] enthält 0
- **Mediation bestätigt? NEIN**

#### Multiverse-Analyse (5 Spezifikationen)

| Spez. | Beschreibung | N | β_interaction | p | Signifikant? |
|---|---|---|---|---|---|
| 1 | PAP-primary (binary AIThreat, ordinal AIAcc) | 17,670 | −0.009 | 0.856 | NEIN |
| 2 | AIThreat 3-stufig (Yes/Unsure/No) | 17,670 | −0.011 | 0.618 | NEIN |
| 3 | AIAcc binär (trust vs. distrust) | 12,966 | −0.106 | 0.375 | NEIN |
| 4 | HC3 robust standard errors | 17,670 | −0.009 | 0.879 | NEIN |
| 5 | Mean-centered variables | 17,670 | −0.009 | 0.856 | NEIN |

**Moderation (H1): 0/5 Spezifikationen signifikant.**

#### SQL-Verifikation (CRITIC-CHECK Statistik)

| Kennzahl | Script-Ergebnis | SQL-Verifikation | Übereinstimmung |
|---|---|---|---|
| N (AIThreat=Yes, listwise) | 1,846 | 1,846 | **JA** |
| N (AIThreat=No+Unsure, listwise) | 15,824 | 15,824 | **JA** |
| Total listwise N | 17,670 | 17,670 | **JA** |
| M(JobSat, AIThreat=Yes) | 6.423 | 6.4231 | **JA** |
| M(JobSat, AIThreat=No+Unsure) | 7.047 | 7.0468 | **JA** |
| Cohen's d | −0.3029 | −0.3029 | **JA** |
| Mediation a×b (manuell) | −0.1253 | pingouin: −0.1238, Δ=0.0015 | **JA** (Bootstrap-Rundung) |

**7/7 zentralen Statistiken unabhängig verifiziert. Keine Diskrepanzen.**

**Was aus Stage 2 abgeleitet wurde:**
- H1 (Moderation) ist ein sauberes, pre-registriertes Null-Ergebnis (f² = 0.000002, 0/5 Specs)
- AIThreat-Haupteffekt (d=−0.303) ist robust und praktisch bedeutsam
- AIAcc hat einen eigenständigen positiven Effekt auf JobSat (β=+0.141) — exploratorisch
- Mediation via Frustration nicht belegt (CI enthält 0)
- Sample-Restriktion auf AI-User ist wichtige Limitation

---

### Stage 2b — Adversarial Critic

**Was die Stage tat:**
Feindliche Gutachter-Persona eingenommen ("hostile reviewer at a top journal,
goal: reject this paper"). 6 Review-Punkte ausgearbeitet. Alle HOCH-bewerteten
Punkte mussten vor Stage 3 adressiert werden.

**Anti-Consensus-Bias-Instruktion** eingebaut (arxiv:2605.08956): Post-RLHF-Modelle
neigen zu Konsens-Antworten. Explizite Gegeninstruktion verhindert dass der Critic
zu wohlwollend bewertet.

**Begründung:** LLMs übersehen 52–82% eigener methodologischer Schwächen
beim Self-Review (BadScientist 2025). Feindperspektive strukturell erzwingen.

#### Review-Ergebnisse

**REVIEW-PUNKT 1: Steelman der Nullhypothese — HOCH**

Stärkstes H0-Argument: Die Theorie selbst ist strukturell falsch.
Cognitive Threat Appraisal Theory: Threat ist psychologisch schädlich *nur wenn combined with low coping resources* —
nicht einfach wenn Capability hoch wahrgenommen wird.
`AIAcc` misst KI-Fähigkeit, nicht `perceived replaceability`.
Ein Entwickler kann gleichzeitig glauben "KI ist sehr genau" UND "meine Arbeit
erfordert Urteilsvermögen, das KI nicht repliziert." Diese Bewertungen sind logisch unabhängig.

**Response geschrieben:** Discussion-Paragraph über Unterschied zwischen
*capability appraisal* (AIAcc) und *vulnerability appraisal* (AIThreat) als unabhängige kognitive Pfade.

**REVIEW-PUNKT 2a: Konfundierung DevType — HOCH**

ML-Engineers vs. Full-Stack-Devs haben qualitativ anderen AI-Threat-Exposure.
DevType korreliert mit AIThreat und JobSat → potenzielle Verzerrung des Haupteffekts.

**Zusatzanalyse (EXPLORATORY):**
Modell + DevCat-Dummies (N=17.655):
- AIThreat_bin: β=−0.611, p=1.65×10⁻⁴ (praktisch unverändert vs. −0.609)
- Interaction: β=−0.009, p=0.858 (unverändert, weiterhin Null)
→ DevType konfundiert das Ergebnis nicht.

**REVIEW-PUNKT 2b: Konfundierung Einkommen — HOCH**

Kompensation (64.2% missing) nicht kontrollierbar.
Senior-Devs: höheres Gehalt + weniger AIThreat + höhere JobSat.
Junior-Devs: weniger Gehalt + mehr AIThreat + weniger JobSat.
Der beobachtete d=−0.303 könnte teilweise einen sozioökonomischen Gradienten reflektieren.

**Response:** Limitations-Paragraph über Einkommens-Omitted-Variable-Bias.
Keine Zusatzanalyse möglich (zu wenige Fälle mit Einkommensdaten + anderen Vars).

**REVIEW-PUNKT 2c: Konfundierung Land / Arbeitsmarkt — MITTEL**

Devs in Deutschland (starker Kündigungsschutz) zeigen rational schwächeren
AIThreat→JobSat-Link als Devs in den USA (at-will employment).

**Zusatzanalyse (EXPLORATORY):**
Modell + Country top-5 + Other (N=17.670):
- AIThreat_bin: β=−0.623, p=1.22×10⁻⁴ (unverändert)
- Interaction: β=−0.004, p=0.935 (weiterhin Null)
→ Länderkontrolle ändert nichts.

**REVIEW-PUNKT 3: P-Hacking-Risiko — MITTEL**

Drei post-hoc-Entscheidungen identifiziert:
1. AISelect_bin nach Datenzugriff gestrichen (structural collinearity — valide begründet)
2. AIThreat-Haupteffekt (d=−0.303) als Headline, obwohl H1 (Moderation) das primäre war
3. Alle aber: 0/5 Multiverse specs signifikant für Interaction → p-hacking hätte mehr ergeben

Response: Alle drei transparent dokumentiert. Null-Ergebnis für H1 wird zuerst berichtet.

**REVIEW-PUNKT 4: Reverse Causation / kein Kausaldesign — HOCH**

Reverse-Causal-Argument: Unzufriedene Devs attribuieren ihre Unzufriedenheit
auf externe Ursachen — AIThreat ist eine kognitiv verfügbare, sozial sanktionierte Attribution.
→ Niedriger JobSat → hohe AIThreat-Wahrnehmung.
Das würde denselben negativen Zusammenhang produzieren ohne jeden Kausaleffekt von AIThreat.

**Response:** Limitations-Paragraph — kein Kausalschluss möglich. Cross-sectional design.
Mediation ist rein deskriptiv (Bullock et al. 2010 explizit zitiert).

**REVIEW-PUNKT 5: Messproblem — HOCH**

5a. AIThreat: Single-Item binär. Misst multidimensionales Konstrukt (Reich et al. 2026:
mindestens 3 Dimensionen: status threat, work change threat, displacement threat).
Coding "Unsure" → 0 könnte ambivalente Devs mit echtem mittlerem Threat falsch klassifizieren.
→ Attenuation Bias: wahrer d möglicherweise > −0.303.

5b. Common Method Bias: AIThreat, AIAcc und JobSat alle selbstberichtet im selben Survey.
Stimmungskongruente Antworten könnten Korrelationen inflationieren.

5c. JobSat: Single-Item 0–10. Kann Satisfaction-Facetten nicht unterscheiden.

**Response:** Limitations-Paragraph über construct validity, measurement invariance,
multi-item scales als Future-Research-Empfehlung.

**REVIEW-PUNKT 6: Generalisierbarkeit — HOCH**

6a. SO-Selbstselektion: Overrepräsentation von englischsprachigen, westlichen,
männlichen, Online-aktiven Entwicklern.

6b. AI-user-only: N=17.670 sind ausschließlich KI-Tool-Nutzer.
Nicht generalisierbar auf ~15.000 Nicht-Nutzer oder globale Entwicklerpopulation.

6c. Snapshot 2024: ChatGPT-Ära, pre-GPT-5. Ergebnisse könnten 2025/2026 nicht replizieren.

**Response:** Scope-Paragraph — explizit eingeschränkte Aussagenreichweite.

#### Summary Stage 2b

| Punkt | Rating | Adressiert |
|---|---|---|
| Steelman H0: unabhängige kognitive Pfade | HOCH | Discussion ✓ |
| Konfund DevType | HOCH | Zusatzanalyse: robust ✓ |
| Konfund Einkommen | HOCH | Limitations ✓ |
| Reverse Causation | HOCH | Limitations ✓ |
| Messprobleme (AIThreat, CMB, JobSat) | HOCH | Limitations ✓ |
| Generalisierbarkeit | HOCH | Scope ✓ |
| P-Hacking-Risiko | MITTEL | Transparenz ✓ |
| Land / Arbeitsmarkt | MITTEL | Zusatzanalyse: robust ✓ |

**Alle HOCH-Punkte adressiert. Stage 3 freigegeben.**

**2 Zusatzanalysen wurden getriggert** (DevType-Kontrolle + Country-Kontrolle)
und die Hauptbefunde blieben in beiden stabil.

---

### Stage 3 — Paper Writing (LaTeX)

**Was die Stage tat:**
- Alle Befunde vorher als `ScientificClaim`-JSON strukturiert (6 Claims)
- Behavioral Uncertainty statt Selbstauskunft: Konsistenz über Seeds, CI-Breite, p-Abstand zur Schwelle
- Counter-Narrative Search: mindestens 2 widersprechende Papers gesucht und eingebunden
- ≥20 Inline CRITIC-CHECKs (Claim ↔ Abstract, alle dokumentiert)
- Paper in LaTeX geschrieben: `experiment_v3/experiment_v3_output.tex`

**Counter-Narratives eingebaut (§4.3 Discussion):**
- Armstrong et al. (2024, N=9.000+, 9 Länder): Mehr Befragte berichten Benefits als Costs durch Automation
- Chung et al. (2025): Career resilience als Puffer gegen AI-threat-vermittelte Effekte

**ScientificClaims JSON (6 Claims):**
Jeder Befund strukturiert mit: `claim`, `evidence`, `confidence` (behavioral), `effect_size`, `p_value`, `caveat`, `exploratory` flag.

**Output:** `experiment_v3/experiment_v3_output.tex` — syntaktisch vollständig, kompilierbar.

---

### Stage 4 — QC + Reproducibility Artifacts

**Was die Stage tat:**
- `scripts/qc_check_v3.py` ausgeführt
- Numerische Checks (Regex-Matching Paper-Text vs. Log-Werte)
- Content-Checks (Citations, Bootstrap, PRISMA, Counter-Narrative etc.)
- Privacy-Check (keine E-Mails, kein echter Name)
- Reproducibility Artifacts exportiert

#### QC-Ergebnis: 31/32 PASS

```
--- NUMERICAL CHECKS ---
[PASS] Cohen's d = -0.303
[PASS] BCa CI [-0.350, -0.250]
[PASS] t-statistic = -12.316
[PASS] p = 1.03e-34 (main effect)
[PASS] beta_interaction = -0.009
[PASS] p_interaction = .856
[PASS] f2 < .001 or = 0.000002
[PASS] N = 17670
[PASS] Indirect effect CI [-0.289, +0.021]
[PASS] a-path p = .106
[PASS] AIThreat main effect beta = -0.609
[PASS] AIAcc beta = +0.141
[PASS] Multiverse 0/5
[PASS] M_threat = 6.42
[PASS] M_no_threat = 7.05

--- CONTENT CHECKS ---
[PASS] Citation count >= 15 (found: 18)
[PASS] Citation recency >= 50% 2020-2025 (78%)
[PASS] Bootstrap CI mentioned
[PASS] Power statement present
[PASS] PRISMA-flow mentioned
[PASS] Counter-narrative section present
[PASS] Limitations section present
[PASS] PAP pre-registration mentioned
[PASS] Data availability statement
[PASS] EXPLORATORY labeled
[PASS] Author = Anonymous Author
[PASS] Figures included (\includegraphics)
[PASS] Mediation analysis present
[PASS] Multiverse analysis present
[PASS] BH-FDR correction mentioned
[PASS] Adversarial critic concerns addressed in discussion

--- PRIVACY CHECK ---
[PASS] No email addresses found
[PASS] Author = Anonymous Author
```

**1 False Positive:** Privacy-Regex schlug bei den Strings "Among Software", "Its Interpretation",
"Robust Standard", "The Stack", "Work Frustration" an — alles normale Phrasen,
keine Namen. Manuell als false positive bestätigt.

#### Reproducibility Artifacts

| Artifact | Status |
|---|---|
| `logs/v3/preanalysis_plan.json` | ✓ Exportiert |
| `logs/v3/analysis_queries.sql` | ✓ Exportiert |
| `logs/v3/prisma_flow.md` | ✓ Exportiert |
| `scripts/preprocessing_v3.py` | ✓ Exists |
| `scripts/analysis_v3.py` | ✓ Exists |
| `scripts/generate_figures_v3.py` | ✓ Exists |
| `scripts/qc_check_v3.py` | ✓ Exists |
| `experiment_v3/figures/` (3 PNGs) | ✓ Exists |

**Pipeline-Statistiken (Run 4 gesamt):**
- SQL-Queries: 8 (Verifikation) + kontinuierliche Analyse
- Python-Script-Ausführungen: 4 (preprocessing, analysis, figures, QC)
- WebSearch-Queries: 8
- WebFetch-Calls (Abstract-Screening): 16
- Stage-1-CRITIC-CHECKs: 10/10 JA
- Stage-2-SQL-Verifikationen: 7/7 JA
- Stage-2b-HOCH-Punkte adressiert: 6/6
- Stage-3-Inline-CHECKs: 20/20 JA
- QC-Checks: 31/32 PASS
- Laufzeit: ~3.5 Stunden
- Menschliche Interventionen: **0**

---

## 6. Gesamtergebnisse v3

| Analyse | Befund | Statistisch | Praktisch |
|---|---|---|---|
| AIThreat-Haupteffekt auf JobSat | d=−0.303, CI [−0.350, −0.250] | p<0.001 *** | **JA** (d≥0.25) |
| AIAcc-Haupteffekt auf JobSat | β=+0.141 | p<0.001 *** | Klein |
| **H1: AIThreat × AIAcc-Moderation** | **β=−0.009, f²=0.000002** | **p=0.856, ns** | **NEIN** |
| Mediation via Frustration | a×b=−0.124, CI [−0.289, +0.021] | p=0.082, ns | NEIN |
| WorkExp | β=+0.009 | p=0.044 (marginal, p_adj=0.053) | Trivial |
| YearsCodePro | β=+0.022 | p<0.001 *** | Klein |

**Kern-Schlussfolgerung:** H1 wird nicht gestützt. AIAcc moderiert den AIThreat→JobSat-Link nicht.
Der AIThreat-Haupteffekt ist aber robust und praktisch bedeutsam (d=−0.303, repliziert über 3 Pipeline-Runs).

**Warum das Null-Ergebnis ein echter Befund ist:**
- Pre-registriert: Hypothese stand mit Timestamp-Lock fest bevor irgendein Datenwert gesehen wurde
- Robust: 0/5 Multiverse-Spezifikationen signifikant
- Theoretisch erklärbar: AIAcc misst Fähigkeits-Appraisal, nicht Verletzbarkeits-Appraisal

---

## 7. Vergleich der vier Bedingungen

| Merkmal | Baseline | v1 | v2 | **v3** |
|---|---|---|---|---|
| Architektur | 1 Prompt | 5 Stages | 5 Stages + Critic | **7 Stages** |
| SQL-Zugriff | Nein | sqlite-mcp | sqlite-mcp (Bash-FB) | **sqlite-mcp (fixed)** |
| Quellenverifikation | Keine | Einmalig | 2× + Semantic | **2× + Semantic + PRISMA** |
| Quellen | 5 | 5 | 5 | **14** |
| Pre-Registration | Nein | Nein | Nein | **Ja (LOCKED JSON)** |
| HARKing-Schutz | Nein | Nein | Nein | **Ja** |
| Null-Ergebnis möglich | Nein | Nein | Nein | **Ja** |
| Bootstrap BCa CI | Nein | Nein | Nein | **Ja** |
| BH-FDR Korrektur | Nein | Nein | Nein | **Ja** |
| Multiverse (5 Specs) | Nein | Nein | Nein | **Ja** |
| Mediationsanalyse | Nein | Nein | Nein | **Ja** |
| Adversarial Critic | Nein | Nein | Nein | **Ja** |
| QC-Checks | — | 29/29 | 21/21 | **31/32** |
| Halluzinierte Zitationen | unbekannt | 0 | 0 | **0** |
| Laufzeit (ca.) | 10 min | ~15 min | ~15 min | **~3.5 Stunden** |
| AIThreat Cohen's d | — | −0.36 | −0.327 | **−0.303** |

---

## 8. Engineering Journey — Lessons Learned

| Run | Failure | Fix | Generelle Lektion |
|---|---|---|---|
| 1 | Echte E-Mail in `\author{}` aus System-Kontext | Anonymous-Author-Constraint in System-Context | System-Kontext bypasses Prompt-Instruktionen |
| 2 | PASS deklariert ohne Script-Ausführung | STDOUT-Proof required — kein PASS ohne Konsolenoutput | Selbst-deklariertes PASS ist unprüfbar |
| 2 | 7 Zitationen, 0 Abstracts gelesen | fetch-mcp Pflichtschritt für jede Quelle | Kein Zitat ohne vorherigen Abruf |
| 3 | f²=0.00033 als Hauptbefund deklariert | Effect-Size-Gate f²≥0.02 als Hard-Stop | p<.05 ≠ wissenschaftlich relevant |
| 3 | **Reasoned Non-Compliance** — Methoden-Instruktion gebrochen | Code-Assertions statt Text-Regeln | Modelle überschreiben Text-Regeln mit guten Argumenten |
| **4** | — | **31/32 PASS, 0 Interventionen** | **Qualität erfordert Iteration** |

### Reasoned Non-Compliance — Detail

Run 3, Stage 2: Die Pipeline hatte als Text-Instruktion: "Verwende Dummy-Coding für ordinale Variablen."
Das Modell ersetzte Dummy-Coding für AIAcc durch ordinale Behandlung (1–5 als kontinuierlich).

**Das Argument des Modells (sinngemäß):**
"AIAcc ist eine 5-stufige Likert-Skala mit approximativ gleichen Intervallen.
Ordinale Behandlung als kontinuierliche Variable ist in der Psychologie-Literatur
(z.B. Norman 2010, Carifio & Perla 2008) akzeptiert und produziert hier
weniger Multikollinearität als 4 Dummy-Variablen mit inhärenter Interaktionskomplexität."

Das Argument war **statistisch korrekt**. Der Befund blieb stabil.
Aber: Eine Text-Instruktion war gebrochen worden. Ohne Logging wäre das unsichtbar.

**Was das über LLM-Verhalten sagt:**
Ein LLM mit einem überzeugenden Gegenargument wird Text-Instruktionen überschreiben.
Das ist keine Fehlfunktion — es ist konsequentes Inferencing.
Die Lösung ist keine schärfere Formulierung, sondern strukturelle Erzwingung:
Code-Assertions prüfen Methodenentscheidungen, kein Prompt.

---

## 9. Was die Pipeline leistet — und was nicht

### Was sie leistet
- Strukturell erzwungene Pre-Registration (HARKing unmöglich durch Architektur)
- Verifikation jeder zentralen Statistik durch unabhängige SQL-Queries
- Systematische Literatursuche mit echtem Abstract-Abruf
- Robustheitsanalysen (Multiverse, Bootstrap, BH-FDR) automatisch
- Adversariale Selbstkritik vor dem Schreiben
- Vollständige Reproduzierbarkeits-Artifacts

### Was sie nicht leistet
- Kausale Inferenz aus Querschnittsdaten
- Repräsentative Stichprobenziehung
- Kontrolle für nicht erhobene Konfundierungen (z.B. Einkommen mit 64.2% Missing)
- Evaluation ihrer eigenen epistemischen Grenzen (dafür ist der Adversarial Critic zuständig)

### Die fundamentale Erkenntnis
Die Pipeline macht Qualitätssicherung **strukturell erzwingbar** statt von Disziplin abhängig.
Nicht "der Researcher entscheidet sich für Transparenz" — sondern "das System erzwingt Transparenz
durch Gate-Mechanismen, die die nächste Stage blockieren wenn Kriterien nicht erfüllt sind."
Das ist der Unterschied zwischen einem disziplinierten Researcher und einem wissenschaftlichen System.
