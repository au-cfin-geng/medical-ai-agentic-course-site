# MRI Preprocessing

Raw MRI data from a scanner cannot be fed directly into a deep learning model. Before any AI analysis, a standard neuroimaging preprocessing pipeline must be applied. This section describes the four core steps, explains why each matters, and notes what BraTS has already done for you — and what you will need to do yourself when working with clinical data.

!!! success "BraTS Has Done This For You"
    All BraTS 2021 data has been skull-stripped, bias-field corrected, co-registered, and resampled to 1mm isotropic. You can focus on the model. When you move to clinical deployment, you will need to implement every step in this pipeline yourself.

---

## Step 1: Skull Stripping (Brain Extraction)

**What it is:** Removing all non-brain tissue from the MRI volume — skull, scalp, eyes, sinuses, and neck — leaving only the brain parenchyma and its immediate surrounding CSF.

**Why it matters:**

- The skull is extremely bright on T1 (bone marrow is fat-rich and has short T1). Without skull stripping, the model wastes capacity learning to ignore the skull and may produce spurious activations near the skull base.
- Scalp and skull intensities can overlap with tumour and enhance with gadolinium, creating false positives near the brain surface.
- Removing non-brain tissue reduces the proportion of background voxels, improving training efficiency.

**Tools used in practice:**

- **HD-BET** (Isensee et al.) — deep learning-based, highly robust to pathological brains; recommended for tumour cases.
- **BET** (FSL) — classical method, fast but can fail with large lesions near the brain surface.
- **ANTs/antsBrainExtraction** — template-based, reliable for standard anatomy.

**Common failure modes:** Aggressive stripping that removes parts of the cortex (especially the temporal poles or cerebellum); incomplete stripping that leaves dura or fat; complete failure on severely distorted tumour anatomy.

```
Before skull stripping:         After skull stripping:

  ████████████████████            ░░░░░░░░░░░░░░░░░░░░
  ██┌──────────────┐██            ░░┌──────────────┐░░
  ██│  BRAIN       │██    →       ░░│  BRAIN       │░░
  ██│              │██            ░░│              │░░
  ██└──────────────┘██            ░░└──────────────┘░░
  ████████████████████            ░░░░░░░░░░░░░░░░░░░░
  skull + scalp present           only brain voxels
```

---

## Step 2: Bias Field Correction

**What it is:** Correcting a smooth, spatially varying intensity artefact caused by inhomogeneity in the RF transmit and receive fields of the MRI scanner.

**Why it matters:** In a perfectly uniform scanner field, a voxel of grey matter anywhere in the brain would have the same intensity. In reality, the same tissue type can appear 10-30% brighter near the scanner coil than far from it. This systematic variation fools intensity-based normalisation and can cause the model to learn a spurious correlation between position and tissue type.

**The bias field** is a smooth, low-frequency multiplicative field overlaid on the true image:

```
Observed image = True image × Bias field

         True signal            Bias field           Observed (biased)
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │ GM: 400  GM: 400│    │ 1.0  →  →  1.3 │    │ GM: 400  GM: 520│
    │                 │  × │                 │  = │                 │
    │ GM: 400  GM: 400│    │ 1.0  →  →  1.3 │    │ GM: 400  GM: 520│
    └─────────────────┘    └─────────────────┘    └─────────────────┘
    uniform grey matter    scanner inhomogeneity   same tissue, different values
```

**Tool:** N4ITK (Tustison et al.) — the current standard. It estimates the bias field iteratively using a B-spline model and corrects the image by dividing out the estimated field. Implemented in SimpleITK and ANTs.

---

## Step 3: Registration (Co-registration and Atlas Registration)

**What it is:** Aligning multiple images to the same 3D coordinate space by finding and applying a geometric transformation.

Two types of registration are required:

**Co-registration:** Aligning all four modalities (T1, T1ce, T2, FLAIR) for the same patient to the same space. Each sequence is acquired separately and, due to patient movement between sequences, the volumes are not perfectly aligned. A 1-2mm misalignment means that the voxel at position (120, 120, 77) represents different anatomy in T1 vs. T2.

