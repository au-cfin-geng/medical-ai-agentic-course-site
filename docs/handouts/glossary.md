# Glossary

> **For print:** use browser Print -> Save as PDF. Recommended: A4, portrait, two columns if your browser supports it.

---

Alphabetical reference for all key terms used across the lab. Each entry includes a brief definition and a tag indicating which part of the course it belongs to.

---

## A

**Agent** — An AI system that takes actions in its environment (reading files, running code, browsing the web) rather than simply generating text. In this lab, Claude Code acts as an agent: it reads your project files, writes scripts, and runs commands on your behalf. [Agentic Coding]

**Algorithm** — In clinical AI, a computational procedure that receives input data (e.g. MRI volumes) and produces a structured output (e.g. a segmentation mask or a classification label). The word is used loosely in regulatory documents to mean any AI/ML-based software function. [Clinical AI]

**Affine matrix** — A 4 x 4 matrix stored in the NIfTI file header that maps voxel coordinates (i, j, k) to physical world coordinates (x, y, z) in millimetres. Must be used when computing distance-based metrics such as HD95. [MRI]

**Argparse** — A Python standard library module for building command-line interfaces. Scripts in this lab use argparse to expose hyperparameters (learning rate, epochs, paths) as command-line arguments, making them reproducible without editing source code. [Agentic Coding]

**Atlas registration** — The process of aligning an individual brain MRI to a standard brain template (atlas), such as the SRI24 atlas used in BraTS preprocessing. Enables spatial correspondence across patients. [MRI]

**Augmentation** — Applying random transformations (rotation, flipping, intensity scaling, elastic deformation) to training images to artificially increase dataset diversity and reduce overfitting. Common in medical imaging where labelled data is scarce. [Machine Learning]

**AUC (Area Under the Curve)** — Most commonly refers to the area under the ROC (Receiver Operating Characteristic) curve. A value of 1.0 means perfect discrimination; 0.5 means no better than chance. Used for classification tasks, not segmentation. [Clinical AI]

**Axial** — The horizontal plane that divides the head into top (superior) and bottom (inferior) portions. The most commonly viewed plane in brain MRI. In a 3D volume (X, Y, Z), axial slices correspond to varying the Z index. [MRI]

---

## B

**Batch** — A fixed number of training examples processed together in one forward and backward pass. Larger batches use more memory but produce more stable gradient estimates. In 2D slice training, a batch typically contains 8-16 slices. [Machine Learning]

**Bias field** — A smooth, low-frequency intensity inhomogeneity in MRI caused by non-uniformity in the radiofrequency coil. Can make the same tissue type appear brighter in one region and darker in another. Corrected using algorithms such as N4ITK. [MRI]

**Binary segmentation** — A segmentation task with two classes: foreground (e.g. tumour) and background (non-tumour). In BraTS, whole tumour (WT) detection can be framed as binary segmentation. Contrasted with multi-class segmentation. [Segmentation]

**BraTS (Brain Tumour Segmentation Challenge)** — An annual segmentation benchmark and dataset providing multi-parametric MRI of glioblastoma cases with expert annotations. The de facto standard for evaluating brain tumour segmentation algorithms. Pre-processed data includes skull stripping, co-registration, atlas alignment, and intensity normalisation. [BraTS]

---

## C

**Calibration** — The degree to which a model's predicted probabilities match observed frequencies. A well-calibrated model that predicts 80% confidence is correct about 80% of the time. Poor calibration means a model may be confidently wrong. Important when model uncertainty is used in clinical decisions. [Clinical AI]

**CE Mark** — European conformity marking required for medical devices (including SaMD) placed on the EU market under the Medical Device Regulation (MDR 2017/745). Equivalent in intent but different in process from FDA clearance. [Clinical AI]

**Class imbalance** — When one class (e.g. background voxels) vastly outnumbers another (e.g. tumour voxels). In brain tumour segmentation, background typically constitutes over 98% of all voxels. Causes naive classifiers to predict all-background and still achieve high accuracy; handled by Dice loss, weighted loss, or oversampling. [Machine Learning]

**Claude.md** — A markdown file placed at the project root that provides persistent context for Claude Code sessions. Includes project summary, file map, working commands, and current status. Because Claude Code has no memory between sessions, CLAUDE.md is the mechanism for session continuity. [Agentic Coding]

**Context (prompt context)** — The information provided to an AI model before its main instruction. In Claude Code, context includes the CLAUDE.md file, any files Claude has read in the current session, and the conversation history. Context is finite; long contexts can cause important information to be overlooked. [Agentic Coding]

**Coronal** — The frontal plane that divides the head into front (anterior) and back (posterior) portions. In a 3D volume, coronal slices correspond to varying the Y index. [MRI]

---

## D

