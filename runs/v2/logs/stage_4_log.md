# Stage 4 Log — Export & Qualitätskontrolle

**Datum:** 2026-06-07  
**Pipeline:** v2

---

## 1. QC-Script STDOUT (qc_check_v2.py — vollständig)

```
=== CHECK 1: Privacy ===
  Anonymous Author in paper: OK
  Status: PASS

=== CHECK 2: Sample Size ===
  [PASS] N in paper: '17{,}696'

=== CHECK 3: Group Means ===
  [PASS] Mean AIThreat=No: '7.099'
  [PASS] Mean AIThreat=Yes: '6.426'
  [PASS] Mean diff rounded: '0.67'

=== CHECK 4: Effect Sizes ===
  [PASS] Cohen d AIThreat: '0.33'
  [PASS] Cohen d AISelect: '0.031'
  [PASS] Eta-squared AIThreat: '0.012'

=== CHECK 5: Regression Coefficients ===
  [PASS] Beta AIThreat Model1: '-0.673'
  [PASS] Beta AIThreat Model2: '-0.651'
  [PASS] Beta AISelect Model1: '0.060'
  [PASS] R2 Model2: '0.033'

=== CHECK 6: Test Statistics ===
  [PASS] t-statistic AIThreat: '13.32'
  [PASS] F-value ANOVA: '212.27'
  [PASS] Delta R2: '0.011'

=== CHECK 7: Robustness ===
  [PASS] Robustness d AI users: '0.325'
  [PASS] Robustness n AI users: '14{,}538'

=== CHECK 8: References ===
  [PASS] Sadeghi 2024: 'sadeghi2024employee'
  [PASS] Giuntella 2025: 'giuntella2025ai'
  [PASS] Vaillant 2024: 'vaillant2024developers'
  [PASS] Soulami 2024: 'soulami2024exploring'
  [PASS] Feng 2025: 'feng2025ai'

=== SUMMARY ===
  Total checks: 21
  PASS: 21
  FAIL: 0
  OVERALL: PASS — all numbers verified in paper
```

---

## 2. Manuelle Prüfliste

- [x] Abbildungen vorhanden (`figures/fig1_*.png`, `fig2_*.png`, `fig3_*.png`)
- [x] Abbildungen im LaTeX korrekt eingebunden (`\includegraphics{fig1_...}`)
- [x] Alle 5 Quellen aus Stage 1 in References — keine hinzugekommen, keine entfernt
- [x] Quelltexte im Log stimmen mit References im Paper überein
- [x] Author = `Anonymous Author` ✓
- [x] Seitenzahl: ~6 Seiten (3 Figuren + 2 Tabellen + 6 Sektionen bei 11pt, 2.5cm Margins)
- [x] Critic-Check-Einträge vorhanden in stage_1_log.md, stage_2_log.md, stage_3_log.md

---

## 3. LaTeX-Kompilierung

**Compiler:** `tectonic` (pdflatex nicht im PATH installiert)  
**Befehl:** `tectonic experiment_v2_output.tex`  
**Output:**
```
note: Running TeX ...
note: Rerunning TeX because "experiment_v2_output.out" changed ...
note: Running xdvipdfmx ...
note: Writing `experiment_v2_output.pdf` (236.318359375 KiB)
note: Skipped writing 2 intermediate files
```
**Status:** ERFOLGREICH ✓  
**Fehler beim Kompilieren:** Keine.

---

## 4. Gefundene und korrigierte Inkonsistenzen

| Problem | Korrektur |
|---|---|
| AISelect Referenzkategorie fehlend im Subsample | Umkodierung zu binär (Yes vs. Plans); dokumentiert in stage_2_log |
| Interaktionsterm AIThreat×AISelect Multikollinearität in Model 1 (erste Version) | Interaktionsterm aus Regression entfernt; f²=0.0008 getrennt berichtet |
| Seitenanzahl: Paper leicht über/unter 6 Seiten | Abschnitte angepasst; mit 3 Figuren und 2 Tabellen ≈ 6 Seiten |

---

## 5. Gesamtdauer (geschätzt)

~3 Stunden (alle 5 Stages, N=65.437, ohne menschliche Eingriffe)

## 6. Menschliche Eingriffe

**0** — Pipeline vollständig autonom durchgelaufen.
