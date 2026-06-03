# MRI Cheat Sheet

> **For print:** use browser Print → Save as PDF. Recommended: A4, portrait, single page.

---

## Modality Comparison Table

| Tissue / Region | T1 | T2 | FLAIR | T1ce (T1 + contrast) |
|---|---|---|---|---|
| **CSF** | Dark (hypointense) | Bright (hyperintense) | Dark (suppressed) | Dark |
| **Grey Matter** | Intermediate grey | Intermediate grey | Intermediate grey | Intermediate grey |
| **White Matter** | Bright | Dark | Dark | Bright |
| **Necrotic Tumour Core** | Dark | Bright | Bright | Dark (no enhancement) |
| **Peritumoral Oedema** | Slightly dark | Very bright | Very bright | Slightly dark |
| **Enhancing Tumour** | Bright | Variable | Variable | Very bright (enhancement) |
| **Primary Clinical Use** | Anatomy, post-op assessment | Oedema, lesion extent | White matter lesions, leptomeningeal disease | Active tumour, blood-brain barrier breakdown |

**Rule of thumb:** Use T1ce to find active tumour (enhancing). Use FLAIR to find the full extent of disease. Use both together for treatment planning.

---

## BraTS Label Classes

| Label Value | Region | Abbreviation | Colour Convention |
|---|---|---|---|
| **0** | Background (non-brain + healthy tissue) | BG | Black / transparent |
| **1** | Necrotic and non-enhancing tumour core | NCR | Red |
| **2** | Peritumoral oedema | ED | Yellow |
| **4** | Enhancing tumour | ET | Cyan / Blue |

**Note:** There is no label 3. The jump from 2 to 4 is a historical artefact of the BraTS annotation protocol.

### Derived Regions for Evaluation

| Region | Definition | Clinical Relevance |
|---|---|---|
| **Whole Tumour (WT)** | Labels 1 + 2 + 4 | Full extent of disease; surgical planning |
| **Tumour Core (TC)** | Labels 1 + 4 | Resectable tumour core; treatment target |
| **Enhancing Tumour (ET)** | Label 4 only | Active disease; response to treatment |

---

## Preprocessing Checklist

When receiving raw BraTS data, confirm the following have been applied (BraTS data is pre-processed):

- [ ] **Skull stripping** — non-brain tissue removed; only brain parenchyma remains
- [ ] **Bias field correction** — low-frequency intensity inhomogeneity from the scanner corrected (e.g. N4 algorithm)
- [ ] **Co-registration** — all 4 modalities aligned to the same space (same voxel grid)
- [ ] **Atlas registration** — volumes registered to SRI24 atlas (standard brain template)
- [ ] **Intensity normalisation** — per-modality normalisation (z-score or percentile-based)

**For your own data (not BraTS):** each of these steps must be done explicitly. Missing any one will cause model performance to degrade significantly.

---

## Common MRI Artefacts

| Artefact | Appearance | Cause | Effect on AI |
|---|---|---|---|
| **Motion** | Blurring, ghosting | Patient moved during acquisition | Blurred boundaries confuse segmentation |
| **Susceptibility / Magnetic susceptibility** | Signal dropout (black regions) near metal or bone | Susceptibility differences between tissues and implants | Missing signal can look like tumour absence |
| **Gibbs Ringing** | Oscillating bands near sharp edges | Truncation of k-space (Fourier series truncation) | False edges confuse boundary detection |
| **Bias Field** | Smooth intensity gradient across image | RF coil inhomogeneity | Changes apparent tissue intensity; breaks intensity-based features |
| **Chemical Shift** | Bright/dark bands at fat-water interfaces | Frequency difference between fat and water | Rare in brain MRI; more relevant in body imaging |

---

## Spatial Orientation and Key Terms

| Term | Definition | Example |
|---|---|---|
| **Axial** | Horizontal plane — top-down view, divides head into top and bottom | "Looking down at the brain from above" |
| **Coronal** | Frontal plane — front-to-back view, divides head into front and back | "Face-on view of the brain" |
| **Sagittal** | Lateral plane — left-right view, divides head into left and right | "View from the side" |
| **Voxel** | Volumetric pixel — the 3D equivalent of a pixel | One cubic unit of MRI volume |
| **Spacing** | Physical size of one voxel in mm (x, y, z) | e.g. 1.0 × 1.0 × 1.0 mm (isotropic) |
| **Isotropic** | Voxel spacing is equal in all three dimensions | 1 mm × 1 mm × 1 mm |
| **Anisotropic** | Voxel spacing differs between dimensions | 0.5 × 0.5 × 5 mm (thin slices, large gap) |
| **Affine matrix** | 4×4 matrix encoding voxel-to-world space mapping | Stored in NIfTI header; needed for correct metric computation |
| **NIfTI** | Neuroimaging Informatics Technology Initiative file format (.nii, .nii.gz) | Standard format for brain MRI in research |
| **DICOM** | Clinical imaging format; one file per slice | Convert to NIfTI before most research pipelines |
| **PACS** | Picture Archiving and Communication System; the hospital's image storage system | Where real clinical MRI lives before research transfer |
