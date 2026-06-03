# Assessment Rubric

!!! warning "Instructor Resource"
    This page is for instructors and teaching assistants. Share with students only after the course is complete and grades have been submitted.

The lab is assessed out of 100 points across eight categories. The rubric distinguishes between items that can be evaluated automatically (by checking artifact structure and reproducibility) and items that require human judgment (clinical reasoning quality, translation brief credibility). Both types of assessment are described below.

---

## Overview

| Category | Points | Primary assessor |
|---|---|---|
| 1. Artifact completeness | 10 | Automated |
| 2. Reproducibility | 10 | Automated + human |
| 3. Clinical reasoning — data and baseline | 10 | Human |
| 4. Error analysis quality | 15 | Human |
| 5. Controlled improvement | 20 | Human |
| 6. Study design | 15 | Human |
| 7. Clinical translation | 15 | Human |
| 8. Optional exploration | 5 | Human |
| **Total** | **100** | |

---

## Category 1: Artifact Completeness (10 points)

**Automated check.** All seven required output artifacts are present and structurally valid (parseable JSON, correct key names, non-empty content).

| Points | Criteria |
|---|---|
| 10 | All 7 artifacts present, all JSON files parse without error, all specified keys present in each artifact |
| 7–9 | 5–6 artifacts present and valid; or all artifacts present but 1–2 have missing keys |
| 4–6 | 3–4 artifacts present and valid |
| 1–3 | Fewer than 3 artifacts, or major structural errors throughout |
| 0 | No artifacts submitted |

Required artifacts: `outputs/preflight_report.json`, `outputs/m01_data_summary.json`, `outputs/m02_metrics.json`, `outputs/m03_error_analysis.json`, `outputs/m04_comparison.json`, `outputs/m05_study_design.md`, `reports/m06_translation_brief.md`.

---

## Category 2: Reproducibility (10 points)

**Automated + human check.** The automated component checks for a fixed random seed in the CLAUDE.md or in the pipeline code. The human component evaluates whether the CLAUDE.md and prompt log contain enough information for an independent researcher to reproduce the main result.

| Points | Criteria |
|---|---|
| 9–10 | Fixed seed declared; CLAUDE.md contains data path, research question, and output conventions; prompt log saved in `prompts/`; a second person could reproduce the Mission 2 result from the artifacts alone |
| 6–8 | Seed declared; CLAUDE.md present but incomplete; prompt log partially saved |
| 3–5 | No seed declared; CLAUDE.md minimal; some prompts saved |
| 0–2 | CLAUDE.md absent or empty; no prompt log; reproduction impossible |

---

## Category 3: Clinical Reasoning — Data and Baseline (10 points)

**Human review.** Assesses the quality of reasoning in the Mission 1 data summary and the Mission 2 baseline evaluation narrative. The question is not what Dice score they achieved but whether they understand what the Dice score means.

| Points | Criteria |
|---|---|
| 9–10 | Data summary identifies at least one clinically meaningful distributional property (e.g., tumour size variation, missing modalities). Baseline evaluation compares result to the BraTS reference range and names at least one interpretation of what the result implies about the model. |
| 6–8 | Data summary is present and structured. Baseline metrics reported. At least one interpretive comment that goes beyond restating the number. |
| 3–5 | Data summary is a raw table without interpretation. Metrics reported but not interpreted. |
| 0–2 | Data summary absent or contains only file paths. No clinical interpretation of baseline results. |

---

## Category 4: Error Analysis Quality (15 points)

**Human review.** Assesses Mission 3. The failure analysis is the highest-leverage analytical step in the course — a well-reasoned failure analysis directly enables Mission 4's controlled experiment.

| Points | Criteria |
|---|---|
| 13–15 | One primary failure mode identified using the taxonomy (undersegmentation / oversegmentation / boundary / location / fragmentation / subregion confusion). Anatomical location of failure stated. Clinical implication named specifically (e.g., "missed enhancing tumour in the posterior fossa would underestimate residual disease after surgery"). Failure hypothesis is falsifiable and stated before Mission 4 implementation. |
| 9–12 | Failure mode identified. Some anatomical specificity. Clinical implication named but not fully grounded. Hypothesis present but vague. |
| 5–8 | Failure mode described in general terms. No anatomical specificity. Clinical implication generic. |
| 0–4 | Failure analysis absent or consists only of low Dice score without characterisation. |

---

## Category 5: Controlled Improvement (20 points)

**Human review.** This is the largest single category because it assesses the core experimental competency: forming a falsifiable hypothesis, implementing exactly one change, and interpreting the result against the hypothesis.

