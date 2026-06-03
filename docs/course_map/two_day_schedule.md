# Two-Day Schedule

This schedule is designed for a cohort of 10–25 PhD students meeting in a single room with adequate WiFi and individual laptop access. Times are approximate. Sessions marked with a star (★) are the minimum viable set if time must be cut.

---

## Day 1 — From Zero to First Model

Day 1 moves from orientation and conceptual grounding through environment setup and data exploration, arriving at a working segmentation baseline and a structured failure analysis by the close of the afternoon. Students who have never touched a terminal before Day 1 should be able to complete Missions 0–3 with instructor support.

| Time | Activity | Duration | What Happens | Relevant Tutorial Page |
|------|----------|----------|--------------|------------------------|
| 09:00 | Opening and onboarding ★ | 30 min | Instructor introduces the course narrative and clinical motivation. GitHub Classroom links distributed. Students accept assignment and verify repo access. Brief round of introductions. | [Home](../index.md) |
| 09:30 | Foundations lecture: Clinical AI and the problem of translation ★ | 60 min | Lecture covering: what clinical AI is and is not; the gap between benchmark performance and clinical utility; the regulatory landscape; why the prompt-first approach is a research skill, not a shortcut. Q&A included. | [Clinical AI](../foundations/clinical_ai.md) · [Ethics](../foundations/ethics_privacy_and_safety.md) |
| 10:30 | **Mission 0 — Wake the Lab** ★ | 45 min | Instructor walks through M0 live with the class. Students verify environment: Python, dependencies, Claude Code access, data directory. First structured prompt: ask Claude Code to confirm the environment and list installed packages. Expected output: a green-status environment report. | [What Is Agentic Coding](../agentic_research/what_is_agentic_coding.md) · [Claude Code Workflow](../agentic_research/claude_code_workflow.md) |
| 11:15 | **Mission 1 — Receive the Signal** ★ | 60 min | Students work independently or in pairs. Load the BraTS-style MRI dataset. Inspect voxel spacing, intensity statistics, label coverage. Produce a one-page data quality report using a Claude Code prompt from the Prompt Library. Instructor circulates; common issues discussed as group. | [MRI Basics](../mri/what_is_mri.md) · [T1, T2, and FLAIR](../mri/t1_t2_flair.md) · [Data Inspection](../medical_ai_workflow/data_inspection.md) |
| 12:15 | **Lunch break** | 60 min | — | — |
| 13:15 | MRI and metrics lecture ★ | 45 min | Lecture covering: how MRI sequences encode tissue contrast; what Dice coefficient, sensitivity, and specificity mean in clinical imaging; common failure modes of segmentation models in brain tumour imaging. Emphasis on clinical interpretation, not mathematical derivation. | [Voxels, Slices, and Spacing](../mri/voxels_slices_and_spacing.md) · [Metrics](../medical_ai_workflow/metrics_dice_sensitivity_specificity.md) |
| 14:00 | **Mission 2 — Build the First Detector** ★ | 90 min | Students write a structured prompt directing Claude Code to implement a baseline segmentation model (threshold or atlas-based, depending on environment). Run on three MRI cases. Collect Dice, sensitivity, specificity for each case. Fill in the metrics table in the mission brief. Discuss early results as a class for the final 10 minutes. | [Baseline Modeling](../medical_ai_workflow/baseline_modeling.md) · [Segmentation Basics](../foundations/segmentation_basics.md) · [Modeling Prompts](../prompt_library/modeling_prompts.md) |
| 15:30 | **Mission 3 — Investigate Failure** | 60 min | Select the worst-performing case from M2. Write a structured failure analysis using the error analysis prompt template. Identify: was the failure a false positive, false negative, or boundary error? What tissue type was misclassified? Write a one-paragraph failure hypothesis. | [Error Analysis](../medical_ai_workflow/error_analysis.md) · [Brain Tumour Imaging](../foundations/brain_tumour_imaging.md) · [Error Analysis Prompts](../prompt_library/error_analysis_prompts.md) |
| 16:30 | Day 1 debrief ★ | 30 min | Whole-group discussion. Each participant or pair shares: (1) their worst Dice score, (2) their failure hypothesis in one sentence. Instructor synthesises common patterns. Students are asked to read [Prompt as Protocol](../agentic_research/prompt_as_experimental_protocol.md) before Day 2. | — |
| 17:00 | End of Day 1 | — | — | — |

---

## Day 2 — From Failure to Translation

Day 2 begins with a deeper methodological lecture, moves through an intentional improvement cycle, addresses study design, and closes with a formal translation assessment and student showcase. The emphasis shifts from building to reasoning: why does the model do what it does, and what would it take to trust it with a patient?

