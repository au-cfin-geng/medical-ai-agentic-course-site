# Quality Control for MRI Datasets

Data quality is the most underestimated determinant of AI model performance. A state-of-the-art architecture trained on poor-quality data will be outperformed by a simple model trained on clean data. This section covers how to identify and manage MRI quality problems — a skill every AI practitioner working with medical imaging must develop.

!!! danger "Garbage In, Garbage Out"
    This clinical maxim applies with particular force to medical AI. Unlike natural image datasets where a blurry photo is still recognisably a cat, a motion-corrupted MRI may look like plausible brain anatomy to an algorithm while containing no usable diagnostic information. Models do not detect corrupt inputs by default — they produce confidently wrong outputs.

---

## Why QC Is Non-Negotiable

Consider what happens without QC:

1. A training set contains 5% of scans with severe motion artefact. The model learns that ghosting patterns near white matter are associated with tumour. On clean test data, it generates false positives in high-motion regions.
2. A registration failure causes FLAIR and T1 to be offset by 3mm. The model learns that FLAIR hyperintensity at position X predicts a T1 structure at position X+3mm — a spurious spatial pattern that will not generalise.
3. Skull stripping removed 8mm of right temporal cortex. The model learns that absent signal at the right temporal pole indicates glioma infiltration.

These failure modes are not hypothetical. They have been documented in published AI studies. QC is the gate that prevents them.

---

## Visual QC: What to Look For

Visual QC means a human (or an AI trained to replicate human inspection) reviews images systematically. For each case and each modality, check:

### Motion Artefacts

The most common artefact. Caused by patient movement during acquisition.

```
Clean scan:                    Motion-corrupted scan:

  ┌──────────────┐               ┌──────────────┐
  │  ────────    │               │ ~~─~──~──~── │  ← blurring
  │  ████████    │               │ ████████░░░░ │  ← ghosting
  │  ────────    │               │ ──────░░──── │  ← ringing
  └──────────────┘               └──────────────┘
  sharp tissue boundaries        blurred, with ghost copies
```

**What to look for:** Blurring of tissue interfaces; "ghost" copies of structures (especially brain or skull) displaced across the image in the phase-encode direction; loss of fine sulcal detail.

**Severity grading:** Mild motion (slight blurring, usable) vs. severe motion (gross ghosting, unusable). A common rule: if you cannot confidently identify the grey-white matter boundary in at least 80% of slices, exclude the scan.

### Susceptibility Artefacts

Caused by local magnetic field distortions near air-tissue interfaces (sinuses, ear canals) or metallic implants (surgical clips, dental work, haemorrhage).

**What to look for:** Black signal dropout regions — areas of complete signal loss, often with geometric distortion at the boundaries. Common locations: inferior frontal lobes (near sinuses), posterior fossa (near petrous bone), and anywhere near prior surgery.

!!! note "Susceptibility vs. Tumour"
    Haemorrhage within a GBM creates susceptibility artefact (signal dropout on T2*). This is not an imaging failure — it is real pathology. True susceptibility artefact from metallic implants is geometric and does not correspond to known anatomy. Learning to distinguish them requires pattern recognition that comes with experience.

### Gibbs Ringing (Truncation Artefact)

Oscillating bands of bright and dark signal radiating from sharp edges (brain surface, ventricle walls). Caused by truncation of the k-space signal in Fourier reconstruction.

**What to look for:** Parallel lines at approximately equal spacing, emanating from high-contrast interfaces. Mild Gibbs ringing is ubiquitous and acceptable. Severe Gibbs ringing can create apparent lesions near ventricles.

### Incomplete Brain Coverage

**What to look for:** Slices at the top or bottom of the volume that are cut off — missing cerebellum, brainstem, or frontal lobes. On axial images, the top slice should include the vertex; the bottom should include the full cerebellum.

**Why it matters for AI:** A model trained on full-brain volumes will have undefined behaviour when portions of the brain are absent. It may attempt to segment tumour in the missing region or produce errors near the volume boundary.

### Failed Preprocessing Checks

During visual QC, also verify preprocessing quality:

