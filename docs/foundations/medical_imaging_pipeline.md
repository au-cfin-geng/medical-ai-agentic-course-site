# The Medical Imaging Pipeline

The gap between a patient lying inside a scanner and a training example inside a model is large and underappreciated. Every step of that journey — acquisition, archiving, transfer, anonymisation, curation, annotation — introduces decisions, conventions, and potential errors that propagate silently into model behaviour. Understanding this pipeline is not administrative background knowledge. It is essential to interpreting AI results and diagnosing failures.

## From Scanner to Archive: DICOM

Medical imaging data is stored and transmitted in DICOM format — Digital Imaging and Communications in Medicine. DICOM is a standard that defines both the file format and the network protocol for exchanging medical images. Every MRI scanner, CT scanner, and ultrasound machine in a modern hospital speaks DICOM.

A DICOM file is not just an image. It is an image embedded in a container of metadata. That metadata includes the patient's name, date of birth, and medical record number (which is why de-identification is non-trivial). It also includes clinically important information: scanner manufacturer and model, magnetic field strength, acquisition date, pulse sequence parameters (TR, TE, flip angle), slice thickness, pixel spacing, and reconstruction kernel. This metadata is what allows a radiologist — or an AI system — to interpret the image correctly.

The metadata matters for AI in ways that are not always obvious. Scanner manufacturer is correlated with image texture. Field strength (1.5T vs 3T) affects signal-to-noise ratio and contrast characteristics. Slice thickness affects what structures are resolvable in the image. When a model learns that certain pixel patterns correlate with pathology, it may be learning a correlation mediated by scanner type rather than by tissue biology — a classic confound that appears in many published AI studies and is very difficult to detect retrospectively.

!!! clinical "Clinical Relevance"
    In radiology departments, images flow from scanner to PACS (Picture Archiving and Communication System) automatically. Radiologists read from PACS. AI tools in clinical use must integrate into this workflow — typically receiving images from PACS, processing them, and returning results to PACS or to a separate notification system. The fact that clinical AI operates within DICOM and PACS infrastructure means that researchers building clinical tools must understand both the data format and the workflow. A model that works perfectly in a Python notebook but cannot interface with a hospital's PACS is not a clinical tool.

## Anonymisation and De-identification

Patient data is protected by law. In Europe, the General Data Protection Regulation (GDPR) requires that personal data be processed lawfully, and health data is a special category requiring explicit legal basis. In the United States, HIPAA (Health Insurance Portability and Accountability Act) governs protected health information. Using patient imaging data for AI training without appropriate legal basis — whether consent, a data processing agreement, or a research ethics waiver — is not a technical mistake; it is a legal violation.

Anonymisation means removing or obscuring identifying information. In DICOM this means stripping metadata fields: patient name, date of birth, address, referring physician, accession number. But full anonymisation is technically harder than it sounds. Dates can be used to re-identify patients if combined with other information. Patient age calculated from birth date and study date must be replaced with an age range or an offset. Some institutions include patient name burned into the pixel data itself (an artefact of legacy scanning systems), which requires pixel-level de-identification. Three-dimensional facial reconstruction from head MRI scans can recover patient identity even after DICOM metadata is stripped — this is a recognised re-identification risk for neuroimaging data.

The BraTS dataset you will use in the lab has been de-identified and preprocessed by the challenge organisers. This is not a given for clinical datasets you might work with in your own research. It is worth knowing what was done.

## Curation

Raw clinical archives are not suitable for training AI models without curation. A hospital's MRI archive contains every scan taken over years or decades — scans of varying quality, incomplete series, re-scans of the same patient, scans acquired for different clinical indications with different protocols, and incidental findings that may confound the target task. Curation is the process of selecting cases that meet inclusion criteria and excluding those that do not.

Inclusion criteria for an MRI tumour segmentation study might include: complete four-modality acquisition (T1, T1ce, T2, FLAIR), no major acquisition artefacts, confirmed pathological diagnosis, pre-treatment scan. These criteria sound simple; applying them requires reviewing hundreds or thousands of scans, often manually or with semi-automated quality control tools. The decisions made during curation directly shape the distribution of the training data, and therefore the distribution the model learns.

## Labelling and Annotation