**Data leakage** — The accidental inclusion of information from the test set during training or model selection. Examples: splitting by scan rather than patient (multiple scans from one patient appear in both train and test); using test-set statistics for normalisation; selecting hyperparameters based on test performance. Inflates reported performance. [Machine Learning]

**Deployment** — The process of making a trained model available for clinical use, including integration into hospital IT infrastructure (PACS, RIS), staff training, governance processes, and ongoing monitoring. Research performance does not guarantee deployment performance. [Clinical AI]

**Dice (Dice Similarity Coefficient, DSC)** — The primary segmentation metric used in BraTS. Defined as 2TP / (2TP + FP + FN), where TP = true positive voxels, FP = false positives, FN = false negatives. Ranges from 0 (no overlap) to 1 (perfect overlap). Equivalent to the F1 score in the binary case. [Segmentation]

**DICOM (Digital Imaging and Communications in Medicine)** — The clinical standard for storing and transmitting medical images. Stores one image slice per file, with extensive metadata in headers. Must typically be converted to NIfTI or similar research formats before use in AI pipelines. [MRI]

**Distribution shift** — A change in the statistical properties of input data between training and deployment. Common causes: different hospital, different scanner vendor or field strength, different patient population, updated imaging protocol. Can cause substantial performance degradation even for high-performing models. [Clinical AI]

---

## E

**ED (Peritumoral Oedema)** — Label class 2 in BraTS. The region of tissue swelling surrounding the tumour, visible as hyperintensity on T2 and FLAIR sequences. Part of the Whole Tumour (WT) region. [BraTS]

**Enhancing Tumour (ET)** — The tumour region where the blood-brain barrier has broken down, causing gadolinium contrast agent to accumulate. Appears very bright on T1ce (T1 with contrast). Label class 4 in BraTS. Clinically significant as a marker of active disease and treatment response. [BraTS]

**Epoch** — One complete pass through the training dataset. If you have 1,000 training slices and a batch size of 10, one epoch consists of 100 gradient update steps. Model performance is typically reported per epoch. [Machine Learning]

**ET fraction** — The ratio of enhancing tumour (ET) voxels to whole tumour (WT) voxels for a given case. A useful case-level feature for error analysis; cases with very small ET regions are typically harder to segment correctly. [BraTS]

**External validation** — Testing a trained model on data from a different institution, scanner, or patient population than the training data. The most important evidence required before clinical deployment. Absence of external validation is a major red flag in clinical AI papers. [Clinical AI]

---

## F

**F1 score** — The harmonic mean of precision and recall: 2 x (Precision x Recall) / (Precision + Recall). Mathematically equivalent to the Dice score in the binary segmentation case. Used interchangeably with Dice in medical imaging. [Segmentation]

**False Negative (FN)** — A voxel that is truly tumour but was predicted as background. In clinical terms: missed disease. A high false negative rate means the model under-segments, leaving tumour unlabelled. [Segmentation]

**False Positive (FP)** — A voxel that is truly healthy tissue but was predicted as tumour. In clinical terms: hallucinated disease. A high false positive rate means the model over-segments, labelling healthy tissue as tumour. [Segmentation]

---

## G

**GBM (Glioblastoma Multiforme)** — The most aggressive primary brain tumour, classified as WHO grade IV. BraTS data consists predominantly of GBM cases (and lower-grade gliomas in some editions). Characterised by necrotic core, enhancing rim, and surrounding oedema — the three tumour regions annotated in BraTS. [Clinical AI]

**Gibbs ringing** — An MRI artefact appearing as oscillating bands near sharp edges (e.g. the skull-brain boundary). Caused by truncation of k-space data during acquisition. Can create false edges that confuse segmentation boundary detection. [MRI]

---

## H

**Hausdorff Distance 95th Percentile (HD95)** — A boundary-based segmentation metric. Computes the 95th percentile of all pairwise distances between the predicted boundary and the ground truth boundary, in millimetres. The 95th percentile is used instead of the maximum to reduce sensitivity to single outlier voxels. Clinically relevant for radiotherapy planning where boundary accuracy directly affects treatment margins. [Segmentation]

**HD95** — See Hausdorff Distance 95th Percentile.

---

## I

**Inter-rater variability** — The degree of disagreement between two or more expert annotators labelling the same case. Measured as Dice between their annotations. Non-zero inter-rater variability means there is an upper bound on achievable segmentation performance — a model cannot do better than the experts agree with each other. [Segmentation]

**Isotropic** — Describes a voxel with equal physical dimensions in all three spatial directions (e.g. 1.0 mm x 1.0 mm x 1.0 mm). BraTS data is resampled to isotropic 1 mm spacing during preprocessing. Anisotropic spacing (unequal dimensions) must be accounted for in distance metric computation. [MRI]

---

## L

