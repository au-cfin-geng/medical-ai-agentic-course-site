# Error Analysis Prompts

Use these templates during Mission 3 — Investigate Failure. Error analysis is the scientific core of the lab. The goal is not to explain away failures — it is to generate testable hypotheses about why the model fails on specific cases, so that Mission 4 improvements are targeted rather than random.

These prompts assign Claude the roles of analyst, inspector, and critic. Each role has a specific cognitive function.

---

## 1. Performance Ranking Prompt

**When to use:** Immediately after running evaluation on the test set, as the first step of Mission 3.

**Why it works:** Sorting cases by performance creates a clear, reproducible ranking that all subsequent analysis builds on. Asking for the worst 10 (not just the mean) makes the problem concrete and actionable.

**Failure it prevents:** Analysing the "average" failure instead of the actual failures, which often share specific characteristics that are invisible in aggregate statistics.

**Customisation:** Change the metric (`dice_wt`, `dice_tc`, `dice_et`, `hd95_wt`) depending on which region your team is investigating. Adjust `[N]` based on how many cases you have time to inspect.

```
Act as a performance analyst.

Load the per-case evaluation results from [METRICS_CSV_PATH].
Columns: case_id, dice_wt, dice_tc, dice_et, hd95_wt, hd95_tc, hd95_et

Produce the following:

1. Full ranking table (all cases, sorted by dice_wt ascending)
   Add a "rank" column (1 = worst)
   Add a "percentile" column (percentile rank of this case)

2. Summary statistics:
   | Metric | Mean | Std | Median | P25 | P75 | Min | Max |
   (for dice_wt, dice_tc, dice_et, hd95_wt)

3. Worst [N] cases by dice_wt:
   Show: case_id, dice_wt, dice_tc, dice_et, hd95_wt
   Also show: whether this case was in the worst 10% for TC and ET as well
   Label cases that fail all three regions as "triple failure"

4. Best [N] cases by dice_wt:
   Same columns as above

5. Discordant cases (high dice_wt but low dice_et, or vice versa):
   Cases where |dice_wt - dice_et| > 0.3 — these are interesting edge cases

6. Save the full ranked table to [PROJECT_ROOT]/results/case_ranking.csv
   Save the worst [N] case IDs to [PROJECT_ROOT]/results/worst_cases.txt (one ID per line)

Print a two-sentence interpretation: what does the spread of Dice scores tell you about the model?
```

---

## 2. Failure Pattern Analysis Prompt

**When to use:** After ranking cases and identifying the worst [N]. This is the core Mission 3 prompt.

**Why it works:** The Inspector role assigns Claude a specific analytical task: not just describing what failed, but identifying patterns across failures. Requiring structured hypotheses (not prose observations) means each hypothesis can be tested with a targeted experiment.

**Failure it prevents:** Concluding "the model is bad at ET" without understanding whether the failure is due to small ET regions, low contrast, incorrect preprocessing, or class imbalance — conclusions that point to completely different fixes.

```
Act as an Inspector. Your task is to identify failure patterns in the worst-performing cases.

Inputs:
- Worst case IDs: [PROJECT_ROOT]/results/worst_cases.txt
- Full evaluation metrics: [METRICS_CSV_PATH]
- Data statistics computed earlier: [PROJECT_ROOT]/results/data_statistics.csv
  (columns: case_id, tumour_volume, et_fraction, mean_t1ce_intensity, contrast_to_noise_ratio, n_components)

Analysis steps:

1. Merge the two CSVs on case_id.
   For the worst [N] cases, extract: dice_wt, dice_tc, dice_et, tumour_volume, et_fraction, contrast_to_noise_ratio, n_components

2. Compare the worst cases to the best cases (top [N] by dice_wt):
   - Are tumour volumes systematically different? (t-test or Mann-Whitney, report p-value)
   - Are contrast-to-noise ratios different?
   - Are the number of connected components different?
   - Is the ET fraction (ET/WT ratio) different?

3. For each failure pattern hypothesis below, report SUPPORTED / NOT SUPPORTED / INCONCLUSIVE
   based on the statistics:
   - "Small tumours are harder to segment" (worst cases have lower tumour volume)
   - "Low contrast tumours are harder" (worst cases have lower CNR)
   - "Multi-focal tumours are harder" (worst cases have more connected components)
   - "Cases with prominent ET are harder" (worst cases have higher ET fraction)

4. Generate 2 additional hypotheses of your own, based on the data.
   For each: state the hypothesis, what evidence supports it, and what experiment would test it.

5. Rank all hypotheses by: (a) strength of evidence and (b) ease of testing.

Present results as a structured table:
| Hypothesis | Evidence | Supported? | Experiment to test |

Do not propose any model changes yet.
```

