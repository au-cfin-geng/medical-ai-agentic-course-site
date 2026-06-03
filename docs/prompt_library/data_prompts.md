# Data Inspection Prompts

Use these templates during Mission 1 — Receive the Signal. The goal of data inspection is to form a factual picture of your dataset before you make any modelling decisions. Every assumption you leave unverified at this stage becomes a potential source of error that is much harder to diagnose later.

These prompts assign Claude the role of a rigorous data analyst. They ask for structured outputs you can read quickly and refer back to throughout the lab.

---

## 1. Dataset Summary Prompt

**When to use:** The first time you interact with a new dataset, before any visualisation or modelling.

**Why it works:** It forces a complete enumeration of the dataset rather than relying on README claims. Counts, shapes, and class distributions are computed from the actual files, not from documentation that may be out of date.

**Failure it prevents:** Training a model on an unbalanced dataset without knowing it; using the wrong input shape; missing cases because a subdirectory was overlooked.

**Customisation:** Replace `[DATA_ROOT]` with your actual path. If your dataset uses a different label convention (e.g. 0/1/2/3 vs 0/1/2/4), update the class list. Add `include_intensity_stats: True` if you want mean and standard deviation per modality.

```
Act as a data analyst. Produce a complete summary of the BraTS dataset at [DATA_ROOT].

For each split (train, validation, test — or all cases if no split exists):

1. Case count
   - Total number of cases
   - Number of complete cases (all 4 modalities present: T1, T1ce, T2, FLAIR)
   - Number of incomplete cases (any modality missing)

2. Volume dimensions
   - List all unique (X, Y, Z) shapes found across the dataset
   - Report voxel spacing (mm) for the first 5 cases
   - Flag any case where spacing differs from the majority

3. Label statistics (from segmentation masks)
   - For each label class (0=background, 1=NCR, 2=ED, 4=ET):
     * Mean voxel count across all cases
     * Minimum and maximum voxel count
     * Number of cases where this class has zero voxels (class absent)
   - Derived regions: WT (1+2+4), TC (1+4), ET (4) — same statistics

4. Data types
   - NIfTI header dtype for images and labels
   - Any cases where dtype is unexpected (e.g. float label maps)

5. File size summary
   - Mean and total size of image files (MB)

Present all results as tables. Do not plot anything yet.
At the end, list any anomalies or cases I should inspect manually.
```

---

## 2. Label Quality Check Prompt

**When to use:** After the dataset summary, to verify that segmentation labels are anatomically plausible before training.

**Why it works:** It assigns Claude the role of a neuroradiology-aware analyst who checks spatial consistency, not just voxel counts. Many corrupted or mislabelled cases have correct file headers but anatomically impossible labels.

**Failure it prevents:** Training on corrupted labels that look fine statistically but are spatially wrong — for example, an enhancing tumour label appearing in the skull, or a necrotic core with no surrounding oedema.

**Customisation:** Adjust `[N_CASES]` based on your dataset size. For a dataset of 50 cases, inspect all of them. For 300+, a random sample of 20 is sufficient. Add specific anatomical rules if you know them (e.g. "ET should only appear within TC").

```
Act as a neuroradiology-aware data quality engineer.
Inspect the segmentation labels for [N_CASES] randomly selected cases from [DATA_ROOT].

For each case, check the following and report PASS / WARN / FAIL:

Spatial plausibility checks:
1. Is the tumour (WT = classes 1+2+4) located within the brain parenchyma?
   (Approximate check: WT centroid should be within the central 60% of the volume)
2. Is the enhancing tumour (ET, class 4) contained within the tumour core (TC = 1+4)?
3. Is the necrotic core (NCR, class 1) surrounded by enhancing tumour or oedema?
4. Are there any isolated label voxels (single-voxel islands disconnected from the main region)?

Size plausibility checks:
5. Is WT volume between 100 and 200,000 voxels? (flag if outside this range)
6. Does each class that is present have a contiguous connected component of at least 10 voxels?

Consistency checks:
7. Does the label file have the same spatial dimensions as the corresponding T1ce image?
8. Does the label file contain only expected values (0, 1, 2, 4)? Flag any unexpected value.

Report format:
| Case ID | Check 1 | Check 2 | ... | Check 8 | Overall | Notes |

After the table, summarise:
- How many cases passed all checks?
- Which checks generated the most warnings or failures?
- Name the top 3 cases I should visually inspect as a priority.
```

---

## 3. Missing Modality Check Prompt

**When to use:** Mission 1, after the dataset summary, specifically if the summary flagged any incomplete cases.

**Why it works:** It produces an exact inventory of what is missing rather than a vague "some modalities may be absent." This lets you make an explicit decision — exclude those cases, impute, or flag for the report — rather than silently training on incomplete data.

**Failure it prevents:** A training loop that crashes or silently uses zeros for missing modalities, producing a model that behaves unexpectedly on complete data at inference time.

**Customisation:** Update `[EXPECTED_MODALITIES]` if your dataset uses different naming conventions. Add a column for file size if you suspect some files exist but are empty.

