# Mission 4 — Improve With Intent

This mission is the scientific method applied to model development. You have a hypothesis from Mission 3. You will now test it — with one change, clearly documented, compared to a fixed baseline. The result, whether positive or negative, is science.

---

## Scientific Purpose

The dominant failure mode in applied machine learning research is the untethered improvement cycle: a researcher adds multiple changes, gets a slightly better number, and reports it without being able to explain which change was responsible. This is not science — it is trial and error with a metric. The alternative is hypothesis-driven improvement: you identify a specific failure mode, you identify a mechanism by which a specific intervention should address that failure mode, you make exactly that change, and you evaluate whether performance improved specifically on the cases that were previously failing. This mission requires that discipline. The intervention you make must follow directly from the Mission 3 hypothesis. The evaluation must be specific enough to determine whether the hypothesis was correct — not merely whether the overall metric improved.

---

## Required Background Reading

Before starting this mission, read the following pages on this site:

- [Model Improvement](../medical_ai_workflow/model_improvement.md) — understand the structured improvement cycle and why controlled experiments matter
- [Metrics: Dice, Sensitivity, Specificity](../medical_ai_workflow/metrics_dice_sensitivity_specificity.md) — understand how to read a comparison table
- [Reproducibility](../foundations/reproducibility.md) — understand what must be held constant across runs to make a comparison valid
- [Prompt Best Practices](../agentic_research/prompt_best_practices.md) — the one-change-at-a-time principle

---

## What You Will Ask Claude to Build

Your goal is to implement exactly one hypothesis-driven modification to the training pipeline, retrain the model under otherwise identical conditions, and produce a structured comparison of results.

The modification depends on your Mission 3 hypothesis. Common examples are:

- **If hypothesis was "model fails on small tumours due to class imbalance at the slice level":** add a weighted sampler that over-samples slices containing tumour, or switch to a Dice loss that is less sensitive to class imbalance.
- **If hypothesis was "model fails on small tumours due to lack of augmentation":** add elastic deformation or random scaling augmentation specifically designed to preserve small structures.
- **If hypothesis was "model fails on tumours near the ventricles due to confounding with CSF signal":** investigate whether the T2/FLAIR contrast ratio changes near the ventricles and consider adding a ventricle-proximity feature or adjusting the input normalisation.

Ask Claude to: implement only the specified change in the appropriate script (e.g., only the dataloader, or only the loss function); retrain with the same seed, same number of epochs, and same hyperparameters as the baseline; produce the same evaluation artifacts as Mission 2 (per-case metrics CSV, training log, prediction overlays); and produce a comparison table and a written interpretation of the results.

---

## Expected Artifacts

| Filename | Contents | What Correct Looks Like |
|---|---|---|
| `results/improved/val_metrics.csv` | Per-case Dice for the improved model | One row per case; same case IDs as baseline metrics |
| `results/improved/training_log.csv` | Loss per epoch for the improved run | Comparable or better convergence profile than baseline |
| `results/comparison/comparison_table.md` | Side-by-side comparison of baseline vs improved model | Shows overall mean Dice, but also separately shows Dice for previously-failing cases and previously-succeeding cases |
| `results/comparison/hypothesis_test_figure.png` | Visual evidence for or against the hypothesis | E.g., scatter plot of tumour volume vs Dice for both models overlaid; or bar chart of Dice split by tumour volume quartile |
| `results/comparison/interpretation.md` | Written scientific interpretation | States whether the hypothesis was supported, with reference to specific numbers; acknowledges limitations |

---

## How to Inspect Results

**The comparison table.** Do not look only at overall mean Dice. Look specifically at the cases that were in the failure group in Mission 3. Did those cases improve? By how much? It is entirely valid — and scientifically interesting — if the previously-failing cases improved but some previously-succeeding cases got slightly worse. Document this and try to explain it.

**The hypothesis test figure.** If your hypothesis was about tumour volume, the figure should show Dice vs tumour volume for both models. If your intervention worked, you should see the scatter points in the low-volume region shift upward in the improved model. If the scatter looks identical, the intervention did not address the failure mode.

**The written interpretation.** Read it before you accept it. Does it actually engage with the specific hypothesis from Mission 3, or does it make vague claims about "improvement"? A scientifically honest interpretation might say: "The improved model shows a mean Dice increase of 0.03 on the 10 previously-failing cases, compared to 0.01 on the previously-succeeding cases. This is consistent with the hypothesis that the intervention specifically helps small-tumour cases, though the absolute improvement is modest and may not be clinically meaningful."

**Was the intervention isolated?** Check the git diff (or ask Claude to show you what files were changed). Was exactly one thing changed? If more than one thing changed, you cannot attribute the result to the hypothesis.

