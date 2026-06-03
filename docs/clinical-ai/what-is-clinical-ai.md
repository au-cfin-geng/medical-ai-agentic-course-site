# What Is Clinical AI?

Clinical AI refers to machine learning systems applied to clinical data — imaging, laboratory values, clinical notes, genomics, or waveforms — to support diagnosis, prognosis, treatment planning, or workflow automation. The defining feature is the operational context: the outputs of these systems influence decisions about real patients, which creates obligations around safety, reliability, and oversight that do not apply to general-purpose AI.

## Types of Clinical AI Tasks

Clinical AI tasks fall into several broad categories. **Classification** assigns a label to a study or patient — benign vs malignant, high-risk vs low-risk, positive vs negative. **Detection** localises findings within an image — flagging a pulmonary nodule, marking a microbleed, identifying a fracture line. **Segmentation** delineates exact boundaries — tracing the tumour margin, measuring organ volume, tracking lesion extent over time. **Prognosis** predicts future outcomes from current data — survival probability, treatment response, readmission risk. **Workflow automation** handles administrative and logistical tasks — prioritising worklists, routing urgent studies, pre-populating reports.

This course focuses on segmentation, specifically brain tumour segmentation on MRI, because it encompasses the full pipeline: raw volumetric data, multi-modal inputs, spatial output, and clinically interpretable evaluation metrics.

## The Supervised Learning Paradigm

Almost all deployed clinical AI relies on supervised learning: a model is trained on a large dataset of (input, label) pairs, where labels were assigned by expert humans. The model learns to map inputs to outputs by minimising a loss function that measures disagreement with the labels. At test time, the model applies the learned mapping to new inputs and produces predictions. The quality of those predictions depends entirely on the quality, size, and representativeness of the training data and labels — which is why data curation and annotation protocols are among the most important engineering decisions in a clinical AI project.

## What AI Can Do Reliably Today

In well-defined imaging tasks with large curated datasets, AI has demonstrated performance matching or exceeding individual expert radiologists:

- Detection of diabetic retinopathy from fundus photographs
- Classification of skin lesions from clinical photographs
- Detection of intracranial haemorrhage on non-contrast CT
- Pulmonary nodule detection and volumetry on chest CT
- Mammographic density assessment

These successes share common properties: large annotated datasets, standardised image acquisition, a well-defined label space, and a specific task that doesn't require integration of broader clinical context.

Risk stratification on structured data (lab values, vital signs, EHR variables) has also produced reliable models for narrow tasks — predicting sepsis onset within a defined time window, flagging acute kidney injury, estimating surgical risk.

## What AI Cannot Do Reliably

AI does not perform causal reasoning. A model that learns an association between image features and a diagnosis cannot tell you why the association holds, whether it will transfer to a new population, or what happens when clinical practice changes. It cannot reliably handle out-of-distribution inputs — a model trained on images from one scanner brand may produce degraded output on a different scanner without any warning. It cannot replace clinical judgment in contexts that require integrating imaging findings with patient history, symptoms, medication effects, and treatment goals.

## FDA-Cleared Clinical AI

As of 2024, the FDA has cleared over 900 AI/ML-based medical devices. Examples include:

- **Viz.ai** (stroke detection from CT angiography — 510(k) cleared)
- **Aidoc** (intracranial haemorrhage triage on CT)
- **IDx-DR** (autonomous diabetic retinopathy screening from fundus images — first autonomous AI diagnostic, De Novo cleared 2018)
- **Arterys Cardio AI** (cardiac MRI segmentation and quantification)

These tools share a property: they are specific, narrow, and validated on prospectively collected data before submission.

## Research AI vs Deployed AI

Research AI is optimised for publication: high performance on a held-out test set, novel architecture, benchmark comparison. Deployed AI must be safe, monitored, maintained, and regulated. A model that achieves state-of-the-art Dice on BraTS may still fail in a hospital because the scanner protocol differs, the patient population differs, the preprocessing pipeline wasn't reproduced correctly, or the model produces confidently wrong outputs with no uncertainty signal.

## Distribution Shift

A model trained at Hospital A learns the joint distribution of imaging features and labels at Hospital A. When deployed at Hospital B — with a different scanner, different acquisition parameters, different patient demographics, different radiologist annotation style — the input distribution shifts, and model performance degrades. This is not a theoretical concern. Numerous published studies have shown 10-20% Dice score drops when models trained on one institution's data are tested on another's. Distribution shift is the central practical challenge of clinical AI deployment.

## The Key Lesson

Clinical AI is an engineered system requiring scientific rigor, clinical domain knowledge, and regulatory discipline. It is not magic, and it is not a research paper. The gap between "this model achieves 0.87 Dice on our test set" and "this model is ready for clinical use" is measured in years of validation work.

!!! warning "Common misconception"
    "High accuracy on a test set means the model is clinically ready."

    This is false for several reasons. First, test set performance reflects in-distribution performance only — it says nothing about how the model will behave on data from a different site, scanner, or patient population. Second, aggregate metrics like accuracy or Dice conceal failure modes that may be systematically dangerous (e.g., the model works well on typical cases but fails catastrophically on edge cases that happen to be the sickest patients). Third, clinical readiness requires prospective validation, workflow integration testing, and regulatory review — none of which are captured by a retrospective benchmark.

!!! note "Connect to the lab"
    In this course, you build a research-grade prototype — not a clinical product. The BraTS dataset provides a controlled, pre-processed, multi-institutional benchmark that lets you focus on the modelling pipeline. Mission 6 asks you to explicitly locate your prototype on the clinical readiness spectrum and communicate its limitations honestly. The distance between where you end up and a deployable clinical tool is part of what you are meant to understand.
