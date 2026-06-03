# MRI Segmentation Cheatsheet

> **For print:** File → Print → Save as PDF. Keep beside you during Missions 1–4.

---

## MRI Modality Table

| Modality | What it shows | Appearance convention | Primary clinical use |
|---|---|---|---|
| **T1** | Tissue anatomy, fat | White matter bright, grey matter dark, CSF dark | Anatomical reference; pre/post-contrast comparison |
| **T2** | Water content, oedema | CSF bright, oedema bright, white matter dark | Whole tumour extent; infiltrative oedema |
| **FLAIR** (Fluid Attenuated Inversion Recovery) | Like T2 but CSF signal suppressed | CSF dark, oedema bright | Infiltrative tumour near CSF spaces; peritumoral region |
| **T1ce** (T1 + contrast enhancement) | Blood-brain barrier breakdown | Enhancing tissue bright; areas of active tumour bright | Active tumour boundary; treatment response monitoring |

**Rule of thumb:** Use T2/FLAIR for whole tumour extent. Use T1ce for the active core and enhancing boundary. Use T1 as anatomical reference for registration verification.

---

## BraTS Label Conventions

| Label value | Region name | Abbreviation | What it represents |
|---|---|---|---|
| **0** | Background / healthy tissue | — | Everything not tumour |
| **1** | Necrotic and non-enhancing tumour core | NCR/NET | Necrotic core; non-perfused tumour |
| **2** | Peritumoral oedema | ED | Infiltrative oedema surrounding the tumour |
| **4** | Enhancing tumour | ET | Active, contrast-enhancing tumour margin |

**Derived evaluation subregions used in scoring:**

| Subregion | Label combination | Clinical rationale |
|---|---|---|
| **Whole Tumour (WT)** | Labels 1 + 2 + 4 | Full extent of disease visible on imaging |
| **Tumour Core (TC)** | Labels 1 + 4 | Surgically relevant core (necrosis + enhancing) |
| **Enhancing Tumour (ET)** | Label 4 only | Active tumour; relevant for treatment response |

Note: label value 3 is not used in current BraTS conventions (historical artefact from earlier editions).

---

## Preprocessing Checklist

Before any segmentation pipeline runs on a BraTS case, the following steps should have been applied. Verify them in Mission 1.

- [ ] **Skull stripping** — non-brain tissue (skull, dura, scalp fat) removed from the volume. Presence of skull increases false positives at the brain boundary.
- [ ] **Bias field correction** — low-frequency intensity inhomogeneity from the MRI scanner corrected (N4 or equivalent). Uncorrected bias fields cause threshold-based methods to fail systematically.
- [ ] **Co-registration** — all four modalities (T1, T1ce, T2, FLAIR) aligned to the same coordinate space. Misregistration causes modality mismatch errors; verify by checking that the same anatomical landmark is at the same voxel coordinate across modalities.
- [ ] **Intensity normalisation** — voxel intensities standardised (z-score or percentile normalisation). Without normalisation, intensity-based methods are not comparable across patients.

In the BraTS dataset, all four steps are pre-applied. In your own data: verify each step explicitly.

---

## Common Segmentation Errors

| Error type | Where it appears | Diagnostic clue | Clinical impact |
|---|---|---|---|
| **False positives near ventricles** | Lateral ventricle walls | CSF-adjacent voxels flagged as tumour; bright on FLAIR in ventricle wall | Overestimates tumour volume; may suggest involvement where none exists |
| **False negatives at tumour boundary** | Peripheral infiltrating margin | Boundary voxels missed; Dice moderate, HD95 high | Underestimates extent; may miss infiltrative disease |
| **Necrotic core missed** | Central hypointense region on T1ce | Label 1 absent or fragmented | Underestimates core volume; affects surgical planning |
| **Enhancing tumour fragmented** | ET subregion | Multiple small disconnected ET blobs | ET Dice low despite reasonable WT Dice; affects response assessment |
| **Over-segmentation into normal white matter** | White matter adjacent to oedema | Large ED region extending beyond visible FLAIR signal | Overestimates infiltration extent |
| **Registration ghost** | Edges of brain on T1/T2 comparison | High-intensity edge artefacts on one modality | Can cause spurious detections at the brain surface |
