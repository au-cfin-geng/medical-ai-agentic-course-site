# Modeling Prompts

Use these templates during Mission 2 — Build the First Detector. The core principle is: **plan before you code**. The planner prompt is not optional. Starting with code before a plan is the most reliable way to produce a technically impressive but scientifically wrong implementation.

These prompts follow a deliberate sequence: plan → implement → train → evaluate → compare. Do not skip steps.

---

## 1. Planner Role Prompt

**When to use:** Before asking Claude to write any modelling code. This is the first prompt in the Mission 2 sequence.

**Why it works:** Assigning Claude the role of a Planner — with explicit instruction to produce a plan and stop — prevents the most common agentic coding failure: generating a long, complex implementation immediately, which looks impressive but embeds decisions that should have been made explicitly. A plan forces those decisions to the surface where you can review them.

**Failure it prevents:** A training loop that uses the wrong loss function for multi-class segmentation, a U-Net with an incorrect number of output channels, or an evaluation that measures accuracy instead of Dice — all because implementation proceeded before requirements were clear.

**Customisation:** Fill in your specific constraints (GPU/CPU, time budget, expected dataset size). Add any architectural preferences you already have. If you want Claude to use a specific library (e.g. `monai`, `segmentation_models_pytorch`), state it here.

```
Act as a Planner. Your job is to produce a complete step-by-step implementation plan.
You must not write any code until I approve the plan.

Task: Implement a 2D U-Net for brain tumour segmentation on BraTS data.

Project context:
- Framework: PyTorch [VERSION or "latest stable"]
- Hardware: [CPU only / GPU: describe]
- Dataset: BraTS [YEAR], [N] training cases, 4 modalities, label classes 0/1/2/4
- Input: 2D axial slices extracted from 3D volumes
- Output: Per-pixel class predictions (4 classes: background, NCR, ED, ET)
- Evaluation metrics: Dice for WT, TC, ET; HD95 for WT, TC, ET
- Time budget: [DURATION] minutes of training

Produce a plan with these sections:

1. Architecture decision
   - Why 2D slices (not 3D volumes)?
   - U-Net depth (number of encoder levels) — justify the choice
   - Number of filters at each level
   - Input channels: [state how you handle 4 modalities]
   - Output channels: [state how you handle BraTS label convention including class 4 vs index 3]

2. Data pipeline
   - How will slices be extracted from 3D volumes?
   - How will the dataset be split (train/val/test)?
   - What augmentations will you apply and why?
   - How will you handle class imbalance?

3. Training setup
   - Loss function — justify choice for multi-class segmentation
   - Optimiser and learning rate schedule
   - Batch size (given the hardware constraint)
   - Number of epochs
   - Checkpoint strategy

4. Evaluation
   - How will Dice be computed (per-case or averaged over batches)?
   - How will BraTS derived regions (WT, TC, ET) be assembled from model output?
   - What constitutes a successful baseline? (state a target Dice)

5. File structure
   - What files will be created?
   - What goes in each file?

6. Risks and assumptions
   - List 3 decisions that could be wrong and would be difficult to fix later.
   - For each, state what evidence you would need to confirm the decision.

Do not proceed to code until I say "approved — proceed to implementation".
```

---

## 2. U-Net Implementation Prompt

**When to use:** After approving the Planner's output. Provide the approved plan as context.

**Why it works:** It specifies the architecture completely — encoder depth, skip connections, output activation, channel counts — leaving no room for Claude to make silent architectural decisions. It also requires the model to be testable immediately with a random tensor, which catches shape bugs before any real data is involved.

**Failure it prevents:** A U-Net with a ReLU before the final layer (wrong for logits), incorrect skip connection handling, or an output channel count that does not match the number of label classes.

**Customisation:** Adjust `[ENCODER_LEVELS]`, `[BASE_CHANNELS]`, and `[INPUT_CHANNELS]` to match your approved plan. If you want batch normalisation replaced by instance normalisation (common in medical imaging), state it explicitly.

