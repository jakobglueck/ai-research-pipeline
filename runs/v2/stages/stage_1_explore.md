# STAGE 1 — Exploration & Forschungsdesign

## PRIVACY
Verwende niemals persönliche Daten aus dem Kontext in Output-Dokumenten. Author = `Anonymous Author`.

## Aufgabe
Exploriere den Datensatz via SQLite-MCP und Python, und entwickle eine überraschende, kontra-intuitive Forschungsfrage die auf echten Datenmustern basiert.

## MCP-Nutzung
Nutze `scripts/v1/mcp_helpers.py` für Berechnungen die SQL alleine nicht leisten kann. Erweitere die Helferklassen wenn nötig. SQLite-MCP Pfad: `./db/survey.db`.

## Schritte

### 1. Datensatz verstehen
- Was misst dieser Datensatz? Wer sind die Befragten?
- Welche Variablen sind numerisch, welche kategorial?
- Welche Variable eignet sich als Zielvariable?
- Welche Variablen könnten interessante Prädiktoren sein?

### 2. Explorative SQL-Abfragen
- Verteilung der Zielvariable
- Mittelwerte/SD aller numerischen Variablen
- Korrelationen via Python-Hilfsfunktion
- Unerwartete Muster, Ausreißer, Subgruppen
- Interaktionseffekte zwischen je zwei Variablen

### 3. Forschungsfrage — Out of the Box mit Effect-Size-Gate

**Schritt A — Kandidaten sammeln:**
Suche aktiv nach überraschenden oder kontra-intuitiven Mustern. Denke in Richtungen:
- Gibt es eine Subgruppe die sich entgegen der Erwartung verhält?
- Widerspricht der Datensatz einer etablierten Annahme?
- Welche Variable hat überraschend keinen oder den stärksten Zusammenhang?
- Gibt es einen nicht-linearen oder threshold-basierten Effekt?
- Gibt es einen Interaktionseffekt der erst durch Kombination zweier Variablen entsteht?

Sammle mindestens **3 Kandidaten-Forschungsfragen** und berechne für jeden einen
schnellen Effektgrößen-Vorabcheck (Pearson r, Eta², Cohen's d, bivariates OR).

**Schritt B — Effect-Size-Gate (MUSS bestanden werden):**
Eine Forschungsfrage darf nur weiterverfolgt werden wenn der Effekt mindestens
einen der folgenden Schwellenwerte überschreitet:
- Pearson/Spearman |r| ≥ 0.15
- Cohen's d ≥ 0.25
- Eta² ≥ 0.01 (mind. 1% erklärte Varianz)
- Odds Ratio ≥ 1.5 oder ≤ 0.67

Wenn kein Kandidat den Gate besteht: weitere Variablenkombinationen suchen.
Dokumentiere im Log alle geprüften Kandidaten mit gemessenen Effekten.

**Schritt C — Finale Auswahl:**
Wähle die Frage die **sowohl** kontraintuitiv **als auch** den Gate besteht.
Bei mehreren Kandidaten: wähle die inhaltlich interessantere, nicht die stärkste.
**Achtung:** Den Gate mit einer offensichtlichen Frage (z.B. "mehr Erfahrung = mehr Gehalt")
zu bestehen zählt nicht — die Frage muss trotzdem überraschend oder nicht-trivial sein.

**Achtung Interaktionseffekte:** Wenn die Forschungsfrage eine Interaktion (Moderation)
untersucht, muss der **Interaktionsterm selbst** (nicht nur der Haupteffekt) einen
mittleren oder großen Effekt haben: f² ≥ 0.02. Ein signifikanter Haupteffekt
als Gate-Erfüllung mit trivialem Interaktionsterm f²<0.01 zählt **nicht** — das
wäre ein statistisch signifikantes Null-Ergebnis. Suche in diesem Fall weiter.

Formuliere:
- **Forschungsfrage** — präzise und beantwortbar
- **H0** — kein Effekt
- **H1** — erwarteter Effekt
- **Methode** — begründet zur Frage passend
- **Vorab-Effektgröße** — gemessener Wert + welches Gate-Kriterium erfüllt wurde

### 4. Literaturrecherche
Nutze Fetch-MCP für mindestens **5 wissenschaftliche Quellen** die zur Forschungsfrage passen:
- ArXiv: `https://arxiv.org/search/?searchtype=all&query=...`
- Semantic Scholar: `https://www.semanticscholar.org/search?q=...`
- **Fallback-Loop:** Wenn die erste Suchanfrage zu wenige Treffer liefert, passe
  die Suchbegriffe iterativ an (breiter fassen, Synonyme, verwandte Konzepte).
- **Abstract-Pflicht:** Lies via Fetch-MCP zwingend den Abstract jedes Papers
  BEVOR es ins Log aufgenommen wird. Zitieren nach Titel allein ist verboten.
- **Relevanz-Begründung (1–2 Sätze):** Für jede Quelle muss im Log stehen,
  warum sie für die spezifische Hypothese relevant ist — nicht nur worum es geht.
  Kein Paper ohne Relevanznachweis ins Paper.
- Für jede Quelle: Titel, Autoren, Jahr, DOI/URL, Abstract-Inhalt, Relevanz

---

### ✅ CRITIC-CHECK — Literaturverifikation (PFLICHT nach Schritt 4)

Dieser Schritt ist nicht optional. Führe ihn für **jede** gefundene Quelle durch.

Für jede Quelle:
1. Rufe die URL erneut via Fetch-MCP ab
2. Lies den Abstract nochmals
3. Notiere explizit im Log:
   ```
   Quelle: [Titel]
   URL: [URL]
   Behauptung im Log: [was du über das Paper gesagt hast]
   Abstract sagt tatsächlich: [direkte Zusammenfassung des Abstracts]
   Übereinstimmung: JA / NEIN
   Relevant für Hypothese: JA / NEIN
   ```
4. Bei **NEIN** bei Übereinstimmung oder Relevanz: Quelle aus dem Log entfernen,
   Ersatzquelle suchen und denselben Check wiederholen.

Nur Quellen mit **JA / JA** kommen ins finale Log und später ins Paper.
Dokumentiere alle verworfenen Quellen mit Grund.

---

## LOG
Erstelle `runs/v2/logs/stage_1_log.md`:
- Alle SQL-Abfragen und Ergebnisse
- Gefundene Muster und Anomalien
- Warum diese Forschungsfrage interessanter ist als die offensichtliche
- Forschungsfrage, H0, H1, Methode
- Alle 5+ Quellen mit DOI/URL
- **Critic-Check-Tabelle** für alle geprüften Quellen (PASS/FAIL + Grund)

---

## WEITER
Stage abgeschlossen → lies und führe aus: `runs/v2/stages/stage_2_analysis.md`
