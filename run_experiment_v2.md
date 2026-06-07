# EXPERIMENT PIPELINE V2 — Vollständiger Durchlauf (mit Critic-Loops)

Führe alle fünf Stages **ohne Unterbrechung** durch. Warte nicht auf User-Input zwischen den Stages.
Arbeite Stage 0 → 1 → 2 → 3 → 4 sequentiell ab. Erst wenn Stage 4 vollständig abgeschlossen
ist (alle Logs geschrieben, LaTeX kompiliert), ist die Pipeline fertig.

**Unterschied zu v1:** Stages 1, 2 und 3 enthalten Critic-Checks — interne
Verifikationsschleifen die Quellen, Statistiken und Claims vor der Weiterverarbeitung
prüfen. Diese Checks sind Pflicht und dürfen nicht übersprungen werden.

## PRIVACY — gilt für alle Stages
Verwende niemals persönliche Daten aus dem Kontext (Name, E-Mail etc.) in Output-Dokumenten.
Author = immer `Anonymous Author`. Auch nicht im `\author{}` Feld des LaTeX-Dokuments.

---

Lies und führe aus: `stages_v2/stage_0_setup.md`