```
Implement a 2D U-Net for brain tumour segmentation based on the approved plan.

Architecture specification (from approved plan):
- Input: (batch, [INPUT_CHANNELS], H, W) — [INPUT_CHANNELS] modalities as channels
- Encoder: [ENCODER_LEVELS] levels, base channels = [BASE_CHANNELS], doubling each level
- Bottleneck: [BASE_CHANNELS × 2^ENCODER_LEVELS] channels
- Decoder: symmetric to encoder, with skip connections via concatenation
- Output: (batch, [NUM_CLASSES], H, W) — raw logits, no softmax (softmax in loss)
- Normalisation: [BatchNorm / InstanceNorm] after each convolution
- Activation: ReLU (not LeakyReLU unless justified)
- Pooling: MaxPool2d(2) in encoder, ConvTranspose2d(2) in decoder

Requirements:
1. Implement in a file: scripts/model.py
2. The class must be named UNet2D
3. Include a forward() method
4. Include a docstring describing input/output shapes
5. Add a quick test at the bottom:
   if __name__ == "__main__":
       model = UNet2D(in_channels=[INPUT_CHANNELS], num_classes=[NUM_CLASSES])
       x = torch.randn(2, [INPUT_CHANNELS], 256, 256)
       out = model(x)
       print(f"Input: {x.shape} → Output: {out.shape}")
       assert out.shape == (2, [NUM_CLASSES], 256, 256), f"Shape mismatch: {out.shape}"
       print("Shape test passed.")

After writing the file:
1. Run python scripts/model.py
2. If the shape test fails, fix the bug before reporting to me
3. Show me the full model summary: total parameters, trainable parameters
4. Confirm that gradients flow through the model (use torch.autograd.grad or backward on a dummy loss)
```

---

## 3. Training Loop Prompt

**When to use:** After the U-Net passes its shape test and the data loader is verified.

**Why it works:** It specifies every component of the training loop explicitly — loss function, metric logging, checkpoint frequency, validation cadence — and requires the loop to log to a file as well as the console. This makes training resumable and auditable, not just runnable.

**Failure it prevents:** A training loop that crashes at epoch 10 with no checkpoint saved, losing all progress. Or a loop that logs only to the console, making it impossible to plot training curves later. Or a Dice metric computed over batches (batch-averaged) rather than per-case, which gives a biased estimate.

**Customisation:** Adjust `[LOSS_FUNCTION]` (e.g. `CrossEntropyLoss`, `DiceLoss`, `DiceCELoss`), `[CHECKPOINT_EVERY_N_EPOCHS]`, and `[MAX_EPOCHS]`. If using a learning rate scheduler, specify it here.

```
Implement a training loop for the UNet2D model.

Write to: scripts/train.py

Requirements:

1. Command-line interface (argparse):
   --data_dir [default: data/]
   --output_dir [default: results/]
   --epochs [default: 50]
   --batch_size [default: 8]
   --lr [default: 1e-4]
   --checkpoint_every [default: 5]
   --resume [optional: path to checkpoint to resume from]
   --seed [default: 42]

2. Reproducibility:
   - Set random seeds for Python, NumPy, and PyTorch at the start
   - Log the full argparse config to [output_dir]/config.json

3. Loss function: [LOSS_FUNCTION]
   - If using CrossEntropyLoss, remap BraTS label 4 → index 3 before computing loss
   - Class weights: [none / compute from class frequency / specify: ...]

4. Training loop (per epoch):
   - Iterate over training batches, compute loss, backpropagate, update weights
   - Log: epoch, batch, loss (every 10 batches)
   - Compute mean training loss for the epoch

5. Validation loop (every epoch):
   - No gradient computation
   - Compute per-case Dice for WT, TC, ET (assemble from model output)
   - Compute mean Dice across all validation cases (not batch average)
   - Log: epoch, val_loss, val_dice_wt, val_dice_tc, val_dice_et

6. Logging:
   - Append all epoch-level metrics to [output_dir]/training_log.csv
   - Print a one-line summary per epoch to console
   - Format: "Epoch {e}/{total} | Loss: {l:.4f} | Val Dice WT: {d:.3f} TC: {d:.3f} ET: {d:.3f}"

7. Checkpointing:
   - Save checkpoint every [CHECKPOINT_EVERY_N_EPOCHS] epochs to [output_dir]/checkpoints/
   - Always save the best model (by val_dice_wt) to [output_dir]/best_model.pt
   - Checkpoint must include: model state, optimiser state, epoch, best metric so far

8. After writing, show me the argparse help text to confirm all arguments are present.
   Then run: python scripts/train.py --epochs 2 --batch_size 2 --data_dir [DATA_DIR] --output_dir results/smoke_test/
   This should complete without error and produce a training_log.csv.
```

---

## 4. Evaluation Loop Prompt

**When to use:** After training is complete, to produce per-case metrics for the full test set.

**Why it works:** Separating evaluation from training means the evaluation script is reusable across multiple model checkpoints and can be run without re-training. Requiring per-case metrics (not just the mean) is essential for Mission 3 error analysis.

**Failure it prevents:** Evaluating only on validation cases (not the held-out test set), computing Dice on batch-averaged predictions (not per-case), or not saving the metrics to a file — making it impossible to compare models later.