---

## Prompt Principle

**One change at a time. Specify the scope of the change explicitly.**

The most common error in this mission is scope creep: Claude, trying to be helpful, makes additional improvements it infers you would want. This destroys the experimental validity of the comparison. You must explicitly name what should not change.

!!! failure "Underconstrained improvement prompt"
    ```
    Improve the model to better handle small tumours.
    ```
    Claude adds augmentation, changes the loss function, adjusts the learning rate schedule, and adds a class-weighted sampler — all at once. When the result improves, you cannot determine which change was responsible.

!!! success "One-change, explicit-scope prompt"
    ```
    Based on the Mission 3 error analysis, I hypothesise that the model fails on small tumours
    because cross-entropy loss gives these voxels negligible gradient signal when class imbalance
    is severe within a 2D slice.

    I want to test this hypothesis by switching from binary cross-entropy to Dice loss.

    Make ONLY the following change:
    - In scripts/loss.py, replace the BinaryCrossEntropy loss with a soft Dice loss.
    - Do not change: model architecture, dataloader, augmentation, learning rate, batch size,
      number of epochs, or random seed.

    After making the change:
    1. Confirm in writing which exact lines changed and in which file.
    2. Retrain using the same command as Mission 2.
    3. Produce results/improved/val_metrics.csv with the same format as Mission 2.
    4. Produce results/comparison/comparison_table.md comparing baseline vs improved,
       broken down by tumour volume quartile.
    ```

The principle: **name the hypothesis → name the intervention → name what must NOT change → specify the evaluation.**

---

## Reflection Questions

1. Your improved model achieves a higher mean Dice than the baseline. How do you know this improvement is not due to random variation? What sample size would you need for the difference to be statistically significant at p < 0.05? (Hint: consider a paired Wilcoxon signed-rank test on per-case Dice scores.)

2. The improvement on previously-failing cases was 0.05 Dice. Is this clinically meaningful? Who would you ask to find out? What would a clinician need to know about a Dice score to judge its clinical relevance?

3. You made one isolated change and got an improvement. A different student made a different change and also got an improvement. How would you determine which change is better? Is "better" even the right word, or are the two changes addressing different failure modes?

4. The improvement required retraining from scratch. In a real clinical AI development cycle with large datasets, retraining might take days. How would you design an ablation study that minimised compute cost while still testing the hypothesis?

5. Your hypothesis was partially supported — the model improved on some failure cases but not others. What does this tell you about the completeness of your Mission 3 hypothesis? What additional failure mode might explain the remaining cases?

---

## Optional Challenge

Perform a two-factor ablation. In addition to your primary intervention, implement one additional change (e.g., if your primary change was the loss function, also test augmentation). Train four models: baseline, loss-only, augmentation-only, and both. Compare all four in a 2x2 table showing mean Dice and failure-case Dice. This is a factorial experimental design — a standard approach in ML research papers that want to attribute credit to specific components. Document whether the effects are additive or whether there is an interaction.

---

## Common Failure Modes

**Multiple changes made simultaneously.** This is the most critical failure. If you compare a model with a new loss function, new augmentation, and a lower learning rate against the baseline, you cannot interpret the result. If you find that Claude has changed more than one thing, ask it to revert to a single change before retraining.

**Comparison uses a different random seed.** If the baseline used seed 42 and the improved model uses seed 0, some of the performance difference may be due to weight initialisation, not the intervention. Verify that the seed is identical across runs.

**No per-case breakdown in the comparison.** Reporting that "mean Dice improved from 0.78 to 0.81" is insufficient to test the hypothesis. You need to show the change specifically in the failure-case subgroup. Ask Claude to produce the comparison table split by tumour volume quartile or by the failure/success classification from Mission 3.

**Declaring success based on a 0.01 Dice improvement.** A change of 0.01 on a 50-case validation set is likely within the variation range of different training runs with the same configuration. Do not claim the hypothesis is confirmed unless the improvement is consistent and plausibly larger than run-to-run noise.

**The intervention trains a new model but evaluation compares to stale baseline metrics.** Verify that the baseline metrics in your comparison table are from the Mission 2 run, not regenerated. If you regenerated them with a different seed, the comparison is confounded.

---

## Expected Learning Outcome

After completing this mission you can: translate a specific scientific hypothesis into a precisely scoped code change; run a controlled experiment with one variable changed and all others held constant; produce a comparison table that breaks down results by the subgroup relevant to the hypothesis; write a scientific interpretation that honestly addresses whether the hypothesis was confirmed, refuted, or partially supported; explain why ablation studies are a core tool in ML research and what makes them valid.
