# Evaluation Metrics for Segmentation

## Why Choosing the Right Metric Is a Clinical Decision

In brain tumour segmentation, choosing the wrong evaluation metric is not just a methodological error — it can lead you to believe a clinically useless model is performing well. This page covers the metrics used to evaluate segmentation algorithms, with formulas, worked examples, and clinical interpretation for each.

---

## Why Pixel Accuracy Fails

**Pixel accuracy** counts the fraction of correctly classified voxels:

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

In brain tumour segmentation, approximately 95% of all brain voxels are background (non-tumour). A model that predicts "no tumour" for every voxel achieves 95% accuracy. It will detect zero tumours. It is clinically worthless.

This is the **class imbalance problem**. Because the negative class (background) dominates, accuracy is an uninformative metric for any task where the positive class is rare. For the enhancing tumour region in BraTS, the positive class may be less than 1% of all voxels — a model predicting all-negative achieves >99% accuracy.

The lesson: always think about what your metric rewards before choosing it. A metric that rewards predicting nothing is not useful for a detection task.

---

## Dice Coefficient (F1 Score for Segmentation)

The Dice coefficient, also known as the Sorensen-Dice similarity coefficient or F1 score adapted for binary masks, is the primary metric for medical image segmentation:

$$\text{Dice} = \frac{2|A \cap B|}{|A| + |B|}$$

Where:
- $A$ = predicted segmentation mask (set of voxels predicted as tumour)
- $B$ = ground truth segmentation mask (set of voxels labelled as tumour by experts)
- $|A \cap B|$ = number of voxels in both A and B (true positives)
- $|A|$ = total predicted tumour voxels
- $|B|$ = total ground truth tumour voxels

In terms of TP, FP, FN:

$$\text{Dice} = \frac{2 \cdot \text{TP}}{2 \cdot \text{TP} + \text{FP} + \text{FN}}$$

**Range**: 0 (no overlap at all) to 1 (perfect overlap).

**Intuition**: What fraction of the combined area is shared? A Dice of 0.5 means that the combined size of the predicted and ground truth regions is twice as large as their shared region — they overlap by half their total area.

**Why Dice is class-imbalance resistant**: Dice ignores TN entirely. It only measures how well the model handles the positive class (tumour). A model predicting all-negative gets Dice = 0, correctly identified as useless.

### Clinical Interpretation of Dice Values

| Dice Range | Clinical Interpretation |
|-----------|------------------------|
| >0.90 | Excellent — within inter-rater variability between expert annotators |
| 0.80-0.90 | Good — acceptable for most research applications; clinical deployment needs further validation |
| 0.70-0.80 | Moderate — may be adequate for coarse volume estimation; not for precise boundary-dependent tasks |
| 0.60-0.70 | Poor — large systematic errors present; likely not safe for clinical use |
| <0.60 | Unacceptable — do not interpret as "partially correct"; investigate failures immediately |

### BraTS Challenge Benchmarks (Published Top Performers)

| Region | Competitive Dice (Top 10) |
|--------|--------------------------|
| Whole Tumour (WT) | 0.89 - 0.92 |
| Tumour Core (TC) | 0.83 - 0.88 |
| Enhancing Tumour (ET) | 0.78 - 0.84 |

A solid U-Net baseline achieving WT Dice of 0.82 is meaningful — it is in range, not state of the art, and tells you what improvements are worthwhile to pursue.

---

## Sensitivity (Recall)

$$\text{Sensitivity} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$

Of all actual tumour voxels, what fraction did the model correctly detect?

**Range**: 0 to 1. High sensitivity means few false negatives — few actual tumour voxels were missed.

**Clinical priority**: In brain tumour segmentation for treatment planning, **high sensitivity is usually the priority**. Missing tumour (false negative) means undertreating disease. A radiation plan that excludes 15% of the actual tumour volume is clinically dangerous. A plan that includes 15% more tissue than necessary is less dangerous — it may increase side effects but will not leave disease untreated.

This asymmetry means that in many clinical contexts, you should tolerate lower specificity (more false positives) in exchange for higher sensitivity (fewer false negatives). The appropriate trade-off depends on the downstream clinical action.

---

## Specificity

$$\text{Specificity} = \frac{\text{TN}}{\text{TN} + \text{FP}}$$

Of all actual background voxels, what fraction were correctly labelled as background?

**Range**: 0 to 1. High specificity means few false positives — few background voxels were incorrectly called tumour.

**Clinical consequence of low specificity**: False positive segmentation of normal brain as tumour can lead to:
- Overestimation of tumour volume, potentially triggering more aggressive treatment
- Radiation to normal eloquent cortex (speech, motor) causing neurological deficits
- Unnecessary surgical intervention

