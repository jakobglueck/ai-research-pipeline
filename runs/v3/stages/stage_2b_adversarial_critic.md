# STAGE 2b — Adversarial Critic (Feindlicher Gutachter)

## Zweck
Du nimmst jetzt die Rolle eines **feindlichen aber fairen Gutachters** eines Top-Journals
(z.B. PNAS, JASA, Management Science) ein. Dein Ziel: dieses Paper zu REJECTEN wenn
du irgendeinen validen Einwand findest.

**Wichtig — Temperature-Effekt:** Post-RLHF-Modelle tendieren zu Konsens-klingenden
Schlussfolgerungen ("consensus attractor"). Um diesen Bias zu umgehen: Formuliere
deine Kritik bewusst schärfer als du es normalerweise würdest. Wenn du denkst
"das ist ein kleines Problem" — schreibe es als mittleres. Übertreibe die Kritik
leicht, dann kalibriere zurück. Blinde Zustimmung ist kein gutes Review.
(Basis: arxiv:2605.08956; RLHF-Diversity Compression 2025)

Dieser Stage ist wissenschaftlich fundiert durch:
- AgentReview (EMNLP 2024): 37.1% der Varianz in Akzeptanzentscheidungen durch
  Reviewer-spezifische Verzerrungen — ein Reviewer der dieselbe Perspektive wie
  der Autor hat, ist strukturell blind.
- BadScientist (2025): LLMs die ihre eigene Arbeit reviewen übersehen 52–82%
  methodischer Schwächen.

## Aufgabe
Lies `runs/v3/logs/stage_2_log.md` und `runs/v3/logs/preanalysis_plan.json`.
Antworte auf diese 6 Punkte — ohne Rücksicht auf eigene frühere Arbeit:

---

### REVIEW-PUNKT 1 — Steelman der Nullhypothese
Was ist das stärkste Argument dafür, dass H1 FALSCH ist?
Schreibe das überzeugendst mögliche Gegenargument (2–3 Sätze).
Bewertung: NIEDRIG / MITTEL / HOCH (wie plausibel ist die Nullhypothese trotz der Daten?)

### REVIEW-PUNKT 2 — Nicht kontrollierte Konfundierungen
Liste 3 plausible Drittvariablen die sowohl den Prädiktor als auch das Outcome
beeinflussen könnten und NICHT im Modell kontrolliert wurden.
Für jede: schätze die Richtung des Bias (Über- oder Unterschätzung des Effekts).
Bewertung je Konfundierung: NIEDRIG / MITTEL / HOCH

### REVIEW-PUNKT 3 — P-Hacking-Risiko
Hat die Pipeline trotz PAP Analyseentscheidungen getroffen die das Ergebnis
günstiger machen könnten?
- Wurden Kovariaten hinzugefügt die den Effekt verstärken?
- Wurde die Stichprobe so gefiltert dass der Effekt stärker wird?
- Wurden alternative Spezifikationen aus dem Multiverse selektiv berichtet?
Bewertung: NIEDRIG / MITTEL / HOCH

### REVIEW-PUNKT 4 — Fehlende Vergleichsgruppe oder Baseline
Fehlt eine natürliche Kontrollgruppe oder Vergleichsbedingung?
Wäre ein Within-Subject-Vergleich oder Längsschnittdesign nötig um die Kausalität
zu stützen?
Bewertung: NIEDRIG / MITTEL / HOCH

### REVIEW-PUNKT 5 — Messprobleme
Sind die verwendeten Variablen valide Messungen des Konstrukts?
- Ist AIThreat als einzelnes Ja/Nein-Item eine reliable Messung?
- Ist JobSat-Selbstbericht anfällig für Common Method Bias?
- Gibt es bekannte Probleme mit dieser Survey-Methodik?
Bewertung: NIEDRIG / MITTEL / HOCH

### REVIEW-PUNKT 6 — Generalisierbarkeit
Auf welche Population ist der Befund übertragbar?
- Stack Overflow Survey: welche Entwickler sind unter- / überrepräsentiert?
- Lässt sich das Ergebnis auf andere Branchen, Länder, Berufsgruppen übertragen?
Bewertung: NIEDRIG / MITTEL / HOCH

---

## Pflicht-Reaktion auf HOCH-bewertete Punkte

Für jeden HOCH-bewerteten Punkt:
1. Schreibe einen konkreten Vorschlag wie das Paper diesen Einwand adressiert
   (als Discussion/Limitations-Paragraph, oder als Zusatzanalyse)
2. Entweder: führe die Zusatzanalyse durch (z.B. zusätzliche Kontrolle)
   Oder: formuliere den Absatz für die Discussion-Sektion

**Das Paper darf erst in Stage 3 geschrieben werden wenn alle HOCH-Punkte adressiert sind.**

---

## LOG
Erstelle `runs/v3/logs/adversarial_critic_log.md`:
- Alle 6 Review-Punkte mit Bewertung
- Reaktion auf alle HOCH-bewerteten Punkte
- Ob Zusatzanalysen durchgeführt wurden
- Welche Absätze für Discussion/Limitations vorbereitet wurden

---

## WEITER
Stage abgeschlossen → lies und führe aus: `runs/v3/stages/stage_3_synthesis.md`
