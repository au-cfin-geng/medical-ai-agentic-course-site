# Mission 3 — Investigate Failure

Your model produces a number. That number means nothing until you understand what it is hiding. This mission is the scientific act of not being satisfied with the mean — of asking which cases failed, why they failed, and whether the pattern is explainable.

---

## Scientific Purpose

Aggregate performance metrics like mean Dice are averages over a distribution of cases, and averages conceal structure. A model with mean Dice 0.82 might be achieving Dice > 0.90 on 80% of cases and Dice < 0.20 on the remaining 20%. Those 20% are not statistical noise — they are a signal. They reveal something about the limits of the model's generalisation: the kinds of cases it does not yet handle. In clinical medicine, a model that fails 20% of the time in a predictable pattern is a model that can be improved with intent — but only if the pattern has been identified. This mission is about finding that pattern. You will rank cases by performance, examine the worst failures visually, identify a structural commonality, and write a testable hypothesis about why the model fails. That hypothesis becomes the input to Mission 4.

---

## Required Background Reading

Before starting this mission, read the following pages on this site:

- [Error Analysis](../medical_ai_workflow/error_analysis.md) — understand what a rigorous error analysis covers and how to structure one
- [Metrics: Dice, Sensitivity, Specificity](../medical_ai_workflow/metrics_dice_sensitivity_specificity.md) — understand what Dice = 0.0 means versus Dice = 0.3
- [Brain Tumour Imaging](../foundations/brain_tumour_imaging.md) — understand the morphological characteristics that vary across BraTS cases (size, location, subtype)
- [Roles for Claude](../agentic_research/roles_for_claude.md) — understand the Critic/Analyst role before you assign it

---

## What You Will Ask Claude to Build

Your goal is to produce a structured error analysis that identifies and explains the failure pattern of the baseline model. This is analysis work, not model development — Claude should write data loading, metric sorting, and visualisation code, but not any new training or architecture code.

Ask Claude to: load the per-case validation metrics from Mission 2; sort cases by Dice score from lowest to highest; load the original images, ground-truth labels, and model predictions for the 10 worst-performing cases; produce visualisation figures for each failure case showing the predicted segmentation overlaid on the MRI alongside the ground-truth segmentation; and compute summary statistics for the failure cases versus the success cases — including tumour volume (derived from the ground-truth label), tumour location (centroid coordinates), and any other feature that seems relevant.

Then, in a separate step: ask Claude to read the analysis results and write a written hypothesis (1-2 paragraphs) about what structural feature distinguishes the failure cases from the successes. This should be a scientific claim, not a vague statement. "The model tends to fail on cases with small tumour volumes (< 5 cm³)" is a hypothesis. "The model needs more training" is not.

---

## Expected Artifacts

| Filename | Contents | What Correct Looks Like |
|---|---|---|
| `results/error_analysis/failure_ranking.csv` | All validation cases sorted by Dice, with tumour volume and location columns | One row per case; failure cases at the top; tumour volume in cm³ |
| `results/error_analysis/failure_cases/case_XXX_analysis.png` | Side-by-side: ground truth overlay vs prediction overlay for each of the 10 worst cases | Images are clearly labelled; both GT and prediction are shown; the discrepancy is visually apparent |
| `results/error_analysis/failure_vs_success_comparison.png` | Box plot or scatter plot comparing a key feature (e.g., tumour volume) between failure and success groups | A visible difference should be apparent if the hypothesis is correct; if not, the hypothesis may be wrong — that is also a valid finding |
| `results/error_analysis/error_analysis_report.md` | The full written error analysis | Includes the ranking table, figure references, a written hypothesis, and a proposed intervention for Mission 4 |

---

## How to Inspect Results

**Failure case images.** Look at each failure case. Is the tumour small? Is it near the ventricles? Is the enhancing tumour absent (some tumours have no enhancing component)? Is the ground-truth segmentation itself plausible — could the annotation be questionable? Note your observations — do not let Claude make these observations for you. Your clinical intuition is part of the scientific method here.

**The comparison plot.** Does the box plot of tumour volumes show a clear separation between failure and success cases? If it does, your hypothesis has visual support. If it does not, consider other features: location (distance from centroid to image centre), tumour shape (elongated vs compact), or presence of specific subregions (does the model fail when enhancing tumour is absent?).

**The written hypothesis.** Read it critically. Is it specific enough to design an experiment around? "The model fails on small tumours because they represent fewer than 50 voxels in the 2D slice view, making the class imbalance within each slice even more severe than in the overall dataset" is testable. "The model struggles with difficult cases" is not.

**Is the hypothesis falsifiable?** Ask yourself: what result in Mission 4 would prove the hypothesis wrong? If you cannot answer that question, the hypothesis is not precise enough.

