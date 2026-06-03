# Mission 1 — Receive the Signal

You have a dataset. You have not looked at it. Mission 1 is the act of looking. Before any model is trained, a scientist must understand the raw material: how many cases, what modalities, what the labels look like, where the distribution is skewed. This mission produces that understanding.

---

## Scientific Purpose

The single most common cause of poor model performance is a dataset the researcher did not understand before training. Class imbalance that is ignored leads to models that predict the dominant class; corrupt or outlier cases that are not identified during training pollute the loss signal; spatial resolution differences across scanners that are not detected lead to systematic generalisation failures. This mission is not preprocessing. It is not training. It is disciplined observation — the same scientific act that precedes any experiment. You will produce a data report that would let a colleague understand the dataset without opening a single file themselves. This report will become the Methods section of any paper you write based on this data.

---

## Required Background Reading

Before starting this mission, read the following pages on this site:

- [MRI Basics](../foundations/mri_basics.md) — understand what T1, T2, and FLAIR sequences show
- [Brain Tumour Imaging](../foundations/brain_tumour_imaging.md) — understand the BraTS label structure (whole tumour, tumour core, enhancing tumour)
- [Voxels, Slices, and Spacing](../mri/voxels_slices_and_spacing.md) — understand how MRI volumes are structured as 3D arrays
- [Labels, Masks, and Annotation](../mri/labels_masks_and_annotation.md) — understand what the segmentation masks contain
- [Data Inspection](../medical_ai_workflow/data_inspection.md) — understand what a good data inspection covers
- [Roles for Claude](../agentic_research/roles_for_claude.md) — understand the Inspector role before you assign it

---

## What You Will Ask Claude to Build

Your goal is to produce a comprehensive data inspection report for the BraTS dataset in your lab repository. The report should cover: how many training cases are present; what files are in each case directory; the voxel dimensions and spacing for a sample of cases (and whether they are consistent); the intensity distribution of each MRI modality (T1, T1ce, T2, FLAIR) across a sample of cases; the class distribution in the segmentation labels — how many voxels are background, whole tumour, tumour core, and enhancing tumour, expressed both as raw counts and percentages; and visualisations of representative MRI slices with the segmentation overlay for at least 5 cases.

The report should also flag any suspicious cases: cases where the label file is empty (no tumour annotated), cases where image dimensions differ from the majority, or cases where intensity values are extreme (suggesting a normalisation issue).

Ask Claude to act specifically as a data analyst, not a model developer. If Claude starts writing training code, redirect it. The goal is insight, not a model.

---

## Expected Artifacts

| Filename | Contents | What Correct Looks Like |
|---|---|---|
| `data_inspection/data_report.md` | Main report with statistics, observations, and embedded figure references | Organised sections; includes a table of summary statistics; explicitly states class imbalance ratio |
| `data_inspection/figures/sample_slices_case_XXX.png` | Axial, coronal, and sagittal slice for 5 cases with segmentation overlay | Brain anatomy is recognisable; tumour overlay (coloured) corresponds to a plausible location within the brain |
| `data_inspection/figures/class_distribution.png` | Bar chart of voxel counts per label class | Background should be ~95-97% of voxels; tumour subregions add to ~3-5% |
| `data_inspection/figures/intensity_histograms.png` | Intensity histograms for each modality | Each modality shows a roughly bimodal distribution (brain tissue, non-brain); no modality has all values at zero |
| `data_inspection/suspicious_cases.txt` | List of any flagged cases with reason | If none, file says "No suspicious cases found." |

---

## How to Inspect Results

Do not simply check that the files exist. Look at them.

**Slice figures:** Open a few PNG files. Do you see a recognisable brain cross-section? Is the tumour overlay in a plausible location (not at the edge of the image, not covering the entire brain)? Do the FLAIR slices look qualitatively different from the T1 slices? If the images are all black or all white, something went wrong with the windowing.

**Class distribution:** The BraTS 2020 dataset has severe class imbalance — approximately 97% background voxels. If your plot shows something close to 50/50, the label loading is wrong. If the enhancing tumour class is larger than the tumour core, something is wrong with the label interpretation.

**Intensity histograms:** Each modality should show a histogram with most values near zero (skull-stripped background) and a peak representing brain parenchyma. If all values are in a very narrow range (0 to 1), the data has already been normalised — note this in the report; it is important context for your training script.

