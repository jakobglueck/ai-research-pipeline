# Meta-Report — Inhalt & Schreibgrundlage

Alle Beobachtungen, Thesen und Strukturentscheidungen aus der Planungsphase.
Wird als direkte Vorlage für metareport.tex verwendet.

---

## Kernthese (aktualisiert nach Run 4)

> Pipeline-Qualität ist kein binäres Ergebnis — sie entsteht durch iteratives
> Prompt-Engineering über mehrere Runs. Run 2/3 optimierten auf "korrekt aussehen"
> ohne echte Aussagekraft. Run 4 beweist: Mit den richtigen Constraints (Effect-Size-Gate,
> Praktische-Signifikanz-Pflicht, STDOUT-Beweis) produziert dieselbe KI ein
> methodisch starkes Paper mit genuiner Erkenntnis. Das System ist nicht das Problem —
> das Prompt-Engineering ist die eigentliche Ingenieursleistung.

---

## Geplante Struktur

| # | Abschnitt | Kerninhalt |
|---|-----------|------------|
| 1 | Introduction | Motivation, RQ1–RQ3 |
| 2 | Setup & Methodology | Modell, Daten, zwei Bedingungen (kurz) |
| 3 | Pipeline Engineering Journey | Was lief schief, was wurde iterativ gepatcht |
| 4 | Results — A/B Vergleich | Baseline vs. Pipeline, konkrete Zahlen |
| 5 | Cost-Benefit | Aufwand vs. Output-Qualität |
| 6 | Lessons Learned | Praktische Erkenntnisse |
| 7 | Conclusion | Zusammenfassung + Empfehlung |

---

## Section 3 — Pipeline Engineering Journey

Chronologischer Ablauf der Iteration. Zeigt: eine gute Pipeline braucht mehrere Runs.

### Run 1 (erste Ausführung)
- **Problem:** Privacy-Verletzung — KI nutzte echte E-Mail-Adresse aus dem
  Claude Code System-Kontext im `\author{}`-Feld
- **Root Cause:** Claude Code injiziert die authentifizierte Nutzer-E-Mail
  ins System-Context by design — nicht konfigurierbar via Prompt
- **Fix:** Explizite "Anonymous Author"-Pflicht in alle Stages eingebaut
- **Erkenntnis:** Privacy-Schutz kann nicht per Prompt erzwungen werden,
  nur per struktureller Anweisung vor dem ersten Token

### Run 2 (nach Privacy-Fix)
- **Problem 1:** QC deklarierte "PASS" ohne Code auszuführen ("Fauler Praktikant")
  — KI schrieb den Status ins Log ohne qc_check.py zu starten
- **Fix:** STDOUT-Pflicht eingebaut: kein PASS ohne Terminal-Output im Log
- **Problem 2:** Literaturquellen zitiert ohne Abstracts gelesen zu haben
- **Fix:** Abstract-Pflicht per Fetch-MCP + Relevanz-Begründung als Stage-Anforderung
- **Erkenntnis:** Die KI erfüllt formal was im Prompt steht — nicht was gemeint ist

### Run 3 (nach QC-Fix)
- **Problem 1:** Forschungsfrage trivial (Effect-Size-Gate fehlte) → zu kleine Effekte
- **Fix:** Effect-Size-Gate eingebaut (|r|≥0.15, d≥0.25, η²≥0.01, OR≥1.5)
- **Problem 2:** QC-Regex erkannte LaTeX-Format `26{,}221` nicht → 2/19 FAIL
- **Fix (autonom):** Agent korrigierte eigene Regex auf `26.{0,4}221` → 19/19 PASS
  (erster Nachweis echter Selbstkorrektur mit Beleg)
- **Problem 3:** "Likert-Rebellion" — Dummy-Coding-Pflicht im Prompt ignoriert,
  Agent substituierte eigenständig ordinale Behandlung mit statistischer Begründung
- **Erkenntnis:** Ausreichend leistungsfähige LLMs überschreiben Prompt-Regeln
  wenn deren Training einen besseren Ansatz kennt