In brain tumour segmentation, specificity is typically very high (>0.99) because the vast majority of background voxels are correctly classified. This makes specificity a less informative metric than sensitivity for this task — its high value is partially artefactual due to class imbalance. Do not use specificity as your primary metric.

---

## Precision (Positive Predictive Value)

$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$

Of all voxels the model predicted as tumour, how many were actually tumour?

**Range**: 0 to 1. Low precision means lots of false positives — the model over-segments, extending predicted tumour into normal brain.

**Relationship with sensitivity**: Precision and sensitivity are in tension. A model that predicts the entire brain as tumour has perfect sensitivity (every tumour voxel is "detected") but zero precision. A model that predicts only the single most certain voxel as tumour has high precision but very low sensitivity. Dice is the harmonic mean of precision and recall, balancing both.

---

## HD95 (95th Percentile Hausdorff Distance)

Dice measures volumetric overlap. HD95 measures boundary accuracy. These are complementary.

**Definition**: The Hausdorff distance between two point sets is the maximum distance from any point in one set to the nearest point in the other set. HD95 is the 95th percentile of this distance, dropping the worst 5% of outlier boundary distances:

$$\text{HD95}(A, B) = \max(\text{percentile}_{95}\{d(a, B) : a \in \partial A\}, \text{percentile}_{95}\{d(b, A) : b \in \partial B\})$$

Where $\partial A$ and $\partial B$ are the boundary voxels of predicted and ground truth masks, and $d(x, Y)$ is the Euclidean distance from point $x$ to the nearest point in set $Y$.

**Units**: millimetres (using voxel spacing metadata).

**Why HD95 rather than HD100**: The maximum Hausdorff distance is extremely sensitive to single outlier voxels — one misclassified voxel far from the tumour inflates the metric catastrophically. HD95 truncates the worst 5%, making the metric robust to rare spurious predictions.

**Clinical meaning**: HD95 captures how far off the tumour boundary the model is at its worst. For radiation planning, boundary accuracy matters directly — a boundary error of 10mm translates to a 10mm error in the treatment margin.

**Benchmark values**: HD95 < 5mm is generally considered acceptable for whole-tumour segmentation in brain tumours. HD95 < 2mm is excellent, approaching inter-rater variability.

---

## BraTS Evaluation Regions

BraTS evaluates each algorithm on three nested regions, each with its own Dice, Sensitivity, Specificity, and HD95:

| Region | Definition | Clinical Relevance |
|--------|-----------|-------------------|
| **Whole Tumour (WT)** | Entire abnormality on FLAIR (labels 1+2+3+4 combined) | Oedema extent, surgical approach planning |
| **Tumour Core (TC)** | Non-enhancing tumour + necrosis + enhancing tumour (labels 1+3+4) | Surgical resection target |
| **Enhancing Tumour (ET)** | Only the contrast-enhancing region (label 4) | Treatment response assessment, RT boost volume |

A model can perform well on WT while performing poorly on ET. This is common: the whole tumour boundary (on FLAIR) is relatively easy to detect; the fine boundary of the enhancing tumour (on T1ce) is harder and has more inter-rater variability in the ground truth.

---

## Metrics Summary Table

| Metric | Formula | Range | What It Measures | Clinical Priority for GBM |
|--------|---------|-------|------------------|--------------------------|
| **Accuracy** | (TP+TN)/(N) | 0-1 | Overall correctness | Not recommended (misleading) |
| **Dice** | 2TP/(2TP+FP+FN) | 0-1 | Volumetric overlap | Primary metric |
| **Sensitivity** | TP/(TP+FN) | 0-1 | Tumour detection rate | High priority |
| **Specificity** | TN/(TN+FP) | 0-1 | Background correct rate | Secondary |
| **Precision** | TP/(TP+FP) | 0-1 | Prediction accuracy | Secondary |
| **HD95** | 95th pct boundary distance | mm | Boundary accuracy | Important for planning |

!!! note "Connect to Lab Mission"
    **Now do the lab — M2 and M3 (Baseline Evaluation and Metrics Deep Dive).**

    In Mission 2, after training your baseline, compute all six metrics above for the whole-tumour region. In Mission 3, extend this to all three BraTS evaluation regions. For each metric, write one sentence of clinical interpretation: not "Dice is 0.82" but "a Dice of 0.82 means approximately 82% of the combined predicted and ground truth tumour volume is shared — this may be adequate for volume estimation but requires further validation before use in radiation planning." Compute both mean and per-case distribution (box plot). Identify the three cases with the lowest Dice and the three with the worst HD95 — are they the same cases?
