# Dice and Error Analysis Cheatsheet

> **For print:** File → Print → Save as PDF. Keep beside you during Missions 2–4.

---

## Dice Formula and Worked Example

**Formula:**

```
DSC = (2 × |Predicted ∩ Reference|) / (|Predicted| + |Reference|)
    = 2 × TP / (2 × TP + FP + FN)
```

Range: 0 (no overlap) to 1 (perfect overlap).

**Worked example:**

```
Reference mask:  1000 tumour voxels
Predicted mask:  1100 voxels flagged as tumour

True Positives (TP):   900   (in both)
False Positives (FP):  200   (predicted but not in reference)
False Negatives (FN):  100   (in reference but not predicted)

DSC = 2 × 900 / (2 × 900 + 200 + 100)
    = 1800 / 2100
    = 0.857
```

This model over-segments slightly (more FP than FN) but achieves reasonable overlap.

---

## Sensitivity and Specificity Formulas

| Metric | Formula | Clinical interpretation |
|---|---|---|
| **Sensitivity** (Recall) | TP / (TP + FN) | Proportion of true tumour voxels correctly detected. Low sensitivity = missed tumour. |
| **Specificity** | TN / (TN + FP) | Proportion of healthy voxels correctly labelled healthy. Low specificity = over-segmentation into healthy tissue. |
| **Precision** (PPV) | TP / (TP + FP) | Of voxels called tumour, how many actually are? Useful for characterising false positive burden. |

Note: Dice is a function of TP, FP, and FN only — it does not use TN. For volumetric segmentation, TN (background voxels correctly labelled background) is enormous and would dominate accuracy calculations. Dice avoids this distortion.

---

## HD95 Explanation

**Hausdorff Distance at 95th percentile (HD95)** measures boundary accuracy, not volume overlap. While Dice tells you how much of the tumour you found, HD95 tells you how far off your boundary is at its worst point (excluding the top 5% of outliers).

```
HD95 units: millimetres (or voxels, depending on implementation)
HD95 = 0:   perfect boundary agreement
HD95 = 5:   boundary errors up to 5 mm (clinically meaningful in brain tumour)
HD95 = 20:  boundary errors up to 20 mm (large systematic error)
```

**When to use HD95:** When Dice scores are similar between methods but clinical application is sensitive to boundary accuracy (e.g., radiation therapy planning where the margin is defined at the tumour boundary).

---

## BraTS Benchmark Reference Ranges

These ranges represent approximate performance levels from the BraTS challenge leaderboard history. They serve as calibration, not as targets. Your baseline will likely sit below the "good" range; that is expected.

| Subregion | Below expectation | Acceptable | Good | Top-performing |
|---|---|---|---|---|
| **Whole Tumour (WT)** | < 0.70 | 0.70–0.82 | 0.83–0.90 | > 0.90 |
| **Tumour Core (TC)** | < 0.55 | 0.55–0.72 | 0.73–0.85 | > 0.85 |
| **Enhancing Tumour (ET)** | < 0.50 | 0.50–0.68 | 0.69–0.82 | > 0.82 |

WT is systematically the easiest subregion because it is the largest and most diffuse. ET is systematically the hardest because it is the smallest and most variable. A simple threshold baseline will typically score in the "acceptable" range for WT and "below expectation" for ET.

---

## Error Map Colour Code

When generating a voxel-level error map, use this colour convention consistently across all missions:

| Colour | Meaning | Formula | Clinical significance |
|---|---|---|---|
| **Green** | True Positive (TP) | Predicted = 1, Reference = 1 | Correctly identified tumour |
| **Red** | False Positive (FP) | Predicted = 1, Reference = 0 | Healthy tissue labelled as tumour |
| **Blue** | False Negative (FN) | Predicted = 0, Reference = 1 | Tumour tissue missed by the model |
| **Black** | True Negative (TN) | Predicted = 0, Reference = 0 | Correctly identified background |

In your visualisation prompts: "Produce an error map using green=TP, red=FP, blue=FN, black=TN for the whole tumour subregion."

---

## Failure Mode Taxonomy

Use this taxonomy when writing your Mission 3 failure analysis. Assign one primary failure mode per case.

| Failure mode | Definition | Metric signature | Likely cause | Mission 4 hypothesis direction |
|---|---|---|---|---|
| **Undersegmentation** | Predicted volume substantially smaller than reference | Low sensitivity, moderate specificity, low Dice | Threshold too high; conservative model | Lower threshold; reduce size filter |
| **Oversegmentation** | Predicted volume substantially larger than reference | High sensitivity, low specificity, moderate Dice | Threshold too low; aggressive model | Raise threshold; add connected component filter |
| **Boundary error** | Volume correct but boundary inaccurate | Moderate Dice, high HD95 | Insufficient spatial resolution; smoothing kernel mismatch | Adjust postprocessing; use boundary-aware loss |
| **Location error** | Prediction in wrong anatomical region | Very low Dice despite reasonable predicted volume | Registration failure; modality confusion | Verify registration; add anatomical prior |
| **Fragmentation** | Correct voxels but scattered as disconnected components | Low precision; multiple small FP blobs | No connectivity constraint | Apply largest-component filter; add morphological closing |
| **Subregion confusion** | Whole tumour reasonable but TC/ET wrong | WT Dice acceptable, TC or ET Dice very low | Label hierarchy misapplied | Verify label convention; check if label 4 is being correctly isolated |
