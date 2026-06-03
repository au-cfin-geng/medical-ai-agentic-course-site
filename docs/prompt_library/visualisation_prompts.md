# Visualisation Prompts

Visualisation is not decoration — it is verification. Every plot you generate during this lab should answer a specific question. These templates ask Claude to produce plots that are readable, correctly labelled, and interpretable by someone who has not seen the data before.

After each plot is generated, use the "What to Check" section to verify the output before trusting it.

---

## 1. MRI Slice with Label Overlay

**When to use:** Mission 1 (data inspection) and Mission 3 (error analysis). Use any time you need to see whether labels align with the underlying anatomy.

**Why it works:** It specifies exactly which modality, which slice plane, how many cases, and how the overlay should be rendered. This prevents Claude from producing a technically correct plot that is visually uninterpretable (wrong colourmap, overlay too opaque, slice not through tumour).

**Failure it prevents:** An overlay where the label and image are misaligned because the NIfTI affine was not applied, or a colourmap where background and tumour are indistinguishable.

```
Generate a figure showing MRI slices with segmentation label overlays.

Data: [DATA_ROOT]
Cases to show: [CASE_ID_1], [CASE_ID_2], [CASE_ID_3]
Modality: [MODALITY] (e.g. T1ce)
View: axial (fixed at the slice with maximum tumour area for each case)
Layout: 3 rows (one per case) × 3 columns (image only | label only | overlay)

Rendering requirements:
- Image: use a grey colourmap, normalise intensity to [1st, 99th] percentile per case
- Label colourmap (fixed across all cases):
    0 = background: fully transparent
    1 = NCR (necrotic core): red, alpha 0.5
    2 = ED (oedema): yellow, alpha 0.4
    4 = ET (enhancing tumour): cyan, alpha 0.6
- Add a legend to the first row only
- Add a colourbar for the image intensity to the "image only" column
- Title each row with the case ID
- Title each column: "T1ce", "Label", "Overlay"
- Add a scale bar indicating 10 mm (use the voxel spacing from the NIfTI header)
- Figure size: 12 × 10 inches at 150 dpi

Save to: [PROJECT_ROOT]/results/figures/label_overlay_[MISSION].png

After saving, open the file and verify:
- Is the tumour visible in the image?
- Does the label overlay sit on top of the tumour (not in an empty region)?
- Are all three label classes present in at least one case?
```

**What to check in the generated figure:**

- Tumour is visible in the image column (not a blank slice)
- Overlay colours match the legend
- Label boundaries align with visible signal changes in the image
- Case IDs are correct in the row titles
- Scale bar is present and plausible (should span roughly 10 mm of anatomy)
- No row is all-black or all-white (suggests normalisation failure)

---

## 2. Training Curve Plot

**When to use:** During or after Mission 2 training, to monitor learning progress.

**Why it works:** It specifies both axes, both metrics, dual y-axes if needed, and the smoothing method — preventing a plot that is technically correct but unreadable because raw batch-level loss is too noisy.

**Failure it prevents:** A training curve that does not separate train and validation, making it impossible to diagnose overfitting. Or a Dice curve that starts at zero because the model learns slowly and the y-axis was not adjusted.

```
Generate a training curve figure from the training log at [LOG_FILE_PATH].

Expected log format: CSV or JSON with columns/keys:
epoch, train_loss, val_loss, train_dice, val_dice
(if your log has different column names, adapt the prompt accordingly)

Plot specification:
- Figure size: 12 × 5 inches
- Two subplots side by side:

  Left subplot — Loss:
  - x-axis: Epoch (integer)
  - y-axis: Loss value (log scale if loss > 10× initial value by end of training)
  - Two lines: train_loss (solid blue) and val_loss (dashed orange)
  - Apply Savitzky-Golay smoothing (window=7, poly=2) if more than 30 epochs
  - y-axis label: "Loss"

  Right subplot — Dice score:
  - x-axis: Epoch (integer)
  - y-axis: Dice score (range 0 to 1)
  - Three lines if available: Dice for WT (solid), TC (dashed), ET (dotted)
  - Or single Dice line if only one region was tracked
  - Add a horizontal dashed grey line at y=0.85 labelled "Good performance threshold"

Both subplots:
- Add vertical dashed red line at the epoch with the best val_loss (annotate with epoch number)
- x-axis label: "Epoch"
- Legend in upper right
- Grid lines: major only, alpha 0.3
- Title: "Training Curves — [MODEL_NAME] — [DATE]"

Save to: [PROJECT_ROOT]/results/figures/training_curves_[RUN_ID].png
Also print: best epoch number, best val_loss, Dice at best epoch.
```

