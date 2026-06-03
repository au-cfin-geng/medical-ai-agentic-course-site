# Brain Tumour Imaging

Brain tumours are among the most challenging problems in oncology — not because imaging is inadequate, but because the disease itself is biologically complex, infiltrating, and heterogeneous. Understanding what brain tumours look like on MRI, and why, is prerequisite knowledge for working with brain tumour segmentation AI.

## Glioblastoma: The Prototype

Glioblastoma multiforme (GBM), classified as WHO Grade 4 glioma, is the most common primary malignant brain tumour in adults. Approximately 3 per 100,000 people per year are diagnosed. Median survival with standard of care — surgical resection followed by concurrent chemoradiotherapy (Stupp protocol: temozolomide + radiotherapy) — is approximately 14-16 months. Five-year survival is below 5%. These are not statistics to recite; they are the clinical reality that makes accurate imaging and AI-assisted planning genuinely consequential.

GBM is not a single disease. The name describes a histological pattern — a highly cellular, mitotically active, microvascularly proliferative neoplasm with areas of necrosis — that can arise from multiple molecular subtypes. IDH-wildtype GBM (the most common) behaves more aggressively than IDH-mutant variants. Molecular profiling (IDH, MGMT methylation, 1p/19q codeletion) has become standard because it influences prognosis and treatment decisions. Imaging cannot yet reliably determine molecular subtype, though radiogenomics — associating imaging features with molecular markers — is an active area of AI research.

The term "multiforme" in the original name refers to the tumour's morphological heterogeneity — it looks different from region to region within the same lesion. This heterogeneity is not cosmetic; it reflects underlying biological differences: proliferating tumour, necrosis, oedema, infiltrating tumour cells in normal-appearing tissue. Segmentation that respects these subregions is clinically meaningful because different subregions are treated differently and measured differently in response assessment.

!!! clinical "Clinical Relevance"
    Accurate volumetric segmentation of brain tumours directly affects clinical decisions. Pre-operative planning uses tumour extent to plan safe resection while preserving function. Radiotherapy target volumes — the gross tumour volume (GTV), clinical target volume (CTV), and planning target volume (PTV) — are derived from segmented tumour boundaries. Response assessment by the RANO (Response Assessment in Neuro-Oncology) criteria uses volumetric changes in enhancing tumour to classify response, stable disease, or progression. Manual volumetric measurement of a complex GBM takes an experienced radiologist 30-90 minutes; automated segmentation can deliver the same measurement in seconds with consistent methodology.

## Lower-Grade Gliomas

WHO Grade 1 and 2 gliomas (pilocytic astrocytoma, diffuse astrocytoma, oligodendroglioma) are lower-grade tumours with longer survival but significant long-term morbidity from treatment and disease progression. WHO Grade 3 tumours (anaplastic astrocytoma, anaplastic oligodendroglioma) occupy an intermediate position. Lower-grade gliomas typically appear differently on MRI: they tend to be T2 hyperintense and infiltrating without the prominent necrosis and enhancement pattern of GBM. This affects segmentation: in lower-grade tumours, the enhancing core — often the most reliably delineated subregion — may be absent.

The BraTS dataset includes both GBM (Grade 4) and lower-grade gliomas (Grade 2-3), which is one reason the segmentation task is challenging: the target appearance varies substantially across cases.

## How Tumours Appear on Each MRI Modality

Understanding the characteristic appearance of GBM on each modality is not academic knowledge — it is the clinical reasoning that justifies the multi-modal imaging protocol.

**T1 (pre-contrast):**
The tumour core and necrotic regions appear hypointense (dark) relative to normal brain. Healthy white matter is slightly brighter than grey matter on T1. A large GBM on unenhanced T1 may be relatively inconspicuous — the main value of pre-contrast T1 is as a baseline for assessing enhancement when gadolinium is added, and for detecting T1-bright signals like blood products (subacute haemorrhage) or fat.

**T1ce (T1 post-contrast, post-gadolinium):**
This is the most diagnostically distinctive sequence for high-grade glioma. Gadolinium is an intravenous contrast agent that shortens T1 relaxation time in regions where it accumulates. Gadolinium cannot cross an intact blood-brain barrier; it accumulates where the barrier is disrupted, which in GBM corresponds to regions of active tumour vasculature. The result is ring-like or irregular enhancement surrounding the necrotic core — bright on T1ce where normal brain or necrosis is dark. The enhancing tumour (ET) region on T1ce is used in clinical practice as a proxy for viable, high-grade tumour burden, and is the primary target for radiotherapy dose escalation.

**T2:**
Tumour tissue and surrounding vasogenic oedema both appear bright (hyperintense) on T2-weighted images. T2 hyperintensity reflects increased tissue water content — this occurs both in solid tumour regions and in the surrounding reactive oedema. The tumour on T2 typically appears as a bright region that extends well beyond the enhancing rim visible on T1ce. The infiltrating edge of GBM — tumour cells that have invaded apparently normal brain — often lies within the T2 hyperintense region beyond the enhancing margin. This is why resecting the enhancing tumour alone is insufficient to remove all malignant cells.

