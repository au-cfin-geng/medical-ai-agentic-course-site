# Medical Image Segmentation

Segmentation is the process of assigning a label to every pixel in a 2D image or every voxel in a 3D volume. It is one of the most fundamental tasks in medical image analysis, and one of the areas where deep learning has had the most direct clinical impact. Understanding segmentation — what it does, how it works, and where it fails — is essential background for the lab.

## What Segmentation Is and Is Not

Segmentation turns an unstructured image into a structured spatial map. Where image classification answers "does this image contain a tumour?", segmentation answers "which voxels contain tumour, and which subregion does each voxel belong to?" The output is a mask — an array of the same shape as the input image, where each element contains a class label.

**Semantic segmentation** assigns each voxel to a class (tumour, white matter, CSF, background) without distinguishing between separate instances of the same class. For brain tumour segmentation, this is typically sufficient: there is usually one primary lesion, and the goal is to map its subregions.

**Instance segmentation** separately identifies each distinct object and segments them individually. This matters in pathology (counting individual cells) or in scenarios with multiple lesions, but is not the primary paradigm for BraTS-style brain tumour segmentation.

## Why Segmentation Is Clinically Useful

The clinical value of segmentation is grounded in measurement and structure. Manual volumetric measurement of a complex brain tumour is time-consuming, operator-dependent, and typically not done in routine practice — clinicians instead use qualitative descriptors ("stable," "progressing") or at best 2D diameter measurements. Automated segmentation enables:

- **Volumetric measurement** of tumour and its subregions, which is more sensitive to treatment response than diameter-based metrics
- **Longitudinal consistency**: the same algorithm applied at baseline and follow-up eliminates inter-reader variability from volumetric comparisons
- **Radiotherapy planning**: delineated tumour volumes feed directly into treatment planning systems; reducing contouring time from hours to minutes has direct workflow value
- **Surgical planning**: visualisation of tumour extent relative to eloquent cortex (motor, language, visual areas) in pre-operative 3D models
- **Research**: structured volumetric data enables large-scale association studies (imaging biomarkers vs genomics, survival, treatment response)

## The Challenge of Ground Truth

The word "ground truth" is widely used in machine learning and carries an implicit claim: there is a correct answer, and the label represents it. In medical image segmentation, this claim is problematic.

Tumour borders are biologically fuzzy. The transition from viable tumour to oedematous brain to normal parenchyma is not a sharp boundary; it is a gradient of cellular density, metabolic activity, and tissue composition. The segmentation mask that an expert draws represents their best judgment about where clinically meaningful distinction lies, not a biological fact. Different experts, given the same scan and the same task definition, will draw different boundaries — not because one is wrong, but because the boundary itself is indeterminate.

The practical consequence is that AI models trained on expert annotations are learning to mimic expert judgment, not to locate a biological ground truth. Evaluating such models against a single expert's annotation gives one measure of performance; evaluating against consensus of multiple experts is more robust; evaluating against an annotation whose inter-rater agreement is known gives the most interpretable result.

For brain tumour segmentation, inter-rater Dice scores between experienced annotators have been reported in the range of 0.74-0.85 depending on the subregion. This is an upper bound on what we should expect from automated systems evaluated against a single rater. A model that achieves Dice 0.90 against one annotator may simply be approximating that annotator's idiosyncratic style rather than producing a universally superior segmentation.

!!! warning "Common Misconception"
    **The model is learning the "right" answer.**

    The model is learning to replicate the annotation of the annotators who labelled the training data. If those annotators systematically over- or under-include a particular tissue boundary, the model will learn to replicate that systematic error. If the annotation convention changes (e.g., because the BraTS committee updated the label definition between challenge years), the model trained on older data will produce outputs that are inconsistent with the new convention — not because the model failed, but because it learned the old convention faithfully. This is not a hypothetical: BraTS label definitions have evolved across years, and models trained on one version do not automatically generalise to another.

## The U-Net Architecture: Conceptual Overview

The dominant deep learning architecture for medical image segmentation is the U-Net, introduced by Ronneberger et al. in 2015 for biomedical image segmentation and now ubiquitous in the field. Its continued dominance is not inertia; it reflects properties that are genuinely well-suited to medical image segmentation tasks.

The U-Net has two halves connected by skip connections:

**The encoder (contracting path):** A series of convolutional blocks, each followed by pooling, progressively reduces spatial resolution while increasing the number of feature channels. This is the "what" pathway: the encoder learns to recognise that a pattern (enhancing tumour texture, necrotic core signal) is present somewhere in the image, at the cost of spatial precision.