**What to check in the generated figure:**

- Both train and validation lines are present
- Loss is decreasing over time (if flat from epoch 1, something is wrong)
- Dice is increasing over time
- The best-epoch marker is plausible (not epoch 1, not the last epoch with worse performance)
- No line goes to exactly 0 or 1 (suggests a bug in the metric calculation)
- Axis labels are present and correctly named

---

## 3. Per-Case Metric Comparison Chart

**When to use:** Mission 3 (error analysis) — after evaluation, to see the distribution of performance across cases.

**Why it works:** Summary statistics (mean Dice) hide the distribution. This plot reveals bimodal performance (easy cases and hard cases), outliers, and which region is hardest to segment. Assigning Claude to produce a sorted plot forces per-case granularity.

**Failure it prevents:** Reporting a mean Dice of 0.82 while missing that 10% of cases have Dice below 0.3 — which would be clinically dangerous.

```
Generate a per-case metric comparison chart from the evaluation results at [METRICS_CSV_PATH].

Expected CSV columns: case_id, dice_wt, dice_tc, dice_et, hd95_wt, hd95_tc, hd95_et

Plot specification:
- Figure size: 14 × 8 inches
- Two subplots stacked vertically:

  Top subplot — Dice scores:
  - x-axis: Cases sorted by dice_wt (ascending left to right)
  - y-axis: Dice score (0 to 1)
  - Three grouped bars per case: WT (blue), TC (orange), ET (green)
  - Bar width: narrow enough to see all cases without overlap
  - Add a horizontal dashed line at the mean for each region (same colour, dashed)
  - Annotate: mean ± std in the legend label, e.g. "WT: 0.85 ± 0.12"
  - y-axis label: "Dice Score"
  - Title: "Per-Case Dice Scores (sorted by WT Dice)"

  Bottom subplot — HD95 scores:
  - Same x-axis ordering (same case sort as top)
  - y-axis: HD95 in mm
  - Three lines (not bars): one per region
  - y-axis label: "Hausdorff Distance 95% (mm)"
  - Add a horizontal dashed grey line at HD95 = 5 mm labelled "Radiotherapy planning threshold"

Both subplots:
- x-axis tick labels: case IDs, rotated 90°, font size 6
- Shade the worst 10% of cases (by WT Dice) in a light red background
- Add a text box in the bottom-left: "Worst 10%: N=[COUNT] cases"

Save to: [PROJECT_ROOT]/results/figures/per_case_metrics.png
Also print the IDs of the 10 worst cases by WT Dice.
```

**What to check in the generated figure:**

- Cases are correctly sorted (WT Dice should increase left to right)
- The shaded region marks the worst cases, not the best
- Mean lines are visually distinguishable from bar heights
- The HD95 plot uses the same x-axis case ordering as the Dice plot
- Case IDs are readable (even if small)

---

## 4. Failure Case Gallery

**When to use:** Mission 3 (error analysis), after identifying the worst-performing cases.

**Why it works:** Looking at failure cases visually is irreplaceable — a case with Dice 0.2 might have a completely missed tumour, a fragmented prediction, or a good prediction of a tiny tumour. The visual tells you which. This template asks Claude to select and render the worst N cases in a consistent layout.

**Failure it prevents:** Drawing conclusions about failure modes from metrics alone, missing the difference between a systematic spatial error and a data labelling anomaly.

