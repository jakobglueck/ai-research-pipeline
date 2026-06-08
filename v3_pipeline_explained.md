# Pipeline v3 — Vollständige Erklärung
## Was jede Stage macht, warum, und was sie produziert

---

## Das Grundprinzip

Die Pipeline v3 ist eine Abfolge von 7 Stufen (Stages) die ein großes
Sprachmodell (Claude Sonnet 4.6) sequenziell abarbeitet — ohne menschlichen
Eingriff zwischen den Stufen. Jede Stage hat genau eine Aufgabe, produziert
einen dokumentierten Output, und übergibt dann an die nächste Stage.

Das zentrale Design-Prinzip: **Trennung von Denken und Testen.**
Stage 0b denkt die Hypothese aus — bevor die Daten gesehen wurden.
Stages 1–4 testen sie so rigoros wie möglich.

---

## Stage 0 — Setup & Datenbank

### Was passiert
Der Agent prüft ob die Infrastruktur bereit ist:
- Verzeichnisse anlegen (`experiment_v3/figures/`, `logs/v3/`)
- Prüfen ob `db/survey.db` existiert (kein Re-Import — DB kommt aus v1)
- Schema lesen: Spaltennamen, Datentypen, Zeilenanzahl
- Mögliche Zielvariablen und Mediator-Variablen identifizieren

### Warum dieser Stage existiert
Vor dem eigentlichen Denken muss sichergestellt sein dass die Daten
vorhanden und intakt sind. Außerdem braucht Stage 0b die Spaltennamen
(aber nicht den Inhalt) um eine theoretisch fundierte Hypothese zu formulieren.

### Wichtige Design-Entscheidung
Die Datenbank heißt `survey.db` mit der Tabelle `survey` — bewusst generisch,
nicht "stackoverflow.db". Damit ist die Pipeline auf jeden tabellarischen
Surveydatensatz übertragbar ohne eine einzige Zeile Code zu ändern.

### Output
`logs/v3/stage_0_log.md` — DB-Status, Schema, identifizierte Variablen

---

## Stage 0b — Pre-Analysis Plan (PAP)

### Was passiert
Der Agent formuliert die vollständige Forschungsstrategie — **bevor er auch
nur eine einzige inhaltliche SQL-Query ausführt.**

Konkret:
1. Primäre Forschungsfrage + H0/H1 (aus Theorie, nicht aus Daten)
2. Erwartete Richtung des Effekts mit theoretischer Begründung
3. Mediationshypothese: Gibt es eine Zwischenvariable die den Effekt erklärt?
4. Geplante Methode, Kovariaten, Missing-Data-Strategie
5. **Novelty-Check:** Wie ähnlich ist die Frage zu v1/v2? Bei >70% Ähnlichkeit
   → neue Frage formulieren
6. **Text-DAG:** Kausale Annahmen explizit als Pfeildiagramm
7. Exploratorische Analysen klar als solche markieren

Der Plan wird als `preanalysis_plan.json` gespeichert und ist ab diesem
Moment **locked** — jede Abweichung davon muss im Paper als EXPLORATORY
markiert werden.

### Warum dieser Stage der wichtigste ist
**HARKing** (Hypothesizing After Results Known) ist das größte methodische
Problem in der empirischen Forschung: Man schaut in die Daten, findet etwas
Interessantes, und tut dann so als hätte man genau das vorhergesagt. Das
sieht aus wie Bestätigung, ist aber eigentlich Entdeckung — was die
Wahrscheinlichkeit falsch-positiver Ergebnisse massiv erhöht.

Stage 0b macht HARKing **strukturell unmöglich**: Die Hypothese existiert als
Datei mit Timestamp bevor irgendein Dateninhalt gesehen wurde.

**Wissenschaftliche Basis:** Journal of Political Economy 2024 — nur
Pre-Analysis Plans (nicht nur Pre-Registration) reduzieren p-Hacking
nachweisbar. Registered Reports produzieren 44% positive Ergebnisse vs.
96% bei Standard-Papers — weil Null-Ergebnisse nicht mehr versteckt werden.