---

## Prompt Principle

**Assign a Critic/Analyst role and explicitly prohibit training code.**

The most common deviation in this mission is that Claude, trained to be helpful, anticipates that you want to improve the model and starts writing new training code. This is exactly what you do not want. You want analysis — understanding — before any intervention.

!!! failure "Vague task that invites coding"
    ```
    Look at where the model is failing and help me improve it.
    ```
    Claude reads the metrics, identifies that small tumours fail, and immediately writes a new training script with augmentation. You have skipped the hypothesis formation step and will not know whether the change helped the specific failure mode.

!!! success "Analyst role with explicit boundary"
    ```
    Act as a research analyst, not a model developer.
    Read results/val_metrics.csv from Mission 2.
    Do the following — do not write any training, fine-tuning, or architecture code:
    1. Sort cases by Dice score (lowest first). Print the 10 worst.
    2. For each of the 10 worst cases, load the MRI (FLAIR modality), the ground-truth label, and the prediction.
       Save a side-by-side figure showing GT vs prediction overlay.
    3. For each case, compute the tumour volume in cm³ from the ground-truth label.
    4. Create a scatter plot: x = tumour volume, y = Dice score, for all validation cases.
    5. Write a 1-paragraph hypothesis about what causes the failures. The hypothesis must be specific enough to design an experiment.
    Save everything to results/error_analysis/.
    ```

The key moves: explicit role, explicit prohibition, numbered subtasks, explicit output paths.

---

## Reflection Questions

1. You identified a pattern in the failure cases. How confident are you? You have a validation set of roughly 50 cases. How many cases would you need to see the pattern you identified with statistical confidence? What would a proper significance test look like?

2. Your hypothesis proposes a structural cause of failure (e.g., small tumour volume). Is this the only possible explanation? What alternative hypotheses are also consistent with the data? How would you design an experiment to distinguish between them?

3. Some of the "failure" cases may have Dice = 0 because the ground-truth label is empty (no tumour annotated). This is a fundamentally different failure mode from a case where the model misses a real tumour. How does your error analysis handle this distinction? If it does not, how would you modify it?

4. You looked at the 10 worst cases. Did you look at the 10 best cases? What would you expect to find there? Is there something the best cases have in common that the worst cases lack?

5. Error analysis is a scientific act that requires domain knowledge. Claude found statistical patterns — you provided the biological interpretation. What domain knowledge did you use in this mission that Claude could not have supplied on its own?

---

## Optional Challenge

Extend the error analysis to include a spatial failure map. For each validation case, compute the voxel-level disagreement between the ground-truth label and the model prediction (a binary disagreement mask). Average these disagreement masks across all failure cases (those with Dice < 0.5). The result is a spatial heatmap showing which anatomical locations most frequently have disagreements. Display this heatmap overlaid on the mean FLAIR image of the validation set. This kind of spatial error analysis is used in clinical AI papers to demonstrate that a model's failures are not random but anatomically structured.

---

## Common Failure Modes

**Student reports only mean Dice and declares the analysis done.** The entire point of this mission is per-case analysis. If you can only cite a single number, you have not done error analysis — you have done evaluation. Push past the aggregate.

**Failure cases visualised without labels or captions.** A row of unlabelled brain images is not an error analysis. Every figure must have the case ID, the ground-truth Dice, the tumour volume, and clear labels for which side is GT and which is prediction. Ask Claude to add these to the figure generation code.

**Hypothesis is vague or circular.** "The model fails because the task is hard" explains nothing and predicts nothing. A valid hypothesis names a specific feature (tumour volume, location, subregion presence) and predicts a specific relationship (cases below a volume threshold fail more). If your hypothesis does not constrain what you would expect to see in Mission 4, sharpen it.

**Tumour volume computed from prediction instead of ground truth.** This introduces confounding — cases where the model predicted zero volume will have computed volume = 0 regardless of the actual tumour. Always compute morphological features from the ground-truth label, not the prediction.

**Empty label cases not handled.** Some BraTS cases in the validation split may have zero annotated voxels (Grade I gliomas, or protocol edge cases). Attempting to compute Dice on these cases with a naive implementation will produce a 0/0 division. Ask Claude to detect and separately report these cases rather than letting them silently corrupt the metrics.

---

## Expected Learning Outcome

After completing this mission you can: produce a ranked failure analysis from a per-case metrics file; load, visualise, and compare ground-truth and predicted segmentations for specific cases; identify a morphological or statistical pattern that distinguishes failure cases from success cases; articulate a specific, testable hypothesis about a model's failure mode; explain why aggregate metrics are insufficient for scientific evaluation of a medical AI model.
