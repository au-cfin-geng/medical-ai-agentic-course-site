# MRI Fundamentals for AI Researchers

You do not need to understand quantum mechanics to work with MRI data. But you do need to understand enough about what MRI measures — and what it does not measure — to reason about why AI models trained on MRI behave the way they do. This page covers the conceptual foundations without the physics formalism.

## What MRI Actually Measures

MRI measures the response of hydrogen nuclei (protons) in tissue water and fat to a carefully orchestrated sequence of radiofrequency pulses and magnetic field gradients. The key word is *response*. Different tissue environments cause protons to respond differently — and those differences in response create the image contrast that makes MRI clinically informative.

The dominant signal comes from water. Every tissue in the body contains water, but the water behaves differently in different environments. Cerebrospinal fluid (CSF) is free water with highly mobile protons. White matter contains water tightly associated with myelin. Tumour tissue contains water in a different microstructural environment again. These differences in the *physical environment* of water protons are what MRI encodes as image contrast.

Crucially, MRI uses no ionising radiation. It is a purely electromagnetic technique. Protons are temporarily perturbed by radiofrequency energy and release that energy as a detectable signal as they return to equilibrium. This is why MRI is preferred over CT for brain tumour imaging: serial scanning over months of treatment does not accumulate radiation dose.

!!! clinical "Clinical Relevance"
    In neuro-oncology, MRI is the primary imaging modality for tumour detection, characterisation, treatment planning, and response monitoring. A newly diagnosed glioblastoma patient will typically have an MRI before surgery, within 48 hours after surgery (to assess residual tumour before post-operative changes confound the image), then every 2-3 months during chemoradiotherapy, and at each clinical follow-up visit. Over a disease course of 12-18 months, this can mean 8-12 MRI scans — a rich longitudinal dataset that AI tools are increasingly being designed to exploit.

## T1 and T2 Relaxation: What the Letters Mean

After a radiofrequency pulse tips protons out of alignment with the main magnetic field, they return to equilibrium by two independent processes, characterised by time constants T1 and T2. Understanding these qualitatively — not mathematically — is sufficient for this course.

**T1 relaxation** (longitudinal relaxation) describes how quickly protons give up their absorbed energy to the surrounding molecular lattice and return to alignment with the main field. Tissues where protons interact efficiently with their surroundings have short T1 — they recover quickly. Fat has a short T1; it appears bright on T1-weighted images. CSF has a long T1; it recovers slowly and appears dark.

**T2 relaxation** (transverse relaxation) describes how quickly protons lose phase coherence with each other. As protons dephase, the signal decays. Tissues with mobile, freely moving protons — like CSF — maintain coherence for longer and therefore appear bright on T2-weighted images. Tissues with restricted proton motion — like white matter — dephase quickly and appear dark.

The practical summary: on a **T1-weighted image**, fat is bright, CSF is dark, grey matter is slightly brighter than white matter. On a **T2-weighted image**, CSF is bright (water appears bright), and pathological processes that increase tissue water content (oedema, tumour, infarction) also appear bright.

## Why Different Sequences Emphasise Different Contrasts

The pulse sequence — the specific pattern of radiofrequency pulses and timing — determines which tissue properties are emphasised in the image. Two key parameters:

**TR (Repetition Time)**: Time between successive excitation pulses. Short TR emphasises T1 differences (tissues with short T1 recover fully between pulses; tissues with long T1 do not). Long TR allows full T1 recovery, reducing T1 contrast and allowing T2 differences to dominate.

**TE (Echo Time)**: Time between excitation and signal readout. Short TE is read out before significant T2 decay has occurred, so T2 differences are not yet apparent. Long TE allows T2 differences to accumulate.

The combination of these parameters defines the image weighting: short TR / short TE gives T1 weighting; long TR / long TE gives T2 weighting. FLAIR (Fluid-Attenuated Inversion Recovery) is a T2-like sequence with an inversion pulse that suppresses free water signal — CSF appears dark, while water in tissue (oedema, tumour) remains bright. FLAIR is particularly useful for detecting perilesional changes because it removes the competing bright signal from CSF.

## The Non-Absolute Nature of MRI Signal

Here is the property of MRI that matters most for understanding AI models: **MRI signal intensity values are not absolute**. Unlike CT, where Hounsfield units have a physical definition (water = 0, air = -1000, dense bone = +1000), MRI signal depends on scanner hardware, calibration, and acquisition parameters. The same tissue scanned at 1.5T and 3T will produce images with different signal intensities. The same scan repeated on the same day on the same scanner will produce slightly different intensities due to thermal noise.