### In v3 passierte das
Der Agent formulierte eigenständig: *"Moderiert Vertrauen in KI-Genauigkeit
(AIAcc) den negativen Zusammenhang zwischen AIThreat und JobSat?"*
Theoretische Basis: Lazarus & Folkman 1984 Cognitive Threat Appraisal Theory.
Novelty-Score vs. v1: NIEDRIG. Novelty-Score vs. v2: NIEDRIG. ✓

### Output
`logs/v3/preanalysis_plan.json` — locked JSON mit allen Spezifikationen
`logs/v3/stage_0b_log.md` — Begründungen für alle Entscheidungen

---

## Stage 1 — Exploration & PRISMA-Literatursuche

### Was passiert
Zwei parallele Aufgaben:

**Aufgabe A — Effect-Size-Gate:**
Der Agent prüft ob die im PAP spezifizierte Hypothese den Gate besteht:
- Cohen's d ≥ 0.25 ODER Eta² ≥ 0.01 ODER |r| ≥ 0.15
- Falls nicht: Null-Ergebnis dokumentieren, Alternative aus PAP wählen
- In v3: d = −0.295 → Gate bestanden ✓

**Aufgabe B — PRISMA-lite Literatursuche (systematisch):**
1. Suchstrings definieren und loggen (z.B. "AI threat AND job satisfaction")
2. Mindestens 8 Web-Searches mit verschiedenen Suchstrings
3. 30+ Kandidaten identifizieren
4. Für jeden Kandidaten: Abstract via Fetch-MCP abrufen
5. Screening: INCLUDE oder EXCLUDE mit Begründung
6. PRISMA-Flow dokumentieren: N_identified → N_screened → N_included
7. Datenextraktion: Stichprobe, Methode, Hauptbefund, Effektgröße

**Prompt Injection Sanitizer (neu in v3):**
Alle abgerufenen Inhalte werden auf eingebettete KI-Instruktionen geprüft
bevor sie weiterverarbeitet werden. Schutz gegen manipulierte Webinhalte.

**CRITIC-CHECK:**
Jede final ausgewählte Quelle wird ein zweites Mal abgerufen.
Explizite Prüfung: *"Behauptung im Log vs. was der Abstract wirklich sagt — JA/NEIN"*
Bei NEIN: Quelle raus, Ersatz suchen.

### Warum PRISMA statt einfach 5 Quellen suchen
5 Quellen (wie in v1/v2) ist für ein empirisches Paper über ein bekanntes
Thema zu wenig — kein Journal würde das akzeptieren. PRISMA erzwingt einen
dokumentierten, reproduzierbaren Suchprozess:
- Jeder kann nachvollziehen welche Papers gefunden und warum ausgeschlossen wurden
- Kein Cherry-Picking von Quellen die nur die eigene Hypothese stützen
- Die Literaturbasis wird zu einem wissenschaftlichen Beitrag, nicht nur Dekoration

**In v3:** 36 Kandidaten → 33 gescreent → 14 eingeschlossen

### Output
`logs/v3/stage_1_log.md` — PRISMA-Flow, alle 30+ Kandidaten, Datenextraktionstabelle,
CRITIC-CHECK-Tabelle

---

## Stage 2 — Statistische Analyse (erweitert)

### Was passiert
Der Agent schreibt und führt Python-Scripts aus. Alle Scripts mit `_v3`-Suffix
damit v1/v2-Scripts nicht überschrieben werden.

