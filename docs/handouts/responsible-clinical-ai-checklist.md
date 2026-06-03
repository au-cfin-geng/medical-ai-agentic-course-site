# Responsible Clinical AI Checklist

> **For print:** File → Print → Save as PDF. Complete both checklists before submitting your Mission 6 translation brief.

This checklist operationalises the responsible clinical AI principles practised throughout the course. It is not a bureaucratic exercise — each item maps to a documented failure mode in real clinical AI deployments. Skipping an item is a decision with consequences, and those consequences should be named.

---

## Checklist A: Before Claiming a Result

Complete this checklist before reporting any performance number from your segmentation pipeline.

- [ ] **Patient-level train/test split.** Confirm that no patient who appears in training data (or in any preprocessing step that uses labels) also appears in the test set. Slice-level or case-level mixing inflates all metrics.

- [ ] **Fixed random seed declared.** The random seed used for any stochastic component (initialisation, data shuffling, augmentation) is recorded in CLAUDE.md and in your outputs. A result that cannot be exactly reproduced is not a result.

- [ ] **External or held-out validation attempted.** At minimum, the test set is held out from all development decisions. Note explicitly if no external (different-site) validation was performed — this limits generalisability claims.

- [ ] **Failure analysis completed.** You have characterised at least the worst-performing case. Reporting only the mean Dice without examining failures is incomplete reporting.

- [ ] **Class imbalance acknowledged.** The proportion of tumour to background voxels in your test set is reported. Metrics that ignore class imbalance (such as accuracy) are not used without justification.

- [ ] **Metrics appropriate for the clinical task.** Dice and HD95 are appropriate for segmentation. If you are making a claim about clinical utility, you have identified a clinical outcome metric (not just Dice) and noted whether you measured it.

- [ ] **Comparison to baseline included.** Your result is compared to at least one interpretable baseline (threshold, atlas, or published benchmark). A result without a baseline is uninterpretable.

- [ ] **Uncertainty acknowledged.** You have reported confidence intervals, standard deviation across cases, or at minimum noted the number of cases on which your estimate is based. A Dice of 0.84 based on three cases is not the same as a Dice of 0.84 based on 300 cases.

---

## Checklist B: Before Communicating to a Clinical Collaborator

Complete this checklist before presenting your Mission 6 translation brief to anyone outside the lab — including a simulated clinical collaborator during the student showcase.

- [ ] **Plain language used throughout.** Every technical term (Dice, sensitivity, false positive, segmentation) is either defined in plain English on first use or replaced with a clinical equivalent. Read your brief aloud: if it sounds like an ML paper, it is not ready for a clinical audience.

- [ ] **No ML jargon without definition.** Specific jargon check: "model," "threshold," "training data," "ground truth," "epoch," "inference." If any of these appear undefined, rewrite.

- [ ] **Prototype maturity stated explicitly.** The brief states, in its opening paragraph, which level of clinical readiness the system has reached (Level 1–5; see Clinical AI One-Page Reference). The phrase "ready for clinical use" is not used unless the system has regulatory clearance.

- [ ] **At least three specific limitations listed.** Limitations are specific to this system, this dataset, and this evaluation — not generic disclaimers. "This was evaluated on BraTS-style synthetic data, not on routine clinical MRI from your institution" is a specific limitation. "AI systems have limitations" is not.

- [ ] **What was NOT demonstrated is explicitly named.** A dedicated section or bullet list states: what patient populations were excluded, what clinical conditions were not tested, what workflow steps were not evaluated. A collaborator who acts on your brief deserves to know its boundaries.

- [ ] **Human oversight requirements specified.** The brief describes concretely who reviews the model output, at what point in the workflow, and what decision authority they have. It does not assume that the model output is self-evidently interpretable to a non-specialist.

- [ ] **Not described as "ready for deployment."** Confirm that no sentence in the brief — including any AI-generated language — implies the system is ready to enter clinical use without further validation. If Claude generated any such language, it has been removed.

- [ ] **Stakeholder questions anticipated.** The brief anticipates and addresses at least two questions a clinical collaborator would reasonably ask: "How does this compare to what a radiologist would do?" and "What would happen if the model was wrong?" If you do not have answers, say so explicitly.