---

## 3. Spatial Error Visualisation Prompt

**When to use:** After identifying the worst cases, to understand the spatial structure of errors.

**Why it works:** Spatial errors have structure — the model may consistently fail at tumour boundaries, in the centre of large tumours, or at specific anatomical locations. A spatial heatmap makes this structure visible, which a Dice score cannot.

**Failure it prevents:** Assuming that all error is uniform when in fact the model has a specific spatial blind spot (e.g. consistently undersegmenting the posterior tumour boundary in radiotherapy-relevant anatomy).

**Customisation:** Adjust the `[WORST_N_CASES]` to match your worst case list. If you want to separate error types (FP vs FN), the template already handles this — but you can restrict to just FN if clinical false negatives are your primary concern.

```
Generate spatial error maps for the worst-performing cases.

Inputs:
- Worst case IDs: [PROJECT_ROOT]/results/worst_cases.txt (use first [WORST_N_CASES])
- Predictions: [PREDICTIONS_DIR]/{case_id}_pred.nii.gz
- Ground truth: [GROUND_TRUTH_DIR]/{case_id}_seg.nii.gz

For each case:
1. Create a 3D error volume where each voxel is coded as:
   - 0: True Negative (background in both GT and prediction)
   - 1: True Positive (tumour in both)
   - 2: False Negative (tumour in GT, background in prediction) — missed tumour
   - 3: False Positive (background in GT, tumour in prediction) — hallucinated tumour

2. Compute, per axial slice:
   - Count of FN voxels
   - Count of FP voxels
   - Fraction of GT tumour that is FN per slice
   Identify the "most errored slice" (highest FN count) per case.

3. For the worst [WORST_N_CASES] cases, produce:
   - A 4-panel figure per case:
     Panel 1: T1ce axial slice through the most errored slice
     Panel 2: GT label overlay
     Panel 3: Predicted label overlay
     Panel 4: Error map (0=grey, 1=green, 2=red, 3=blue)
   - Label FP and FN counts in the panel 4 title

4. Aggregate spatial analysis (across all worst cases):
   - Average FN rate per axial slice position (z position as fraction of volume height)
   - Plot this as a line chart: x = normalised z position (0=bottom, 1=top), y = mean FN rate
   - This shows whether errors are concentrated in specific regions of the head (e.g. near the skull base)

Save all figures to [PROJECT_ROOT]/results/figures/spatial_errors/
Save the per-slice error statistics to [PROJECT_ROOT]/results/spatial_error_stats.csv
```

---

## 4. Hypothesis Generation Prompt

**When to use:** After spatial analysis, to move from description to explanation. This is where you ask Claude to act as a critic who generates competing explanations.

**Why it works:** The Critic role prevents premature convergence on a single explanation. By requiring multiple competing hypotheses and ranking them by testability, this prompt structures the intellectual work of root-cause analysis and directs it toward actionable experiments.

**Failure it prevents:** Jumping from "the model fails on small tumours" directly to "I should add data augmentation" without considering whether the failure is actually caused by class imbalance, intensity non-normalisation, architectural receptive field limitations, or label noise.