**Schritt 1 — CoT Decision Pivots:**
Vor jeder statistischen Schlussfolgerung muss der Agent explizit 4 Checkpoints
als Scratchpad im Log dokumentieren:
```
CHECKPOINT 1: H0 lautet: [...]
CHECKPOINT 2: N = [...], Power-Schwelle erfüllt: JA/NEIN
CHECKPOINT 3: p_roh = [...], nach BH-FDR: p_adj = [...]
CHECKPOINT 4: Effektgröße = [...], Richtung entspricht H1: JA/NEIN
```
Das verhindert das häufigste LLM-Fehler: stilles Vorzeichen-Wechseln und
implizites Überspringen von Korrekturen.

**Schritt 2 — Standard-Analyse:**
- Missing Data Analyse (welche Variablen fehlen wie oft, warum)
- Preprocessing: Dummy-Coding, Skalierungen, begründet und dokumentiert
- OLS Multiple Regression mit VIF-Check
- Cohen's d für den Haupteffekt

**Schritt 3 — Bootstrap BCa Konfidenzintervalle:**
Statt: *"d = 0.303, das stimmt schon so"*
Jetzt: *"d = −0.303, 95% BCa CI [−0.350, −0.250]"*
1.000 Resampling-Iterationen, Seed festgelegt für Reproduzierbarkeit.
Zeigt nicht nur den Punktschätzer sondern die Unsicherheit darum.

**Schritt 4 — BH-FDR Korrektur:**
Wenn mehrere Hypothesen getestet werden steigt die Chance zufällig etwas
zu finden. BH-FDR (Benjamini-Hochberg) korrigiert alle p-Werte gemeinsam
so dass maximal 5% der als signifikant deklarierten Ergebnisse falsch-positiv sind.

**Schritt 5 — Mediationsanalyse:**
Test ob ein Mediator (M) den Effekt von X auf Y erklärt (X → M → Y).
Via `pingouin.mediation_analysis()`, bootstrapped, 3 Seeds für Self-Consistency.
In v3: AIThreat → Frustration → JobSat → Null-Ergebnis

**Schritt 6 — Multiverse-Analyse (5 Spezifikationen):**
Das Hauptmodell in 5 vernünftigen Varianten:
1. Hauptmodell (PAP-konform)
2. AIThreat ordinale (3-stufig statt binär)
3. AIAcc binär (trust vs. distrust statt 5-Stufen)
4. HC3 Robust Standard Errors
5. Mean-centered predictors

Wenn das Ergebnis in 5/5 Specs konsistent ist → robuster Befund.
In v3: Null-Moderation in 0/5 Specs signifikant → sehr klares Null-Ergebnis.

**Schritt 7 — CRITIC-CHECK (SQL-Verifikation):**
Jede Kernzahl aus dem Python-Script wird unabhängig via sqlite3 Bash nachgerechnet:
```
Kennzahl:          Cohen's d für AIThreat
Script-Ergebnis:   −0.303
SQL-Verifikation:  Mittelwerte aus DB + manuelle Pooled-SD-Formel = −0.303
Übereinstimmung:   JA (Toleranz ±0.001)
```
Keine einzige Zahl gelangt ins Paper ohne unabhängige SQL-Bestätigung.

### Warum so viel Statistik
Jede Methode löst ein spezifisches Problem:

| Methode | Problem das sie löst |
|---|---|
| Bootstrap CI | "Stimmt der Punkt-Schätzer wirklich?" |
| BH-FDR | "Haben wir durch viele Tests Glück gehabt?" |
| Mediation | "Warum gibt es den Effekt?" |
| Multiverse | "Gilt das nur für diese eine Modellwahl?" |
| CoT Pivots | "Hat das LLM still Vorzeichen gewechselt?" |
| SQL-Verifikation | "Sind die Zahlen überhaupt korrekt?" |

### Output
`logs/v3/stage_2_log.md` — alle Script-Outputs, SQL-Verifikationen,
Multiverse-Tabelle, Bootstrap-CIs, Self-Consistency-Check

---

## Stage 2b — Adversarial Critic

### Was passiert
Der Agent wechselt die Rolle: er ist jetzt ein feindlicher Gutachter eines
Top-Journals. Sein Ziel ist es das Paper zu **rejecten** wenn er irgendeinen
validen Einwand findet.