| Points | Criteria |
|---|---|
| 18–20 | Hypothesis explicitly stated in `outputs/m04_comparison.json` before implementation (or in the prompt log with a timestamp before the implementation run). Single change implemented. Result compared directly to the stated hypothesis prediction. Conclusion notes whether the hypothesis was supported, partially supported, or refuted, and proposes an explanation for any discrepancy. |
| 13–17 | Hypothesis present. Single change implemented. Result reported and compared to baseline. Hypothesis-to-result comparison present but not fully explicit. |
| 8–12 | Hypothesis stated but multiple changes made, or hypothesis stated after implementation (post-hoc rationalisation). Result reported without comparison to hypothesis. |
| 3–7 | No hypothesis stated. Change made and result reported. |
| 0–2 | Mission 4 not completed, or multiple undocumented changes with no result interpretation. |

**Common failure mode for this category:** Students who change threshold, add a connected component filter, and adjust the minimum size cutoff simultaneously. If you see multiple simultaneous changes, assign points in the 3–7 range regardless of the quality of the reported result, because the result cannot be attributed to any single change.

---

## Category 6: Study Design (15 points)

**Human review.** Assesses Mission 5. The study design does not need to be clinically publishable — it needs to demonstrate that the student understands what a prospective validation study requires.

| Points | Criteria |
|---|---|
| 13–15 | Patient population specified with inclusion and exclusion criteria. Reference standard named and justified (why this standard, not another). At least one primary endpoint with metric named. Sample size rationale present (even if informal: "30 patients would give us approximately X power to detect a Dice difference of Y"). At least two sources of bias identified. Skeptical Reviewer role output present in the prompt log. |
| 9–12 | Population specified. Reference standard named. Endpoint named. Sample size stated without justification. One source of bias identified. |
| 5–8 | Population described in general terms. Endpoint is "Dice score" without specification. No sample size reasoning. |
| 0–4 | Study design absent or is a rephrasing of the Mission 4 experiment without prospective elements. |

---

## Category 7: Clinical Translation (15 points)

**Human review.** Assesses Mission 6. The key criterion is honesty: does the brief accurately represent what was and was not demonstrated? A brief that is technically accurate but overconfident should not score above 10.

| Points | Criteria |
|---|---|
| 13–15 | Clinical readiness level stated explicitly (Level 1 or 2 in the Clinical Readiness Spectrum). At least three specific limitations named (not generic). "What was not demonstrated" section present with at least three items. Human oversight mechanism specified. No language implying deployment readiness without explicit caveats. Regulatory pathway identified and correctly matched to system risk level. |
| 9–12 | Clinical readiness mentioned. Two or more specific limitations. Human oversight referenced. Minor overconfident language present but not central to the brief. |
| 5–8 | Limitations present but generic. No "what was not demonstrated" section. Regulatory pathway absent or incorrect. |
| 0–4 | Translation brief overconfident throughout. No limitations section. Implies system is ready for clinical use. |

**Automatic deduction:** Any translation brief that uses the phrase "ready for clinical use," "clinical-grade," or "deployable" without an immediate explicit caveat loses 5 points from this category, regardless of other quality. Document this deduction when providing feedback.

---

## Category 8: Optional Exploration (5 points)

**Human review.** Awarded for work that goes beyond the minimum mission requirements. Examples that qualify: second controlled experiment in Mission 4 with a different hypothesis; sample size power calculation in Mission 5; TRIPOD+AI checklist completion in Mission 6; additional error map visualisations for a second failing case; a written reflection on how the agentic methods would apply to the student's own research.

| Points | Criteria |
|---|---|
| 5 | Substantial optional work completed: constitutes a meaningful extension of one mission, not just additional formatting. |
| 3–4 | Minor optional work: one additional visualisation, one additional case analysed. |
| 1–2 | Minimal optional work: a brief note or additional bullet point. |
| 0 | No optional work. |

---

## Automated vs. Human Review Workflow

**Automated review** (Category 1 and part of Category 2) can be run using the grading script in the teacher-ta-repo (`tools/grade_artifacts.py`). This script checks artifact presence, JSON parseability, and key completeness. It does not assess content quality.

**Human review** (Categories 3–8) should be conducted by the instructor or a trained TA who has read these rubric descriptions and reviewed at least three student submissions together before grading independently. The most common inter-rater disagreements occur in Category 5 (controlled improvement — did the student state the hypothesis before or after implementation?) and Category 7 (translation — is this overconfident or appropriately confident?). When in doubt, discuss with a co-assessor before assigning a score.

**Feedback timing:** Return scores and written feedback within 5 business days of the course end. Students should receive at minimum: their score in each category, one specific strength, and one specific area for improvement. For Category 5 and 7, quote the specific text that informed the score.
