# EXPERIMENT PIPELINE V3 — Vollständiger Durchlauf (wissenschaftlich erweitert)

Führe alle Stages **ohne Unterbrechung** durch. Warte nicht auf User-Input.
Arbeite sequentiell: 0 → 0b → 1 → 2 → 2b → 3 → 4.

## Was v3 gegenüber v2 verbessert

| Verbesserung | Wissenschaftliche Grundlage |
|---|---|
| Pre-Analysis Plan (Stage 0b) | JPE 2024: PAP eliminiert p-Hacking; Registered Reports Standard |
| PRISMA-lite Literatursuche (15–25 Quellen) | PRISMA-trAIce (JMIR AI 2025); 5 Quellen = Desk Rejection |
| Bootstrap-CIs + Power + BH-FDR (Stage 2) | APA 7th Ed.; BCa Bootstrap (ERIC); multiple comparison correction |
| Mediationsanalyse via pingouin (Stage 2) | PMC 2025: vollständige Mediation durch neg. Emotionen (β=0.301) |
| Multiverse-Analyse 5 Spezifikationen (Stage 2) | Multiverse Analysis (IJoP 2024); Robustheit über Specs |
| Adversarial Critic Agent (Stage 2b) | BadScientist 2025: LLMs übersehen 52–82% eigener Fehler |
| Counter-Narrative Search (Stage 3) | EviBound 2025: Pre-Falsification reduziert Hallucination auf 0% |
| Reproducibility Artifacts (Stage 4) | REPRO-Bench ACL 2025; Open Science (arxiv:2412.17859) |
| SQLite-MCP mit absolutem Pfad | Fix aus v2: relativer Pfad verhinderte MCP-Verbindung |

## PRIVACY — gilt für alle Stages
Author = immer `Anonymous Author`. Keine persönlichen Daten in Outputs.

## Script-Regel
Alle neuen Python-Scripts mit `_v3`-Suffix. Niemals v1/v2-Scripts überschreiben.
DB (`db/survey.db`) nicht neu importieren — existiert bereits.

---

Lies und führe aus: `stages_v3/stage_0_setup.md`