6 Pflicht-Review-Punkte:

**1. Steelman der Nullhypothese**
Was ist das überzeugendste Argument dafür dass H1 falsch ist?
In v3: "Der Effekt könnte vollständig durch ungemessene Jobinsicherheit erklärt
werden — AIThreat misst möglicherweise nur einen Proxy." → HOCH

**2. Nicht kontrollierte Konfundierungen**
3 plausible Drittvariablen die sowohl Prädiktor als auch Outcome beeinflussen.
In v3: Jobinsicherheit, Negativer Affekt, Gehalt (nicht kontrollierbar — 64% missing)

**3. P-Hacking-Risiko**
Hat die Pipeline trotz PAP Entscheidungen getroffen die das Ergebnis
günstiger machen? In v3: AISelect_bin wegen Konstanz gedroppt → korrekt und
transparent dokumentiert → NIEDRIG

**4. Fehlende Vergleichsgruppe**
Fehlt eine natürliche Kontrollgruppe? In v3: Keine Nicht-KI-Nutzer im Sample
(AIAcc-Filter schließt sie aus) → HOCH

**5. Messprobleme**
AIThreat = ein einziges Ja/Nein-Item. Common Method Bias (alle Variablen
selbstberichtet im selben Survey). → HOCH

**6. Generalisierbarkeit**
Stack Overflow Survey: überrepräsentiert westliche, englischsprachige,
männliche Entwickler. Sample nach Listwise Deletion: nur aktive KI-Tool-Nutzer.

**Pflicht:** Alle HOCH-bewerteten Punkte müssen vor Stage 3 adressiert werden —
entweder durch eine Zusatzanalyse oder einen vorbereiteten Limitations-Absatz.

In v3 wurden 2 Zusatzanalysen durchgeführt:
- DevType-Kontrolle: AIThreat-Effekt bleibt β ≈ −0.61, p < .001 ✓
- Country-Kontrolle: AIThreat-Effekt bleibt stabil ✓

### Warum dieser Stage
**BadScientist (2025):** LLMs die ihre eigene Arbeit reviewen übersehen
52–82% methodischer Schwächen. Der aktuelle Critic-Check (Stage 2) prüft
nur Zahlen — korrekt oder nicht. Stage 2b prüft **Konzepte** — ist die
Forschungsfrage überhaupt so beantwortbar wie behauptet?

**Anti-Consensus-Bias:** Post-RLHF-Modelle tendieren zu konsens-klingenden
Schlussfolgerungen. Stage 2b enthält explizit die Instruktion: schärfer
kritisieren als normal, dann zurückkalibrieren.

### Output
`logs/v3/adversarial_critic_log.md` — alle 6 Review-Punkte mit Bewertung,
Reaktionen, durchgeführte Zusatzanalysen

---

## Stage 3 — Paper-Schreiben

### Was passiert

**Schritt 1 — ScientificClaim JSON:**
Vor dem Schreiben wird jeder empirische Befund als strukturiertes JSON erfasst:
```json
{
  "claim_id": "C1",
  "claim": "AIThreat predicts lower JobSat",
  "evidence": "d = −0.303, 95% BCa CI [−0.350, −0.250]",
  "confidence": "high — consistent across 5 specs, 3-seed stable",
  "source": "logs/v3/stage_2_log.md, section Cohen's d",
  "effect_size": -0.303,
  "p_value": 1.03e-34,
  "caveat": "cross-sectional, no causality",
  "exploratory": false
}
```
Jeder Satz im Paper ist mit einer Claim-ID verknüpft. Das macht Verifikation
präzise — nicht "stimmt das ungefähr" sondern "ist Claim C1 belegt?"

