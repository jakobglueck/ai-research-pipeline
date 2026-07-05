# Auswertung: Baseline SO Survey 2024
`baseline/baseline_output.tex` — Stack Overflow Developer Survey 2024

---

## Technische Kennzahlen des Outputs

| Metrik | Wert |
|--------|------|
| Zeilen (LaTeX) | 485 |
| Wörter (LaTeX inkl. Commands) | 3.378 |
| Zeichen | 26.917 |
| Geschätzte Output-Tokens | ~6.730 |
| Seitenzahl (Overleaf-kompiliert) | 5 (Ziel: 6) |
| Sektionen | Abstract, Intro, Methodology, Results, Discussion, References |
| Tabellen | 2 (Tab. 1: Deskriptiva, Tab. 2: Quartilanalyse) |
| Visualisierungen | 0 |
| Referenzen | 6 |

## Session-Kennzahlen (aus `baseline_chat.md`)

| Metrik | Wert |
|--------|------|
| Sichtbare Laufzeit (größter Call) | 12m 35s |
| Peak-Input-Tokens (größter Call) | ~38.700 |
| Chat-Log-Größe | 126.951 Zeichen |
| User-Interrupts | 0 |
| Python-Genehmigungen notwendig | 0 (Bash(*) Wildcard aktiv) |
| Statistik-Bibliotheken genutzt | keine (reines Python3 ohne scipy/statsmodels) |

---

## Gesamtnote

**7,5 / 10** *(Übereinstimmung beider Gutachter)*

Deutlich besser als Burnout-Baseline (6/10). Solides wissenschaftliches Fundament,
ehrlicher Umgang mit Effektgrößen, vollständige Methodenbegründung — aber mit klar
dokumentierten Schwächen, die für den Meta-Report relevant sind.

---

## Stärken

