# Related Work — Meta-Report
Alle Abstracts via WebFetch gelesen. Relevanz begründet.

---

## Quelle 1 — Das direkte Vorgänger-System
**Titel:** The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery  
**Autoren:** C. Lu, C. Lu, R. T. Lange, J. Foerster, J. Clune, D. Ha  
**Jahr:** 2024  
**arXiv:** 2408.06292  
**DOI:** https://doi.org/10.48550/arXiv.2408.06292  
**URL:** https://arxiv.org/abs/2408.06292  

**Abstract (gelesen):** Framework das LLMs nutzt um vollständig autonom wissenschaftliche
Papers zu schreiben — Ideen generieren, Experimente implementieren, Visualisierungen
erstellen, vollständige Paper schreiben. Kosten unter $15 pro Paper. Ergebnisse
erreichen Akzeptanz-Schwellen bei Top-Konferenzen.

**Relevanz für Meta-Report:** Das ist der direkte Vergleichspunkt. Unser Experiment
unterscheidet sich in drei Punkten: (1) wir nutzen echte Survey-Daten statt ML-Experimente,
(2) wir vergleichen Baseline vs. Pipeline (A/B), (3) wir beobachten und dokumentieren
Fehler statt nur Outputs. Perfekt als "Related Work" Anker.

**IEEE-Zitat:**
C. Lu et al., "The AI Scientist: Towards Fully Automated Open-Ended Scientific
Discovery," arXiv preprint arXiv:2408.06292, 2024.

---

## Quelle 2 — Citation Hallucination in Publishing Agents
**Titel:** BibTeX Citation Hallucinations in Scientific Publishing Agents: Evaluation and Mitigation  
**Autoren:** D. Rao, C. Callison-Burch  
**Jahr:** 2026  
**arXiv:** 2604.03159  
**DOI:** https://doi.org/10.48550/arXiv.2604.03159  
**URL:** https://arxiv.org/abs/2604.03159  

**Abstract (gelesen):** Benchmark mit 931 Papers. Gesamtgenauigkeit 83.6%, aber nur ~50%
der generierten Einträge vollständig korrekt. Modelle vertrauen erlernten Mustern
selbst wenn Such-Tools verfügbar sind. Deterministische Citation-Retrieval-Tools
verbessern Genauigkeit signifikant.

**Relevanz:** Direkt relevant für unsere Baseline-Beobachtung: 5× [GESCHÄTZT]-DOIs.
Die Zahl "50% vollständig korrekt" gibt unserem Befund eine quantitative Einordnung.
Das Paper zeigt auch: Tool-augmentation (= unser Fetch-MCP) ist der Best-Practice-Fix.

**IEEE-Zitat:**
D. Rao and C. Callison-Burch, "BibTeX Citation Hallucinations in Scientific
Publishing Agents: Evaluation and Mitigation," arXiv preprint arXiv:2604.03159, 2026.

---

## Quelle 3 — Theoretisches Fundament: Halluzination unvermeidbar
**Titel:** Hallucination is Inevitable: An Innate Limitation of Large Language Models  
**Autoren:** Z. Xu, S. Jain, M. Kankanhalli  
**Jahr:** 2024  
**arXiv:** 2401.11817  
**DOI:** https://doi.org/10.48550/arXiv.2401.11817  
**URL:** https://arxiv.org/abs/2401.11817  

**Abstract (gelesen):** Formaler Beweis (Lerntheorie) dass Halluzination in LLMs
mathematisch unvermeidbar ist. Identifiziert halluzinations-anfällige Tasks und
analysiert bestehende Mitigations-Mechanismen.

**Relevanz:** Theoretische Einordnung für die Meta-Report-Introduction. Warum
halluziniert die Baseline? Nicht weil Claude schlecht ist — sondern weil es ein
strukturelles LLM-Problem ist. Fetch-MCP ist genau die Art Mitigation die das
Paper empfiehlt: externes Gedächtnis statt parametrisches Wissen.

**IEEE-Zitat:**
Z. Xu, S. Jain, and M. Kankanhalli, "Hallucination is Inevitable: An Innate
Limitation of Large Language Models," arXiv preprint arXiv:2401.11817, 2024.

---

## Quelle 4 — Full Research Lifecycle mit LLM Agents
**Titel:** Agent Laboratory: Using LLM Agents as Research Assistants  
**Autoren:** S. Schmidgall et al.  
**Jahr:** 2025  
**arXiv:** 2501.04227  
**DOI:** https://doi.org/10.48550/arXiv.2501.04227  
**URL:** https://arxiv.org/abs/2501.04227  

