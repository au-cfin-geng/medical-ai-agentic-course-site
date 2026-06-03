# Data Inspection Before Modeling

## Look at Your Data — Every Time, Without Exception

There is an informal rule among experienced ML researchers: the number of times you have looked at your data is never enough. Papers routinely skip this step in their methods sections because it does not seem like a scientific contribution. But skipping data inspection before modeling is the single most reliable way to waste weeks of compute time on a fundamentally broken experiment.

This page covers what to inspect in medical imaging data, how visualisation reveals problems that summary statistics miss, and how to use Claude to conduct data inspection systematically.

---

## What to Inspect Before Training Anything

### 1. Case Count and Class Distribution

The first number to establish is how many cases you have. For BraTS, this is a few hundred cases — a number that sounds adequate until you realise that for some tumour subtypes there may be fewer than 50 examples. Then count voxels: how many voxels in the entire dataset are labelled as tumour versus background?

In brain tumour segmentation, tumour voxels typically constitute **less than 5% of all brain voxels**. In many cases, the enhancing tumour (ET) region is less than 1% of the total volume. This is the class imbalance problem.

The consequence is immediate: a naive model that predicts "no tumour everywhere" achieves **95%+ voxel-level accuracy**. If you use accuracy as your evaluation metric, this model looks excellent. It is, of course, clinically catastrophic. This is why accuracy is the wrong metric for this task, and why Dice coefficient is used instead (see [Evaluation Metrics](metrics_dice_sensitivity_specificity.md)).

### 2. Image Dimensions and Voxel Spacing

MRI volumes are 3D arrays with associated metadata specifying the physical size of each voxel. In BraTS, cases are pre-processed to a common resolution (1mm isotropic), but in real-world data this is rarely true. You need to verify:

- Are all volumes the same spatial dimensions (e.g., 240 x 240 x 155)?
- Is voxel spacing consistent across cases?
- Does the label volume have the same dimensions as the image volume for each case?

A mismatch between image dimensions and label dimensions is a silent error. If your code does not check for this, it may silently crop the label or pad it with zeros, producing training samples where the label is misaligned with the image. This is not a hypothetical — it has caused real research to be retracted.

### 3. Label Quality

Even in a curated dataset like BraTS, you should look at the segmentation masks visually. Ask:

- Do the masks look anatomically plausible? Is the tumour in an expected location (cerebral hemispheres, usually supratentorial for GBM)?
- Are there any cases where the label appears to be all zeros (empty mask) despite the patient clearly having a tumour visible on imaging?
- Are there cases with unusual label patterns — scattered single voxels, or labels that extend outside the brain boundary?
- Do the three BraTS regions (WT, TC, ET) maintain the expected hierarchical nesting (ET is a subset of TC, TC is a subset of WT)?

Label errors in training data teach the model to replicate those errors. In the BraTS dataset, labels have been quality-controlled, but you should still verify that your data loading pipeline is reading labels correctly and not, for example, swapping the label indices.

### 4. Modality Completeness

Each BraTS case should have four MRI modalities: T1, T1ce (T1 with contrast), T2, and FLAIR. For some cases, one modality may be missing due to patient intolerance, protocol deviation, or file corruption. If you assume all four modalities are always present and do not check, your data loader will fail at runtime — or worse, silently concatenate the wrong channels.

Check: for every case in your dataset, do all four modality files exist and are they non-empty?

### 5. Outlier Cases

After checking the basics, look specifically for outliers:

- Cases with unusually large tumours (>100 mL volume): these may skew loss functions during training
- Cases with unusually small tumours (<1 mL): these are hardest to segment and may produce unstable gradients
- Cases with unusual tumour location (e.g., brainstem, cerebellum): less common in GBM but present in the data
- Cases with significant imaging artefacts: motion artefact, susceptibility artefact from prior surgery

These cases will not show up as problems in summary statistics. They will show up as your worst-performing cases after training, and you will wish you had identified them first.

---

## Visualisation Reveals What Metrics Miss

Consider a scenario where your model achieves mean Dice 0.85 across the test set. This sounds like a strong result. But suppose the distribution of per-case Dice scores looks like this:

- 90 cases with Dice 0.88-0.92 (excellent)
- 5 cases with Dice 0.0-0.15 (complete failure)
- 5 cases with Dice 0.5-0.6 (poor)

The mean is 0.85, but 10% of cases are failures. If you deployed this model clinically and one in ten patients had their tumour completely missed, that would be a serious patient safety event. The mean Dice number would not have told you this.

The only way to find this is to plot the distribution of per-case metrics and look at the worst cases as images. Load the three or four worst-performing cases from your validation set and visualise:

- The input MRI (at minimum, FLAIR and T1ce)
- The ground truth segmentation
- The model prediction
- A difference map (where does the prediction differ from ground truth?)

This visual inspection takes 20 minutes and will tell you more about your model's failure modes than hours of metric computation.

---

## Using Claude for Systematic Data Inspection

Claude can help you write data inspection code quickly. A useful prompt for the lab:

> "Read the BraTS dataset directory. For each case, check whether all four modality files (T1, T1ce, T2, FLAIR) exist and are non-empty. Report total case count, flag any cases with missing modalities, print the image dimensions of the first five cases, and compute the mean and standard deviation of the tumour label volume in mL across all cases."

This prompt is specific enough that Claude can generate working code, not generic template code. The specificity — naming the four modalities, asking for volumes in mL rather than voxels, asking for distribution statistics not just counts — is what produces useful output.

When you run this code, expect to find:

- A few cases with dimension mismatches from incomplete downloads
- High variance in tumour volume (coefficient of variation >1 is common for GBM)
- Clear class imbalance in the voxel-level label distribution

Document these findings. They will inform your choice of loss function, sampling strategy, and evaluation approach.

---

## Common Findings and Their Implications

| Finding | Implication |
|---------|-------------|
| Tumour voxels <5% of total | Do not use accuracy; use Dice. Consider weighted sampling or Dice loss |
| Missing modality in some cases | Build modality-robust model or exclude those cases with documentation |
| High variance in tumour size | Report per-case metrics, not just mean; consider stratified evaluation |
| Outlier cases with artefact | Exclude with documented justification, or treat as a hard-case sub-analysis |
| Label nesting violated | Check your label loading code; may indicate index swapping |

---

!!! note "Connect to Lab Mission"
    **Now do the lab — M1 (Data Exploration).**

    In Mission 1, you will conduct a systematic inspection of the BraTS dataset using Claude to help write the inspection code. Your task: establish case count, verify modality completeness, compute class imbalance statistics, and identify at least two outlier cases that you would flag for closer inspection. Visualise at least five cases across different tumour sizes. Write a brief (one paragraph) data characterisation note that could appear in a Methods section. This is not busywork — it is the first step any rigorous clinical AI study requires.
