# Translation and Communication Prompts

Use these templates during Missions 5 and 6 — Design the Next Study and Translate Responsibly. These prompts shift focus from model performance to clinical reality. A model with Dice 0.85 that no clinician can interpret, trust, or use has not achieved anything clinically meaningful.

These prompts ask Claude to translate between the technical world you have been working in and the clinical, regulatory, and institutional worlds the model must eventually enter.

---

## 1. Clinician Summary Prompt

**When to use:** When you need to explain your results to a clinician collaborator, hospital administrator, or ethics committee — anyone who will not understand Dice scores or loss curves.

**Why it works:** Asking Claude to write for a specific clinician persona prevents the most common communication failure: writing what is technically accurate but clinically unintelligible. Requiring concrete clinical analogies, avoiding all abbreviations, and specifying the exact audience forces a genuine translation.

**Failure it prevents:** A one-page summary that says "our model achieved mean Dice of 0.82 for whole tumour segmentation using a 2D U-Net trained with categorical cross-entropy loss" — which communicates nothing to a neurosurgeon, and may actually reduce their confidence.

**Customisation:** Replace `[CLINICIAN_ROLE]` with the specific audience (neurosurgeon, neuro-oncologist, radiologist, oncology nurse). Adjust the clinical context and the metric translations based on your actual results.

```
Write a plain-language summary of our brain tumour segmentation model results for a [CLINICIAN_ROLE].

Assume the reader:
- Has no knowledge of machine learning, neural networks, or technical metrics
- Understands brain tumour anatomy (GBM, oedema, enhancing tumour)
- Is familiar with MRI but not with how AI processes it
- Cares primarily about: will this be useful, will it be safe, what does it do that I cannot?

Our results (fill in your actual values):
- What the model does: automatically outlines brain tumours on MRI scans
- Tumour regions it identifies: the whole tumour, the tumour core, and the enhancing portion
- How accurate it is: [DICE_WT]% overlap with expert neuroradiology annotation for whole tumour
- Where it struggles: [DESCRIBE FAILURE CASES IN PLAIN TERMS]
- What it was trained on: [N] MRI scans from [DESCRIBE DATASET]
- What it has NOT been tested on: scans from different hospitals, scanners, or patient populations

Write a 3-paragraph summary:
Paragraph 1: What the system does, in one concrete sentence. Then explain the accuracy
in clinical terms — e.g. "For every 10 voxels a neuroradiologist marks as tumour, our
model correctly identifies approximately [X] of them."
Paragraph 2: What the system cannot do yet. Be honest about limitations.
Do not use the word "limitations" — instead say "what this system is not ready for."
Paragraph 3: What the next step would be before this system could be used alongside
a clinical team. (One or two specific validation steps, not a general disclaimer.)

Rules:
- No acronyms (write out Dice, U-Net, NIfTI in full or omit them)
- No reference to training, epochs, loss functions, or model architecture
- Every claim about accuracy must be translatable to "this means that in practice, [X]"
- Maximum length: one page (approximately 400 words)
```

---

## 2. Regulatory Pathway Prompt

**When to use:** Mission 6, when discussing what it would take to move this model from a research lab to clinical use.

**Why it works:** Regulatory pathways are specific and consequential. Vague statements like "this would need FDA approval" are not useful. This prompt asks Claude to identify the specific device class, the relevant clearance pathway, and the concrete evidence requirements — which gives the discussion a grounded structure that clinicians and hospital leadership can engage with.

**Failure it prevents:** The common mistake of treating regulatory compliance as an afterthought ("we will deal with that later") or as a binary ("it either has approval or it doesn't"), when in fact it is a multi-year, evidence-intensive process that must be designed for from the start.

**Customisation:** Specify the jurisdiction (`[US_FDA / EU_MDR / UK_MHRA]`). Update the intended use statement to match your model's actual function. If the model is intended as decision support (not autonomous), state that clearly.