For supervised learning, every training example needs a label. In medical imaging, generating labels means having expert clinicians review and annotate images. For brain tumour segmentation, this means neuroradiologists or neurosurgeons drawing voxel-level masks around tumour subregions. For a single patient with a complex glioblastoma, this can take 30-90 minutes. For a dataset of 500 patients, that is hundreds of person-hours of expert clinical time.

This has two important implications. First, labelled medical imaging datasets are expensive to produce, which is why publicly available benchmark datasets like BraTS are disproportionately influential — they are used by most papers in the field simply because they exist. Second, labels are expert judgments, not ground truth in any objective sense. Experienced neuroradiologists disagree about tumour borders. The BraTS dataset addresses this by having multiple expert annotators per case and using a consensus (STAPLE) or majority-vote label. The resulting annotation is still a distribution of expert opinion, not a biological fact.

Inter-rater agreement is typically quantified by metrics like the Intraclass Correlation Coefficient (ICC) for continuous measurements or Cohen's kappa for categorical labels. For brain tumour segmentation, inter-rater Dice scores between expert annotators often fall in the 0.7-0.85 range depending on subregion — which establishes a ceiling on what we should expect from AI models.

!!! warning "Common Misconception"
    **The annotation is the ground truth.**

    Annotations are human judgments made under uncertainty. For pathological processes with diffuse borders — like the infiltrating edge of a glioblastoma or the perilesional oedema on FLAIR — the "true" boundary is biologically ambiguous, not just hard to see. When we evaluate a model against an expert annotation and calculate a Dice score, we are measuring agreement with one (or a consensus of several) expert's judgment, not with an objective biological reality. This distinction matters when interpreting model performance and when deciding whether performance differences are clinically meaningful.

## The Pipeline as a Source of Bias

Each step in the pipeline is a decision point, and each decision point is a potential source of bias. Scanner bias enters at acquisition. Site bias enters at curation (if all positive cases come from one institution). Demographic bias enters if the recruited patient population does not represent the target population. Annotation bias enters if annotators share systematic tendencies — for example, if annotators in the US tend to include enhancing regions more liberally than annotators in Europe.

These biases are not random errors; they are systematic and therefore not averaged away by larger datasets. A model trained on biased data learns the bias. Identifying and characterising pipeline bias is a prerequisite for understanding model behaviour and for making claims about generalisability.

## Key Terms

| Term | Definition |
|------|-----------|
| DICOM | Digital Imaging and Communications in Medicine; the standard format for medical imaging files and transfer |
| PACS | Picture Archiving and Communication System; hospital infrastructure for storing and distributing images |
| Anonymisation | Removal of identifying information from data to protect patient privacy |
| Curation | Selection of cases from a larger archive that meet defined inclusion criteria |
| Annotation | Expert labelling of image data; for segmentation, drawing masks on each case |
| Gold standard | The best available reference label, usually expert consensus annotation |
| Inter-rater agreement | Statistical measure of consistency between independent annotators |

!!! example "Why This Matters for the Lab"
    The BraTS dataset has already passed through this entire pipeline: it was acquired at multiple institutions, de-identified, curated for completeness and quality, and annotated by multiple expert raters with consensus labels. When you load a BraTS case in Mission 1, you are working with the output of thousands of hours of clinical and scientific effort. Understanding that history helps you understand why the data looks the way it does — why intensities are normalised, why skull stripping has been applied, why some cases are harder than others.

!!! question "Reflect"
    1. A research team builds a tumour detection model using scans from their hospital archive without formal ethics approval, arguing that the data is anonymised. What risks does this create — legal, scientific, and ethical?
    2. If expert annotators disagree on tumour borders with a Dice score of 0.80 between them, what is the maximum Dice score you should expect from an automated segmentation model evaluated against a single rater?
    3. A dataset was curated to include only "high-quality, complete" scans. How might this selection criterion bias the resulting model's clinical applicability?

!!! note "Connect to Lab Mission"
    **M1 (Data Exploration):** You will load and inspect BraTS DICOM/NIfTI files, examine metadata, visualise the multi-modal acquisitions, and characterise the dataset distribution. You will use Claude Code to help you write the exploration code. The goal is not just to see what the data looks like, but to develop the habit of interrogating where data comes from before building models on it.