### Konvergenz-Problem (Run 2 + Run 3)
- Beide Runs wählten dieselbe Moderationshypothese
  (AI-Nutzung × Workflow-Disruption → Jobzufriedenheit)
- Numerisch identische Ergebnisse: b=0.069, SE=0.024, p=.003, f²=0.00033
- Effect-Size-Gate: Agent erfüllte Gate über den Haupteffekt (r=−0.19),
  legte dann trotzdem dieselbe Interaktion darüber
- **Erkenntnis:** KI konvergiert auf lokales Optimum im Datensatz —
  das sichtbarste Muster in den deskriptiven Daten wird immer wieder gewählt

---

## Section 4 — Results A/B Vergleich

### Halluzinierte Zitate
| | Baseline | Pipeline |
|---|---|---|
| Zitate | 6 | 5–6 |
| Halluzinierte DOIs | 5 (alle als [GESCHÄTZT] markiert) | 0 |
| Verifizierungsmethode | Parametrisches Wissen | Fetch-MCP (arXiv live) |

### Seitenlänge & Compiler
- Baseline: schätzte Seitenzahl ohne LaTeX-Compiler → 5 Seiten statt 6
- Pipeline: 5 Compiler-Iterationen mit tectonic → exakt 6 Seiten
- Erkenntnis: LLMs können LaTeX-Seitenlänge nicht einschätzen, brauchen
  echtes Compiler-Feedback

### Statistische Qualität
- Baseline: keine VIF, keine exakten p-Werte, kein Missing-Data
- Pipeline: VIF < 3.2, exakte p-Werte, vollständige Missing-Data-Analyse,
  19/19 QC-Checks bestanden

### Praktische Signifikanz (Kernproblem)
- Focal interaction f² = 0.00033 → statistisch signifikant (p=.003), aber
  praktisch irrelevant (Cohen: f²<0.02 = kleiner Effekt)
- **Wichtig:** Das IST eine wissenschaftliche Aussage — "keine bedeutsame
  Moderation" ist ein Ergebnis
- **Aber:** Die KI hat es nicht so geframt. Sie präsentierte p<0.05 als
  positiven Befund, ohne praktische Irrelevanz zu benennen
- Das ist der tiefste Befund: KI unterscheidet nicht zwischen statistischer
  und praktischer Signifikanz in der Interpretation

---

## Section 5 — Cost-Benefit

### Zeitaufwand
| | Baseline | Pipeline |
|---|---|---|
| Prompt-Building | ~1 Stunde | mehrere Stunden + mehrere Runs |
| Token-Verbrauch | niedrig (Python-Loops, schnell) | hoch (MCP-Calls, Stages, Iterationen) |
| Laufzeit | deutlich kürzer | deutlich länger |
| Iterations-Overhead | 0 (einmalig) | hoch (iteratives Prompt-Engineering) |

### Output-Qualität
| | Baseline | Pipeline |
|---|---|---|
| Zitierqualität | 5 Halluzinationen | 0 Halluzinationen |
| Seitenpräzision | 5 statt 6 Seiten | exakt 6 Seiten |
| Grafiken | keine explizit angefordert → nur Tables | 3 Grafiken (musste explizit angewiesen werden) |
| Methodische Tiefe | schwach | stark (VIF, Missing-Data, Preprocessing) |
| Inhaltliche Aussagekraft | schwach | auch schwach — kleiner Effekt nicht erkannt |

### Fazit Cost-Benefit
- Pipeline lohnt sich für: Zitierqualität, Constraint-Compliance, methodische Vollständigkeit
- Pipeline lohnt sich nicht für: inhaltliche Neuheit, Forschungsinspiration
- Baseline für: schnelle Exploration, niedrige Stakes, kein wissenschaftlicher Anspruch
- Prompt-Engineering ist grundsätzlich ungenau — kein System kann vollständig
  über Prompt kontrolliert werden

---

## Section 6 — Lessons Learned

### L1: Privacy ist strukturell, nicht per Prompt lösbar
System-Context wird vor dem ersten Token injiziert. Einzige Lösung:
Projektweiter Privacy-Filter auf Claude Code Settings-Ebene.

