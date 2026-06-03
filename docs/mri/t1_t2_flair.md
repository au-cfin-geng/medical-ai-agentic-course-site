# T1, T2, and FLAIR

The four MRI sequences in BraTS — T1, T1ce, T2, and FLAIR — are not redundant. Each one illuminates a different aspect of the tumour. A neuroradiologist reads all four together, and your AI model should too. This section explains what each sequence actually measures and what it looks like in brain tumour cases.

## The Two Relaxation Times

All MRI contrast ultimately comes from two relaxation processes:

- **T1 (longitudinal relaxation)**: how quickly protons return to alignment with the main magnetic field after the RF pulse. Short T1 = fast recovery = bright on T1-weighted images. Fat has a short T1 (bright); CSF has a long T1 (dark).
- **T2 (transverse relaxation)**: how quickly the emitted signal decays due to protons falling out of phase with each other. Long T2 = slow decay = bright on T2-weighted images. Fluids and tissues with high water content have long T2 (bright); solid, organised structures like white matter have shorter T2.

By choosing short TR/TE timing, you get T1-weighted contrast. By choosing long TR/TE, you get T2-weighted contrast. FLAIR is a T2-weighted sequence with an additional inversion pulse that nulls the CSF signal.

---

## T1-Weighted Imaging

**Physical principle:** Short TR and TE emphasise differences in how quickly tissues recover longitudinal magnetisation.

**Tissue appearances:**

- White matter: **bright** (myelinated axons have short T1 due to fat-like lipid content of myelin)
- Grey matter: **intermediate** (slightly darker than white matter)
- CSF: **dark** (long T1)
- Tumour: **iso- to hypointense** (most tumours appear similar to or darker than grey matter)
- Fat/marrow in skull: **very bright**

**Primary clinical use:** Anatomical reference. T1 is the best sequence for seeing cortical morphology, deep grey matter structures (basal ganglia, thalamus), and mass effect (midline shift, herniation). It is the standard pre-operative planning sequence.

**What neuroradiologists look for:** Midline shift, effacement of sulci (indicating mass effect), T1-hypointense lesions suggesting tumour or oedema, and the overall structural anatomy that contextualises everything else.

---

## T1ce — T1 Post-Contrast (Gadolinium-Enhanced)

**Physical principle:** The patient receives an intravenous injection of a gadolinium-based contrast agent. Gadolinium shortens T1 relaxation time of nearby water molecules, making areas where it accumulates appear **bright** on T1-weighted images.

**Why gadolinium accumulates in tumours:** The blood-brain barrier (BBB) normally prevents large molecules from entering brain tissue. High-grade tumours (especially glioblastoma) disrupt the BBB, so gadolinium leaks into the tumour and surrounding tissue — this leakage appears as enhancement.

**Tissue appearances:**

- Normal brain: same as T1 (gadolinium does not cross intact BBB)
- Glioblastoma core: **bright ring enhancement** (irregular, heterogeneous)
- Necrotic core of GBM: **dark** (no vascularity, no enhancement)
- Low-grade gliomas: typically **no enhancement** (intact BBB — important prognostic distinction)
- Vessels, choroid plexus, pituitary: bright (naturally lack BBB)

**Primary clinical use:** Distinguishing high-grade from low-grade tumours. Defining the enhancing tumour boundary for surgical planning and radiotherapy targeting. Monitoring treatment response — disappearing enhancement may indicate treatment effect; new enhancement may indicate progression.

!!! warning "Enhancement vs. Tumour"
    Enhancement shows where the BBB is broken, not where the tumour is. Tumour cells infiltrate well beyond the enhancing margin — this is captured by T2/FLAIR. The enhancing region is what the surgeon targets; the full infiltration zone is what the radiation oncologist targets. This distinction directly maps to the BraTS label hierarchy (ET vs. WT).

---

## T2-Weighted Imaging

**Physical principle:** Long TR and TE emphasise differences in transverse relaxation. Tissues with high water content (fluids, oedema, most tumours) decay slowly and remain bright.

**Tissue appearances:**

- CSF: **very bright** (fluid has longest T2)
- Oedema: **bright** (increased water content)
- Most tumours: **bright to very bright**
- Grey matter: **intermediate**
- White matter: **slightly darker than grey matter** (reversal from T1)
- Normal vessels (flowing blood): **dark** (flow-related signal loss)

**Primary clinical use:** Detecting the full extent of tumour and surrounding oedema. T2 is often the most sensitive sequence for identifying an abnormality in the first place. It shows the total lesion volume — the surgical and oncological concern extends to everything that is T2-hyperintense.

**What neuroradiologists look for:** The boundary of T2 signal change (which approximates the outermost extent of tumour infiltration and oedema), signal heterogeneity within the lesion (suggesting different biological zones), and involvement of eloquent cortex or white matter tracts.

---

## FLAIR — Fluid Attenuated Inversion Recovery

**Physical principle:** FLAIR is a T2-weighted sequence with an additional inversion recovery pulse timed to null (cancel) the CSF signal. The result is a T2-like image where CSF appears **dark** instead of bright.

**Why this matters:** On standard T2, the bright CSF in the ventricles and subarachnoid space is so intense that it obscures lesions immediately adjacent to them. FLAIR removes this problem, making periventricular lesions and cortical/subcortical oedema clearly visible.

**Tissue appearances:**

- CSF: **dark** (nulled by the inversion pulse)
- Oedema and tumour: **bright** (like T2)
- Grey matter: **intermediate**
- White matter: **intermediate to dark**

**Primary clinical use:** Essential for glioma assessment. Shows tumour infiltration near the ventricles and along white matter tracts. In BraTS, FLAIR captures the peritumoral oedema region (label 2) most clearly — this is the region that typically appears bright on FLAIR but dark on T2 (relative to CSF).

**What neuroradiologists look for:** FLAIR-hyperintense signal extending beyond the T2-defined lesion core; signal change adjacent to or crossing the ventricles (suggesting subependymal spread); multifocal lesions that would otherwise be hidden by bright CSF.

---

## Comparison Table: All Four BraTS Modalities

| Modality | CSF | Grey Matter | White Matter | Tumour (GBM) | Oedema | Primary Use |
|----------|-----|-------------|--------------|--------------|--------|-------------|
| **T1** | Dark | Intermediate | Bright | Hypointense | Hypointense | Anatomy, mass effect |
| **T1ce** | Dark | Intermediate | Bright | Bright ring (enhancing rim) | No enhancement | BBB breakdown, surgical target |
| **T2** | Very bright | Intermediate | Slightly darker | Bright | Bright | Full lesion extent, sensitivity |
| **FLAIR** | Dark (nulled) | Intermediate | Intermediate | Bright | Bright | Periventricular lesions, infiltration |

!!! tip "BraTS Segmentation Logic"
    - The **enhancing tumour (ET)** — BraTS label 4 — is best seen on T1ce (bright ring).
    - The **necrotic core** — BraTS label 1 — appears dark on T1ce (no enhancement) and bright on T2.
    - The **peritumoral oedema** — BraTS label 2 — is bright on T2 and FLAIR, but not enhancing on T1ce.
    - Using all four modalities together allows a model to separate these three regions, which individually can look similar on any single sequence.

## Why All Four Modalities Together?

No single sequence is sufficient. T2 alone cannot distinguish enhancing tumour from oedema. T1ce alone misses the non-enhancing infiltrating edge. FLAIR alone cannot separate enhancement from oedema. The four-modality protocol exists precisely because the clinical questions require multi-parametric evidence — and this is why every competitive BraTS model is multimodal.
