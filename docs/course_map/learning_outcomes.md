# Learning Outcomes

By the end of this two-day course, participants will have achieved a structured set of competencies organised across three domains: Knowledge, Skills, and Attitudes. Each outcome is mapped to the specific lab mission where it is assessed or practised, so that participants can trace the connection between what they learn conceptually and where they apply it.

The distinction between domains is deliberate. Knowledge outcomes can be assessed in conversation or short-answer form. Skill outcomes require a produced artefact. Attitude outcomes are observable in the quality of reasoning students bring to the showcase and the mission reflection questions.

---

## Domain 1: Knowledge

*What students will know and be able to explain at the end of the course.*

### K1 — Scope and Limitations of Clinical AI

Students will be able to explain what clinical AI systems can and cannot do: the distinction between association and causation in ML models; why high benchmark accuracy does not imply clinical safety; how training data distribution shapes what a model can generalise to; and why model outputs require clinical interpretation rather than blind acceptance.

**Assessed in:** Mission 6 translation brief; Day 1 debrief discussion
**Tutorial sections:** [Clinical AI](../foundations/clinical_ai.md), [Ethics, Privacy and Safety](../foundations/ethics_privacy_and_safety.md)

---

### K2 — MRI Contrast Types and Clinical Relevance

Students will be able to describe the four standard sequences used in brain tumour imaging (T1, T1 post-gadolinium contrast, T2, FLAIR), explain what tissue property each sequence is sensitive to, and identify the clinical role of each sequence in tumour characterisation and treatment response assessment.

**Assessed in:** Mission 1 data quality report; Mission 3 failure analysis
**Tutorial sections:** [What Is MRI](../mri/what_is_mri.md), [T1, T2, and FLAIR](../mri/t1_t2_flair.md), [Brain Tumour Imaging](../foundations/brain_tumour_imaging.md)

---

### K3 — Segmentation Metrics in Clinical Terms

Students will be able to define Dice coefficient, sensitivity, and specificity; explain each metric using clinical language that a radiologist or oncologist would recognise (e.g., "sensitivity is the fraction of true tumour voxels that the model detects; missing tumour has different clinical consequences from over-calling it"); and identify the clinical implications of each type of error for treatment planning and follow-up.

**Assessed in:** Mission 2 metrics table; Mission 3 failure analysis; Mission 5 study design endpoints
**Tutorial sections:** [Metrics](../medical_ai_workflow/metrics_dice_sensitivity_specificity.md), [Error Analysis](../medical_ai_workflow/error_analysis.md)

---

### K4 — Regulatory Frameworks for AI Medical Devices

Students will be able to name the primary regulatory frameworks governing clinical AI in major jurisdictions (FDA 510(k) in the USA; MDR Class IIb in the EU); explain the TRIPOD+AI reporting standard for transparent reporting of AI prediction models; and describe what constitutes a Software as a Medical Device (SaMD) under current guidance.

**Assessed in:** Mission 6 translation brief
**Tutorial sections:** [Clinical Translation](../medical_ai_workflow/clinical_translation.md), [Ethics, Privacy and Safety](../foundations/ethics_privacy_and_safety.md)

---

### K5 — Ethical Risks in Clinical AI Deployment

Students will be able to identify at least five categories of ethical risk in clinical AI systems: training data bias; labelling subjectivity; demographic underrepresentation; automation bias in clinical users; and opacity of model reasoning. Students will be able to describe one concrete mitigation strategy for each category.

**Assessed in:** Mission 6 failure mode catalogue; reflection questions in M1 and M3
**Tutorial sections:** [Ethics, Privacy and Safety](../foundations/ethics_privacy_and_safety.md), [Clinical Translation](../medical_ai_workflow/clinical_translation.md)

---

## Domain 2: Skills

*What students will be able to do with the tools and knowledge provided.*

### S1 — Dataset Inspection and Quality Assessment

Students will be able to load a multi-contrast MRI dataset in NIfTI format, inspect voxel spacing and orientation metadata, compute intensity histograms per sequence, compare label coverage across cases, and identify at least two data quality issues that could affect downstream modelling.

**Assessed in:** Mission 1 data quality report
**Tutorial sections:** [Voxels, Slices, and Spacing](../mri/voxels_slices_and_spacing.md), [Quality Control](../mri/quality_control.md), [Data Inspection](../medical_ai_workflow/data_inspection.md)

---

### S2 — Structured Prompt Writing for Research Tasks

Students will be able to write a structured research prompt containing: a role specification for the AI agent; a clear task description; relevant constraints (output format, data paths, library preferences); success criteria that allow the student to verify the output; and a request for explanation of any assumption the agent makes. Students will be able to distinguish a high-quality prompt from a vague one by applying the specificity, verifiability, and constraint criteria practised in the Day 2 prompting workshop.

**Assessed in:** Prompts submitted with Missions 0–4; prompting workshop participation
**Tutorial sections:** [Prompt as Protocol](../agentic_research/prompt_as_experimental_protocol.md), [Prompt Best Practices](../agentic_research/prompt_best_practices.md), [Roles for Claude](../agentic_research/roles_for_claude.md)

---

### S3 — Running and Interpreting a Segmentation Pipeline

