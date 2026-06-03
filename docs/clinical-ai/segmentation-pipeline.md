# The Segmentation Pipeline

A brain tumour segmentation system is not just a model. It is a pipeline of decisions, transformations, and checks — and errors introduced early propagate through every subsequent stage. This page walks through the full pipeline from raw MRI acquisition to final evaluation output, for each step explaining what it does, why it matters for AI, and what goes wrong when it is skipped or done incorrectly.

## Step 1: Data Acquisition

**What it does**: An MRI scan is acquired at a clinical site using a specific scanner, field strength, coil configuration, and pulse sequence protocol. The result is raw k-space data that is reconstructed by the scanner into image volumes.

**Why it matters for AI**: Every parameter of the acquisition protocol affects image appearance — TR, TE, field strength, slice thickness, in-plane resolution, number of averages. Two scanners from different vendors running nominally the same protocol will produce images with measurably different intensity distributions. If training data was acquired on 3T scanners and inference is attempted on 1.5T data, performance will degrade.

**What goes wrong**: Protocol drift within a site over time (scanner software updates, coil replacement) can silently degrade model performance. Acquisition artefacts (motion, susceptibility, Gibbs ringing) that were rare in the training set may cause unpredictable failures at inference.

## Step 2: DICOM Conversion

**What it does**: Raw scanner output is stored in DICOM format (Digital Imaging and Communications in Medicine), a complex standard that encodes image data alongside extensive metadata. Clinical AI pipelines convert DICOM to simpler research formats: NIfTI (`.nii.gz`) for volumetric data, or NRRD, MHA for variants.

**Why it matters for AI**: DICOM conversion is a frequent source of orientation errors. NIfTI uses a specific coordinate system; if the conversion software interprets the DICOM orientation incorrectly, the resulting volume may be flipped or rotated. A model trained on correctly oriented data will produce garbage output on a flipped volume.

**What goes wrong**: Different DICOM converters (dcm2niix, dcm2nii, MRIcroGL) handle edge cases differently. Series with unusual acquisition orientations are particularly prone to conversion errors. Left-right flipping is hard to detect visually and can cause systematic downstream failure.

## Step 3: Anonymisation

**What it does**: Patient identifying information is removed from DICOM metadata headers (name, date of birth, accession number, referring physician) and from burned-in image annotations if present. This is a legal and ethical requirement for research data sharing and model training.

**Why it matters for AI**: Improperly anonymised data cannot be legally used for training or validation in most jurisdictions. Missed identifying information can cause privacy breaches and regulatory problems. Some metadata (scanner model, acquisition date) may be legitimately useful for model development but must be handled carefully.

**What goes wrong**: Automated anonymisation tools miss non-standard DICOM tags. Burned-in annotations in images (patient name overlaid on the image itself) require active removal. Dates must be shifted consistently to preserve relative timing while removing absolute dates.

## Step 4: Quality Control

**What it does**: Automated and manual checks verify that each volume is usable: expected sequences are present, volumes have correct dimensions and voxel spacing, no catastrophic artefacts are present, coverage includes the full brain.

**Why it matters for AI**: A model fed a truncated volume (missing superior slices), a motion-corrupted scan, or the wrong sequence (T2 labelled as FLAIR) will produce predictions that are silently wrong. Quality control at the input stage catches problems before they produce misleading results.

**What goes wrong**: Skipping QC is the fastest way to introduce hard-to-debug failures. A single corrupted training sample can degrade convergence. A corrupted test sample will produce an outlier metric that looks like a model failure but is actually a data failure.

## Step 5: Preprocessing

Preprocessing is the most complex pipeline stage and the one with the most decisions. For brain MRI, it typically includes:

**Skull stripping (brain extraction)**: Remove non-brain tissue — skull, scalp, dura — from the volume, retaining only the brain parenchyma. Tools: FSL BET, HD-BET, SynthStrip. Failure to skull-strip can cause models to use skull intensity as a spurious feature. Poor skull stripping (removing part of the brain, or leaving skull fragments) introduces artefacts that propagate into segmentation errors.

