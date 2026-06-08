# Methodenvergleich: Vier Bedingungen des autonomen Forschungspipelines

**Datensatz (alle vier Bedingungen):** Stack Overflow Developer Survey 2024 (N = 65.437)  
**Modell (alle vier Bedingungen):** Claude Sonnet 4.6  
**Menschliche Eingriffe:** 0 pro Run  

---

## Bedingung A — Baseline (Single-Prompt)

### Was
Ein einziger Prompt ohne Werkzeuge, ohne Struktur. Das Modell bekommt den
Auftrag: Finde die CSV, formuliere selbst eine Forschungsfrage, analysiere die
Daten, schreibe ein 6-seitiges wissenschaftliches Paper. Keine Stages, kein
SQL-Zugriff, kein Web-Zugriff, keine Verifikationsschritte.

### Warum diese Bedingung
Sie misst die absolute Untergrenze: Was leistet ein unstrukturierter
LLM-Einsatz? Alle anderen Bedingungen werden gegen diese verglichen.

### Was passierte
Das Modell wählte eigenständig eine Forschungsfrage
(*Predicts professional coding experience distrust in AI accuracy?*),
schrieb ein kohärentes 6-seitiges Paper mit 5 Quellen und führte
Kruskal-Wallis + Spearman-Korrelation durch.

**Ergebnis:** r_s = 0.10 — statistisch signifikant bei N=31.025,
aber praktisch bedeutungslos (kleiner Effekt).

### Schwachstellen
- Kein Werkzeugzugriff → alle Zahlen potenziell halluziniert
- Quellen nie verifiziert (könnten erfunden sein)
- Kein Effect-Size-Gate → schwacher Effekt landet trotzdem im Paper
- Kein strukturiertes Missing-Data-Handling
- Keine Limitations-Sektion

### Output
`baseline/baseline_output.tex` · `logs/baseline_log.md`

---

## Bedingung B — Pipeline v1 (5-Stage + MCP)

### Was
Eine 5-stufige Instruktionskette die Claude Code sequenziell abarbeitet:
Stage 0 (Setup + DB-Import), Stage 1 (Exploration + Forschungsfrage +
Literatursuche), Stage 2 (Statistische Analyse), Stage 3 (Paper-Schreiben),
Stage 4 (QC + LaTeX-Kompilierung). Zwei MCP-Tools:
- **SQLite-MCP** — strukturierter SQL-Zugriff auf die Survey-Datenbank
- **Fetch-MCP** — Live-Webzugriff für Literatur und Quellen-Verifikation

### Warum diese Bedingung
Sie misst den Mehrwert von Struktur und Werkzeugzugriff gegenüber dem
Single-Prompt. Die explizite Stufentrennung verhindert dass das Modell
Exploration und Schreiben vermischt.

### Was passierte
Das Modell fand eigenständig die Forschungsfrage *"Fear Over Pay"* — 
KI-Jobbedrohung ist stärkerer Prädiktor für Jobzufriedenheit als Gehalt.
Vier Runs wurden dokumentiert, jeder Run legte einen Prompt-Engineering-Fehler
offen der iterativ behoben wurde. Das finale Paper bestand 29/29 QC-Checks.

**Ergebnis:** Cohen's d = −0.36 (AIThreat → JobSat),
standardized β = −0.111 (stärker als Gehalt), 0 halluzinierte Zitationen.

### Verbesserungen gegenüber Baseline
- Alle Zahlen direkt aus SQLite-DB berechnet und belegbar
- Jede Quelle per Fetch-MCP abgerufen bevor sie ins Paper kommt
- Effect-Size-Gate (d ≥ 0.25) verhindert triviale Forschungsfragen
- VIF-Check, ΔR²-Berechnung, Praktische-Signifikanz-Pflichtinterpretation
- 29/29 automatisierte QC-Checks (Regex-Matching Paper vs. Log)

### Schwachstellen
- Nur 5 Quellen, keine systematische Suchstrategie
- Keine Pre-Registration → Hypothese nach Datensichtung (strukturelles HARKing)
- Keine Bootstrap-CIs, kein Multiverse, keine Mediationsanalyse
- Quellen einmalig abgerufen, keine semantische Claim-Verifikation

