# Metrics Cheat Sheet

> **For print:** use browser Print → Save as PDF. Recommended: A4, portrait, single page.

---

## Metric Formulas and Intuitions

Let: **TP** = true positives (voxels correctly predicted as tumour), **FP** = false positives (background predicted as tumour), **FN** = false negatives (tumour predicted as background), **TN** = true negatives (background correctly predicted as background).

---

### Dice Coefficient (Dice Similarity Coefficient, DSC)

$$\text{Dice} = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$$

**Intuition:** The proportion of the union of GT and prediction that both agree is tumour. A value of 1.0 means perfect overlap; 0.0 means no overlap at all.

**Note:** Dice is identical to the F1 score in the binary classification case.

**Typical values for good brain tumour segmentation:**

| Region | Acceptable | Good | Excellent |
|---|---|---|---|
| Whole Tumour (WT) | > 0.75 | > 0.85 | > 0.90 |
| Tumour Core (TC) | > 0.65 | > 0.80 | > 0.87 |
| Enhancing Tumour (ET) | > 0.55 | > 0.75 | > 0.82 |

**Clinical interpretation:** A Dice of 0.80 means that if you overlap the AI prediction and the expert annotation, the shared area represents 80% of their combined footprint. In practice, boundaries will be slightly off; the core region will be mostly correct.

---

### Sensitivity (Recall, True Positive Rate)

$$\text{Sensitivity} = \frac{TP}{TP + FN}$$

**Intuition:** Of all the voxels that are truly tumour, what fraction did the model find? High sensitivity means very few tumour voxels were missed.

**Typical values:** > 0.85 for WT, > 0.80 for TC/ET in a good model.

**Clinical interpretation (Sensitivity):** Missing tumour voxels means the model is leaving disease unmarked. In the context of radiotherapy planning, under-segmenting the tumour may result in inadequate radiation coverage of disease.

---

### Specificity (True Negative Rate)

$$\text{Specificity} = \frac{TN}{TN + FP}$$

**Intuition:** Of all the voxels that are truly healthy tissue, what fraction did the model correctly identify as healthy? High specificity means very few healthy voxels were incorrectly called tumour.

**Typical values:** > 0.99 for all regions (the brain volume is predominantly background, so this metric is easy to achieve; do not use it as your primary metric).

**Clinical interpretation (Specificity):** A false positive (predicting tumour where there is none) could lead to unnecessary biopsy, overtreatment, or unwarranted alarm. In GBM management, false positives in follow-up scans could be misinterpreted as disease progression.

---

### Precision (Positive Predictive Value)

$$\text{Precision} = \frac{TP}{TP + FP}$$

**Intuition:** Of all the voxels the model called tumour, what fraction were actually tumour? High precision means the model's tumour predictions are trustworthy.

**Typical values:** > 0.80 for WT; ET precision is harder to achieve for small lesions.

**Clinical interpretation:** Low precision means the model is "crying wolf" — labelling too much tissue as tumour. A surgeon relying on a low-precision model would be operating in a larger area than necessary.

---

### F1 Score

For binary segmentation:

$$F_1 = \frac{2 \cdot \text{Precision} \cdot \text{Sensitivity}}{\text{Precision} + \text{Sensitivity}} = \text{Dice}$$

F1 and Dice are mathematically equivalent in the binary case. The difference in naming is primarily a convention: Dice is used in the medical imaging literature; F1 is used in the NLP and general ML literature.

---

### Hausdorff Distance 95th Percentile (HD95)

No simple closed-form formula — it is a distance-based metric.

**Definition:** For every point on the predicted boundary, compute the distance to the nearest point on the GT boundary (and vice versa). HD95 is the 95th percentile of all these distances, measured in millimetres using the voxel spacing from the NIfTI header.

**Why 95th percentile, not maximum?** The maximum Hausdorff distance is sensitive to single outlier voxels. The 95th percentile ignores the worst 5% of boundary errors, making the metric more robust.

**Units:** Always millimetres (mm), not voxels. Always use voxel spacing when computing.

**Typical values for good brain tumour segmentation:**

| Region | Good | Acceptable |
|---|---|---|
| Whole Tumour (WT) | < 5 mm | < 10 mm |
| Tumour Core (TC) | < 6 mm | < 12 mm |
| Enhancing Tumour (ET) | < 4 mm | < 8 mm |

**Clinical interpretation (HD95):** In radiotherapy planning, a HD95 of 5 mm means the model's tumour boundary is within 5 mm of the expert's boundary for 95% of boundary points. Most radiotherapy planning margins (CTV expansion) are 5-15 mm, so a model with HD95 < 5 mm is contributing a boundary accurate enough to be meaningful within that margin.

---

## BraTS Evaluation Reference Table

Performance ranges from published BraTS challenge results (approximate):

| Region | Metric | First Baseline | Competitive | Top Method |
|---|---|---|---|---|
| WT | Dice | 0.75–0.80 | 0.85–0.88 | 0.90–0.92 |
| TC | Dice | 0.65–0.72 | 0.78–0.83 | 0.85–0.88 |
| ET | Dice | 0.55–0.65 | 0.72–0.78 | 0.80–0.84 |
| WT | HD95 (mm) | 15–25 | 5–10 | 3–6 |
| TC | HD95 (mm) | 18–30 | 7–14 | 4–8 |
| ET | HD95 (mm) | 12–22 | 4–9 | 2–5 |

---

## When Each Metric Matters Most

| Clinical Scenario | Primary Metric | Reason |
|---|---|---|
| **Screening** (do not miss disease) | Sensitivity | Missing tumour is dangerous; accept some false positives |
| **Surgical planning** (avoid unnecessary resection) | Specificity + Precision | False positives could expand surgical margins into healthy eloquent cortex |
| **Radiotherapy planning** (accurate tumour boundary) | HD95 | Boundary accuracy directly affects treatment plan quality |
| **Treatment response monitoring** (detect change over time) | Dice + Sensitivity | Need consistent detection across time points |
| **Model comparison** (which is better overall?) | Dice (primary) + HD95 (secondary) | Standard BraTS benchmark; enables literature comparison |
