# MRI Basics for AI Researchers

You do not need to understand the physics of MRI to build a brain tumour segmentation model. You do need to understand what MRI is measuring, why different sequences look different, and why the lack of standardised intensity units is a fundamental problem for AI. This page gives you the minimum clinical context to make sensible decisions in the lab.

## What MRI Measures

MRI exploits the fact that hydrogen nuclei (protons) in water molecules respond to magnetic fields. When placed in a strong magnetic field and excited with radiofrequency pulses, protons absorb energy and then release it as they return to their equilibrium state. The rate at which they release this energy depends on the molecular environment — the viscosity of the surrounding tissue, the presence of large molecules, the water content. Two different relaxation time constants, **T1** and **T2**, characterise this recovery, and by designing pulse sequences to be sensitive to one or the other, radiologists can create images with dramatically different tissue contrasts from the same anatomy.

This is fundamentally different from CT, where image intensity reflects X-ray attenuation and is calibrated in Hounsfield units — a global standard across scanners and sites. MRI intensities have no absolute scale. The signal in a voxel depends on the scanner field strength, the coil used, the specific pulse sequence parameters, and post-processing applied by the scanner vendor. This has profound consequences for AI.

## The Four Key Sequences

**T1-weighted (T1)** images have short repetition time (TR) and short echo time (TE). Fat and white matter appear bright; grey matter appears slightly darker; CSF appears dark. T1 provides excellent anatomical detail and is the primary sequence for measuring brain volume, identifying haemorrhage, and characterising lesions that alter normal tissue architecture.

**T2-weighted (T2)** images have long TR and long TE. Water-rich tissues appear bright — CSF is very bright, oedema is bright, most tumours are bright. White matter appears darker than grey matter. T2 is the most sensitive sequence for detecting pathology: almost any disease process increases tissue water content and therefore T2 signal.

**FLAIR (Fluid-Attenuated Inversion Recovery)** is a T2 variant with an additional inversion pulse that suppresses the signal from free CSF. This makes perilesional changes and white matter lesions far more visible than on standard T2, because the bright CSF no longer obscures adjacent pathology. In glioma imaging, FLAIR is essential for visualising the full extent of tumour infiltration and surrounding oedema — the tumour often extends well beyond the visible enhancing core, and FLAIR captures this infiltrative margin.

**T1 post-contrast (T1ce)** is a T1-weighted sequence acquired after intravenous injection of a gadolinium-based contrast agent. Gadolinium shortens T1 relaxation time, causing tissues where it accumulates to appear very bright on T1. In the normal brain, the blood-brain barrier prevents gadolinium from entering tissue. In high-grade gliomas, the blood-brain barrier breaks down at the actively proliferating tumour rim, allowing contrast to leak in. T1ce therefore shows enhancement specifically at regions of active tumour growth, neoangiogenesis, and blood-brain barrier disruption — the most clinically aggressive part of the tumour.

## Why Intensities Are Not Standardised

A key contrast with CT: in CT, a voxel with a Hounsfield unit of -1000 is air and a voxel at +1000 is dense bone, everywhere, on every scanner, globally. MRI has no such calibration. A white matter voxel might have an intensity of 800 on one scanner and 1,600 on another, depending on coil sensitivity, field strength (1.5T vs 3T), and acquisition parameters. This means you cannot directly compare intensities across subjects or sites, and you cannot use absolute thresholds.

For AI, this means intensity normalisation is mandatory — but there is no agreed-upon standard. Common approaches include z-score normalisation per volume, percentile-based normalisation, and histogram matching to a reference subject. Each makes different assumptions, each fails differently, and each is an active research question. The BraTS dataset applies a specific normalisation as part of its preprocessing pipeline; in raw clinical data, you must make this choice yourself.

## The Four BraTS Modalities Together

The BraTS challenge provides all four sequences (T1, T1ce, T2, FLAIR) co-registered to the same space and resampled to 1mm isotropic voxels. No single sequence captures the full clinical picture:

| Modality | What it shows | Key tissue contrast | Clinical use |
|---|---|---|---|
| T1 | Anatomy, tissue type | White matter bright, CSF dark, grey matter intermediate | Brain structure, haemorrhage, mass effect |
| T1ce | Blood-brain barrier breakdown | Actively enhancing tumour very bright vs normal brain | Identify active tumour rim, monitor treatment response |
| T2 | Total water content | CSF and oedema very bright, white matter moderately dark | Detect pathology and oedema extent |
| FLAIR | Infiltration without CSF confusion | Perilesional changes bright, free CSF suppressed | Tumour infiltration margin, white matter lesions |

A neuroradiologist integrating all four modalities can characterise: the total abnormal signal region (FLAIR), the enhancing active tumour (T1ce), the necrotic core (dark on T1ce, often heterogeneous on T1 and T2), and mass effect on normal structures (T1). Using all four together gives the most complete picture of tumour extent — which is exactly why BraTS provides all four, and why multi-modal fusion is standard practice in high-performing segmentation models.

## What a Neuroradiologist Looks For

In reviewing a glioblastoma case, a neuroradiologist evaluates: the location and laterality of the tumour; the presence and extent of enhancement (suggesting high grade); the degree of surrounding oedema and mass effect; involvement of eloquent cortex (motor strip, language areas) that would affect surgical planning; signs of midline shift; and the relationship of the tumour to white matter tracts. None of this is captured in a segmentation mask. The segmentation is one input into a much richer clinical reasoning process, which is why AI segmentation supports but does not replace the radiologist.

## Why Standardisation Is a Hard Problem for AI

Because MRI intensities are site- and scanner-specific, a model trained on data from one group of institutions may fail at a new site simply because that site uses a slightly different acquisition protocol. The model learns to exploit intensity patterns that correlate with the label in the training distribution, but those patterns may not transfer. Intensity normalisation reduces but does not eliminate this problem. Multi-site training with harmonisation methods (ComBat, deep learning-based harmonisation) are active research directions. For this course, you are working with BraTS data that has already been preprocessed and partially harmonised — a significant advantage over raw clinical data that it is worth explicitly acknowledging.

!!! note "For the lab"
    The teaching data in `data/sample/` includes all four BraTS modalities for each subject: `_t1.nii.gz`, `_t1ce.nii.gz`, `_t2.nii.gz`, and `_flair.nii.gz`. Mission 1 asks you to inspect and document what is present — including the voxel dimensions, intensity ranges, and visual appearance of each modality. Understanding what you are feeding into your model is the first step of responsible ML development.
