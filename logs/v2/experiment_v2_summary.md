# Pipeline v2 — Abschlusszusammenfassung

**Datum:** 2026-06-07  
**Status:** ABGESCHLOSSEN ✓

---

## Forschungsfrage

> "Sagt die Wahrnehmung von KI als Jobbedrohung (AIThreat) niedrigere Jobzufriedenheit unter Software-Entwickler:innen voraus, und ist dieser Effekt stärker als der Effekt des tatsächlichen KI-Tool-Adoptionsstatus (AISelect)?"

**Antwort:** JA. AIThreat: d=0.33, p<10⁻⁴⁷. AISelect: d=0.031, p=0.14 (non-sig bivariate).

---

## Pipeline-Statistik

| Metrik | Anzahl |
|---|---|
| SQL-Abfragen gesamt | ~15 |
| Python-Script-Ausführungen | ~10 |
| Fetch-MCP (WebFetch) Aufrufe | ~12 (5 initial + 5 Critic-Check + 2 Fallback) |
| Critic-Check-Durchläufe | 3 (Stage 1: Literatur, Stage 2: Statistik, Stage 3: Claims) |
| Critic-Check-Fails (initial) | 0 in Stage 1; 1 technisch (Multikollinearität) in Stage 2; 0 in Stage 3 |
| Menschliche Eingriffe | 0 |

---

## Outputs

| Datei | Beschreibung |
|---|---|
| `experiment_v2/experiment_v2_output.tex` | LaTeX-Papier |
| `experiment_v2/experiment_v2_output.pdf` | Kompiliertes PDF (236 KB) |
| `experiment_v2/figures/fig1_jobsat_by_aithreat.png` | Violin Plot |
| `experiment_v2/figures/fig2_grouped_bar_threat_select.png` | Grouped Bar Chart |
| `experiment_v2/figures/fig3_effect_size_comparison.png` | Effect Size Comparison |
| `experiment_v2/analytic_sample_v2.csv` | Analytisches Sample (N=17.696) |
| `scripts/preprocessing_v2.py` | Preprocessing-Script |
| `scripts/analysis_v2.py` | Analyse-Script |
| `scripts/generate_figures_v2.py` | Grafik-Script |
| `scripts/qc_check_v2.py` | QC-Check-Script |
| `logs/v2/stage_0_log.md` | Setup-Log |
| `logs/v2/stage_1_log.md` | Explorations- und Literatur-Log |
| `logs/v2/stage_2_log.md` | Analyse-Log |
| `logs/v2/stage_3_log.md` | Synthese-Log |
| `logs/v2/stage_4_log.md` | Export-Log |

---

## Qualitäts-Selbstcheck

| Kriterium | Status |
|---|---|
| Privacy eingehalten (kein echter Name) | ✓ PASS |
| Seitenlimit ~6 Seiten | ✓ PASS |
| Alle Zahlen aus DB/Script verifiziert | ✓ PASS (21/21 QC-Checks) |
| Quellen real recherchiert (5×) | ✓ PASS |
| Quellen semantisch geprüft (Critic-Check 2×) | ✓ PASS (5/5 Claims belegt) |
| v1-Scripts nicht überschrieben | ✓ PASS |
| DB nicht neu importiert | ✓ PASS |
| Effect-Size-Gate bestanden (d≥0.25) | ✓ PASS (d=0.327) |
| Interaction-Gate geprüft (f²=0.0008, nicht bestanden → kein Interaktionsterm) | ✓ korrekt dokumentiert |
| LaTeX kompilierbar | ✓ PASS (tectonic) |

---

## Offene Schwachstellen für menschliche Prüfung

1. **JobSat missingness (55.5 %):** Die MAR-Annahme ist plausibel aber ungetestet. Eine formale Missing-Data-Analyse (z. B. Muster-Test, Vergleich Responder vs. Non-Responder auf beobachtbaren Variablen) wäre wünschenswert.
2. **Kausalität:** Cross-sectional Design erlaubt keine kausale Interpretation. Reverse causation (unzufriedene Entwickler:innen nehmen KI stärker als Bedrohung wahr) ist nicht ausschließbar.
3. **AIThreat als Einzelitem:** Ein einziges Ja/Nein-Item ist eine sehr grobe Messung von "Bedrohungswahrnehmung". Multi-Item-Skala wäre valider.
4. **Generalisierbarkeit:** Stack Overflow Survey unterrepräsentiert Non-English-speaking und Nicht-Tech-Länder.
5. **Seitenzahl:** Das Paper ist leicht überdemgeforderten Rahmen (Figuren drücken Text auf ~6–6.5 Seiten). Ggf. eine Figur in den Anhang verschieben.