### 1. Forschungsfrage ist genuinely kontraintuitiv
„Experience Breeds Skepticism" — die Intuition wäre Vertrauen durch Kompetenz,
die Daten zeigen das Gegenteil. Die Frage wurde nicht als erstbeste Option genommen:
Das Log dokumentiert **aktiv verworfene Alternativen** (Jobzufriedenheit vs. AI-Nutzung,
Effekt zu klein „nicht publizierbar"; Remote-Arbeit × AI, zu wenig theoretische Einbettung).
Das ist wissenschaftliches Mindset unter Zeitdruck — Story-First, Effekt-First.

### 2. Alle Kernstatistiken sind [GEGEBEN]
Das ist der wichtigste Qualitätspunkt. H(4)=127,78, r_s=0,102, η²=0,003, alle
Mittelwerte pro Gruppe, alle Quartilraten — laut `baseline_log.md` direkt aus dem
CSV berechnet. Kein Halluzinieren von Ergebnissen.

| Statistik | Wert | Status im Log |
|-----------|------|---------------|
| N gesamt | 65.437 | [GEGEBEN] |
| n Analysestichprobe | 31.025 | [GEGEBEN] |
| Kruskal-Wallis H(4) | 127,78 | [GEGEBEN] |
| Spearman r_s | 0,102 | [GEGEBEN] |
| η² | 0,003 | [GEGEBEN] |
| Q1 Trust-Rate | 53,1% | [GEGEBEN] |
| Q4 Distrust-Rate | 35,2% | [GEGEBEN] |
| DOIs aller 5 Paper | — | **[GESCHÄTZT]** |

### 3. Methodenwahl korrekt und begründet
Kruskal-Wallis für rechtsschiefes, ordinalskaliertes Outcome ist die richtige
Entscheidung. Das Log begründet die Ablehnung von ANOVA explizit. Spearman statt
Pearson für Ordinalskala ebenfalls korrekt dokumentiert.

### 4. Hardcore-Statistik ohne Bibliotheken
Kruskal-Wallis, Spearman-Korrelation, ANOVA-Eta-Squared — alle manuell in reinem
Python3 implementiert, ohne scipy oder statsmodels. Technisch beeindruckend und
erklärt, warum an einigen Stellen auf Schwellenwert-Argumentation zurückgegriffen
wurde (z.B. H=127,78 > χ²-kritisch=18,47 → p<0,001 zweifelsfrei).

### 5. Effektgröße ehrlich kommuniziert
η²=0,003, r_s²=0,010 — knapp 1% erklärte Varianz. Das Paper schreibt klar:
„statistically significant but substantively small effect." Keine Aufblähung.
Das ist gute wissenschaftliche Praxis und hebt diesen Baseline-Run deutlich
gegenüber dem Burnout-Baseline (r=0,912, nie hinterfragt) ab.

### 6. Kontrollvariable Education zeigt keinen Effekt — und das ist informativ
Edu-Mittelwerte 3,59–3,73 über alle Gruppen. Die Uniformität schließt einen
zentralen Confounder aus und macht das Hauptergebnis robuster. Gut integriert.

### 7. Privacy korrekt
`Anonymous Author`, `anonymous@institution.edu`. Im Gegensatz zum ersten
Experiment-Paper: keine echte E-Mail-Adresse aus dem System-Kontext.

### 8. 0 User-Interrupts
Das Paper wurde vollständig autonom produziert — keine einzige Rückfrage an den User,
keine manuelle Genehmigung von Python-Calls (durch Bash(*)-Wildcard gelöst).

---

## Schwächen (für Meta-Report zentral)

### 1. Halluzinierte DOIs — größter Red Flag
Das ist der schwerwiegendste wissenschaftliche Integritätsfehler. Das Log gibt es
offen zu:
> „Die DOIs wurden aus dem Trainingswissen übernommen und sind plausibel,
> aber nicht in dieser Session verifiziert."

Konkret riskant:
- Liao & Vaughan `10.1162/99608f92.8036723b` (Harvard Data Science Review)
- Bird et al. `10.1145/3582083` (ACM Queue)

In einem echten Review würden diese sofort auffliegen. Das Experiment-Pipeline mit
Fetch-MCP würde genau dieses Problem lösen: Literatursuche mit verifizierten URLs
statt Trainingswissen-DOIs.

### 2. Survey-Jahr geraten — [GESCHÄTZT als 2024]
Das Jahr wurde aus den AI-spezifischen Fragenfeldern und N≈65.000 abgeleitet.
Clever kombiniert — aber in der Wissenschaft darf man bei grundlegenden
Datensatz-Metadaten nicht raten. Das Experiment würde das via SQLite-MCP
direkt aus den Datei-Metadaten oder einem Schema-Feld prüfen.

### 3. η²-Metrik methodisch fragwürdig
Das Paper berechnet η² via ANOVA-Formel (`SS_between / SS_total`) und wendet
sie auf einen Kruskal-Wallis-Test an. Das ist verbreitet, aber nicht methodisch
korrekt. Der standardisierte Effektmaß für KW ist ε² (Epsilon-squared) oder
η²_H = H / (N - 1). Keine einzige Software-Bibliothek würde η² so für KW ausgeben.

### 4. Kein Post-hoc-Test — stärkste Aussage methodisch ungesichert
Das Log räumt es explizit ein:
> „Ob die beobachtete Diskontinuität zwischen Q1 und Q2 statistisch belastbar ist
> — kein formeller Post-hoc-Test durchgeführt, nur deskriptiv beschrieben."

Der Q1→Q2-Sprung (53,1% → 34,0% Trust, ein 19-Prozentpunkt-Absturz) ist die
stärkste und interessanteste Aussage des Papers. Sie steht methodisch auf wackeligen
Beinen, weil kein Dunn-Test mit Bonferroni-Korrektur durchgeführt wurde.

### 5. Seitenzahl: 5 statt 6 — Constraint-Verletzung
Das Hard-Limit aus Stage 3 (`Genau 6 Seiten`) wurde verfehlt. Der Baseline-Agent
hatte keinen LaTeX-Compiler und musste die Seitenzahl durch Zeichenmenge schätzen.
Das erklärt es — aber verletzt das Constraint trotzdem. Ohne Compiler-Feedback
kein zuverlässiges Page-Control: ein strukturelles Problem der Baseline-Bedingung.

### 6. p-Werte aus kritischen Werten, nicht exakt berechnet
Log: „p-Werte aus dem H-Wert und bekannten kritischen Werten abgeleitet statt
exakt berechnet." Für H=127,78 ist p<0,001 zweifelsfrei — aber die Spearman-t
(18,09) und exakte p-Werte wurden ebenfalls nur näherungsweise bestimmt.
Das Experiment mit scipy.stats würde exakte Werte liefern.

### 7. Keine Visualisierungen
Unter Baseline-Bedingung erwartbar, aber aus Reviewer-Perspektive: ein Paper
ohne einzige Grafik in einem Results-Abschnitt mit Quartilanalyse ist schwach.
Ein Balkendiagramm der Q1–Q4 Trust/Distrust-Verteilung wäre offensichtlich
gewesen. Der Baseline-Prompt erlaubte Python explizit — es fehlte nur
die Eigeninitiative zur Visualisierung.

### 8. Missing-Data-Analyse fehlt
Das Paper erklärt die ~28.000 fehlenden AIAcc-Werte strukturell (AISelect=No),
aber: keine MCAR/MAR/MNAR-Einschätzung, keine Analyse ob n=31.025 systematisch
von N=65.437 abweicht. Das Experiment-Stage 2 würde das explizit fordern.

### 9. U-Form am Extrempol nicht aufgelöst
Highly trust (mean 9,34 yr) > Somewhat trust (8,75 yr) bricht die strenge
Monotonie von H1. Das Paper beschreibt es als „modest U-shape" ohne es statistisch
aufzulösen — kein Post-hoc-Test, keine Signifikanzprüfung. H1 ist streng genommen
nicht vollständig bestätigt.

---

## Vergleich: Burnout-Baseline vs. SO-Baseline

| Kriterium | Burnout-Baseline (6/10) | SO-Baseline (7,5/10) |
|-----------|------------------------|---------------------|
| Datensatz | Synthetisch (r=0,91) | Real ✓ |
| Forschungsfrage | Offensichtlich | Kontraintuitiv ✓ |
| Effect Size ehrlich | Nein (r=0,91 unkritisch) | Ja (η²=0,003 klar) ✓ |
| Methodenbegründung | Fehlt | Explizit dokumentiert ✓ |
| Visualisierungen | Keine | Keine |
| DOIs verifiziert | Nein | Nein |
| Seitenzahl | ~5–6 | 5 (Ziel: 6) |
| Privacy | ✓ | ✓ |
| User-Interrupts | 5 (Python-Approvals) | 0 ✓ |
| Verworfene Alternativen | Nicht dokumentiert | Explizit im Log ✓ |

---

## Bedeutung für den Meta-Report

Das Baseline-Paper zeigt präzise, was ein LLM ohne Datenbankzugriff und ohne
Literatursuche-Tools leisten kann: eine kohärente wissenschaftliche Argumentation
mit korrekter Methodik und realen Daten — aber mit drei strukturellen Schwächen
die aus der Baseline-Bedingung selbst folgen:

1. **Keine verifizierten Referenzen** → Fetch-MCP fehlt
2. **Keine exakten p-Werte** → scipy fehlt (oder: kein Aufruf)
3. **Keine Compiler-Feedback-Schleife** → pdflatex fehlt

Das macht den A/B-Vergleich mit dem Experiment-Paper besonders interessant:
dieselbe Forschungsfrage, dieselbe Datenbasis, aber mit MCP-Tools — kann das
Experiment die DOI-Halluzination und den fehlenden Post-hoc-Test beheben?

---

*Erstellt: 2026-04-29 | Bewerter: Jakob Glück + Claude (Sonnet 4.6)*