Students will be able to direct Claude Code to implement and run a segmentation pipeline on provided MRI data; collect and organise the resulting metric output; visualise segmentation overlays on axial, coronal, and sagittal slices; and interpret the numerical results in the context of published BraTS benchmark performance and clinical acceptability thresholds.

**Assessed in:** Mission 2 metrics table and overlay figure; Mission 4 comparison table
**Tutorial sections:** [Segmentation Basics](../foundations/segmentation_basics.md), [Baseline Modeling](../medical_ai_workflow/baseline_modeling.md), [Metrics](../medical_ai_workflow/metrics_dice_sensitivity_specificity.md)

---

### S4 — Structured Error Analysis

Students will be able to select the worst-performing case from their pipeline output; classify failure mode by type (false positive excess, false negative excess, boundary inaccuracy); identify the anatomical or biological context of the failure (e.g., failure at the tumour-oedema boundary in FLAIR sequences); write a falsifiable hypothesis about the cause; and describe one testable intervention that would confirm or refute the hypothesis.

**Assessed in:** Mission 3 failure analysis document; Mission 4 prediction statement
**Tutorial sections:** [Error Analysis](../medical_ai_workflow/error_analysis.md), [Brain Tumour Imaging](../foundations/brain_tumour_imaging.md)

---

### S5 — Clinical Validation Study Design

Students will be able to draft the core elements of a prospective validation study for a segmentation model: a clearly specified patient population with inclusion and exclusion criteria; a reference standard definition; a primary quantitative endpoint with a prespecified minimum acceptable performance; a sample size rationale; and at least two anticipated sources of bias and proposed mitigations.

**Assessed in:** Mission 5 study design document
**Tutorial sections:** [Study Design](../medical_ai_workflow/study_design.md), [Reproducibility](../foundations/reproducibility.md)

---

## Domain 3: Attitudes

*How students will approach AI-assisted research after this course.*

### A1 — Scientific Scepticism Toward AI Outputs

Students will approach any AI-generated output — code, analysis, written text, model prediction — as a hypothesis to be verified rather than a result to be reported. They will habitually ask: what could be wrong about this output, and how would I know? This attitude will be evidenced by the quality of verification steps included in their mission artefacts and by the questions they ask during the showcase.

**Assessed in:** Mission 3 failure analysis; Mission 4 prediction-vs-outcome assessment; showcase discussion
**Tutorial sections:** [Debugging with Claude](../agentic_research/debugging_with_claude.md), [Reproducibility](../foundations/reproducibility.md)

---

### A2 — Researcher Responsibility in AI-Assisted Work

Students will recognise that the researcher remains responsible for the scientific and ethical quality of any work that AI tools assist with. The agent does not assume responsibility for false negatives in a clinical model; the researcher who deployed it does. This attitude shifts the framing of agentic coding from "the AI does the work" to "I direct work that I am accountable for." It will be evidenced in the Mission 6 translation brief, where students must argue in first-person terms about what they would need to believe before recommending deployment.

**Assessed in:** Mission 6 translation brief; Day 2 debrief discussion
**Tutorial sections:** [Ethics, Privacy and Safety](../foundations/ethics_privacy_and_safety.md), [From Lab to Your Own Research](../agentic_research/from_lab_to_your_own_research.md)

---

### A3 — Distinguishing Model Performance from Clinical Readiness

Students will resist the conflation of good metrics with clinical adequacy. They will be able to articulate the conditions under which a model with moderate metrics could still be clinically useful, and conditions under which a model with strong metrics could still be clinically harmful. This attitude is the integrating competency of the course: it draws on every knowledge and skill outcome above.

**Assessed in:** Mission 6 translation brief; student showcase presentation; reflection questions across all missions
**Tutorial sections:** [Clinical Translation](../medical_ai_workflow/clinical_translation.md), [Clinical AI](../foundations/clinical_ai.md)

---

## Outcome Map Summary

The following table maps every learning outcome to the mission where it is primarily developed and the mission where it is primarily assessed (which are sometimes the same, and sometimes different).

| Outcome | Primary Development | Primary Assessment |
|---------|--------------------|--------------------|
| K1 — Scope and limitations of clinical AI | Day 1 lecture; M0–M1 reading | M6 translation brief |
| K2 — MRI contrast types and clinical relevance | Foundations lecture; M1 | M1 data report; M3 failure analysis |
| K3 — Segmentation metrics in clinical terms | Metrics lecture; M2 | M2 metrics table; M5 endpoints |
| K4 — Regulatory frameworks | M6 brief reading | M6 translation brief |
| K5 — Ethical risks in clinical AI deployment | Foundations lecture; M1 reflection | M6 failure mode catalogue |
| S1 — Dataset inspection and quality assessment | M1 | M1 data quality report |
| S2 — Structured prompt writing | M0–M2; prompting workshop | Prompts from M0–M4 |
| S3 — Running and interpreting a segmentation pipeline | M2 | M2 metrics table; M4 comparison |
| S4 — Structured error analysis | M3 | M3 failure document; M4 prediction |
| S5 — Clinical validation study design | M5 | M5 study design document |
| A1 — Scientific scepticism toward AI outputs | M3–M4 | M3; M4; showcase |
| A2 — Researcher responsibility | M6; Day 2 debrief | M6 brief; debrief discussion |
| A3 — Distinguishing performance from readiness | M2–M6 | M6 brief; showcase |