**Customisation:** Replace `[CHECKPOINT_PATH]` and `[TEST_DATA_DIR]`. If your model was trained on 2D slices, specify how to reconstruct the 3D volume from slice predictions for HD95 computation.

```
Implement a standalone evaluation script.

Write to: scripts/evaluate.py

Requirements:

1. Command-line interface:
   --checkpoint [path to model checkpoint]
   --data_dir [test data directory]
   --output_dir [where to write results]
   --split [train / val / test, default: test]

2. Load the model from the checkpoint and set to eval mode.

3. For each case in the specified split:
   a. Load all 4 modalities
   b. Extract 2D slices, run model inference on each slice
   c. Reconstruct the 3D prediction volume from slice predictions
   d. Apply argmax to get the predicted label map (one label per voxel)
   e. Remap prediction indices back to BraTS convention (if label 4 was remapped during training)

4. Compute per-case metrics on the 3D volumes:
   - Dice for WT (classes 1+2+4), TC (classes 1+4), ET (class 4)
   - HD95 for WT, TC, ET (in mm, using voxel spacing from NIfTI header)
   - Sensitivity for WT, TC, ET
   - Specificity for WT, TC, ET
   - If a region is empty in both GT and prediction: Dice = 1.0 (agreement on absence)
   - If a region is empty in GT but not prediction: Dice = 0.0

5. Save per-case results to [output_dir]/metrics_per_case.csv
   Columns: case_id, dice_wt, dice_tc, dice_et, hd95_wt, hd95_tc, hd95_et, sensitivity_wt, specificity_wt

6. Save summary statistics to [output_dir]/metrics_summary.json
   For each metric: mean, std, median, 25th percentile, 75th percentile, min, max

7. Print a clean summary table to the console.

8. After writing the script, run:
   python scripts/evaluate.py --checkpoint [CHECKPOINT_PATH] --data_dir [TEST_DATA_DIR] --output_dir results/evaluation/
   Show me the console summary table.
```

---

## 5. Model Comparison Prompt

**When to use:** Mission 4 (after implementing an improvement), to formally compare two or more model checkpoints on the same test set.

**Why it works:** A formal comparison requires the same data, the same metric implementation, and a statistical test — not just a visual scan of two mean values. This template enforces that structure and asks for an honest assessment, including cases where the new model is worse.

**Failure it prevents:** Comparing models on different subsets of data, claiming improvement without a statistical test, or not reporting the cases where the improved model actually degraded.

**Customisation:** Add or remove metrics. Specify a different statistical test if appropriate (e.g. Wilcoxon signed-rank test for non-normal distributions, which Dice scores often are).

```
Act as an objective model evaluator. Compare two model checkpoints using the held-out test set.

Model A (baseline): [BASELINE_CHECKPOINT_PATH], name: "[BASELINE_NAME]"
Model B (improved): [IMPROVED_CHECKPOINT_PATH], name: "[IMPROVED_NAME]"
Test data: [TEST_DATA_DIR]
Evaluation script: scripts/evaluate.py (already implemented)

Steps:
1. Run evaluate.py for Model A. Save results to results/eval_baseline/
2. Run evaluate.py for Model B. Save results to results/eval_improved/
3. Load both metrics_per_case.csv files. Verify they cover identical case IDs.
   If not identical, stop and report the difference.

4. For each metric (dice_wt, dice_tc, dice_et, hd95_wt, hd95_tc, hd95_et):
   a. Compute mean ± std for each model
   b. Compute per-case difference (Model B - Model A)
   c. Run a paired Wilcoxon signed-rank test (not paired t-test, as Dice may not be normal)
   d. Report p-value and whether the difference is significant at α = 0.05

5. Produce a comparison table:
   | Metric | Baseline | Improved | Delta | p-value | Significant |

6. Identify cases where Model B degraded relative to Model A (delta < -0.05 on dice_wt):
   - List their case IDs
   - Report their mean Dice under both models
   - These are "regression cases"

7. Write a brief (5-sentence) honest assessment:
   - Did Model B improve overall?
   - Which region benefited most?
   - Were there regressions?
   - Is the improvement clinically meaningful (not just statistically significant)?
   - What would you conclude if reviewing this for a journal submission?

Save the comparison table to results/model_comparison.csv
```

---

## Quick Reference

| Template | Cognitive Task | Must Come Before |
|---|---|---|
| Planner | Decide before acting | Any code |
| U-Net Implementation | Build to specification | Approved plan |
| Training Loop | Produce auditable, resumable training | Verified dataloader + model |
| Evaluation Loop | Measure per-case on held-out set | Trained checkpoint |
| Model Comparison | Compare honestly with statistics | Two evaluation runs |