**Label** — In supervised learning, the known correct output for a training example. In segmentation, a label map is a 3D array where each voxel has a class value (0=background, 1=NCR, 2=ED, 4=ET in BraTS). Also called a mask, annotation, or segmentation map. [Segmentation]

**Label convention** — The specific integer values assigned to each class in a label map. BraTS uses 0/1/2/4 (note: there is no class 3, which is a historical artefact). Confusion between BraTS convention and sequential 0/1/2/3 indexing is one of the most common label bugs in cross-entropy training. [BraTS]

**Learning rate** — A hyperparameter controlling how large a step the optimiser takes when updating model weights. Too high: training diverges. Too low: training is slow and may get stuck. Typical starting value for Adam optimiser: 1e-4. [Machine Learning]

**Loss function** — A function that quantifies how wrong the model's predictions are. Minimised during training via gradient descent. For multi-class segmentation: cross-entropy loss, Dice loss, or their combination (DiceCELoss) are standard choices. [Machine Learning]

---

## M

**Mask** — A binary (or multi-class) image array where 1 (or a class value) indicates the presence of a structure. In segmentation, the ground truth mask is the expert annotation; the predicted mask is the model output after argmax. [Segmentation]

**MHRA (Medicines and Healthcare products Regulatory Agency)** — The UK regulator for medical devices, including AI-based SaMD. Post-Brexit, the UK MDR pathway is distinct from EU MDR. [Clinical AI]

**Mission** — One of the seven lab exercises in this course, each focused on a specific phase of the AI development workflow (environment setup, data inspection, modelling, error analysis, improvement, study design, clinical translation). [Agentic Coding]

**Multi-class segmentation** — A segmentation task with more than two classes. BraTS is a four-class problem (background, NCR, ED, ET). Requires careful handling of the loss function and metric computation compared to binary segmentation. [Segmentation]

---

## N

**NCR (Necrotic and Non-Enhancing Tumour Core)** — Label class 1 in BraTS. The dead or dying tissue at the centre of a GBM, visible as hypointensity on T1ce. Part of both the Whole Tumour (WT) and Tumour Core (TC) derived regions. [BraTS]

**NIfTI (Neuroimaging Informatics Technology Initiative)** — A file format for neuroimaging data (.nii or .nii.gz). Stores the image array together with spatial metadata (affine matrix, voxel spacing, orientation). The standard format for research brain MRI pipelines; BraTS data is distributed as NIfTI. [MRI]

**Normalisation (intensity)** — Rescaling image intensities to a standard range or distribution. MRI intensities are not standardised across scanners. Common methods: z-score normalisation (subtract mean, divide by std), percentile-based clipping (clip at 1st and 99th percentile), or min-max scaling. [MRI]

---

## O

**Overfitting** — When a model learns the training data so well that it performs poorly on unseen data. Signs: training loss continues to decrease after validation loss plateaus or rises. Mitigated by dropout, augmentation, early stopping, and regularisation. [Machine Learning]

---

## P

**PACS (Picture Archiving and Communication System)** — The hospital's clinical image storage and retrieval system. Where real patient MRI data lives before it is transferred for research use. Access to PACS data for AI training requires ethics approval, data governance agreements, and de-identification. [MRI]

**Post-market surveillance** — Ongoing monitoring of a cleared medical device after it is deployed in clinical practice. For AI-based SaMD, this includes monitoring for distribution shift, performance degradation, and unexpected failure modes. Required by both FDA and EU MDR frameworks. [Clinical AI]

**Precision (Positive Predictive Value)** — TP / (TP + FP). Of all voxels the model labelled as tumour, what fraction were truly tumour? High precision means few false alarms. Low precision means the model is over-segmenting. [Segmentation]

**Prompt** — An instruction or query provided to an AI model. In Claude Code, a prompt is text typed into the terminal interface that directs Claude's next action. The quality and structure of a prompt directly determines the quality of the output. [Agentic Coding]

---

## R

**Recall** — See Sensitivity.

**Registration** — The process of aligning two or more images to the same spatial coordinate system. In BraTS, all four modalities (T1, T1ce, T2, FLAIR) are registered to each other before annotation. Required for multi-modal input to ensure modalities describe the same voxels. [MRI]

**Role (prompt role)** — A persona assigned to Claude at the start of a prompt that defines its cognitive stance for the task (e.g. "Act as a data analyst", "Act as a Planner", "Act as a Critic"). Role assignment is a key prompting principle because it activates domain-specific knowledge and sets expectations for output format. [Agentic Coding]

---

## S

**Sagittal** — The lateral plane that divides the head into left and right portions. In a 3D volume, sagittal slices correspond to varying the X index. [MRI]

**SaMD (Software as a Medical Device)** — Software intended to perform a medical device function without being part of a hardware device. AI-based clinical decision support tools (including tumour segmentation software) are classified as SaMD. Subject to medical device regulation (FDA, EU MDR, MHRA). [Clinical AI]