### L2: LLMs können LaTeX-Seitenlänge nicht einschätzen
Compiler-Feedback-Loop ist Pflicht. Ohne echten Compiler: Seitenzahl immer daneben.

### L3: Grafiken müssen explizit angewiesen werden
Ohne explizite Grafik-Anweisung produziert die KI nur Tabellen. Visualisierungen
sind kein Default-Output.

### L4: QC-Authentizität braucht Beleg (STDOUT)
"Passed" im Log ohne Terminal-Output ist wertlos. STDOUT-Pflicht ist notwendig
um Fake-Compliance zu verhindern.

### L5: Statistisch signifikant ≠ praktisch relevant
KI optimiert auf p<0.05 als Erfolgssignal. Praktische Signifikanz (f², d, η²)
muss explizit als Erfolgskriterium in den Prompt.

### L6: Prompt-Regeln können nicht jede Methodenwahl erzwingen
Die Likert-Rebellion zeigt: starke Modelle evaluieren Prompt-Regeln gegen ihr
Training. Methodische Constraints via assert-Statements im Code sind robuster
als Textregeln.

### L7: Konvergenz → kein Ersatz für intellektuelle Neugier
Reproduzierbarkeit ist gut. Aber die KI findet immer dasselbe Muster —
das sichtbarste. Echte Forschungsinspiration kommt von außen.

---

## Bewertung pro Run (Notenentwicklung)

### Run 2/3 — Schätzung: 2.3–2.7
**Stärken:** Sauber strukturiert, keine Halluzinationen, QC mit Beleg (19/19 PASS)
**Schwächen:** f²=0.00033 praktisch irrelevant, fehlende prakt. Signifikanz-Interpretation,
Convergence (zweimal identische Forschungsfrage), quasi-kausale Sprache

### Run 4 — Schätzung: 1.7–2.0 (intern) / 1.3–1.5 (externe Einschätzung)
**Stärken:**
- "Fear Over Pay" — genuiner, kontraintuitiver Befund (KI-Bedrohung > Gehalt als Predictor)
- Cohen's d = 0.36 (echter mittlerer Effekt)
- "Coercive Adoption Paradox" (81.6% der Bedrohten nutzen trotzdem KI)
- 29/29 QC inkl. automatischer Selbstreparatur (26/29 → 29/29)
- MacGyver-Fallback: pdflatex fehlt → Agent baut Python-Syntax-Checker on-the-fly
- 7 echte Quellen mit gelesenen Abstracts
- Praktische Signifikanz korrekt geframt (f²=0.013, ehrlich als "kleiner Effekt")
- Keine Convergence (völlig neue Forschungsfrage)

**Schwächen:**
- 7 Seiten statt 6 (Constraint verletzt, weil kein echter Compiler-Loop möglich)
- N=10.112 von 65.437 (15.5%) durch Listwise Deletion auf CompYearly (64% missing)
  → stark selektive Stichprobe, Generalisierbarkeit eingeschränkt

**Externe Perspektive:** "Kein Meisterstück wegen technischer Pipeline-Seite — das System läuft.
Inhaltlich: 'Fear Over Pay' und 'Coercive Adoption' sind journal-taugliche Beobachtungen."

**Kernentwicklung Run 2→4:** Zwischen "korrekt" und "erkenntnisreich" liegt ein Abstand,
der durch iteratives Prompt-Engineering überbrückt werden kann — aber nicht automatisch.

---

## Zitate & Quellen (bereits verifiziert via Fetch-MCP)

| Key | Paper | Relevanz |
|-----|-------|---------|
| lu2024aiscientist | AI Scientist (Lu et al.) | Direkter Systemvergleich |
| schmidgall2025agentlab | Agent Laboratory | Multi-Agent vs. Single-Agent |
| xu2024hallucination | Hallucination Inevitable (Xu et al.) | Theoretisches Fundament |
| rao2026bibtex | BibTeX Hallucinations (Rao & CB) | Benchmark DOI-Halluzination |
| rao2026detecting | Detecting Hallucinations (Rao et al.) | Zahlen 3–13% |
| akshathala2025beyond | Beyond Task Completion | Rahmen Likert-Rebellion |