**Suspicious cases:** Open the flagged files and look at them visually. Do they actually look abnormal? Are they worth excluding? Make a note of your decision — you will need to justify it if someone asks.

---

## Prompt Principle

**Assign a role that constrains behaviour, not just describes it.**

Telling Claude "act as a data analyst" is weaker than telling Claude "act as a data analyst and do NOT write any model training code." Explicit negatives help in complex codebases where Claude might try to be helpful by setting up the next step before you have asked for it.

!!! failure "Role without constraint"
    ```
    Analyse this dataset and tell me what you find.
    ```
    Claude may write training code, propose a model architecture, and produce figures — but skip the statistical summary you actually needed.

!!! success "Role with constraint and scope"
    ```
    Act as a data analyst, not a model developer. Do not write any training or evaluation code.
    Your task is to inspect the dataset at data/brats2020/training/ and answer these specific questions:
    1. How many cases are present?
    2. Are image dimensions consistent across cases? Report any outliers.
    3. What is the voxel-level class distribution across all training cases?
    4. Produce one figure per question above, saved to data_inspection/figures/.
    5. Write a summary report to data_inspection/data_report.md.
    Begin by reading CLAUDE.md and the data README. Do not start writing code until you have confirmed the data paths are correct.
    ```

The key additions: an explicit negation ("do not write training code"), a numbered task list, explicit output paths, and a confirmation step before coding begins.

---

## Reflection Questions

1. You have just seen the class imbalance in the BraTS dataset. Standard cross-entropy loss treats each voxel equally. Without any modification, what do you expect the baseline model to learn to do? How would you detect this in the model's predictions?

2. You looked at 5 sample cases visually. Is 5 cases a representative sample? What are the risks of making conclusions about a 369-case dataset from 5 examples? What would a more rigorous sampling strategy look like?

3. The intensity histograms show that different modalities have different intensity ranges. If you concatenated all four modalities into a multi-channel input and did NOT normalise, what effect would the dominant modality have on the model's gradients?

4. You found (or did not find) suspicious cases. What is the cost of including a corrupt case in training? What is the cost of excluding a case that was actually valid? How do you weigh these risks?

5. The data report you produced describes the BraTS training set. Would it also describe the BraTS test set? What about a dataset from a different hospital using a different scanner? Why does this matter for clinical translation?

---

## Optional Challenge

Extend the data inspection to quantify tumour morphology across the training set. For each case, compute: the volume of the whole tumour in cubic centimetres (using voxel spacing); the approximate centroid location of the tumour in MNI-like coordinates (simply the mean voxel coordinates multiplied by voxel spacing); and whether the tumour is predominantly unilateral (left or right hemisphere). Plot a histogram of tumour volumes and identify what fraction of tumours are smaller than 5 cm³. This will be directly relevant to the Mission 3 error analysis.

---

## Common Failure Modes

**Visualisation fails because of missing matplotlib backend.** On a headless server, `plt.show()` will fail or produce nothing. Ask Claude to always use `plt.savefig()` and `matplotlib.use('Agg')` at the top of any visualisation script. Check that the PNG files were actually written to disk.

**NIfTI files loaded with wrong orientation.** `nibabel` loads volumes in RAS orientation by default; naively slicing with `[:, :, z]` may produce coronal rather than axial slices. Ask Claude to use `nibabel.as_closest_canonical()` and to explain what the three axes represent.

**Class distribution computed per-case rather than globally.** This gives a very different picture. Ask Claude to explicitly state whether statistics are per-case averages or aggregated across all voxels in all cases.

**Intensity histograms show only the background peak.** If skull-stripping has removed non-brain voxels and they are stored as exact zeros, the zero bin dominates the histogram. Ask Claude to exclude zero-valued voxels from the histogram and replot. Document this exclusion in the report.

**Student skips this mission, trains a model in Mission 2, and later cannot explain why the model fails on small tumours.** The failure pattern was visible in the class distribution and size analysis — but only if Mission 1 was done carefully. This is the most scientifically costly skip in the course.

---

## Expected Learning Outcome

After completing this mission you can: load and visualise multi-modal 3D MRI data with Python; describe the BraTS dataset structure including modalities, label classes, and voxel statistics; articulate the class imbalance problem and why it affects model training; assign a constrained role to Claude that produces analysis code rather than training code; produce a data report that would satisfy a peer reviewer asking "how did you inspect your data before modelling?"
