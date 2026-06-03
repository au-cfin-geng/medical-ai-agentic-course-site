# Mission 2 — Build the First Detector

The baseline model is not the final model. It is the reference point everything else will be measured against. This mission is about running the full train-evaluate loop for the first time, producing concrete numbers, and not claiming more than those numbers support.

---

## Scientific Purpose

A baseline model establishes the lower bound of performance that any subsequent improvement must exceed. Without a properly trained and evaluated baseline, improvement claims are not scientifically credible — you cannot know whether your new technique helped or whether the baseline was simply undertrained. This mission requires you to train a U-Net (or equivalent architecture provided in the lab repository), evaluate it on the held-out validation set, and produce structured metrics and prediction visualisations. The specific Dice score you achieve is less important than the rigour of the evaluation: per-case metrics, not just mean; validation set, not training set; saved predictions you can examine visually, not just numbers.

---

## Required Background Reading

Before starting this mission, read the following pages on this site:

- [Segmentation Basics](../foundations/segmentation_basics.md) — understand U-Net architecture and why it dominates medical image segmentation
- [Baseline Modeling](../medical_ai_workflow/baseline_modeling.md) — understand what a proper baseline evaluation requires
- [Metrics: Dice, Sensitivity, Specificity](../medical_ai_workflow/metrics_dice_sensitivity_specificity.md) — understand how each metric is computed and what it tells you
- [Reproducibility](../foundations/reproducibility.md) — understand why random seeds, saved checkpoints, and logged hyperparameters matter
- [Prompt as Protocol](../agentic_research/prompt_as_experimental_protocol.md) — understand the Planner role before you use it in this mission

---

## What You Will Ask Claude to Build

Your goal is to set up and run a complete training and evaluation loop for the baseline segmentation model. The lab repository contains a model architecture, a dataloader, and a training script stub — your job is to direct Claude to complete and run the training pipeline, not to design it from scratch.

Ask Claude to first describe its plan in plain language before writing any code: what functions it will implement, how data will flow from the NIfTI files through the model to a loss value, how checkpoints will be saved, and how evaluation metrics will be computed per case on the validation set. Review the plan. Then ask Claude to implement it.

The training should run for at least 50 epochs (or whatever the course instructors specify). Metrics must be computed per validation case, not just as a dataset mean. Predictions for a sample of validation cases must be saved as PNG overlays. A training log must be saved as a CSV file showing loss per epoch.

You are responsible for understanding the hyperparameters Claude uses. If Claude chooses a learning rate, batch size, or loss function without explaining why, ask for the rationale before accepting them.

---

## Expected Artifacts

| Filename | Contents | What Correct Looks Like |
|---|---|---|
| `results/training_log.csv` | Loss value (and optionally learning rate) per epoch | Loss should decrease monotonically in early epochs; no NaN values |
| `results/val_metrics.csv` | Per-case Dice, sensitivity, specificity for each validation case | One row per case; no rows with all-zero metrics (suggests prediction is all-background) |
| `checkpoints/best_model.pth` | Best model checkpoint saved by validation Dice | File exists; you can load it with `torch.load()` without errors |
| `results/sample_predictions/case_XXX_overlay.png` | Prediction overlay for 3-5 validation cases | Coloured prediction region corresponds plausibly to the tumour; not entirely blank or entirely filled |
| `results/run_config.json` | Hyperparameters used for this run | Records seed, learning rate, batch size, number of epochs, loss function, augmentation settings |

---

## How to Inspect Results

**Training loss curve.** Open `training_log.csv` and plot it (or ask Claude to plot it). Does the loss decrease? If it does not decrease after the first 10 epochs, something is wrong — check learning rate, data normalisation, and loss function. If the loss drops to zero immediately, check whether the model is being evaluated on the training set rather than the validation set.

**Validation metrics.** Open `val_metrics.csv`. What is the mean Dice across cases? For BraTS whole-tumour segmentation, a properly trained baseline U-Net should achieve Dice > 0.70. If the mean Dice is below 0.30, the model is likely predicting nearly all-background — check the sigmoid threshold. If the mean Dice is above 0.90, verify that you are evaluating on the validation set and not the training set.

**Per-case distribution.** Look at the minimum and maximum Dice values, not just the mean. Are there cases with Dice = 0.0? These are total failures — make a note of them. They will be the focus of Mission 3.

**Prediction overlays.** Look at the PNG files. Do the predicted regions look like tumours — roughly oval, within the brain parenchyma, not spanning the entire image? If predictions look like random noise or cover the entire slice, the model has not learned a useful representation.