```
Generate a failure case gallery for the [N] worst-performing cases.

Input data:
- Metrics CSV: [METRICS_CSV_PATH] (column: dice_wt, case_id)
- Predictions directory: [PREDICTIONS_DIR] (one NIfTI per case: {case_id}_pred.nii.gz)
- Ground truth directory: [GROUND_TRUTH_DIR] (one NIfTI per case: {case_id}_seg.nii.gz)
- Images directory: [IMAGES_DIR] (T1ce: {case_id}_t1ce.nii.gz)

Select the [N] cases with the lowest dice_wt.

For each case, create a row with 4 panels:
  Panel 1: T1ce image, axial slice with max ground truth tumour area, grey colourmap
  Panel 2: Ground truth overlay (same colourmap as the standard: NCR=red, ED=yellow, ET=cyan)
  Panel 3: Prediction overlay (same colourmap)
  Panel 4: Error map:
    - True Positive (both agree tumour): green
    - False Negative (GT tumour, pred background): red
    - False Positive (pred tumour, GT background): blue
    - True Negative (both agree background): white

Each row title: "Case [ID] — WT Dice: [VALUE:.3f] — Rank [RANK]/[TOTAL]"
Add a shared legend below the figure.
Figure size: 16 × (N × 3) inches

Save to: [PROJECT_ROOT]/results/figures/failure_gallery_[N]cases.png

After saving, list the case IDs included and their Dice scores in the terminal.
```

**What to check in the generated figure:**

- Error map colours are logically consistent (green where GT and prediction agree)
- The slice shown is actually through the tumour (not an empty slice)
- Ground truth and prediction panels use identical view and slice for each case
- Case IDs and Dice scores in titles match the metrics CSV

---

## 5. Before/After Improvement Comparison Plot

**When to use:** Mission 4 (model improvement), to demonstrate the effect of a change.

**Why it works:** Side-by-side metric comparisons with the same cases force a fair comparison. Asking for a paired difference plot (not just two separate bar charts) makes it easier to see which cases improved and which regressed — which is more informative than comparing means.

**Failure it prevents:** Concluding that a model improved when the mean Dice increased by 0.01 but variance also increased, meaning some cases got much worse. Or comparing two models on different subsets of cases.

```
Generate a before/after improvement comparison plot.

Input:
- Baseline metrics: [BASELINE_METRICS_CSV] (columns: case_id, dice_wt, dice_tc, dice_et)
- Improved metrics: [IMPROVED_METRICS_CSV] (same format)
- Model names: Baseline = "[BASELINE_NAME]", Improved = "[IMPROVED_NAME]"

Verify that both CSVs contain exactly the same set of case IDs before plotting.
If they differ, report which cases are missing and stop.

Plot layout: 3 subplots side by side (one per region: WT, TC, ET)

For each region subplot:
  Top panel (scatter):
  - x-axis: Baseline Dice for this region
  - y-axis: Improved Dice for this region
  - Each case is a dot
  - Colour: green if improved > baseline + 0.02, red if improved < baseline - 0.02, grey otherwise
  - Add diagonal y=x line (dashed black) labelled "No change"
  - Add text box: "Improved: N cases, Degraded: N cases, Unchanged: N cases"

  Below each scatter (box plot):
  - Two boxes: baseline and improved, for this region
  - Show individual points as jittered dots
  - Annotate with mean ± std

Figure title: "[BASELINE_NAME] vs [IMPROVED_NAME] — [DATE]"
Figure size: 15 × 10 inches

Save to: [PROJECT_ROOT]/results/figures/before_after_[BASELINE_NAME]_vs_[IMPROVED_NAME].png

Print a summary table:
| Region | Baseline Mean | Improved Mean | Delta | p-value (paired t-test) | Cases Improved | Cases Degraded |
```

**What to check in the generated figure:**

- Both CSVs have the same number of cases (check the "Verify" step output)
- The diagonal line is visible and cases scatter around it (not all on one side, which would suggest a bug)
- The colour coding matches the legend
- The p-value is from a paired test, not an unpaired one

---

## Quick Reference

| Template | Question It Answers | Key Check After Plot |
|---|---|---|
| MRI Slice Overlay | Do labels align with anatomy? | Overlay on tumour, not empty region |
| Training Curves | Is the model learning? | Both train and val lines present |
| Per-Case Metrics | Which cases are hardest? | Worst 10% shaded correctly |
| Failure Gallery | What does failure look like spatially? | Error map colours logically consistent |
| Before/After Comparison | Did my change actually help? | Same case IDs in both models |