**The decoder (expanding path):** A series of upsampling operations progressively restores spatial resolution. The decoder learns to localise features identified by the encoder — to answer "where" not just "what."

**Skip connections:** The critical innovation. At each spatial scale, feature maps from the encoder are concatenated with the corresponding decoder feature maps. This allows the decoder to access both high-level semantic information from the bottleneck (the compressed representation from the encoder) and high-resolution spatial detail from the early encoder layers. Without skip connections, fine-grained boundary localisation would be impossible: the bottleneck representation has discarded the precise spatial information needed to correctly delineate tumour borders at the voxel level.

For 3D brain tumour segmentation, the U-Net is naturally extended to 3D convolutions — operating on volumetric patches rather than 2D slices. This is computationally expensive but important: brain tumours are 3D objects, and context from adjacent slices contains critical information about tumour extent.

## A Typical Segmentation Pipeline

Understanding the full pipeline — not just the model — is important for reproducible, deployable systems.

1. **Data loading:** Load NIfTI or DICOM volumes, check orientation (RAS vs LPS), verify voxel spacing
2. **Preprocessing:** Skull stripping (for brain MRI), intensity normalisation (z-score per volume or per channel), resampling to isotropic voxel spacing, registration of multi-modal sequences to a common space
3. **Patch extraction:** For 3D volumes too large to process whole, extract fixed-size patches during training (with appropriate overlap during inference)
4. **Model forward pass:** Input: multi-channel patch (4 channels for BraTS); Output: multi-class probability map per voxel
5. **Post-processing:** Argmax to convert probabilities to class labels, connected component filtering to remove implausibly small predictions, optional test-time augmentation
6. **Evaluation:** Dice coefficient per class, Hausdorff distance at 95th percentile (HD95), volumetric absolute difference

## What Makes Brain Tumour Segmentation Hard

- **Class imbalance**: The tumour regions occupy a small fraction of the total brain volume. Whole tumour is typically 0.1-3% of total voxels; enhancing tumour is even smaller. A naive model that predicts "background" everywhere achieves 97%+ voxel accuracy while being useless for the task.
- **Fuzzy borders**: Especially at the infiltrating edge (WT boundary) and where oedema grades into normal tissue
- **Heterogeneous appearance**: Even within a single tumour subregion, signal intensity varies substantially from case to case
- **Missing modalities**: Clinical cases sometimes lack one of the four modalities; robust models must handle missing data gracefully
- **Scanner variability**: Even after normalisation, residual scanner-specific signatures affect model generalisability

## Key Terms

| Term | Definition |
|------|-----------|
| Semantic segmentation | Assigning each voxel to a class label |
| U-Net | Encoder-decoder architecture with skip connections; standard for medical segmentation |
| Skip connections | Connections from encoder to decoder at matching spatial scales; preserve fine-grained spatial detail |
| Dice coefficient | 2 × |X ∩ Y| / (|X| + |Y|); measures overlap between predicted and reference mask |
| Hausdorff distance | Measure of the maximum boundary discrepancy between two segmentations |
| Class imbalance | Extreme difference in class frequency; tumour voxels are rare relative to background |
| Patch-based training | Training on sub-volumes of the full image to manage memory constraints |

!!! example "Why This Matters for the Lab"
    In Mission 3 (model training) and Mission 4 (evaluation), you will implement and evaluate a segmentation pipeline. You will encounter class imbalance directly when you examine the loss curves and the confusion matrix. You will see that Dice is a better metric than pixel accuracy for this task. You will visualise cases where the model fails and cases where it performs well, and you will be asked to articulate why — which requires understanding the biology, the imaging, and the architecture together.

!!! question "Reflect"
    1. Two segmentation models achieve the same mean Dice score but differ substantially in Hausdorff distance. What clinical scenarios would favour the model with lower Hausdorff distance, even if mean Dice is equal?
    2. Why does training on 2D slices (slice-by-slice) sometimes produce segmentation masks with inconsistent predictions across adjacent slices, and how does 3D convolution address this?
    3. A radiologist reviews the model's output and finds it consistently over-segments the FLAIR hyperintense region (predicts WT too large). Given your understanding of the annotation process, what are two possible explanations for this finding?

!!! note "Connect to Lab Mission"
    **M3 (Model Training) and M4 (Evaluation and Error Analysis):** You will train a U-Net-based model using Claude Code's agentic capabilities and evaluate it on held-out BraTS cases. The evaluation section of the lab specifically asks you to examine failures: which cases does the model struggle with, and what do those cases have in common? Answering this question requires the combined knowledge of MRI appearance, tumour biology, and model architecture covered in these Foundations pages.