**Config file.** Verify that `run_config.json` actually contains the hyperparameters used. You will need these for the comparison table in Mission 4.

---

## Prompt Principle

**Use the Planner role first. Do not let Claude jump straight to code.**

Large codebases have many interactions between components. If Claude writes training code without a plan, it may make architectural assumptions about the dataloader that conflict with what is already in the repository, or use variable names that clash with existing functions. The plan-first approach catches these issues before they are baked into generated code.

!!! failure "Jump-to-code prompt"
    ```
    Write a training script for the U-Net.
    ```
    Claude writes a complete training script. It may work in isolation but conflict with the existing dataloader. You spend 30 minutes debugging import errors.

!!! success "Planner role prompt"
    ```
    Before writing any code, act as a software architect. Read the existing files in scripts/ and models/.
    Describe in plain English:
    1. What functions already exist that the training loop should call
    2. What functions are missing and need to be written
    3. What the data flow looks like from raw NIfTI files to a scalar loss value
    4. How checkpoints will be saved and what filename convention you will use
    5. How validation metrics will be computed per case and written to a CSV
    Do not write any code yet. Wait for my approval of this plan before proceeding.
    ```
    Claude reads existing code, identifies gaps, and proposes a plan that integrates with what is already there. You review it, ask clarifying questions, and only then authorise implementation.

The principle: **plan before code; review before run; check before claim.**

---

## Reflection Questions

1. Your training script uses a fixed random seed. If you deleted the checkpoint and retrained with the same seed, would you get exactly the same validation metrics? What factors could cause the results to differ even with a fixed seed?

2. The validation Dice score you report is the mean across all cases. A colleague claims their model achieves a higher mean Dice. What additional information would you need before concluding their model is better?

3. You saved the model checkpoint after the best validation epoch. What is the risk of using validation loss (or Dice) to decide when to stop training and save the checkpoint? What is this called, and how is it typically addressed in ML research?

4. The training script ran for the specified number of epochs. How do you know it has converged? Plot the loss curve — is it still decreasing at the final epoch? What would you do if it is?

5. Claude chose a specific loss function (e.g., binary cross-entropy, Dice loss, or a combination). Do you understand why? What would change in the predicted output if you switched loss functions? This is not rhetorical — look up the implications of at least two alternatives.

---

## Optional Challenge

Implement a simple test-time augmentation (TTA) strategy: at inference time, predict on the original image and on horizontally flipped copies of the image, then average the probability maps before thresholding. Evaluate whether TTA changes the mean validation Dice. Document the compute cost (inference time with vs without TTA). This is a standard technique in medical image segmentation competitions — understanding it gives you a concrete example of how inference-time choices affect performance independently of training.

---

## Common Failure Modes

**CUDA out of memory.** The most common error when training on MRI volumes. The full 3D volume (240x240x155x4 channels) does not fit in most GPU memories with a batch size > 1. The solution is 2D slice-based training (each slice is an input) or patch-based 3D training. If the lab repository is set up for 2D slice training and you accidentally configure 3D inputs, you will see this error immediately. Ask Claude to check the dataloader's `__getitem__` method and confirm what shape it returns.

**NaN loss from the first epoch.** Causes include: learning rate too high; data not normalised (raw MRI intensities can be in the thousands); sigmoid not applied before Dice loss computation (log of zero). Ask Claude to add a gradient norm check and to print min/max values of the first batch.

**All-zero predictions (Dice = 0 for all cases).** The model predicts background everywhere. This is the class imbalance problem: cross-entropy on an imbalanced dataset will drive the model to predict the majority class. Check whether the loss function uses class weighting or Dice loss. Also check whether the sigmoid threshold (usually 0.5) is appropriate — try lowering it to 0.3.

**Validation metrics not saved per case.** Claude produces a single mean Dice value and considers the evaluation complete. This is insufficient — you cannot do Mission 3 without per-case metrics. Explicitly require a CSV with one row per case before accepting the evaluation as complete.

**Checkpoint not saved.** The training runs but `best_model.pth` does not exist. Either the checkpoint logic has a bug, or the script saved to a different path. Ask Claude to add a line that prints the checkpoint path every time it saves, and check that the file exists on disk after training.

---

## Expected Learning Outcome

After completing this mission you can: direct Claude to implement a training loop that integrates with existing code using a plan-first approach; interpret a training loss curve and identify common failure modes; read and critically evaluate a per-case metrics CSV; articulate what a baseline model is and why it must be evaluated with the same rigour as any improved model; describe the class imbalance problem in medical image segmentation and at least two approaches to address it.
