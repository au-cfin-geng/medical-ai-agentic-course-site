# Clinical AI Cheat Sheet

> **For print:** use browser Print → Save as PDF. Recommended: A4, landscape, single page.

---

## AI Task Types

| Task | What It Predicts | Medical Example | Key Metric |
|---|---|---|---|
| **Classification** | One label for the whole input | "Is this chest X-ray normal or pneumonia?" | AUC, Accuracy, F1 |
| **Segmentation** | A label for every pixel/voxel | "Which voxels are tumour?" | Dice, HD95 |
| **Detection** | Location + presence of an object | "Where are the nodules in this CT?" | Sensitivity, FPR |
| **Prognosis** | Future outcome from current data | "What is 5-year survival from baseline MRI?" | C-index, Brier score |
| **Generation** | Synthetic data or image synthesis | "Synthesise a FLAIR from T1/T2/T1ce" | FID, clinical utility study |

---

## Key Evaluation Metrics

| Metric | Formula | When It Is Useless | When It Matters |
|---|---|---|---|
| **Accuracy** | (TP + TN) / N | When classes are imbalanced (e.g. 1% tumour voxels — a model predicting all background scores 99%) | Only for balanced classes |
| **Dice / F1** | 2TP / (2TP + FP + FN) | When you need to distinguish between missing tumour vs hallucinating tumour | Gold standard for segmentation; handles imbalance |
| **Sensitivity (Recall)** | TP / (TP + FN) | Alone — a model that predicts everything as positive has Sensitivity = 1 | When missing a positive is dangerous (tumour missed) |
| **Specificity** | TN / (TN + FP) | Alone — a model that predicts everything negative has Specificity = 1 | When false positives cause harm (unnecessary surgery) |
| **AUC-ROC** | Area under ROC curve | When you need threshold-specific performance | Comparing models across thresholds |
| **Calibration** | Expected vs observed probabilities | When model scores are not used as probabilities | When model uncertainty is used in clinical decisions |
| **HD95** | 95th percentile Hausdorff distance (mm) | When gross overlap is sufficient | Radiotherapy planning — boundary accuracy matters |

---

## FDA Software as a Medical Device (SaMD) Classes

| Class | Risk Level | Regulatory Path | Example |
|---|---|---|---|
| **Class I** | Low risk | General controls only; most exempt from 510(k) | Fitness tracker, general wellness app |
| **Class II** | Moderate risk | 510(k) Premarket Notification — demonstrate substantial equivalence to predicate | Computer-aided detection of nodules (CAD) |
| **Class III** | High risk | PMA — Premarket Approval, requires clinical trial evidence | AI system making autonomous diagnostic decisions affecting life-sustaining treatment |

**Brain tumour segmentation used as decision support:** typically Class II (moderate risk), 510(k) pathway. Autonomous diagnosis without physician oversight raises Class III questions.

---

## 5 Questions to Ask Before Trusting a Model

1. **What was the training population?**
   (scanner manufacturer, field strength, institution, patient demographics, year of data collection)

2. **What was the test set?**
   (same scanner? same institution? same time period? same label protocol?)

3. **Was the split patient-level?**
   (multiple scans from the same patient must all be in the same split — not split across train/test)

4. **Has it been externally validated?**
   (tested at a different institution, on a different scanner, by a different labelling team)

5. **Who labelled the data and what was inter-rater reliability?**
   (one radiologist? two? what was the Dice between their annotations?)

---

## Red Flags in a Clinical AI Paper

| Red Flag | Why It Matters |
|---|---|
| No patient-level train/test split | Slices or timepoints from the same patient in both sets inflates performance artificially |
| Test set from same scanner and site as training | Model may have learned scanner-specific artefacts, not the clinical pattern |
| No confidence intervals on reported metrics | A Dice of 0.85 means nothing without knowing the uncertainty |
| No failure case analysis | A paper that only shows successes is not describing a real system |
| No clinical comparator | "AI achieves 92%" is uninterpretable without knowing what a radiologist achieves on the same test set |
| Accuracy reported on imbalanced data | Near-perfect accuracy is expected on a 99%/1% dataset from a trivial classifier |
| "Outperforms radiologists" with no reader study | Comparing AI on held-out labels to a radiologist's routine performance is not a fair comparison |