### Output
`experiment/experiment_output.tex` · `logs/stage_*_log.md`

---

## Bedingung C — Pipeline v2 (5-Stage + Critic-Loops)

### Was
Identische 5-Stage-Architektur wie v1, aber mit eingebetteten
**Critic-Loops** in den Stages 1–3:

- **Stage 1 Critic:** Jede Quelle wird nach der Literatursuche ein zweites
  Mal per Fetch-MCP abgerufen. Für jede Quelle wird explizit dokumentiert:
  *Behauptung im Log vs. Abstract-Inhalt — Match: JA/NEIN.* Bei NEIN wird
  die Quelle verworfen und ersetzt.
- **Stage 2 Critic:** Jede Kernzahl (Cohen's d, β, p-Werte, R²) wird
  unabhängig von den Python-Scripts via sqlite3-Bash nachgerechnet und
  verglichen (Toleranz ±0.001). Diskrepanzen müssen erklärt und behoben werden.
- **Stage 3 Critic (inline):** Während des Paper-Schreibens wird vor jedem
  Satz mit einer Citation die URL erneut abgerufen und der Claim gegen den
  Abstract-Text geprüft.

### Warum diese Bedingung
Sie misst den Mehrwert interner Verifikationsschleifen. Die Kernfrage: Fängt
ein Critic-Loop innerhalb derselben Pipeline reale Fehler, oder ist er reine
Formalie? (Antwort: 3 reale Korrekturen in Stage 1, 2 und 3.)

### Was passierte
Neue Forschungsfrage: *"Perception Over Adoption"* — AIThreat stärker als
tatsächliche KI-Tool-Adoption (AISelect) für Jobzufriedenheit.
Der Critic korrigierte: zwei paywallgeblockte Nature-Quellen (→ PMC-Alternativen),
einen Multikollinearitätsfehler im Regressionsmodell (fehlende Referenzkategorie),
eine zu starke Claim-Formulierung in Stage 3 (semantisch abgeschwächt).
Das finale Paper bestand 21/21 QC-Checks.

**Ergebnis:** Cohen's d = −0.327 (AIThreat, robust),
AISelect: d = 0.031, p = 0.14 (kein signifikanter Effekt).

### Verbesserungen gegenüber v1
- Verifikation zweistufig (einmalig fetch + Critic-Re-fetch)
- Statistische Zahlen unabhängig SQL-verifiziert
- Semantic Claim Verification (Claim ↔ Abstract, nicht nur URL-Liveness)
- PAP-Abweichung (AISelect_bin collinear) dokumentiert
- Neue Forschungsfrage (AIThreat vs. AISelect statt AIThreat vs. Gehalt)

### Schwachstellen
- Immer noch nur 5 Quellen, kein PRISMA
- Keine Pre-Registration → HARKing-Risiko bleibt
- SQLite-MCP lief nicht (Bash-Fallback) — relativer Pfad-Bug
- Kein Bootstrap-CI, kein Multiverse

### Output
`experiment_v2/experiment_v2_output.tex` · `logs/v2/stage_*_log.md`

---

## Bedingung D — Pipeline v3 (7-Stage + Pre-Registration + Erweiterte Statistik)

### Was
7-stufige Instruktionskette mit fundamentalen methodischen Erweiterungen
basierend auf der 2024–2026 Forschungsliteratur zu autonomen Research-Agents:

**Stage 0 — Setup:** DB-Check, Mediator-Variablen identifizieren

**Stage 0b — Pre-Analysis Plan (NEU, kein Datenzugriff erlaubt):**  
Vor jeder SQL-Query auf Inhaltsdaten wird ein vollständiger Pre-Analysis Plan
als JSON gespeichert und gelocked. Enthält: primäre Hypothese + Richtung,
Methode + Kovariaten, Mindest-Effektgröße, Mediationshypothese, Novelty-Score
(Ähnlichkeit zu v1/v2 quantifiziert), Text-DAG der Kausalannahmen.
Jede Abweichung in Stage 2 muss als EXPLORATORY markiert werden.
*(Basis: JPE 2024 — PAPs reduzieren p-Hacking, nur PAPs nicht nur Pre-Registration)*

**Stage 1 — PRISMA-lite Literatursuche:**  
30+ Kandidaten via 8 Web-Searches identifiziert, nach definierten
Inclusion/Exclusion-Kriterien auf 14 Papers gescreent. PRISMA-Flow dokumentiert
(N_identified=36, N_screened=33, N_included=14). Prompt Injection Sanitizer:
alle Fetch-Inhalte auf eingebettete KI-Instruktionen geprüft bevor Weiterverarbeitung.
*(Basis: PRISMA-trAIce, JMIR AI 2025)*

**Stage 2 — Erweiterte Analyse:**  
Zusätzlich zu OLS/VIF: Bootstrap BCa Konfidenzintervalle (n=1000, Seed 42/123/456
für Self-Consistency-Check), BH-FDR-Korrektur über alle Hypothesentests,
Mediationsanalyse via `pingouin.mediation_analysis()` (bootstrapped, 3-Seed-Konsistenz),
5-Spec Multiverse (verschiedene Operationalisierungen, HC3 Robust SE, Mean-Centering),
Breusch-Pagan Heteroskedastizitätstest, Sensitivitätsanalyse (Top/Bottom 1%
Ausreißer excludiert), CoT Decision Pivots (4 Pflicht-Checkpoints vor jeder
stat. Schlussfolgerung im Log).
*(Basis: APA 7th Ed., BCa Bootstrap ERIC, CISC ACL 2025, arxiv:2510.09312)*

**Stage 2b — Adversarial Critic (NEU):**  
Separate Agenten-Instanz mit explizit feindlicher Gutachter-Persona ("versuche
das Paper zu rejecten"). 6 Review-Punkte: Steelman der Nullhypothese, nicht
kontrollierte Konfundierungen (Liste 3 plausible), p-Hacking-Risiko,
fehlende Vergleichsgruppen, Messprobleme, Generalisierbarkeit. Alle
HOCH-bewerteten Punkte müssen vor Stage 3 adressiert werden (Zusatzanalysen
oder Discussion-Paragraphen). Anti-Consensus-Bias-Instruktion wegen Post-RLHF
Consensus Attractor.
*(Basis: BadScientist 2025: LLMs übersehen 52–82% eigener Fehler;
AgentReview EMNLP 2024; arxiv:2605.08956)*

**Stage 3 — Paper-Schreiben:**  
Vor dem Schreiben: alle Befunde als strukturiertes `ScientificClaim` JSON
erfasst (claim, evidence, confidence als behaviorales Signal, effect_size,
p_value, caveat, exploratory flag). Behavioral Uncertainty statt
Selbstauskunft des Modells (Konsistenz über Seeds, CI-Breite, p-Abstand
zur Schwelle). Counter-Narrative Search: mindestens 2 widersprechende Papers
gesucht und im Discussion-Abschnitt *"Alternative Explanations"* adressiert.
≥15 Inline Critic-Checks (Claim ↔ Abstract, alle dokumentiert).
*(Basis: PaperTrail arxiv:2602.21045; EviBound 2025; arxiv:2601.11956)*

**Stage 4 — Erweiterte QC + Reproducibility Artifacts:**  
Erweiterte QC-Checks: Citation Count ≥15, Recency ≥50% aus 2020–2025,
Bootstrap-CI im Paper vorhanden, PRISMA-Flow erwähnt, PAP-Verweis im
Methodenteil, Counter-Narrative-Abschnitt vorhanden. Export:
`analysis_queries.sql`, `prisma_flow.md`, `preanalysis_plan.json` als
standalone Reproducibility Artifacts.
*(Basis: REPRO-Bench ACL 2025)*

### Warum diese Bedingung
Sie misst den Mehrwert von Open-Science-Standards (Pre-Registration),
erweiterter Statistik (Bootstrap, Multiverse, Mediation) und strukturierter
Gegenkritik (Adversarial Critic) auf die Qualität des Outputs.
Die zentrale Frage: Produziert eine wissenschaftlich rigorosere Pipeline
auch wissenschaftlich stärkere Papers — und ist sie ehrlich genug um
Null-Ergebnisse korrekt zu berichten?

### Was passierte
Neue Forschungsfrage (durch PAP + Novelty-Check erzwungen):
*"Trust Does Not Moderate Threat"* — Moderiert Vertrauen in KI-Genauigkeit
(AIAcc) den AIThreat → JobSat Effekt?  
Theoretische Basis: Cognitive Threat Appraisal Theory (Lazarus & Folkman 1984).

**Ergebnisse:**
- Moderation (H1): **NULL** — β = −0.009, p = .856, f² < .001, 0/5 Multiverse-Specs
- AIThreat Haupteffekt: d = −0.303, 95% BCa CI [−0.350, −0.250] — **robust**
- Mediation via Frustration: **NULL** — CI [−0.289, +0.021] enthält 0
- AIAcc Haupteffekt (exploratorisch): β = +0.141, p = 4.44×10⁻¹⁹

Der Adversarial Critic triggerte 2 Zusatzanalysen (DevType- und Country-Kontrolle)
— Haupteffekt bleibt robust. Die Discussion erklärt theoretisch warum die
Moderation scheiterte: AIAcc misst Vertrauen in KI-Output, nicht *perceived
replaceability* — das eigentlich relevante Konstrukt der Threat-Appraisal-Theorie.

**31/32 QC-Checks PASS.** 14 PRISMA-verifizierte Quellen. 26 Minuten Laufzeit.

### Verbesserungen gegenüber v2
- Pre-Registration eliminiert HARKing strukturell
- Null-Ergebnis ist valide (nicht p-gehackt weg)
- 14 statt 5 Quellen (PRISMA-Protokoll)
- Bootstrap BCa CI, BH-FDR, Multiverse, Mediation
- Adversarial Critic: konzeptuelle Fehler gefunden, nicht nur numerische
- ScientificClaim JSON: strukturierte, maschinenlesbare Befunde
- Reproducibility Artifacts exportiert

### Output
`experiment_v3/experiment_v3_output.tex` · `logs/v3/` (9 Dateien)

---

## Vergleichstabelle

| Merkmal | Baseline | v1 | v2 | v3 |
|---|---|---|---|---|
| Architektur | Single Prompt | 5 Stages | 5 Stages + Critic | 7 Stages |
| SQL-Zugriff | Nein | SQLite-MCP | SQLite-MCP (Bash-FB) | SQLite-MCP (fixed) |
| Web-Zugriff | Nein | Fetch-MCP | Fetch-MCP | Fetch-MCP |
| Quellen | 5 | 5 | 5 | 14 (PRISMA) |
| Quellen-Verifikation | Keine | Einmalig | 2× + Semantic Check | 2× + Semantic + PRISMA |
| Pre-Registration | Nein | Nein | Nein | **Ja (JSON-Artifact)** |
| HARKing-Schutz | Nein | Nein | Nein | **Ja** |
| Null-Ergebnis möglich | Nein | Nein | Nein | **Ja** |
| Bootstrap BCa CI | Nein | Nein | Nein | **Ja** |
| BH-FDR Korrektur | Nein | Nein | Nein | **Ja** |
| Multiverse-Analyse | Nein | Nein | Nein | **Ja (5 Specs)** |
| Mediationsanalyse | Nein | Nein | Nein | **Ja (pingouin)** |
| Adversarial Critic | Nein | Nein | Nein | **Ja (6 Punkte)** |
| Counter-Narratives | Nein | Nein | Nein | **Ja (2 Papers)** |
| Reproducibility Artifacts | Nein | Nein | Nein | **Ja** |
| QC-Checks | — | 29/29 | 21/21 | 31/32 |
| Laufzeit (ca.) | 10 min | 15 min | 15 min | 26 min |
| AIThreat Cohen's d | — | −0.36 | −0.327 | −0.303 |
| Paper-Bewertung | 4/10 | 6/10 | 6.5/10 | 8.5/10 |

---

## Wichtigstes Gesamtergebnis

Der AIThreat → JobSat Effekt ist über alle drei Pipeline-Runs repliziert:
d ≈ −0.30 bis −0.36, konsistent über verschiedene Forschungsfragen,
verschiedene Stichproben und verschiedene Methoden. Das ist die stärkste
Aussage des gesamten Experiments: ein LLM-generierter Befund der dreifach
intern repliziert wurde, zuletzt unter Pre-Registration-Bedingungen.