**Schritt 2 — Counter-Narrative Search:**
Aktive Suche nach Papers die den Hauptbefund **widerlegen oder relativieren**:
- Search: "AI job threat no significant effect"
- Search: "AI automation positive effect job satisfaction"
- Mindestens 2 widersprechende Papers finden, im Discussion-Abschnitt
  "Alternative Explanations" fair zusammenfassen und erklären warum der
  eigene Befund trotzdem gilt.

**Schritt 3 — Inline CRITIC-CHECK:**
Während des Schreibens, vor jedem Satz mit einer Citation:
```
Claim: "AI anxiety directly reduces life satisfaction through negative affect"
Quelle: Zhao et al. 2025, URL
Abstract sagt: [direkte Zusammenfassung]
Korrekt belegt: JA
```
Mindestens 15 dieser Checks müssen dokumentiert sein.
Behavioral Uncertainty statt Selbstauskunft: Konfidenz wird nicht als
"ich bin mir sicher" berichtet sondern durch: Konsistenz über Seeds,
CI-Breite, Abstand des p-Werts von 0.05.

**Schritt 4 — LaTeX-Paper schreiben:**
6 Seiten, 11pt, 2.5cm Margins. Struktur:
1. Abstract (150 Wörter, Hauptbefund und Null-Ergebnis explizit)
2. Introduction (Theorie, PAP-Verweis, Forschungslücke)
3. Methodology (PRISMA-Flow, Operationalisierungen, Missing Data, Statistik)
4. Results (CONFIRMATORY und EXPLORATORY getrennt, alle Zahlen aus Logs)
5. Discussion (Counter-Narratives, Adversarial Critic Einwände, Limitationen)
6. References (≥15 Quellen, ≥50% aus 2020–2025)

### Warum ScientificClaim JSON
Ohne Struktur prüft der Critic: "Klingt das plausibel?" — das ist subjektiv.
Mit JSON prüft der Critic: "Ist Claim C1.evidence in logs/v3/stage_2_log.md
section Cohen's d vorhanden?" — das ist objektiv verifizierbar.
*Basis: PaperTrail (arxiv:2602.21045)*

### Output
`experiment_v3/experiment_v3_output.tex` — das fertige Paper
`logs/v3/scientific_claims.json` — alle Befunde strukturiert
`logs/v3/stage_3_log.md` — Zahlenquellen, Counter-Narratives, alle Checks

---

## Stage 4 — Export & Qualitätskontrolle

### Was passiert

**Schritt 1 — Automatisierter QC-Check:**
`scripts/qc_check_v3.py` liest das fertige Paper und den Stage-2-Log,
prüft via Regex ob alle zentralen Zahlen übereinstimmen.

Zusätzlich neue Checks in v3:
- Citation Count ≥ 15?
- ≥ 50% Quellen aus 2020–2025?
- Bootstrap-CI im Paper erwähnt?
- PRISMA-Flow im Methodenteil?
- PAP-Verweis vorhanden?
- Counter-Narrative Abschnitt vorhanden?
- Power Statement vorhanden?
- Data Availability Statement vorhanden?
- Exploratorische Analysen als EXPLORATORY markiert?

In v3: **31/32 Checks PASS.**

**Schritt 2 — Reproducibility Artifacts:**
Exportiert für maximale Reproduzierbarkeit:
- `logs/v3/analysis_queries.sql` — alle SQL-Queries aus Stage 2
- `logs/v3/prisma_flow.md` — PRISMA-Suche als eigenständiges Dokument
- `logs/v3/preanalysis_plan.json` — bereits aus Stage 0b vorhanden

**Schritt 3 — LaTeX kompilieren:**
```bash
tectonic experiment_v3/experiment_v3_output.tex
```
→ `experiment_v3_output.pdf` (272 KB)

### Warum Reproducibility Artifacts
**REPRO-Bench (ACL 2025):** Nur 21.4% aller KI-Forschungsassistenten können
korrekt beurteilen ob ein Paper reproduzierbar ist. Die drei Hauptfaktoren
für Reproduzierbarkeit: (1) Daten verfügbar, (2) Code verfügbar,
(3) Analyseschritte eindeutig dokumentiert. v3 erfüllt alle drei.