| Time | Activity | Duration | What Happens | Relevant Tutorial Page |
|------|----------|----------|--------------|------------------------|
| 09:00 | Error analysis lecture ★ | 45 min | Lecture covering: systematic frameworks for analysing segmentation failure (spatial, class-based, patient-subgroup); the distinction between model error and label error; how error analysis informs the next experiment rather than simply documenting failure. | [Error Analysis](../medical_ai_workflow/error_analysis.md) · [Model Improvement](../medical_ai_workflow/model_improvement.md) |
| 09:45 | **Mission 4 — Improve With Intent** ★ | 90 min | Students write a prediction: "If I change X, I expect metric Y to change by approximately Z because of biological/technical reason W." Then encode that prediction as a prompt modification. Re-run the pipeline. Measure the outcome against the prediction. Write a two-paragraph assessment of whether the intervention worked and what the discrepancy (if any) implies. | [Model Improvement](../medical_ai_workflow/model_improvement.md) · [Prompt Best Practices](../agentic_research/prompt_best_practices.md) |
| 11:15 | Prompting workshop | 45 min | Interactive session. Instructor presents three anonymised prompt examples from the current cohort — one excellent, one adequate, one problematic. Group critiques each on: specificity, verifiability, constraint completeness. Students then rewrite the problematic prompt. | [Prompt as Protocol](../agentic_research/prompt_as_experimental_protocol.md) · [Prompt Best Practices](../agentic_research/prompt_best_practices.md) · [Roles for Claude](../agentic_research/roles_for_claude.md) |
| 12:00 | **Mission 5 — Design the Next Study** ★ | 60 min | Using the Mission 5 brief as a scaffold, students write a prospective validation study design. Required elements: patient population, inclusion/exclusion criteria, reference standard, primary and secondary endpoints, sample size rationale, statistical analysis plan outline, anticipated sources of bias. Claude Code used to assist with literature-style structuring of the document. | [Study Design](../medical_ai_workflow/study_design.md) · [Reproducibility](../foundations/reproducibility.md) |
| 13:00 | **Lunch break** | 60 min | — | — |
| 14:00 | **Mission 6 — Translate Responsibly** ★ | 75 min | Students complete the clinical translation assessment using the structured template in the mission brief. Sections: (1) regulatory pathway identification; (2) TRIPOD+AI checklist completion; (3) failure mode catalogue from M3 revisited; (4) deployment prerequisites — what would need to be true before this system entered a real workflow? Final artefact is a one-page translation brief. | [Clinical Translation](../medical_ai_workflow/clinical_translation.md) · [Ethics](../foundations/ethics_privacy_and_safety.md) · [Translation Prompts](../prompt_library/translation_prompts.md) |
| 15:15 | Showcase preparation | 30 min | Groups prepare a 5-minute presentation covering: their best segmentation result, their worst, their failure hypothesis, and their single strongest argument from Mission 6. No slides required — the artefacts from the missions are sufficient. | — |
| 15:45 | Student showcase ★ | 60 min | Each group presents for 5 minutes; 3 minutes of questions from peers and instructor. Instructor facilitates cross-group discussion on divergent failure modes and contrasting translation arguments. | — |
| 16:45 | Closing | 20 min | Instructor summarises the research arc. Brief discussion of how prompt-first methods connect to students' own doctoral research. Pointers to the [From Lab to Your Own Research](../agentic_research/from_lab_to_your_own_research.md) chapter for follow-up. Course evaluation forms distributed. | [From Lab to Research](../agentic_research/from_lab_to_your_own_research.md) |
| 17:05 | End of Day 2 | — | — | — |

---

## Instructor Notes: What to Prioritise When Time Is Short

Unexpected delays are common in computational courses. The following guidance is for instructors managing a compressed timeline.

!!! warning "Instructor guidance — time compression"
    The sessions marked ★ in the tables above are the minimum viable set. If you must cut content, apply the following priority order:

    **Cut first (without breaking the arc):**

    - Mission 3 can be shortened to 30 minutes if students are asked to write only a failure hypothesis sentence rather than a full error analysis paragraph. The M4 intervention exercise still works with a brief hypothesis.
    - The prompting workshop on Day 2 (11:15) can be reduced to 20 minutes or moved to an optional evening session if students are running behind on M4.
    - Mission 5 (study design) can be assigned as a written take-home exercise if time does not permit in-session completion. The artefact is still available for reference in M6.

    **Do not cut:**

    - Mission 0 cannot be shortened significantly — environment failures discovered later cost more time than a careful M0 saves.
    - The Day 1 debrief is critical for cohort calibration. If students do not share their failure hypotheses before Day 2, the Day 2 error analysis lecture loses its concrete grounding.
    - The student showcase is pedagogically the most important session in the course. It is where students integrate everything and practise the kind of scientific communication they will need in clinic-facing research. Protect this time.

    **If hardware or software fails:**

    - Pre-computed segmentation outputs (included in the lab repo as `fallback_outputs/`) can substitute for live model runs in Missions 2 and 4. Missions 3, 5, and 6 are entirely reading-and-writing tasks that do not depend on live computation.
    - Claude Code access issues can be mitigated by working from the Prompt Library and demonstrating outputs from a pre-run session. The conceptual learning is preserved even without live AI interaction.