```
Act as a data integrity auditor.
Perform a complete missing modality audit of the dataset at [DATA_ROOT].

Expected modalities per case: [EXPECTED_MODALITIES]
(e.g. t1.nii.gz, t1ce.nii.gz, t2.nii.gz, flair.nii.gz, seg.nii.gz)

For each case directory:
1. List which expected files are present and which are missing
2. For present files: report file size in KB (flag any file smaller than 100 KB as potentially corrupted)
3. For present files: confirm the NIfTI header can be read without error

Produce:
- A full table: Case ID | t1 | t1ce | t2 | flair | seg | Any issues
  (mark each cell: present / missing / corrupted)
- Summary counts: 
  * Cases with all modalities present
  * Cases missing exactly one modality (list which one)
  * Cases missing two or more modalities
  * Cases with a readable file that returns an error on header read

Recommendation:
- Based on the audit, which cases should be excluded from training?
- Which cases could potentially be salvaged (e.g. only seg missing, images complete)?
- Write the list of excluded case IDs to [PROJECT_ROOT]/results/excluded_cases.txt
```

---

## 4. Outlier Case Identification Prompt

**When to use:** Mission 1, after the basic summary, to flag unusual cases before training.

**Why it works:** Outlier cases — unusually large tumours, extreme class imbalance, unusual imaging intensity — have a disproportionate effect on training. Identifying them early lets you decide whether to include, weight, or exclude them. This prompt assigns Claude the role of a statistical auditor who uses numeric evidence rather than visual inspection.

**Failure it prevents:** A model whose learning is dominated by two unusually large cases, or a validation metric that is inflated because a very easy case is always predicted correctly and masks failure on difficult cases.

**Customisation:** Adjust `[OUTLIER_THRESHOLD]` (default: 2 standard deviations from the mean). Add intensity-based checks if you suspect scanner heterogeneity.

```
Act as a statistical data auditor.
Identify outlier cases in the dataset at [DATA_ROOT] using the following criteria.
Outlier threshold: [OUTLIER_THRESHOLD] standard deviations from the mean (default: 2.0)

Compute the following per-case statistics:
1. Total tumour volume (WT voxel count)
2. Enhancing tumour fraction (ET / WT, or 0 if WT = 0)
3. Mean T1ce intensity within the tumour mask (WT region)
4. Mean T1ce intensity outside the tumour mask (background brain)
5. Contrast-to-noise ratio: (mean_tumour - mean_background) / std_background
6. Number of disconnected components in the WT mask (ideally 1)

For each statistic, flag cases that are more than [OUTLIER_THRESHOLD] SDs from the mean.

Report:
- Table of all cases with their statistics
- Highlighted outliers per criterion
- Cases that are outliers on 3 or more criteria (these are candidates for exclusion)

Save the per-case statistics table to [PROJECT_ROOT]/results/data_statistics.csv
At the end, give a brief interpretation: what do these outliers suggest about the dataset?
Do not exclude any cases yet — only flag them for my review.
```

---

## 5. Data Loading Verification Prompt

**When to use:** After writing or receiving a data loading function, before using it in a training loop.

**Why it works:** Data loading bugs are invisible until training fails or produces unexpected results. This prompt instructs Claude to run a complete batch loading test and check every property that matters for training — shape, dtype, value range, label classes present. It catches problems at the loading stage, where they are easy to fix.

**Failure it prevents:** Training for hours on a dataset where labels were accidentally transposed, intensities were not normalised, or the batch dimension was wrong — producing a model that appears to train but learns nothing.

**Customisation:** Replace `[DATALOADER_FILE]` with your actual data loading script. Adjust `[BATCH_SIZE]` and `[INPUT_CHANNELS]` to match your architecture. Add modality-specific intensity range expectations if you know them.

```
Act as a quality assurance engineer for a machine learning pipeline.
Test the data loading function in [DATALOADER_FILE].

Run the following verification:

1. Instantiate the dataset and dataloader with:
   - batch_size = [BATCH_SIZE]
   - split = 'train'
   - Any required arguments from the function signature

2. Load exactly one batch and check:
   Image tensor:
   - Shape: should be (batch, [INPUT_CHANNELS], H, W) or (batch, [INPUT_CHANNELS], D, H, W)
   - dtype: should be torch.float32
   - Value range: report min and max; flag if min < -10 or max > 10 (suggests no normalisation)
   - Contains NaN: should be False
   - Contains Inf: should be False

   Label tensor:
   - Shape: should match image spatial dimensions
   - dtype: should be torch.long or torch.int64
   - Unique values: report all unique values present; expected set is {0, 1, 2, 4} for BraTS
   - Class distribution in this batch: count of voxels per class

3. Load 5 consecutive batches and verify:
   - No batch causes an exception
   - Shapes are consistent across batches
   - Label unique values remain in expected set

4. Test edge cases:
   - What happens if a case has no tumour (all-zero label)? Does it load without error?

Report format:
| Check | Expected | Actual | Status |

If any check fails, show the exact error message and propose a fix.
Do not modify the dataloader until I approve the proposed fix.
```

---

## Quick Reference

| Template | Role Assigned | Key Output |
|---|---|---|
| Dataset Summary | Data analyst | Tables of counts, shapes, class balance |
| Label Quality Check | Neuroradiology-aware auditor | Per-case PASS/WARN/FAIL table |
| Missing Modality Check | Data integrity auditor | Inventory of missing files, exclusion list |
| Outlier Identification | Statistical auditor | Per-case statistics CSV, flagged outliers |
| Data Loading Verification | QA engineer | Batch-level check table, fix proposals |