**Sensitivity (Recall, True Positive Rate)** — TP / (TP + FN). Of all voxels that are truly tumour, what fraction did the model correctly identify? High sensitivity means few missed tumours. A model that predicts everything as tumour achieves sensitivity of 1.0, so sensitivity must always be reported alongside specificity or precision. [Segmentation]

**Session** — A single continuous interaction with Claude Code from startup to close. Claude Code has no memory between sessions. Context must be re-established at the start of each session using a context-setting prompt and the CLAUDE.md file. [Agentic Coding]

**Skip connections** — In the U-Net architecture, direct connections between the encoder and decoder at matching spatial resolution levels. Skip connections pass fine-grained spatial information from the encoder directly to the decoder, preventing loss of boundary detail through the bottleneck. Critical for segmentation quality. [Machine Learning]

**Skull stripping** — The removal of non-brain tissue (skull, skin, scalp fat) from an MRI volume, leaving only the brain parenchyma. A standard preprocessing step in neuroimaging. BraTS data is pre-processed with skull stripping applied. [MRI]

**Spacing** — The physical size of each voxel in millimetres, specified per dimension (x_mm, y_mm, z_mm). Must be used when computing any distance-based metric (HD95) or when comparing volumes across cases. Stored in the NIfTI file header. [MRI]

**Specificity (True Negative Rate)** — TN / (TN + FP). Of all voxels that are truly background, what fraction did the model correctly identify as background? In brain segmentation, specificity is typically very high (> 0.99) because the brain volume is predominantly background; it is not a useful primary metric. [Segmentation]

---

## T

**T1 (T1-weighted MRI)** — An MRI sequence where signal intensity reflects longitudinal (T1) relaxation time. White matter appears bright, grey matter intermediate, and CSF dark. Used primarily for anatomy and post-operative assessment. [MRI]

**T1ce (T1 contrast-enhanced, T1 with gadolinium)** — A T1-weighted sequence acquired after intravenous injection of a gadolinium-based contrast agent. Regions where the blood-brain barrier is disrupted (such as enhancing tumour) appear very bright. The most informative modality for identifying active tumour. [MRI]

**T2 (T2-weighted MRI)** — An MRI sequence where signal intensity reflects transverse (T2) relaxation time. CSF appears very bright, white matter dark. Excellent for visualising oedema and lesion extent. [MRI]

**TC (Tumour Core)** — A BraTS-derived evaluation region consisting of label classes 1 + 4 (NCR + ET). Represents the resectable core of the tumour. Used as one of the three primary evaluation regions in BraTS alongside WT and ET. [BraTS]

**Test set** — The subset of data held out for final model evaluation after all training and validation-based decisions are made. Must never be used for hyperparameter tuning or model selection. Contamination of the test set is the most common source of inflated performance in clinical AI studies. [Machine Learning]

**Tool use** — The capability of an AI agent to call external tools (file reading, code execution, web search) as part of its reasoning process. Claude Code uses tool use to read and write files, run shell commands, and check its own outputs. [Agentic Coding]

**Training split** — The portion of data used to adjust model weights (via gradient descent). Separate from validation and test splits. In BraTS competitions, the standard split is approximately 70% training, 15% validation, 15% test at the patient level. [Machine Learning]

---

## U

**U-Net** — A convolutional neural network architecture introduced by Ronneberger et al. (2015), originally for biomedical image segmentation. Features an encoder-decoder structure with skip connections. The dominant architecture for medical image segmentation and the model implemented in this lab. [Machine Learning]

---

## V

**Validation** (clinical) — The process of evaluating a medical AI system to confirm it performs safely and effectively for its intended use. Distinct from technical validation (model testing). Encompasses internal validation, external validation, prospective clinical studies, and post-market surveillance. [Clinical AI]

**Validation split** — The subset of data used to monitor model performance during training and to make decisions about hyperparameters and early stopping. Must be kept separate from the test set. Performance on the validation set is used to select the best checkpoint. [Machine Learning]

**Voxel** — The three-dimensional equivalent of a pixel. The fundamental unit of a 3D medical image. Each voxel has a physical size (determined by spacing) and a scalar intensity value. In segmentation, each voxel is assigned a class label. [MRI]

---

## W

**WT (Whole Tumour)** — A BraTS-derived evaluation region consisting of all tumour label classes: 1 + 2 + 4 (NCR + ED + ET). Represents the full spatial extent of the tumour including oedema. Typically the easiest of the three BraTS regions to segment because it is the largest. [BraTS]

---

## X / Z

**z-score normalisation** — Normalising image intensities by subtracting the mean and dividing by the standard deviation of the brain voxels. Produces a distribution with mean approximately 0 and standard deviation 1. Common in BraTS pipelines, often computed per-modality per-case (not across the dataset). [MRI]
