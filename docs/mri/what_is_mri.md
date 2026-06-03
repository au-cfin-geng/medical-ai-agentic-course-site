# What Is MRI?

MRI — Magnetic Resonance Imaging — is the workhorse of neurological diagnosis and the foundation of every dataset you will work with in this course. This section gives you just enough physics to understand why MRI looks the way it does, and why it is so powerful for brain tumour analysis.

## The Core Idea: Protons in a Magnetic Field

Your body is roughly 60% water. Every water molecule contains two hydrogen atoms, and every hydrogen nucleus is a single proton that behaves like a tiny spinning magnet. Under normal conditions, these protons point in random directions and cancel out. Place the patient inside a strong magnetic field (1.5 or 3 Tesla in clinical practice — about 30,000 to 60,000 times the Earth's magnetic field) and the protons align along the field direction, just as iron filings align around a bar magnet.

Now apply a brief radiofrequency (RF) pulse at precisely the right frequency (the Larmor frequency), and the protons are knocked out of alignment. When the pulse stops, they return to their equilibrium state — a process called **relaxation** — and as they do, they emit a tiny electromagnetic signal that the scanner detects.

The critical insight: **different tissues relax at different rates**. Grey matter, white matter, cerebrospinal fluid (CSF), fat, and tumour all have different water content and different molecular environments, so they emit signal at different times and with different intensities. By varying when the scanner listens for that signal (controlled by two timing parameters, TR and TE), the operator can make different tissues appear bright or dark. This is what creates **contrast**.

!!! note "No Ionising Radiation"
    Unlike CT or X-ray, MRI uses no ionising radiation. There is no dose accumulation, making it safe for repeated scanning and for young patients. This is one reason MRI is the modality of choice for brain tumour follow-up, which may involve scans every 2-3 months over years.

## Why MRI Is Ideal for the Brain

The brain is almost entirely soft tissue. CT — which measures X-ray attenuation and is excellent for bone — provides poor contrast between grey matter, white matter, and most tumour types. MRI's sensitivity to water content and molecular environment gives it dramatically superior soft tissue contrast. A GBM visible as a clear heterogeneous mass on MRI may appear as only a subtle density change on CT.

## Pulse Sequences: The Vocabulary of MRI

A **pulse sequence** is a specific pattern of RF pulses and magnetic field gradients that controls what the image shows. By changing the sequence, the radiologist can interrogate different tissue properties. In brain tumour imaging, four sequences are acquired as standard — these are exactly the four modalities in the BraTS dataset:

| Sequence | Primary Use | What Tumour Typically Looks Like | Clinical Value |
|----------|-------------|----------------------------------|----------------|
| **T1** | Anatomy, cortical morphology | Iso- to hypointense (similar to or darker than normal brain) | Baseline anatomy; detect mass effect, herniation |
| **T1ce** (T1 post-contrast) | Blood-brain barrier breakdown | Bright ring of enhancement (in GBM); low-grade gliomas often do not enhance | Distinguishes high-grade from low-grade; defines surgical target |
| **T2** | Oedema, infiltration, full tumour extent | Hyperintense (bright) — tumour and surrounding oedema both bright | Most sensitive for detecting tumour presence and total extent |
| **FLAIR** (Fluid Attenuated Inversion Recovery) | Tumour near ventricles, cortical lesions | Hyperintense, with CSF suppressed to dark | Separates peritumoral oedema from ventricle; critical for infiltration |

No single sequence tells the whole story. The four BraTS modalities are complementary — each reveals a different aspect of the tumour. This is why multimodal AI models consistently outperform single-modality models on brain tumour segmentation.

## Why MRI Takes So Long

A brain MRI study takes 30-60 minutes, compared to seconds for a CT scan. The reasons are structural:

- **Multiple sequences** must be acquired (T1, T1ce, T2, FLAIR — plus often diffusion, perfusion, and spectroscopy for tumour cases).
- **Multiple slices** are acquired to cover the whole brain (typically 150-200 slices for a full 3D acquisition).
- **Signal averaging**: the scanner acquires the same slice multiple times and averages the signals to improve SNR (signal-to-noise ratio). More averages = higher quality but longer scan time.
- **Physics constraints**: the TR (time between RF pulses) must be long enough for tissue to relax before the next pulse. For T2/FLAIR sequences, TR can be several seconds, making whole-brain coverage slow.

This acquisition time is also why motion artefacts matter — even small head movements during a 6-minute sequence can degrade image quality significantly.

## MRI as a 3D Volume

A clinical MRI brain scan is not a photograph — it is a **3D volume**: a stack of 2D slices that together form a three-dimensional representation of the brain.

```
      Z (superior)
      |
      |   [slice 155]
      |   [slice 154]
      |   [  ...   ]    ← 155 axial slices stacked
      |   [slice 001]
      └────────────── X (left-right, 240 voxels)
     /
    / Y (anterior-posterior, 240 voxels)
```

Each slice is a 2D image; the stack of 155 slices forms a volume of dimensions 240 × 240 × 155 — which is the standard BraTS volume shape. Each point in this 3D grid is a **voxel** (volumetric pixel), with a single intensity value. AI models for brain tumour segmentation operate on this full 3D volume, not on individual slices.

!!! tip "Connection to BraTS"
    Every case in the BraTS dataset is a 4-channel 3D volume: T1, T1ce, T2, and FLAIR, all registered to the same 3D space with dimensions 240 × 240 × 155 at 1mm isotropic resolution. When you load a BraTS case in Mission 1, you are loading exactly this structure.

## Summary

MRI works by detecting the relaxation signals of hydrogen protons in a magnetic field. Different tissues relax differently, and different pulse sequences exploit this to create different contrasts. The four sequences in BraTS — T1, T1ce, T2, FLAIR — each capture a different tissue property, and together they give an AI model (and a radiologist) the full picture of a brain tumour.