- **Skull stripping:** Are there brain tissue regions with zero intensity (removed)? Is non-brain tissue present?
- **Co-registration:** Overlay T1 and FLAIR — do sulci, ventricles, and other landmarks align?
- **Bias field:** Is one region of the brain systematically brighter than homologous regions on the opposite side?

---

## Automated QC Metrics

Visual QC is the gold standard but is slow. Automated metrics provide rapid screening:

| Metric | Description | Threshold (approximate) |
|--------|-------------|------------------------|
| **SNR** (Signal-to-Noise Ratio) | Mean signal in brain / std in background | <10 suggests poor quality |
| **CNR** (Contrast-to-Noise Ratio) | Signal difference between tissue types / noise | <5 suggests poor contrast |
| **Foreground coverage** | Fraction of expected brain voxels with valid signal | <0.90 suggests incomplete coverage or failed stripping |
| **Motion score** | AI-based estimate of motion severity (e.g., MRIQC) | Site-specific thresholds |
| **Modality alignment** | Mutual information between T1 and FLAIR after registration | Sudden drops indicate failed registration |

**MRIQC** (Esteban et al.) is the most widely adopted automated QC tool for brain MRI. It computes a comprehensive set of image quality metrics and flags outliers. It was trained on a large normative dataset and can identify most common artefact types.

---

## Common Artefact Reference

| Artefact | Cause | Appearance | Effect on AI |
|----------|-------|------------|-------------|
| **Motion** | Patient movement during acquisition | Blurring, ghosting in phase-encode direction | False edges, blurred segmentation boundaries |
| **Susceptibility** | Metal, haemorrhage, air-tissue interfaces | Signal dropout, geometric distortion | Missing signal interpreted as necrosis/cavity |
| **Partial volume** | Voxel contains multiple tissue types (at boundaries) | Intermediate intensity at interfaces | Blurred boundaries; model uncertainty at tumour edge |
| **Gibbs ringing** | k-space truncation | Oscillating bands near sharp edges | False lesion appearance near ventricles |
| **Zipper artefact** | RF interference from electronic equipment | Bright/dark lines across image in one direction | Corrupts image in affected slices |
| **Wrap-around (aliasing)** | FOV too small for anatomy | Anatomy from one side appears overlaid on opposite side | Confuses spatial layout; misregistration |

---

## QC in the Context of BraTS

The BraTS dataset has been QC'd by the challenge organisers. However, this does not mean every case is easy or artefact-free — it means cases with severe, disqualifying artefacts have been removed. In any large dataset, there are harder and easier cases.

**What to do in Mission 1:** When exploring BraTS cases, deliberately look for variability. Some cases will have:

- Very large tumours with extensive oedema (easier for WT, potentially harder for ET)
- Very small tumours (harder overall, high sensitivity to boundary errors)
- Extensive surgical cavity from prior resection (unusual anatomy)
- Subtle T1ce enhancement (harder ET segmentation)

Identifying these "hard cases" during data exploration is not just academic curiosity. When your model performs poorly on a subset of test cases, the first question is: are these cases harder, or is there a systematic failure mode? Knowing the data distribution helps you answer this.

---

## What to Do with a Failed QC Case

| QC Outcome | Recommended Action |
|------------|-------------------|
| Severe artefact (unusable) | Exclude from training and test sets; document case ID and reason |
| Moderate artefact (marginal) | Manual expert review; if in test set, flag separately in results |
| Failed preprocessing only | Re-run preprocessing with adjusted parameters; do not use original |
| Passes automated QC, borderline visual | Include in training if no better option; note as potential noise source |
| Borderline but in test set | Report metrics both with and without the case; use as sensitivity analysis |

!!! warning "Never Selectively Exclude Test Cases Based on Model Performance"
    Excluding test cases because the model performed poorly on them is data snooping and invalidates your evaluation. QC decisions must be made based on image quality criteria alone, blinded to model outputs. Document all exclusions with the reason before running any model.

---

## Summary

Quality control is not a checkbox — it is an ongoing analytical practice. The BraTS dataset gives you a clean starting point, but the skills you develop looking critically at MRI data are the same skills you will use when building pipelines on raw clinical data where QC has not been done for you.
