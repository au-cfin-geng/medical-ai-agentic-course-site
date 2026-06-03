# Clinical AI One-Page Reference

> **For print:** File → Print → Save as PDF. Keep this beside you during Mission 6 and the student showcase.

---

## AI Task Types

| Task Type | What the model predicts | Clinical example | Primary metric |
|---|---|---|---|
| **Classification** | A category label for the whole input | "Is this scan malignant or benign?" | AUC, accuracy, F1 |
| **Detection** | The presence and location of a finding | "Where are the lesions in this image?" | Sensitivity, PPV, free-response ROC |
| **Segmentation** | Which pixels/voxels belong to a target structure | "Outline the tumour in 3D" | Dice, HD95, sensitivity, specificity |
| **Prognosis** | A future outcome or survival probability | "What is the 12-month recurrence risk?" | C-index, calibration, time-dependent AUC |

In this course: all missions use **segmentation** of brain tumour subregions from multi-modal MRI.

---

## Clinical Readiness Spectrum

| Level | Name | What it means | What evidence exists |
|---|---|---|---|
| 1 | **Proof of concept** | Runs on a sample. No controlled evaluation. | Internal test, no external validation |
| 2 | **Benchmark performance** | Good Dice/AUC on a held-out test set from the same distribution as training | Single-centre or challenge leaderboard |
| 3 | **External validation** | Performance confirmed on data from a different centre or country | Multi-site study, no prospective element |
| 4 | **Prospective validation** | Performance confirmed in prospective patient workflow, not retrospective data | Registered prospective study |
| 5 | **Regulatory clearance** | Approved for a specific clinical use by FDA, CE, or equivalent | FDA 510(k) / De Novo, CE mark |

**After completing this two-day course, your model is at Level 1 or Level 2.** State this explicitly in your Mission 6 translation brief.

---

## 5 Questions Before Trusting Any AI Model

1. **What population was it trained on?** If the training data does not include your patient population, all performance numbers are estimates at best.
2. **What is the reference standard?** Dice against expert annotation is not the same as Dice against pathological ground truth. Know what the labels represent.
3. **Was the test set patient-level separated from training?** If the same patient appears in training and test — even in different time points — the results are invalid.
4. **What are the failure modes?** A model that fails silently on the cases that matter most (small tumours, rare subtypes, atypical presentations) may still have a high mean Dice.
5. **Who has replicated it?** A single paper with a strong result is a hypothesis. A result that survives independent replication is evidence.

---

## Red Flags in a Clinical AI Paper

- Mean performance reported without per-case distribution or confidence intervals.
- No comparison to a simple baseline (thresholding, atlas, or clinician performance).
- Test set from the same scanner or site as the training set, with no external validation.
- Failure modes not characterised, or characterised only as "edge cases."
- Claims about clinical utility without a prospective study or clinical outcome measure.

---

## The Human Oversight Principle

No AI system used in clinical care should operate without a defined mechanism for human review of its outputs before those outputs influence patient decisions. The appropriate level of oversight depends on the risk of the task and the maturity of the evidence base — but for any system at Levels 1–4 on the clinical readiness spectrum, the default is: a qualified clinician reviews the AI output before it is acted upon.