**Atlas registration:** Registering the patient brain to a standard brain template (typically MNI152). This puts all patients into the same coordinate space, enabling population-level analysis and comparison across subjects.

```
Before co-registration:         After co-registration:

T1:    ┌───────────┐            T1:    ┌───────────┐
       │   brain   │                   │   brain   │
       │  ↗ lesion │                   │   lesion  │ ← all modalities
       └───────────┘                   └───────────┘   aligned here
T2:    ┌───────────┐            T2:    ┌───────────┐
       │ brain     │                   │   brain   │
       │    lesion↗│                   │   lesion  │
       └───────────┘                   └───────────┘
       voxels misaligned               voxel-to-voxel correspondence
```

**Why this is essential for multimodal AI:** A 3D UNet receives T1, T1ce, T2, and FLAIR as four input channels at the same voxel position. If co-registration is imperfect, the model sees inconsistent anatomy at each position — the equivalent of training a colour image classifier where the red, green, and blue channels are shifted by different amounts.

**Tools:** ANTs (gold standard for brain MRI), FSL FLIRT/FNIRT, NiftyReg. BraTS registration was performed using rigid registration to the SRI24 atlas.

---

## Step 4: Intensity Normalisation

**What it is:** Scaling MRI intensity values to a consistent range or distribution across patients and scanners.

**Why MRI is different from CT:** CT intensity values have a physical meaning — Hounsfield units are absolute measures of X-ray attenuation. Grey matter is always approximately +25 to +45 HU regardless of scanner. MRI intensities are arbitrary: a grey matter voxel might have intensity 400 on one scanner, 1200 on another, and 3500 on a third, all for the same tissue, the same field strength, and the same pulse sequence. The values depend on receiver gain, coil sensitivity, and dozens of scanner-specific parameters.

**Common approaches:**

| Method | Description | Use Case |
|--------|-------------|----------|
| **Z-score** | Subtract mean, divide by std (per volume, within brain mask) | Most common for deep learning; assumes roughly Gaussian distribution |
| **Percentile scaling** | Scale so that the 1st and 99th percentile map to 0 and 1 | Robust to outlier intensities and truncates extreme values |
| **Histogram matching** | Warp the intensity histogram to match a reference atlas | Multi-site harmonisation; computationally heavier |
| **WhiteStripe** | Normalise using the normal-appearing white matter as reference | Principled for neuroimaging; removes inter-scanner differences |

!!! danger "Training Without Normalisation"
    A model trained on unnormalised data learns to use absolute intensity values, which are scanner-specific. Applied to a new scanner, the same tissue will have different intensities, and the model will fail silently — producing confident but wrong predictions. Intensity normalisation is not optional for multi-site or real-world deployment.

---

## Preprocessing Failure Propagates

The preprocessing pipeline is sequential. Each step assumes the previous step succeeded. A failed skull strip that removes part of the cerebellum will cause the bias field correction to be biased (it estimates the field from remaining tissue). A poorly corrected bias field will cause intensity normalisation to be skewed. Registration of a poorly prepared image will fail or produce a poor alignment.

**Common failure modes to recognise:**

- Skull stripping removed part of the brain: the brain mask has holes, visible as zero-intensity regions inside the brain on visual inspection.
- Residual bias field: a smooth brightness gradient across the image after correction (look for one hemisphere appearing systematically brighter than the other).
- Misregistration: anatomical structures do not overlap between modalities — visible as blurring or double edges when overlaying two modalities.
- Intensity clipping: extreme values were clipped during normalisation, losing information in bright enhancing tumour or dark necrotic core.

!!! tip "Connection to the Lab"
    BraTS data arrives fully preprocessed. But in Mission 4 (clinical deployment scenario), you will encounter raw DICOM data that requires this full pipeline. Understanding what each step does — and what failure looks like — is essential for diagnosing why a well-trained model underperforms on clinical data.