**FLAIR (Fluid-Attenuated Inversion Recovery):**
FLAIR highlights perilesional changes better than T2 because it suppresses CSF signal. On T2, bright CSF adjacent to a bright tumour can make boundaries difficult to interpret. FLAIR removes this ambiguity: CSF is dark, while tumour-associated oedema and infiltrating tissue remain bright. The FLAIR hyperintense region — which includes both the enhancing tumour, the necrotic core, and the surrounding non-enhancing infiltrated tissue — constitutes the "whole tumour" (WT) region in the BraTS annotation scheme.

## The BraTS Challenge and Dataset

The Brain Tumour Segmentation (BraTS) challenge has been running since 2012, hosted annually at major medical image computing conferences (MICCAI). It has become one of the most influential medical image segmentation benchmarks, with hundreds of teams competing each year and thousands of resulting publications.

The BraTS dataset is multi-institutional (contributed by hospitals and academic centres across North America, Europe, and Asia), multi-scanner (acquired on multiple scanner platforms at varying field strengths), and expert-annotated (masks were drawn by experienced neuroradiologists and neurosurgeons, with consensus labels). The dataset is preprocessed to a standard pipeline: co-registered to a common atlas space, skull-stripped, and intensity-normalised. This preprocessing removes some of the scanner-to-scanner variability but also means the BraTS distribution is not identical to raw clinical data.

Each BraTS case provides four modalities (T1, T1ce, T2, FLAIR) and a voxel-level segmentation mask with three labels corresponding to clinically distinct subregions.

## The Four BraTS Subregions

BraTS defines three annotated label classes that correspond to nested anatomical and biological regions:

**Enhancing Tumour (ET, label 4 in BraTS 2020):** Regions that enhance on T1ce relative to T1 pre-contrast. Represents active tumour with disrupted blood-brain barrier. Clinically most important for treatment planning and response assessment.

**Tumour Core (TC):** The union of enhancing tumour and necrotic/non-enhancing tumour core. The necrotic centre of a GBM — which appears dark on T1ce and T2 — is included in TC. This region defines the bulk of the tumour that would be targeted for surgical resection.

**Whole Tumour (WT):** The union of all tumour-related signal, including TC and the non-enhancing, FLAIR-hyperintense surrounding infiltrated region. This is the most extensive region and the most difficult to delineate precisely because its boundary with surrounding oedema is biologically and radiologically ambiguous.

The hierarchical nesting (ET ⊂ TC ⊂ WT) is by design — it reflects the biological organisation of GBM from the dense enhancing tumour core outward to the infiltrating periphery.

!!! warning "Common Misconception"
    **The FLAIR hyperintense region = the tumour.**

    FLAIR hyperintensity in and around a glioma reflects multiple processes: oedema, infiltrating tumour cells, post-treatment gliosis, and reactive changes in adjacent tissue. Not all FLAIR signal represents tumour, and not all tumour is visible as FLAIR signal. Infiltrating tumour cells can be present in brain tissue that appears normal on all conventional MRI sequences. This is why even "complete" resection of the MRI-visible tumour does not cure GBM: microscopic disease extends beyond the visible boundary. Segmentation models trained on expert annotations learn to delineate what experts delineate — the visible boundary — not the biological extent of disease.

## Key Terms

| Term | Definition |
|------|-----------|
| GBM | Glioblastoma multiforme; WHO Grade 4 primary brain tumour |
| IDH | Isocitrate dehydrogenase; key molecular marker in glioma classification |
| MGMT | O6-methylguanine-DNA methyltransferase; methylation status predicts temozolomide response |
| RANO | Response Assessment in Neuro-Oncology; standardised criteria for assessing tumour response to treatment |
| Enhancement | Brightening on T1ce due to gadolinium accumulation; reflects blood-brain barrier disruption |
| Whole Tumour (WT) | All FLAIR-hyperintense tumour-associated regions |
| Tumour Core (TC) | Enhancing tumour plus necrotic core; the bulk tumour region |
| Enhancing Tumour (ET) | T1ce-enhancing regions; reflects viable high-grade tumour with disrupted vasculature |

!!! example "Why This Matters for the Lab"
    The segmentation model you will train in Missions 3 and 4 produces predictions on all three BraTS subregions. When you evaluate performance, you will find that ET Dice is typically higher than WT Dice, and that the most difficult subregion to segment varies by case grade and tumour heterogeneity. This is not arbitrary — it reflects the underlying biology and imaging characteristics described on this page. Understanding the clinical meaning of each subregion helps you judge whether a model's performance profile is acceptable for clinical use.

!!! question "Reflect"
    1. A model achieves Dice 0.90 on whole tumour but only 0.72 on enhancing tumour. Which performance metric is most relevant for radiotherapy planning, and why?
    2. Why does the infiltrating edge of GBM — which lies beyond the FLAIR-hyperintense region — make surgical cure impossible? What does this imply about the clinical ceiling for an AI segmentation tool?
    3. The BraTS dataset includes both Grade 2-3 gliomas (which often lack clear enhancement) and Grade 4 GBM (with prominent enhancing rim). How might including both in the training set affect a model's performance on each subtype separately?

!!! note "Connect to Lab Mission"
    **M3 (Model Training):** You will train a 3D U-Net or nnU-Net model on the BraTS training set, with the segmentation target defined exactly as described here — WT, TC, and ET. When you examine cases where the model fails, your ability to reason about tumour biology and MRI appearance will help you generate hypotheses about why performance degrades in specific cases.
