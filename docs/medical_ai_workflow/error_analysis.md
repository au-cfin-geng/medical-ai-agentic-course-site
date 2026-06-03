# Error Analysis

## Why a Single Aggregate Dice Score Is Not Enough

A mean Dice score of 0.83 across 50 test cases tells you the average overlap between your predictions and the ground truth. It does not tell you whether the model consistently makes small errors everywhere, or makes catastrophic errors on a handful of cases and performs excellently on the rest. It does not tell you whether failures are systematic (always failing on small tumours, or on tumours in a particular location) or random. It does not tell you whether the model's errors are clinically consequential.

Error analysis is the process of understanding where, why, and in what pattern a model fails. It is the bridge between computing metrics and knowing what to do next.

---

## The Principle of Stratified Analysis

Aggregate metrics collapse important structure. The first step of error analysis is stratification: break down performance by clinically meaningful subgroups. For brain tumour segmentation on BraTS:

**By tumour size**:
- Small tumours (<10 mL total volume): harder for the model due to sparse training signal; boundary errors dominate
- Medium tumours (10-80 mL): the model's "comfort zone" — this is where most training examples fall
- Large tumours (>80 mL): often irregular shape, may extend across midline; also harder

**By tumour subtype** (if labels are available):
- GBM vs lower-grade glioma: different enhancement patterns, different prognosis, possibly different segmentation difficulty

**By scanner/institution** (for multi-site datasets):
- If BraTS performance varies by contributing institution, this tells you the model is sensitive to acquisition differences

**By image quality**:
- Cases with visible motion artefact or susceptibility artefact are expected to perform worse

When you stratify performance and find a pattern — for example, Dice drops from 0.88 to 0.61 for tumours smaller than 5 mL — you have actionable information. You know which cases are failing, you have a plausible hypothesis (small tumours are underrepresented in the training set), and you know what to target.

---

## A Taxonomy of Segmentation Errors

Not all segmentation errors are the same clinically. Understanding the type of failure helps you prioritise remediation.

### Undersegmentation

The model predicts a mask that is smaller than the true tumour. In BraTS terms: the predicted mask misses part of the actual tumour, producing high FN. Clinically, undersegmentation in a pre-operative planning context means the surgical or radiation target volume is smaller than it should be — the most dangerous failure mode.

Undersegmentation is common in:
- Tumour borders where FLAIR signal gradually merges with normal-appearing white matter
- Non-enhancing tumour regions where T1ce contrast is absent
- Small tumours where the training signal is sparse

### Oversegmentation

The model predicts a mask that is larger than the true tumour. High FP. The predicted region extends into normal brain tissue, peritumoral oedema, or incidental normal findings. Clinically, oversegmentation in radiation planning could expose normal eloquent cortex to unnecessary radiation.

Oversegmentation is common in:
- Regions near the ventricles (on T1ce, choroid plexus enhancement can mimic tumour)
- Areas of surgical cavity (post-treatment imaging has complex appearance)
- Regions with leukoariosis or other FLAIR-hyperintense normal variants in elderly patients

### Fragmentation

The predicted volume is approximately correct (Dice is moderate) but spatially distributed incorrectly — the model predicts multiple small disconnected islands of "tumour" rather than one connected region. Dice may be acceptable but the spatial distribution is wrong. This is a failure of spatial coherence — the model is making voxel-level decisions without understanding anatomical continuity.

Fragmentation is detectable by computing connected component statistics: if the prediction contains many small disconnected regions, consider applying a connected-component post-processing step (retain only the largest component).

### Location Error

The model predicts tumour in completely the wrong region — for example, predicting an enhancing region in the contralateral hemisphere due to a symmetric enhancement artefact. Dice = 0, and the error is qualitatively different from undersegmentation. This is the rarest failure mode in BraTS (because the dataset is curated) but becomes relevant in real-world deployment with unusual cases.

### Boundary Error

The model gets the bulk of the tumour correct (high sensitivity, reasonable Dice) but the boundary is imprecise. HD95 is elevated even when Dice is acceptable. This is the most common failure mode for well-trained models and the most clinically nuanced — the clinical significance of a 3mm boundary error depends entirely on what structure lies 3mm beyond the tumour.

---

## How to Conduct Error Analysis in Practice

### Step 1: Sort cases by metric, inspect the extremes

Sort your test cases by per-case Dice score (ascending). Load the bottom 5-10 cases and visualise them. Look at:
- The FLAIR and T1ce images
- The ground truth mask
- Your model's prediction
- The difference image (FN in one colour, FP in another)

Classify each failure case into the taxonomy above. Are the failures random or is there a pattern?

### Step 2: Compute error statistics by case characteristic

For each case, compute the tumour volume from the ground truth label. Then make a scatter plot: tumour volume (x-axis) vs Dice score (y-axis). Is there a relationship? Most models show declining Dice for smaller tumours.

If your dataset has metadata (age, sex, tumour grade, scanner type, contributing institution), compute stratified Dice. Any subgroup with substantially lower Dice is a candidate for targeted improvement.

### Step 3: Examine spatial error patterns

Where in the brain do false positives cluster? Where do false negatives cluster? You can visualise this by averaging the FP and FN maps across all test cases in MNI space (after registration). If errors cluster near the ventricles, near surgical cavities, or in a specific lobe, this is a systematic spatial bias.

### Step 4: Compare HD95 to Dice failures

Find cases where Dice is acceptable (>0.75) but HD95 is poor (>10mm). These cases have correct overall volume but inaccurate boundaries. The clinical implications may be different from cases with low Dice and low HD95.

---

## Prioritising Improvements Based on Error Analysis

The goal of error analysis is not just description — it is to guide the next experiment. Prioritise the failure mode that has the largest clinical impact, not necessarily the largest effect on mean Dice.

**Priority hierarchy for clinical brain tumour segmentation**:
1. False negatives (undersegmentation) — missed tumour is dangerous
2. Large boundary errors near critical structures (eloquent cortex, brainstem)
3. Fragmentation producing spatially incoherent predictions
4. General undersegmentation of small tumours
5. Oversegmentation into normal tissue

When you identify a failure mode and hypothesise a cause, you have the starting point for a targeted improvement. This is the error analysis → hypothesis → improvement cycle described in [Improving Your Model](model_improvement.md).

---

!!! warning "Common mistake"
    Do not skip error analysis and go directly from metrics to model changes. If you change your model without understanding why it was failing, you are making arbitrary changes. Some will appear to help by chance. You will not know whether the improvement addresses the actual failure mode.

!!! note "Connect to Lab Mission"
    **Now do the lab — M3 (Error Analysis).**

    In Mission 3, conduct a structured error analysis of your baseline model. Sort your validation cases by Dice score. Visualise the five worst cases and classify each failure using the taxonomy above (undersegmentation, oversegmentation, fragmentation, boundary error, location error). Compute stratified Dice by tumour volume tertile (small, medium, large). Plot the distribution of per-case HD95. Write a one-paragraph error analysis summary: what is the dominant failure mode, what patient subgroup is most affected, and what is your hypothesis for the cause? Use Claude to help generate the visualisation code.