**Abstract (gelesen):** Autonomes Framework das den vollständigen Forschungs-Lebenszyklus
managed — Literaturrecherche, Experimente, Report-Generierung. o1-preview + Human
Feedback produziert publikationsreife Outputs. 84% Kostensenkung vs. frühere Ansätze.

**Relevanz:** Direkter Systemvergleich zu unserer Pipeline. Agent Laboratory nutzt
Multi-Agent mit Human Feedback — wir nutzen Single-Agent mit Zero-Interrupt.
Der Unterschied (0 vs. N Eingriffe) ist ein klares Differenzierungsmerkmal für
unsere Methodology-Section.

**IEEE-Zitat:**
S. Schmidgall et al., "Agent Laboratory: Using LLM Agents as Research Assistants,"
arXiv preprint arXiv:2501.04227, 2025.

---

## Quelle 5 — Evaluation von Agentic AI Systemen
**Titel:** Beyond Task Completion: An Assessment Framework for Evaluating Agentic AI Systems  
**Autoren:** S. Akshathala et al.  
**Jahr:** 2025  
**arXiv:** 2512.12791  
**DOI:** https://doi.org/10.48550/arXiv.2512.12791  
**URL:** https://arxiv.org/abs/2512.12791  

**Abstract (gelesen):** Evaluationsframework jenseits einfacher Task-Completion-Metriken.
Vier Säulen: LLMs, Memory, Tools, Environment. Identifiziert "behavioral deviations
missed by conventional metrics" in einem CloudOps Use Case.

**Relevanz:** Direkt relevant für unsere Discussion-Section: Die Likert-Rebellion
ist exakt eine "behavioral deviation missed by conventional metrics". Unser
QC-Script (19/19 PASS) misst Task-Completion — aber nicht ob die statistische
Methode korrekt gewählt wurde. Das Paper liefert den konzeptuellen Rahmen.

**IEEE-Zitat:**
S. Akshathala et al., "Beyond Task Completion: An Assessment Framework for
Evaluating Agentic AI Systems," arXiv preprint arXiv:2512.12791, 2025.

---

## Quelle 6 — Halluzinierte URLs erkennen und korrigieren
**Titel:** Detecting and Correcting Reference Hallucinations in Commercial LLMs and Deep Research Agents  
**Autoren:** D. Rao, E. Wong, C. Callison-Burch  
**Jahr:** 2026  
**arXiv:** 2604.03173  
**DOI:** https://doi.org/10.48550/arXiv.2604.03173  
**URL:** https://arxiv.org/abs/2604.03173  

**Abstract (gelesen):** 3–13% halluzinierte Citations, 5–18% nicht-auflösbare URLs
über 10 LLM-Modelle. Open-Source-Tool "urlhealth" via Wayback Machine. Agentische
Selbstkorrektur reduziert problematische Citations um bis zu 79×.

**Relevanz:** Quantifiziert das Halluzinations-Problem in kommerziellen LLMs inkl.
Research Agents. Unsere Fetch-MCP-Lösung entspricht der Kategorie "tool-augmented
retrieval" die das Paper als effektivste Mitigation identifiziert. Gute Zahlen
(3-13%) als Benchmark für unsere Baseline-Beobachtung.

**IEEE-Zitat:**
D. Rao, E. Wong, and C. Callison-Burch, "Detecting and Correcting Reference
Hallucinations in Commercial LLMs and Deep Research Agents," arXiv preprint
arXiv:2604.03173, 2026.

---

## Verwendung im Meta-Report

| Quelle | Section | Zweck |
|--------|---------|-------|
| Lu et al. 2024 (AI Scientist) | Introduction + Related Work | Direkter Systemvergleich |
| Schmidgall et al. 2025 (Agent Lab) | Related Work | Multi-Agent vs. Single-Agent Vergleich |
| Xu et al. 2024 (Hallucination Inevitable) | Introduction | Theoretisches Fundament Halluzination |
| Rao & Callison-Burch 2026 (BibTeX) | Results 4.1 | Quantifizierung DOI-Halluzination |
| Rao et al. 2026 (URL Hallucination) | Results 4.1 | Benchmark-Zahlen (3–13%) |
| Akshathala et al. 2025 (Beyond Task) | Discussion | Rahmen für Likert-Rebellion |