```
Act as a regulatory affairs consultant with expertise in [US_FDA / EU_MDR / UK_MHRA] for AI-based medical devices.

Device description: an AI software tool that automatically segments brain tumours (whole tumour,
tumour core, enhancing tumour) on multi-parametric MRI, intended to assist neuroradiologists
in treatment planning and monitoring for glioblastoma.

Intended use: decision support — the output is reviewed and confirmed by a qualified physician
before clinical action is taken.

Provide a regulatory pathway summary covering:

1. Device classification
   - Under [FDA 21 CFR Part / EU MDR Annex VIII / appropriate framework]: what risk class is this?
   - What is the primary predicate device or rule that determines this classification?
   - Why is this classification and not a higher or lower one?

2. Clearance pathway
   - What is the most likely approval route? (e.g. 510(k), De Novo, PMA for FDA; Class IIa/IIb CE Mark for EU)
   - What is a realistic timeline from submission to clearance?
   - What are the key submission requirements?

3. Clinical evidence requirements
   - What clinical study design would be required? (prospective / retrospective, N cases, multi-site?)
   - What comparator is needed? (radiologist performance? existing cleared software?)
   - What performance metrics does the regulator expect?

4. Software as a Medical Device (SaMD) specific requirements
   - What AI/ML-specific guidance applies? (e.g. FDA's AI/ML Action Plan, EU MDCG 2021-6)
   - What does the predetermined change control plan (PCCP) need to address?
   - What post-market surveillance is required?

5. Three things we should be building into the model development process right now
   (before any regulatory submission) that will reduce regulatory risk later.

Present as a structured briefing document. Use plain language where possible,
but retain technical regulatory terms where they are essential.
```

---

## 3. Study Design Prompt

**When to use:** Mission 5 — when designing the next step after the lab, whether a formal validation study, a prospective clinical trial, or a reader study.

**Why it works:** Study design has specific components — sample size, comparator, endpoint, blinding, statistical analysis plan — that must all be specified before data collection begins. Asking Claude to produce a study design protocol rather than a research idea forces these decisions to be made explicitly, which is both more rigorous and more useful to a clinical collaborator.

**Failure it prevents:** Designing a study that cannot answer the research question because the comparator was wrong, the sample size was too small, or the primary endpoint was not pre-specified — which are the most common reasons clinical AI validation studies fail peer review.

```
Act as a clinical trials methodologist and help me design a validation study for our brain tumour segmentation model.

Model summary:
- Task: automatic GBM tumour segmentation (WT, TC, ET) on multi-parametric MRI
- Current performance: [DICE_WT], [DICE_TC], [DICE_ET] on BraTS test set
- Training data: BraTS [YEAR], [N] cases, [DESCRIBE SCANNER/SITE]
- Current limitations: [FROM YOUR ERROR ANALYSIS]

Research question: [STATE YOUR PRIMARY QUESTION]
(e.g. "Can this AI tool reduce the time required for radiotherapy target volume delineation
while maintaining non-inferior agreement with expert neuroradiologist annotation?")

Design the study with these sections:

1. Study type and design
   - Prospective or retrospective?
   - Single-site or multi-site?
   - Randomised or observational?
   - Justify each choice based on the research question.

2. Participants
   - Inclusion criteria (diagnosis, scan protocol, scanner type)
   - Exclusion criteria (prior surgery, incomplete modalities, paediatric cases)
   - Sample size: calculate N based on:
     * Expected primary endpoint value for AI and comparator
     * Desired power (80% or 90%)
     * Alpha level (0.05, two-tailed)
     * Expected dropout rate
     * Show the calculation explicitly

3. Intervention and comparator
   - Intervention: AI-assisted delineation (describe workflow)
   - Comparator: [radiologist alone / radiologist + AI / existing software / random effects model]
   - Primary endpoint: [Dice / time-to-delineation / inter-rater variability / clinical agreement]
   - Secondary endpoints: list at least 3

4. Blinding and randomisation
   - Who is blinded to what?
   - How are cases assigned to reader or condition?

5. Statistical analysis plan (pre-specified)
   - Primary analysis: what statistical test, what non-inferiority margin or superiority threshold?
   - How will you handle missing data?

6. Regulatory and ethical requirements
   - What IRB/ethics approval is needed?
   - Is patient consent required?
   - What data protection considerations apply (HIPAA / GDPR)?

7. Timeline and resource estimate
   - Realistic timeline from protocol approval to publication
   - Key resource requirements (reader time, computing, data storage)
```

---

## 4. Readiness Assessment Prompt

**When to use:** Mission 6, as the final structured exercise — to produce an honest assessment of where the model sits on the readiness scale and what it would take to move it forward.

**Why it works:** "Readiness" is often treated as binary. In clinical AI, it is a continuum with specific evidence requirements at each stage. This prompt forces a structured assessment against a defined framework, which produces an honest answer rather than an optimistic one.

**Failure it prevents:** Concluding that a model "could be used clinically" because its Dice is high, without considering external validation, regulatory status, integration into clinical workflow, or clinician trust — all of which are necessary conditions for clinical use.

