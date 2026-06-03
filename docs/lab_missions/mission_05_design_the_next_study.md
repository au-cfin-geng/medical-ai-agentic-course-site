# Mission 5 — Design the Next Study

You have trained and evaluated a model. Now you must answer a harder question: what would it take to know whether this model actually works in a hospital? This mission moves from computational researcher to clinical researcher. The skills are different, the vocabulary is different, and the stakes are different.

---

## Scientific Purpose

Internal validation on BraTS data tells you that a model learned something from the BraTS distribution. It does not tell you that the model will generalise to patients at your institution, to data from different scanners, to pre-operative imaging from patients with different tumour subtypes, or to clinical workflows where a radiologist will act on the model's output. The gap between internal benchmark performance and clinical utility is where most medical AI fails — not because the algorithms are wrong, but because the validation studies were not designed to detect the failures that matter clinically. This mission is an exercise in prospective thinking: before you build more, you must specify what evidence would convince a clinical partner, a regulatory body, and a patient that this technology is safe and useful.

---

## Required Background Reading

Before starting this mission, read the following pages on this site:

- [Study Design](../medical_ai_workflow/study_design.md) — understand the components of a clinical AI validation study: endpoints, reference standard, sample size, design type
- [Clinical Translation](../medical_ai_workflow/clinical_translation.md) — understand the regulatory and deployment considerations that shape study design
- [Clinical AI](../foundations/clinical_ai.md) — understand what clinical evidence is and how it differs from benchmark performance
- [Ethics, Privacy and Safety](../foundations/ethics_privacy_and_safety.md) — understand the ethical framework that must inform study design

---

## What You Will Ask Claude to Build

Your goal is to produce a structured clinical validation study protocol for the segmentation model developed in Missions 2-4. This is a writing task, guided by Claude acting as a clinical research methodologist. The protocol should read like the Methods section of a clinical AI paper — specific enough that someone could execute the study from your description.

The protocol must cover: the clinical question the study is designed to answer (not "does the model work?" but a specific question like "does AI-assisted segmentation reduce inter-observer variability in tumour volume measurement for treatment planning?"); the target population with explicit inclusion and exclusion criteria; a description of the AI system being evaluated; the reference standard (how ground truth will be established — by consensus of how many radiologists? using what criteria?); the primary endpoint (one metric, pre-specified, with a pre-specified threshold for clinical success); a rough sample size justification; the study design (prospective or retrospective? multi-centre? single arm or comparator?); ethical considerations including patient consent, data governance, and what would trigger early stopping; and the statistical analysis plan.

Instruct Claude to ask you one clarifying question at a time before making assumptions. This is important — if Claude makes all the assumptions itself, the protocol will not reflect your actual clinical context.

---

## Expected Artifacts

| Filename | Contents | What Correct Looks Like |
|---|---|---|
| `results/study_design/study_proposal.md` | Full structured study protocol | All sections above are present; written in academic clinical research language; cites at least one relevant methodological reference (TRIPOD, STARD, or similar) |
| `results/study_design/eligibility_criteria.md` | Inclusion and exclusion criteria | Specific enough that a research nurse could apply them; includes rationale for each criterion |
| `results/study_design/primary_endpoint.md` | Pre-specified primary endpoint and success threshold | One metric; one threshold; references the Mission 2/4 results as context for what threshold is plausible |

A valid study proposal does not need to be long. A 2-page document that specifies the clinical question, population, reference standard, primary endpoint with threshold, and sample size estimate is more valuable than a 10-page document full of vague aspirations.

---

## How to Inspect Results

**The clinical question.** Read the first paragraph. Is the clinical question answerable by the specific model you trained? If your model segments whole tumour on BraTS-style MRI, the study should evaluate whole-tumour segmentation accuracy, not survival prediction or pathology classification. If there is a mismatch between the model's output and the clinical question, the study design is invalid.

**The primary endpoint.** Is it the same metric you used in your model development (Dice, sensitivity, specificity)? If you developed the model using Dice but the primary endpoint is "time saved per case," the study is not measuring what you optimised for — and that is a red flag. If they differ, there should be an explicit justification.

**The sample size.** Is it plausible? A sample size of 10 is never sufficient for a clinical validation study. A sample size of 10,000 might be unnecessarily large for a feasibility study. Ask Claude to show the calculation — even a rough one. What assumptions went into it?

**The reference standard.** Who produces the ground truth in this study? If it is a single radiologist, that is a weak reference standard — radiologist inter-observer variability for brain tumour segmentation is substantial. The protocol should specify at least two independent annotators with a consensus procedure.

**The ethics section.** Does it mention patient consent? Data governance? What happens if the model harms a patient? If the ethics section is a single sentence, it is inadequate. Ask Claude to expand it.