**Bias field correction**: MRI intensities are non-uniformly distributed across the volume due to radiofrequency coil inhomogeneity — the centre of the brain is typically brighter than the periphery. Bias field correction (N4 from ANTs/SimpleITK) estimates and removes this smooth spatial variation. Without correction, the same tissue type has different apparent intensities in different parts of the brain, confusing intensity-based models.

**Registration (co-registration)**: For multi-modal pipelines, all sequences must be aligned to the same physical space — a T1ce voxel and its corresponding T2 voxel must represent the same anatomical point. Patient motion between sequences (even minor head movement) misaligns the volumes. Registration tools (ANTs, FSL FLIRT) compute a spatial transform that aligns each modality to a common reference. Misregistration causes the model to receive contradictory multi-modal signals at each voxel.

**Normalisation**: As discussed in the MRI basics section, MRI intensities have no absolute scale. Intensity normalisation (z-score per channel, percentile normalisation, WhiteStripe) brings intensity distributions to a common range. Inconsistent or incorrect normalisation is one of the most common causes of generalisation failure across sites.

**Resampling**: Images may have different voxel sizes across sequences or subjects. Resampling to a common isotropic resolution (e.g., 1mm x 1mm x 1mm) ensures consistent spatial context for the model. Resampling introduces interpolation artefacts if done incorrectly.

## Step 6: Model Input Preparation

**What it does**: Preprocessed volumes are cropped, padded, and batched into tensors compatible with the model's expected input shape. For 3D models, the full volume may be input at reduced resolution or processed in overlapping patches at full resolution.

**Why it matters for AI**: Patch size, stride, and overlap strategy affect both training dynamics and inference quality. Inference artefacts at patch boundaries (seam lines) can be visible in final predictions if overlap and averaging are not handled correctly.

## Step 7: Inference

**What it does**: The trained model receives the preprocessed multi-modal volume and produces a probability map for each class at each voxel. Argmax over class probabilities produces the hard segmentation mask.

**Why it matters for AI**: GPU memory constraints often require inference at reduced batch size or on CPU. Test-time augmentation (averaging predictions across flipped/rotated versions of the input) can improve robustness. Storing softmax probabilities rather than only the argmax mask preserves uncertainty information for downstream analysis.

## Step 8: Post-processing

**What it does**: Raw model output is refined to improve physical plausibility. Common steps: connected component analysis (keep only the largest component of each predicted class, remove small isolated predictions), hole filling, and anatomical constraint enforcement.

**Why it matters for AI**: A model may predict small scattered false positive voxels in regions inconsistent with anatomy. Post-processing removes these without retraining the model. However, aggressive post-processing can also remove true positives — tuning the thresholds requires validation data.

## Step 9: Evaluation

**What it does**: Predicted segmentation masks are compared to reference annotations using quantitative metrics: Dice, sensitivity, specificity, Hausdorff distance. Results are computed per-case and aggregated across the dataset.

**Why it matters for AI**: Evaluation bugs are common and dangerous — they produce numbers that look plausible but are wrong. Common sources: mask label mismatch (model predicts 1 for tumour but reference uses 4), spacing mismatch in Hausdorff computation, incorrect handling of empty masks (no tumour in reference or prediction).

## Step 10: Reporting

**What it does**: Metrics are reported with appropriate statistical context: mean, standard deviation, per-case distribution, stratified by subgroup where sample sizes allow.

## What the BraTS Data Has Already Done

!!! tip "What the lab's data has already done"
    The teaching data has been skull-stripped, bias-field corrected, and co-registered across modalities. All four sequences are already in the same 1mm isotropic space. You start from a pre-processed state. This is a significant advantage that saves weeks of pipeline engineering and allows you to focus on modelling and evaluation. In real clinical work, you would need to build, validate, and maintain every step described above before touching the model.
