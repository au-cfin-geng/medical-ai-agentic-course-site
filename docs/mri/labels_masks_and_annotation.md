# Labels, Masks, and Annotation

A segmentation model needs two things to train: images and labels. Understanding what a label is, how it was created, and what uncertainty it contains is essential for interpreting model behaviour and avoiding common training pitfalls.

## What a Segmentation Label Is

A **segmentation label** (also called a **mask** or **annotation**) is a 3D volume with exactly the same spatial dimensions as the MRI it annotates. Instead of intensity values, each voxel contains an integer class label:

```
MRI volume (T1):                 Segmentation label:

  voxel value = 423               voxel value = 0  (background)
  voxel value = 612               voxel value = 0  (background)
  voxel value = 890               voxel value = 2  (oedema)
  voxel value = 234               voxel value = 4  (enhancing tumour)
  voxel value = 445               voxel value = 1  (necrotic core)
```

The label volume has the same shape (240 × 240 × 155 for BraTS), the same voxel spacing, and the same affine matrix. Corresponding voxel positions represent the same anatomical location. This spatial correspondence is what makes supervised training possible: the model predicts a class for each voxel, and the label tells it the correct answer.

Labels are stored as NIfTI files (`.nii.gz`) with integer dtype. Visualising them means overlaying the label mask on the MRI with transparency, using a distinct colour per class.

---

## The BraTS Label Hierarchy

BraTS uses a nested subregion structure that reflects clinical and biological distinctions in glioma anatomy. The raw annotations contain four classes:

| Raw Label Value | Region | Description |
|----------------|--------|-------------|
| **0** | Background | Everything outside the brain and non-tumour brain |
| **1** | Necrotic core (NCR) | Dead tissue at the tumour centre; dark on T1ce (no enhancement) |
| **2** | Peritumoral oedema (ED) | Infiltrated brain around the tumour; bright on T2/FLAIR |
| **4** | Enhancing tumour (ET) | Actively proliferating, gadolinium-enhancing rim |

*(Note: label value 3 is not used in BraTS 2021.)*

From these raw labels, three clinically meaningful **subregions** are derived by combining classes. The challenge metrics evaluate these three subregions:

```
Whole Tumour (WT) = labels 1 + 2 + 4   (everything that is not background)
                    ┌──────────────────────────────────┐
                    │ oedema (2)                        │
                    │   ┌──────────────────────┐        │
                    │   │ necrotic core (1)     │        │
                    │   │   ┌──────────┐        │        │
                    │   │   │enhancing │        │        │
                    │   │   │tumour (4)│        │        │
                    │   │   └──────────┘        │        │
                    │   └──────────────────────┘        │
                    └──────────────────────────────────┘

Tumour Core (TC)  = labels 1 + 4        (what the surgeon targets)
Enhancing Tumour  = label 4 only        (the prognostic marker)
(ET)
```

**Why three subregions?**

- **WT** reflects total disease burden — relevant for diagnosis and radiotherapy planning.
- **TC** is the surgical target — what a neurosurgeon aims to resect.
- **ET** is a prognostic biomarker — its extent correlates with survival and is the primary response assessment criterion in clinical trials.

!!! info "BraTS Evaluation"
    Competition submissions are evaluated with Dice score and Hausdorff distance (95th percentile) for each of the three subregions (WT, TC, ET) separately. A model that performs well on WT but poorly on ET has a clinically meaningful failure — it can delineate the full lesion but not identify the most aggressive component.

---

## How Annotations Are Created

BraTS annotations were created by expert neuroradiologists using specialised annotation software, drawing boundaries slice by slice on the axial, coronal, and sagittal views simultaneously. The process for a complex glioblastoma case:

1. Radiologist opens all four modalities side by side.
2. Identifies the enhancing rim on T1ce — traces label 4.
3. Identifies the non-enhancing necrotic core on T1ce (dark within the enhancing ring) — traces label 1.
4. Identifies the FLAIR/T2 signal change beyond the enhancing region — traces label 2 (oedema).
5. Reviews slice by slice in all three planes and corrects.

**Typical annotation time:** 30-90 minutes per GBM case. Simpler cases (small, well-defined) may take 15-20 minutes; complex cases with satellite lesions or extensive oedema can take 2 hours.

**BraTS annotation fusion:** Each BraTS case was annotated by multiple raters (3-5 expert annotators) and the annotations were fused using STAPLE (Simultaneous Truth and Performance Level Estimation) or majority vote. The final label represents the consensus, not any single annotator's opinion.

---

## Inter-Rater Variability: The Ground Truth Is Not Ground Truth

Even highly experienced neuroradiologists disagree on tumour boundaries, particularly:

- The outer edge of peritumoral oedema (where normal brain ends and infiltrated brain begins)
- The distinction between tumour infiltration and reactive oedema on FLAIR
- The exact boundary of the enhancing rim vs. adjacent necrosis

Measured inter-rater Dice scores for GBM annotation between expert radiologists are typically 0.85-0.92 for whole tumour, and lower (0.75-0.85) for tumour core and enhancing tumour. This is not negligence — it is a genuine biological ambiguity that the imaging cannot resolve.

**Implications for AI:**

- A model that achieves Dice > 0.9 on WT is performing at or near human expert level.
- The "ceiling" for model performance is set by inter-rater agreement, not by algorithm design.
- Reported Dice scores should always be interpreted in the context of inter-rater variability.
- Uncertainty quantification in AI predictions should reflect this inherent label uncertainty.

!!! warning "The Model Learns the Errors Too"
    If an annotator systematically under-segments the oedema region (e.g., stopping 5mm inside the true boundary to be conservative), a model trained exclusively on their labels will learn this systematic bias. It will consistently under-segment oedema — not because it is wrong, but because it learned from consistently under-segmented examples. This is one reason multi-rater annotation and label fusion are important.

---

## Visualising Labels

Standard conventions for visualising BraTS labels overlaid on MRI:

| Region | Typical Colour | Background |
|--------|---------------|-----------|
| Whole tumour outline | Yellow border | T2 or FLAIR |
| Peritumoral oedema (label 2) | Green | FLAIR |
| Necrotic core (label 1) | Red | T1ce |
| Enhancing tumour (label 4) | Yellow | T1ce |

In Python with matplotlib, the label mask is overlaid on the MRI slice using `plt.imshow(mri_slice, cmap='gray')` followed by `plt.imshow(label_slice, alpha=0.4, cmap='Set1')`. Always use nearest-neighbour interpolation for the label overlay to avoid blurring class boundaries.

!!! tip "Mission 1 Data Exploration"
    When exploring BraTS cases in Mission 1, examine the labels carefully: load the label NIfTI, plot axial slices with the label overlay, and find cases with small, medium, and large tumours. Note which cases have minimal oedema (label 2 absent or small) and which have extensive infiltration. These differences in case difficulty will help you interpret the model's error distribution later.
