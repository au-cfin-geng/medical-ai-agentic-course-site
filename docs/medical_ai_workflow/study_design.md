# Designing the Next Study

## The Bridge from Computational Research to Clinical Research

After iterating through baseline modeling, error analysis, and targeted improvements, you will reach a point where your model achieves reasonable performance on your internal dataset. The natural question is: what does this actually mean? Can this model be trusted in clinical practice? Should it be tested on patients?

Answering these questions requires a shift from computational thinking to clinical research design. The model's internal validation performance is a necessary but not sufficient condition for clinical utility. The next step is **external validation** — and potentially, formal clinical study design.

---

## Internal vs. External Validation

**Internal validation** uses data from the same source as the training data, even if individual cases are held out. In BraTS, your test set cases come from the same multi-institutional pool, preprocessed identically, with labels from the same annotation protocol. Internal validation estimates performance in your best-case scenario — data that looks like your training data.

**External validation** tests your model on data from a completely separate institution, with different scanners, different patient populations, and potentially different annotation practices. External validation is the real test of generalisation.

The gap between internal and external validation performance is almost always positive — external performance is almost always worse. Papers that report only internal validation overestimate clinical utility. The magnitude of the internal-external gap is itself an informative finding: a gap of 0.05 Dice points suggests good generalisation; a gap of 0.20 suggests the model is highly institution-specific and will not transfer.

---

## Types of Clinical Validation Studies

Once you have a model with acceptable internal performance, the progression toward clinical use follows a staged pathway. Each stage has a different study design:

### Retrospective External Validation

**What it is**: Apply your model to existing clinical data from a different institution, collected before the study started. Compare model predictions to expert reference annotations or to clinical measurements taken at the time of care.

**What it tells you**: Does the model generalise to a new patient population and scanner environment?

**Limitations**: Retrospective data may have selection bias (only patients who received imaging and were diagnosed are in the records). The reference standard (expert annotation) may have been performed differently from the BraTS annotation protocol. Patients who were imaged on old scanners that have since been replaced may not represent current clinical practice.

**When to use it**: This is the appropriate next step after good internal validation. It is relatively inexpensive, does not require ethics approval for re-analysis of existing anonymised data in many jurisdictions (check local requirements), and provides meaningful evidence of generalisability.

### Prospective Observational Validation

**What it is**: Prospectively enroll new patients, collect their imaging, apply the model, and compare to a reference standard — but the model output does not influence clinical decisions. The model runs in parallel to standard care.

**What it tells you**: Does the model work on freshly acquired data from the current clinical environment? Are there operational issues (data transfer, runtime, format compatibility) that were not apparent in retrospective analysis?

**Limitations**: More expensive and time-consuming than retrospective. Requires ethics approval. Model performance on prospective data is not guaranteed to replicate retrospective performance — patients seen prospectively may differ from historical cases.

**When to use it**: After successful retrospective external validation, before considering any study where the model influences care.

### Interventional Study (Clinical Impact)

**What it is**: The model output is shown to the clinician and may influence their decision. You measure not just segmentation accuracy but downstream clinical outcomes — treatment plan quality, time to treatment, inter-observer variability in volume measurement.

**What it tells you**: Does the model actually help? Does using the AI segmentation lead to better treatment plans? Does it save time without compromising quality?

**Limitations**: Most complex and expensive to design. Requires evidence that the model is safe enough to influence decisions — this requires the preceding validation stages. Outcome measures must be clinically meaningful, not just Dice scores.

---

## Elements of a Clinical Validation Protocol

A formal clinical AI validation study requires a prospectus specifying, before any data is collected:

### Research Question and Objectives

**Primary objective**: To determine whether [model name] achieves non-inferior whole-tumour Dice coefficient compared to expert manual segmentation in newly diagnosed glioma patients at [Institution B].

**Secondary objectives**: Tumour core and enhancing tumour Dice; HD95 for all three regions; processing time; proportion of cases requiring manual correction.

### Eligibility Criteria

State explicitly who is and is not included. For a brain tumour segmentation validation:

- *Inclusion*: adult patients (≥18 years), confirmed or suspected glioma on radiological report, complete four-sequence MRI (T1, T1ce, T2, FLAIR) acquired at [Institution B] within the study period, MRI acquired for clinical indication
- *Exclusion*: prior brain radiotherapy, prior brain surgery at the same site, MRI with major artefacts (as judged by the reviewing radiologist), patients unable to receive IV contrast (no T1ce available)

### Reference Standard

Specify how the ground truth is established: single expert annotation, consensus of two experts, or majority vote of three experts? What annotation protocol? What training do annotators receive? The reference standard is the most important decision in the study design — an unreliable reference standard makes the entire study uninterpretable.

### Pre-specified Primary Endpoint and Analysis Plan

State the primary endpoint in advance: "The primary endpoint is whole-tumour Dice coefficient, defined as [formula]. The null hypothesis is that the model Dice is less than 0.75. The study will reject the null if the lower 95% confidence interval bound for mean Dice exceeds 0.75."

Pre-specifying the primary endpoint prevents outcome switching — choosing which metric to report after seeing the data.

---

## Sample Size Estimation

Sample size estimation for segmentation studies is more complex than for classification. You need:

1. **Expected mean Dice**: your best estimate from internal validation, deflated by an assumed internal-external gap (typically 0.05-0.10)
2. **Expected standard deviation**: from your internal validation per-case Dice distribution
3. **Acceptable confidence interval width**: what precision do you need? A 95% CI of ±0.05 for mean Dice is typical
4. **Any subgroup analyses**: subgroup analyses require larger overall samples to maintain power in each subgroup

For a study with expected mean Dice of 0.82, SD of 0.12, and desired 95% CI width of ±0.05:

```
n = (z_{0.975} × SD / (CI_width/2))^2
n = (1.96 × 0.12 / 0.025)^2 ≈ 88 cases
```

Add 10-20% for dropout and cases failing eligibility criteria. A study of 100-110 cases is a reasonable target for this scenario.

---

## Common Design Pitfalls

**No pre-registration**: Without pre-registration (e.g., on ClinicalTrials.gov or OSF), readers have no way to know whether the reported primary endpoint was specified in advance or chosen after seeing results. Pre-registration is increasingly required by journals and expected by regulators.

**Inadequate sample size**: Studies with 20-30 cases cannot reliably estimate mean Dice with confidence intervals narrow enough to support regulatory submissions or clinical policy decisions.

**Unblinded evaluation**: If the annotator producing the reference standard can see the model's prediction, the reference standard may be biased toward the prediction. Annotators should be blinded to model output.

**Primary endpoint does not match clinical need**: Dice score is a research metric. It should be accompanied by at least one clinically meaningful endpoint (e.g., volume agreement in mL, time required for manual correction, proportion of cases requiring major correction).

---

!!! note "Connect to Lab Mission"
    **Now do the lab — M5 (Study Design).**

    In Mission 5, draft a one-page study protocol for a hypothetical external validation study of your brain tumour segmentation model. Include: primary objective, eligibility criteria (5 inclusion and 3 exclusion criteria), reference standard specification, primary endpoint with pre-specified acceptance threshold, and a sample size calculation using the mean Dice and SD you observed in your internal validation. Use Claude to help structure the protocol — prompt it with your internal validation results and ask it to draft the statistical analysis plan section. Critique the protocol you produce: what are its three main weaknesses?