```
Act as a clinical AI readiness assessor. Evaluate the current state of our brain tumour
segmentation model against the FDA AI/ML Readiness Framework stages.

Model details:
- Current Dice (WT/TC/ET): [VALUES]
- Tested on: BraTS [YEAR] only (internal test set)
- External validation: [none / describe]
- Prospective testing: [none / describe]
- Regulatory status: research prototype, no submission
- Clinical integration: [none / describe pilot]
- Clinician engagement: [none / describe]

Assess against each stage:

Stage 1 — Algorithmic Maturity
Criteria: Performance on held-out internal test set exceeds defined threshold
Evidence required: per-case metrics, confidence intervals, failure case analysis
Our status: [your honest assessment]
Gap: [what is missing]

Stage 2 — Internal Validation
Criteria: Performance on prospective cases from same institution
Evidence required: prospective cohort, temporal split, scanner consistency check
Our status: [your honest assessment]
Gap: [what is missing]

Stage 3 — External Validation
Criteria: Performance on data from a different institution and scanner
Evidence required: multi-site study, demographic diversity, different scanner vendors
Our status: [your honest assessment]
Gap: [what is missing]

Stage 4 — Clinical Integration
Criteria: AI output integrated into clinical workflow, clinician trust established
Evidence required: usability study, time-motion analysis, reader study
Our status: [your honest assessment]
Gap: [what is missing]

Stage 5 — Regulatory Clearance and Post-Market
Criteria: Regulatory submission made or cleared, post-market surveillance plan active
Evidence required: regulatory submission, real-world performance monitoring
Our status: [your honest assessment]
Gap: [what is missing]

Summary:
- Current stage: [Stage X]
- Minimum evidence needed to reach Stage [X+1]: [list 3 specific things]
- Realistic timeline to Stage 3 (external validation), assuming dedicated effort: [estimate]
- One thing about the current model that would be a barrier at every stage: [honest answer]
```

---

## 5. Stakeholder Communication Prompt

**When to use:** When presenting results to a mixed audience — clinicians, administrators, funders, ethicists, patients — each of whom has different concerns and different knowledge.

**Why it works:** A single slide deck or report cannot serve all audiences simultaneously. This prompt asks Claude to produce differentiated communications for each stakeholder type, drawing on the same underlying evidence. Differentiating by audience concern (not just vocabulary level) is the key skill.

**Failure it prevents:** Presenting technical results to a hospital ethics committee and losing their trust because the language implied clinical deployment readiness that does not exist. Or presenting to funders with so many caveats that the actual achievements are invisible.

```
Based on our brain tumour segmentation project, produce tailored one-paragraph communications
for each of the following stakeholder groups.

Project results to communicate:
- Achievement: [BRIEF TECHNICAL SUMMARY OF WHAT YOU DID AND YOUR KEY RESULT]
- Stage: research prototype, internally validated on BraTS
- Limitations: [KEY LIMITATIONS FROM ERROR ANALYSIS]
- Next step: [PROPOSED NEXT STUDY OR ACTION]

Write one paragraph (100-150 words) for each audience:

1. Neurosurgery Department Head
   Primary concern: clinical utility, patient safety, workflow disruption
   Avoid: technical metrics, model architecture
   Include: what the AI does for patients, what it does not do, what a pilot would look like

2. Hospital Data Governance / Ethics Committee
   Primary concern: data privacy, algorithmic bias, liability, consent
   Avoid: performance claims without limitations
   Include: training data source, bias risks, what oversight is built in, what approval is needed

3. Research Funder
   Primary concern: novelty, impact, return on investment, clear next milestone
   Avoid: excessive caveats that obscure achievement
   Include: what was accomplished, why it matters, what the specific next milestone is and its cost

4. Patient Advocacy Group
   Primary concern: benefit to patients, transparency, when this might be available
   Avoid: jargon, false hope, vague timelines
   Include: what the system could eventually help with, what stage of development it is at, how patients could be involved

5. Junior Researchers / Students Joining the Project
   Primary concern: what the current state is, what they will be working on, what skills are needed
   Include: honest summary of current model quality, specific open problems, what tools are used

After the five paragraphs, note: which two stakeholders have the most conflicting communication needs,
and how would you handle a meeting where both are present?
```

---

## Quick Reference

| Template | Audience | Key Skill Practised |
|---|---|---|
| Clinician Summary | Clinician collaborator | Technical-to-clinical translation |
| Regulatory Pathway | Regulatory / legal team | Navigating SaMD frameworks |
| Study Design | Clinical research collaborators | Rigorous validation planning |
| Readiness Assessment | Internal team | Honest gap analysis |
| Stakeholder Communication | Mixed audiences | Differentiated communication |