### Output
`experiment_v3/experiment_v3_output.pdf` — finales Paper
`logs/v3/stage_4_log.md` — vollständiger QC-STDOUT, alle Check-Ergebnisse
`logs/v3/experiment_v3_summary.md` — Pipeline-Statistik, Qualitäts-Selbstcheck

---

## Gesamtbild — Wie die Stages zusammenhängen

```
Stage 0        Stage 0b       Stage 1         Stage 2        Stage 2b
Infrastruktur  Hypothese      Literatur +     Statistik +    Feindlicher
prüfen    →    LOCKED    →    Effect-Size  →  Verifikation → Gutachter
               (PAP)          Gate            (SQL-Check)    (6 Punkte)
                                                                  ↓
                                              Stage 4        Stage 3
                                              QC + PDF   ←   Paper
                                              kompilieren    schreiben
```

Jede Stage baut auf der vorherigen auf:
- Stage 0b kann nur sinnvoll arbeiten weil Stage 0 das Schema bereitgestellt hat
- Stage 1 prüft die in Stage 0b gesperrte Hypothese gegen echte Daten
- Stage 2 analysiert was Stage 1 gefunden hat
- Stage 2b reviewt was Stage 2 produziert hat
- Stage 3 schreibt auf Basis von Stage 2 + Stage 2b
- Stage 4 verifiziert was Stage 3 geschrieben hat

---

## Was v3 im Vergleich zu v1 wirklich anders macht

| Was v1 tut | Was v3 stattdessen tut | Warum besser |
|---|---|---|
| Hypothese nach Datensichtung | Hypothese vor Datensichtung (PAP) | Kein HARKing möglich |
| 5 Quellen, keine Strategie | 14 Quellen, PRISMA-Protokoll | Reproduzierbare Literaturbasis |
| Effektgröße als Punkt-Schätzer | + Bootstrap BCa CI | Unsicherheit quantifiziert |
| Nur ein Modell | 5 Spezifikationen (Multiverse) | Robustheit nachgewiesen |
| Keine Mediationsanalyse | Bootstrapped Mediation (pingouin) | "Warum?" testbar |
| Critic prüft nur Zahlen | Adversarial Critic prüft Konzepte | Konzeptuelle Fehler gefunden |
| Keine Counter-Narratives | 2 widersprechende Papers adressiert | Wissenschaftlich ausgewogene Diskussion |
| Keine Reproducibility Artifacts | SQL + PRISMA + PAP exportiert | Jeder kann nachrechnen |

---

## Das Ergebnis von v3

**Forschungsfrage (pre-registered):**
Moderiert Vertrauen in KI-Genauigkeit (AIAcc) den negativen Zusammenhang
zwischen KI-Jobbedrohung (AIThreat) und Jobzufriedenheit (JobSat)?

**Antwort:**
- Moderation: **NULL** — β = −0.009, p = .856, f² < .001, 0/5 Multiverse-Specs
- AIThreat Haupteffekt: **d = −0.303**, 95% BCa CI [−0.350, −0.250] — robust
- Mediation via Frustration: **NULL** — CI [−0.289, +0.021] enthält 0

**Was das bedeutet:**
Das Null-Ergebnis ist wissenschaftlich wertvoll — weil es pre-registriert ist.
Es zeigt: AIAcc (Vertrauen in KI-Output) moderiert die Beziehung nicht, weil
es das falsche Konstrukt misst. Der Theoretical Insight: Für Threat Appraisal
braucht es *perceived replaceability*, nicht nur *AI accuracy trust*.

Der AIThreat-Haupteffekt (d ≈ −0.30) ist jetzt dreifach über unabhängige
Pipeline-Runs repliziert — das ist das stärkste Ergebnis des gesamten Projekts.