```
Act as a Critic. Based on the failure analysis so far, generate competing hypotheses about why the model fails.

Context summary (fill in from your analysis):
- Worst cases are characterised by: [CHARACTERISTICS FROM PATTERN ANALYSIS]
- Spatial errors are concentrated at: [SPATIAL FINDING]
- The model's overall performance is: Dice WT=[X], TC=[Y], ET=[Z]
- Training setup: [BRIEF SUMMARY — epochs, loss, augmentation, architecture]

Task:
Generate exactly 5 competing hypotheses for the observed failures.
Each hypothesis must implicate a different cause from this list (use each category once):
  A. Data quality (label noise, preprocessing inconsistency)
  B. Architecture (insufficient capacity, wrong receptive field)
  C. Training procedure (loss function, class imbalance, learning rate)
  D. Dataset composition (train/val distribution mismatch, outlier cases)
  E. Evaluation methodology (metric bias, boundary handling)

For each hypothesis:
1. State the hypothesis in one clear sentence
2. Explain the causal mechanism: why would this cause the observed failure pattern?
3. Evidence for: what in the analysis supports this?
4. Evidence against: what in the analysis contradicts this?
5. Proposed experiment: what specific change or check would confirm or rule out this hypothesis?
6. Estimated effort: Low (< 1 hour) / Medium (1-4 hours) / High (> 4 hours)
7. Expected impact if hypothesis is correct: Minor / Moderate / Major improvement

Present as a structured table, then rank all 5 by: (effort × expected impact) — prioritise low effort, high impact first.
```

---

## 5. Root Cause Analysis Prompt

**When to use:** After generating and ranking hypotheses, to select the most promising one and design a targeted experiment.

**Why it works:** Root cause analysis (RCA) is a structured process used in engineering and clinical safety to distinguish symptoms from causes. Assigning this role to Claude prevents the common mistake of treating a symptom (low Dice on ET) as a cause — and then optimising the wrong thing.

**Failure it prevents:** Adding data augmentation to solve a problem that is actually caused by a label remapping bug in the data loader, spending lab time on an intervention that cannot work.

```
Act as a Root Cause Analysis engineer. We will investigate the top-priority hypothesis from the analysis.

Top hypothesis to investigate: [HYPOTHESIS FROM STEP 4]
Priority reason: [WHY THIS WAS RANKED HIGHEST]

Conduct a structured root cause analysis:

1. Reproduce the failure
   - Select the single worst-performing case: [CASE_ID]
   - Load the model, run inference on this case only
   - Report: predicted class distribution, GT class distribution, Dice per region
   - Visualise: show the 5 most errored slices

2. Test the hypothesis mechanistically
   For hypothesis [A/B/C/D/E], run the following specific check:
   [DESCRIBE CHECK — e.g. "Inspect the ground truth label for this case visually" / "Print the per-class loss contribution during training" / "Check the receptive field of the model against the tumour size"]

3. Establish the counterfactual
   - What would the output look like if the hypothesis is correct?
   - What would the output look like if the hypothesis is wrong?
   - Which matches what we observe?

4. Decision
   Based on the evidence, state:
   - "Hypothesis CONFIRMED" / "Hypothesis REFUTED" / "Inconclusive — need more data"
   - If confirmed: what is the minimum intervention to fix this?
   - If refuted: which hypothesis should we test next?

5. Write a 3-sentence RCA summary suitable for a lab report:
   "The primary failure mode observed was [X]. The root cause appears to be [Y], as evidenced by [Z]. The recommended intervention is [W]."

Do not implement any fixes yet. Report your findings and wait for my instruction.
```

---

## Quick Reference

| Template | Role Assigned | Output | Leads To |
|---|---|---|---|
| Performance Ranking | Performance analyst | Ranked case table, worst case list | Failure Pattern Analysis |
| Failure Pattern Analysis | Inspector | Hypothesis table with evidence | Spatial Visualisation |
| Spatial Error Visualisation | Visual analyst | Error maps, spatial heatmap | Hypothesis Generation |
| Hypothesis Generation | Critic | 5 competing hypotheses, ranked | Root Cause Analysis |
| Root Cause Analysis | RCA engineer | Confirmed/refuted cause, minimum fix | Mission 4 implementation |