This means you cannot look at an MRI intensity value and say "this voxel is tumour because its value is 847." The meaning of a given intensity value depends entirely on the context of the acquisition. It also means that preprocessing — normalisation, standardisation — is essential before training AI models on multi-site MRI data. The BraTS dataset has been preprocessed precisely to address this: intensities have been normalised, and spatial registration to a standard atlas has been applied.

!!! warning "Common Misconception"
    **MRI intensity values are like CT Hounsfield units — absolute and physically meaningful.**

    They are not. A pixel value of 500 in an MRI means something completely different depending on the scanner, the pulse sequence, the coil, and the normalisation applied. This is why intensity-based preprocessing (z-score normalisation per volume, histogram matching) is standard practice before training AI models on MRI, and why a model trained on data from one scanner without normalisation will often fail on data from another scanner even with identical anatomy.

## What a Neuroradiologist Looks For

Understanding what a radiologist does when reading a brain MRI helps contextualise what we want an AI model to do — and what constitutes a useful model output.

A neuroradiologist evaluating a brain tumour case examines:

- **Location**: Which lobe? Which hemisphere? Does it cross the midline? Proximity to eloquent cortex (motor, language, vision)?
- **Signal characteristics**: T2 hyperintensity (oedema and tumour tissue), T1 hypointensity (necrotic core), post-contrast enhancement (blood-brain barrier breakdown)
- **Enhancement pattern**: Ring-enhancing lesion suggests high-grade glioma or metastasis; solid enhancement or no enhancement has different differentials
- **Mass effect**: Does the lesion displace adjacent structures? Is there midline shift? Herniation risk?
- **Margins**: Infiltrating and poorly defined (suggestive of high-grade glioma) vs well-circumscribed (more characteristic of metastasis or lower-grade tumour)
- **Surrounding oedema**: Vasogenic oedema on FLAIR extending beyond the enhancing lesion; correlates with raised intracranial pressure and neurological symptoms

An AI segmentation model that accurately delineates tumour subregions is directly supporting this clinical reading: it provides volumetric measurements that would take a radiologist 30+ minutes to compute manually, it enables consistent longitudinal comparison across time points, and it creates structured data that can be used for treatment planning.

## Key Terms

| Term | Definition |
|------|-----------|
| T1 relaxation | Longitudinal relaxation — rate at which protons realign with the main magnetic field after excitation |
| T2 relaxation | Transverse relaxation — rate at which protons lose phase coherence; free water has long T2 |
| FLAIR | Fluid-Attenuated Inversion Recovery; T2-weighted with CSF signal suppressed |
| TR / TE | Repetition Time and Echo Time — pulse sequence parameters that determine image weighting |
| Contrast enhancement | Brightening on T1 post-gadolinium injection indicating blood-brain barrier breakdown |
| Gadolinium | Intravenous MRI contrast agent; enhances lesions with disrupted vasculature |
| Pulse sequence | The specific pattern of radiofrequency pulses that defines image contrast |

!!! example "Why This Matters for the Lab"
    In Mission 2, you will visualise and compare the four BraTS modalities (T1, T1ce, T2, FLAIR) for the same patient. You will see that different subregions of the tumour are visible on different modalities: the enhancing rim is clearest on T1ce, the necrotic core appears on T1, perilesional oedema is best seen on FLAIR. Multi-modal models learn to exploit all four sequences jointly — which is why multi-modal input typically outperforms single-modality input for brain tumour segmentation. That observation is grounded in MRI physics, not just in empirical benchmark results.

!!! question "Reflect"
    1. A model trained only on T1-weighted MRI achieves 0.65 Dice on brain tumour segmentation. A multi-modal model (T1, T1ce, T2, FLAIR) achieves 0.85. Why might adding sequences improve performance so substantially for this specific task?
    2. Your hospital has recently upgraded from a 1.5T to a 3T MRI scanner. An existing AI model for brain tumour segmentation begins performing inconsistently on the new scanner's images. Based on your knowledge of MRI physics, what are the likely causes and how would you address them?
    3. FLAIR suppresses CSF signal. Why is this specifically useful for detecting perilesional oedema in brain tumour cases?

!!! note "Connect to Lab Mission"
    **M2 (Data Preprocessing and Visualisation):** You will write code with Claude Code's assistance to load and visualise NIfTI files, display all four modalities in a consistent anatomical orientation, and overlay segmentation masks on the raw images. The goal is to build visual intuition for how different tumour subregions appear across modalities — intuition that will guide your interpretation of model outputs throughout the rest of the course.