---

## Prompt Principle

**Use a collaborative expert role with one-question-at-a-time clarification.**

Study design requires assumptions about your clinical context that Claude cannot know. The most productive approach is to ask Claude to interview you — to elicit the information it needs before drafting. This produces a protocol that reflects your actual situation rather than a generic template.

!!! failure "One-shot study design"
    ```
    Write a clinical validation study for my brain tumour segmentation model.
    ```
    Claude produces a generic template. The clinical question, eligibility criteria, and sample size are plausible but not grounded in your specific model, institution, or patient population. You sign off on it without engaging with the assumptions.

!!! success "Collaborative expert with elicitation"
    ```
    Act as a clinical research methodologist specialising in AI medical device evaluation.
    Your goal is to help me draft a clinical validation study protocol for the model I developed
    in this course.

    Before drafting anything, ask me one clarifying question at a time about:
    - The specific clinical task the model performs
    - The clinical setting where it would be deployed (e.g., pre-operative planning, routine surveillance)
    - Whether the comparison is AI alone, AI-assisted, or AI vs standard of care
    - What outcome matters to clinicians (time saved? measurement accuracy? detection sensitivity?)
    - What patient population is realistic at my institution

    After you have asked all necessary questions and I have answered them, draft a protocol
    following the TRIPOD-AI reporting guideline structure.
    Save the final protocol to results/study_design/study_proposal.md.
    ```

The principle: **expert role + elicitation before drafting + explicit reporting standard.** The protocol you produce will reflect your actual research context, not a generic template.

---

## Reflection Questions

1. Your model was developed and internally validated on BraTS data. Your study protocol proposes to evaluate it at a different institution with a different scanner. What differences between the BraTS dataset and your local data might cause the model's performance to differ? How would you detect these differences before the study starts?

2. You pre-specified a Dice > 0.80 threshold for clinical success. A colleague says this threshold is too low — a clinician relying on this segmentation would need Dice > 0.90 to trust it for treatment planning. How would you respond? What evidence would you need to settle this disagreement?

3. Your study design is retrospective (you will use historical scans). What are the specific limitations of a retrospective study for evaluating a clinical AI tool? Under what circumstances would a prospective study be required?

4. The ethics section of your protocol mentions patient consent. For a study using only retrospective de-identified data, is patient consent required? The answer varies by jurisdiction and institution. What is the process for determining this at a real hospital?

5. Your study has a pre-specified primary endpoint. After you run the study, you notice that the model performs poorly on one specific subgroup (e.g., paediatric patients). You want to report this subgroup finding. What is the risk of reporting an unplanned subgroup analysis? What language should you use when reporting it?

---

## Optional Challenge

Write a simplified CONSORT-style flow diagram (in Mermaid or as a table) showing how patients would flow through your study: how many are screened, how many are excluded for each exclusion criterion, how many complete the study, and how many are included in the primary analysis. This diagram is a standard component of clinical trial reporting and forces you to think concretely about how many patients you need to screen to enrol your target sample size.

---

## Common Failure Modes

**The study uses the same dataset the model was trained on.** This is internal validation, not external validation. A study that evaluates a model on data it was trained on produces an optimistic and clinically misleading estimate of performance. The study population must be independent of the training data.

**The primary endpoint is vague or composite.** "The model must perform well" is not an endpoint. "The model must achieve mean Dice >= 0.82 on the primary tumour region in the target population" is an endpoint. Vagueness invites post-hoc redefinition — the statistical equivalent of moving the goalpost.

**Sample size picked arbitrarily without calculation.** "We will recruit 100 patients" without any calculation is not a scientific decision. Ask Claude to show a rough power calculation, even if it is based on approximate assumptions. The calculation forces clarity about the expected effect size and the acceptable error rates.

**Ethics section is one sentence.** Regulatory reviewers and IRBs will reject study protocols that do not engage seriously with ethics. The protocol must address patient consent, data security, benefit-to-risk ratio, and the process for handling unexpected findings.

**The study design does not include a clinical comparator.** A study that says "the AI achieves Dice 0.85" answers "is the AI accurate?" but not "is the AI better than the current standard?" For a study to support clinical deployment, there must be a comparison — either to unaided radiologists, to a different measurement method, or to historical standards.

---

## Expected Learning Outcome

After completing this mission you can: draft a structured clinical validation study protocol with a pre-specified primary endpoint; apply the distinction between internal and external validation; describe the components of a reference standard and why a single annotator is insufficient; articulate why sample size justification is a scientific requirement, not a formality; use Claude in a collaborative elicitation mode to produce context-specific documents rather than generic templates.
