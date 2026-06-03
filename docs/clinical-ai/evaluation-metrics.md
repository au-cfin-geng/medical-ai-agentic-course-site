# Evaluation Metrics

Choosing the right metric is not a formality — it determines what you are optimising for and what your results actually mean. For clinical segmentation, different metrics capture different aspects of clinical utility, and a model that performs well on one metric while failing on another may be dangerous in practice.

## Why Pixel Accuracy Fails

The most intuitive metric — fraction of voxels correctly classified — fails for any task where classes are imbalanced. In a typical brain MRI volume, tumour voxels constitute approximately 1-5% of all voxels. A model that predicts "background" for every single voxel achieves 95-99% pixel accuracy while providing zero clinical information. This is not a theoretical edge case; it is one of the most common bugs in new segmentation implementations.

**Pixel accuracy** = (TP + TN) / (TP + TN + FP + FN)

A model with this metric at 97% may still have Dice = 0. Never use pixel accuracy as the primary metric for segmentation tasks with class imbalance.

## Dice Similarity Coefficient

The Dice coefficient (also called F1 score when applied per-class) measures the overlap between predicted and reference segmentations, normalised by the total size of both regions. It is insensitive to the large background class.

**Formula**: Dice = 2|P ∩ R| / (|P| + |R|) = 2TP / (2TP + FP + FN)

Where P is the set of predicted positive voxels and R is the set of reference positive voxels.

**Range**: 0 (no overlap at all) to 1 (perfect overlap).

**Intuition**: Dice is the harmonic mean of precision (positive predictive value) and recall (sensitivity), weighted equally. It penalises both false positives (predicting tumour where there is none) and false negatives (missing actual tumour).

**Typical benchmark values on BraTS**:

| Region | Good performance | State-of-the-art |
|---|---|---|
| Whole Tumour (WT) | > 0.85 | > 0.91 |
| Tumour Core (TC) | > 0.80 | > 0.87 |
| Enhancing Tumour (ET) | > 0.75 | > 0.83 |

WT is easiest (oedema is large and FLAIR-bright). ET is hardest (smaller, requires correct T1ce interpretation).

**Clinical meaning**: Dice 0.85 on WT means 85% of the true tumour region is correctly captured with acceptable false positive rate. Dice below 0.70 generally indicates clinically unacceptable segmentation for treatment planning.

## Sensitivity (Recall)

**Formula**: Sensitivity = TP / (TP + FN)

Sensitivity measures the fraction of true tumour voxels that the model correctly identifies. A model with low sensitivity is **missing tumour** — the clinically dangerous direction. In the context of surgical planning or radiotherapy, missing tumour extent means the treatment target is underestimated. Missed tumour that is not irradiated or resected can drive recurrence.

**Clinical consequence of low sensitivity**: Under-treatment. A radiotherapy plan based on an under-segmented tumour may leave viable tumour cells outside the treatment field, contributing to recurrence.

## Specificity

**Formula**: Specificity = TN / (TN + FP)

Specificity measures the fraction of true background voxels correctly identified as background. A model with low specificity produces many false positives — predicting tumour where there is healthy brain.

**Clinical consequence of low specificity**: Over-treatment. A radiotherapy target volume padded with false positive predictions irradiates healthy brain tissue unnecessarily. In surgical planning, over-segmentation may lead surgeons to remove functional brain tissue. The exact clinical impact depends on which brain regions are falsely included.

In practice, there is a sensitivity-specificity trade-off controlled by the threshold applied to model output probabilities. Moving the threshold down increases sensitivity at the cost of specificity. The clinically appropriate operating point depends on the specific clinical use case.

## HD95 Hausdorff Distance

Dice is a volume-based metric and does not directly capture boundary accuracy. A model can achieve high Dice while having local boundary errors of several centimetres in isolated regions. The Hausdorff distance measures the maximum distance between the predicted and reference boundaries.

The **95th percentile Hausdorff distance (HD95)** computes the 95th percentile of all directed boundary distances (rather than the maximum), which reduces sensitivity to single outlier boundary points.

**Formula**: HD95(P, R) = max(d95(P→R), d95(R→P)), where d95 is the 95th percentile of minimum distances from each predicted boundary voxel to the nearest reference boundary voxel, in millimetres.

**Range**: 0mm (perfect boundary match) upward. For brain tumour segmentation, HD95 < 5mm is generally considered acceptable for WT. ET boundaries are harder and values of 5-10mm are common in current models.

**Clinical meaning**: HD95 answers the question "how far is the worst-case boundary error?" For radiotherapy planning, where treatment margins are defined in millimetres, a boundary error of 20mm represents a substantial planning inaccuracy.

## Summary Metrics Table

| Metric | Formula | Range | Clinical meaning | Typical benchmark (WT) |
|---|---|---|---|---|
| Pixel Accuracy | (TP+TN)/(all) | 0-1 | Misleading for imbalanced data — do not use alone | N/A |
| Dice (DSC) | 2TP/(2TP+FP+FN) | 0-1 | Overall overlap quality | > 0.85 |
| Sensitivity | TP/(TP+FN) | 0-1 | Tumour detection completeness | > 0.85 |
| Specificity | TN/(TN+FP) | 0-1 | False positive rate in healthy tissue | > 0.98 |
| HD95 | 95th pct boundary distance | mm | Boundary accuracy | < 5mm |

## Why BraTS Reports WT, TC, ET Separately

A model that achieves Dice 0.90 on WT but Dice 0.60 on ET has failed at the most clinically critical region. Reporting all three regions separately prevents a single aggregate number from hiding clinically meaningful failures. The multi-region evaluation is one of the reasons BraTS has become the canonical benchmark: it forces models to demonstrate competence at multiple scales and with different imaging signals simultaneously.

!!! warning "Common mistake in Mission 2"
    A Dice score of 0 on validation while training loss continues to decrease usually means an evaluation bug, not a model failure. The most common cause: the model is predicting all-zero masks (background everywhere), which gives loss values that decrease (cross-entropy with heavy background weighting can still converge toward all-background) but Dice of exactly 0 because there is no overlap. Check that your validation predictions contain non-zero values. Also check that your label mapping is consistent between training and evaluation — if training labels use value 1 for tumour and evaluation checks for value 4, Dice will always be 0.
