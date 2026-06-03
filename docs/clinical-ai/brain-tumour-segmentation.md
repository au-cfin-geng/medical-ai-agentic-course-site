# Brain Tumour Segmentation

## Glioblastoma: The Clinical Context

Glioblastoma multiforme (GBM) is the most common primary malignant brain tumour in adults, accounting for approximately 50% of all primary malignant brain tumours. It is aggressive, infiltrating, and carries a poor prognosis: median survival with standard treatment (surgery + temozolomide chemotherapy + radiotherapy) is approximately 15 months. GBM does not respect anatomical boundaries — tumour cells infiltrate along white matter tracts, crossing into adjacent lobes and sometimes crossing the corpus callosum to the contralateral hemisphere. This infiltrating biology means there is rarely a clean boundary between tumour and normal brain tissue, which has direct consequences for how hard segmentation is.

The clinical challenges of GBM make it an important target for AI. Treatment planning for radiotherapy requires accurate delineation of the tumour target volume and surrounding structures. Surgical planning requires understanding tumour location relative to eloquent cortex and major white matter tracts. Response assessment after treatment requires reproducible volume measurements over time — a task that is time-consuming and highly variable when done manually.

## How Glioblastoma Appears on MRI

GBM typically presents as a heterogeneous mass with several distinct regions, each visible on different MRI sequences:

- **Necrotic core**: A central region of tumour necrosis (dead tissue) that appears dark on T1ce (does not enhance because there are no functioning blood vessels) and heterogeneous on T2 and FLAIR.
- **Enhancing rim**: The actively proliferating tumour margin where blood-brain barrier breakdown allows gadolinium contrast to accumulate. This appears bright on T1ce. This is the most biologically aggressive region.
- **Oedema and infiltration**: Beyond the enhancing rim, FLAIR signal is elevated in a larger zone that contains a mixture of vasogenic oedema (fluid due to blood-brain barrier leak) and tumour cell infiltration. This region is difficult to delineate precisely — neuroradiologists cannot reliably distinguish pure oedema from infiltrated tissue on standard MRI.

This layered structure is why the BraTS challenge defines multiple segmentation targets rather than a single binary mask.

## The BraTS Challenge

The Brain Tumour Segmentation (BraTS) challenge was established to provide a standardised multi-institutional benchmark for automated brain tumour segmentation. The dataset includes MRI volumes from multiple institutions, acquired on different scanners, pre-processed to a common space (1mm isotropic, skull-stripped, co-registered), and annotated by expert neuroradiologists following a structured protocol.

BraTS annotations define four label values:
- **0**: Background / healthy tissue
- **1**: Necrotic tumour core (NCR)
- **2**: Peritumoral oedema/invasion (ED)
- **4**: Gadolinium-enhancing tumour (ET)

These four labels are combined into three evaluation regions with complementary clinical meanings.

## The Three BraTS Evaluation Regions

| Region | BraTS labels included | Clinical significance |
|---|---|---|
| Whole Tumour (WT) | Labels 1 + 2 + 4 | Total disease extent, relevant for radiotherapy planning |
| Tumour Core (TC) | Labels 1 + 4 | Surgically targetable volume; excludes oedema |
| Enhancing Tumour (ET) | Label 4 only | Actively proliferating margin; primary target for treatment and response assessment |

Each region answers a different clinical question. WT tells you the total footprint of abnormal tissue. TC approximates the volume a neurosurgeon would aim to resect. ET is the most aggressive component and the one most closely correlated with tumour grade and treatment response. Evaluating all three separately forces a model to be accurate at multiple scales simultaneously — a model that segments the whole tumour well but misses the enhancing core has limited clinical value for surgery planning.

## Why This Is a Hard Segmentation Problem

Brain tumour segmentation presents multiple technical challenges that make it harder than many other medical imaging segmentation tasks:

**Tumour heterogeneity**: No two glioblastomas look the same. Tumour size, location, shape, degree of necrosis, and oedema extent vary enormously across patients. Models trained on a finite sample of this variability will encounter cases that fall outside their learned distribution.

**Infiltrating borders**: The boundary between FLAIR signal abnormality and normal-appearing brain is diffuse and not physically sharp. The ground truth annotation at this boundary reflects a judgment call, not a physical measurement.

**Scanner variability**: Even within the BraTS dataset, data was acquired at multiple institutions with different scanners, field strengths, and protocols. The preprocessing pipeline mitigates but does not eliminate this variability.

**Inter-rater disagreement**: Multiple expert annotators do not always agree, particularly at the infiltrative margin and the boundary between necrosis and enhancing tumour. The BraTS annotation protocol uses majority voting across multiple raters to produce a consensus label, but the underlying disagreement remains.

**Class imbalance**: Tumour voxels typically constitute 1-5% of a brain volume. A model that predicts "background" everywhere will have very high voxel-level accuracy but zero clinical utility.

## What Ground Truth Means and Does Not Mean

The BraTS "ground truth" segmentations are expert human annotations made according to a structured protocol, reviewed by senior neuroradiologists, and resolved by consensus. They are the best available labels. They are not physical ground truth. The true extent of tumour infiltration at the cellular level cannot be measured from standard MRI — it would require histopathological analysis of tissue samples from across the brain, which is not clinically feasible. This means that a model achieving Dice 1.0 against BraTS labels has matched human expert consensus annotation, not the biological ground truth. This distinction matters when communicating model performance to clinical audiences.

!!! note "For the lab"
    Your baseline model in Mission 2 will attempt whole-tumour segmentation — predicting which voxels belong to any of labels 1, 2, or 4. This is the easiest of the three evaluation targets because it includes the most signal (oedema is large and bright on FLAIR). Mission 3 asks you to identify which cases your model fails on and to form a specific hypothesis about why. The clinical and imaging context in this page gives you the vocabulary to make that hypothesis clinically meaningful, not just statistically observed.
