# From Clinical Question to Dataset

## The Framing Step Most Papers Skip

The majority of medical AI papers begin with a dataset. A group of researchers obtains access to imaging data, notices that the data has labels, and asks: what can we build? This is the wrong order. The correct order is to start with a clinical question, then ask what data would be needed to answer it. The difference is not pedantic — it determines whether the resulting model is clinically useful or merely technically impressive.

This page walks through how to translate a clinical problem into a well-defined AI task, using brain tumour segmentation as the worked example throughout.

---

## The Clinical Question Drives Everything

The clinical question for brain tumour segmentation is: **"How large is this tumour, where is it relative to critical structures, and how has it changed since the last scan?"**

Answering that question requires measuring tumour volume — and measuring volume from MRI requires delineating the tumour boundary. That is the clinical justification for pixel-wise segmentation. Not "segmentation is an interesting computer vision problem" but "a clinician needs a volume number and a spatial map to guide treatment."

This distinction matters because it immediately tells you:

- What counts as a correct answer: a segmentation that matches what an expert radiologist would draw for the purpose of treatment planning, not some abstract ground truth
- What precision is clinically meaningful: a volume error of 0.5 mL matters less for a 40 mL GBM than for a 2 mL metastasis
- What the downstream action is: radiation planning, surgery approach, response assessment — each has different tolerance for segmentation error

---

## From Question to Task: The Translation Steps

### Step 1 — What are you labelling, and why?

The clinical outcome drives what you annotate. For GBM, the clinically relevant regions are:

- **Whole tumour (WT)**: the full extent of abnormality on FLAIR — relevant for oedema and infiltration
- **Tumour core (TC)**: the necrotic core plus enhancing rim — relevant for surgical planning
- **Enhancing tumour (ET)**: the actively enhancing region on T1ce — relevant for treatment response

BraTS uses all three regions because different clinical questions require different regional definitions. If you only care about radiotherapy target volume, you might only need the enhancing tumour plus a margin. Knowing the clinical endpoint determines which regions you need to label, which determines the annotation protocol you give to radiologists.

### Step 2 — Who to include and exclude

Patient selection criteria are not just methodological housekeeping. They define the population your model will and will not work on. For brain tumour segmentation:

- **Include criteria**: adult patients (>18), confirmed GBM or lower-grade glioma on histopathology, complete four-sequence MRI (T1, T1ce, T2, FLAIR), MRI within 48 hours pre-operatively or at diagnosis
- **Exclude criteria**: prior radiation to brain (changes enhancement patterns), prior surgery at same site (creates artefacts), inadequate image quality, MRI acquired with implants that cause susceptibility artefacts

These exclusions mean your model is trained on relatively clean cases. When deployed in a district hospital where patients arrive post-op and with older scanners, it will encounter cases that were systematically excluded from your training data.

### Step 3 — Scanner and acquisition inclusion criteria

MRI is not like a photograph. The same tumour can look dramatically different on a 1.5T scanner vs a 3T scanner, or with different sequence parameters. BraTS explicitly designed its dataset to include scans from multiple institutions and multiple scanner types to test generalisation. If you only train on 3T Siemens data, your model may systematically underperform on 1.5T GE data.

---

## The PICO Framework Adapted for AI

Clinical research uses the PICO framework to structure research questions. It applies directly to medical AI:

| Element | Clinical Meaning | AI Adaptation |
|---------|-----------------|---------------|
| **P** — Population | Which patients? | Patient selection criteria, scanner criteria, disease subtype |
| **I** — Intervention | What AI system? | Model architecture, training data, inference protocol |
| **C** — Comparator | Compared to what? | Manual expert annotation? Another algorithm? Previous software version? |
| **O** — Outcome | What are we measuring? | Dice coefficient? Volume agreement? Clinical impact? Time saved? |

The BraTS challenge uses this framework implicitly: P = multi-institutional glioma patients, I = any submitted algorithm, C = expert consensus annotation, O = Dice and Hausdorff distance on three tumour regions. The challenge design reflects clinical reality: the task is generalisable across institutions (multi-site data), and the comparator is expert annotation (the clinical standard).

---

## How BraTS Was Constructed

The Brain Tumour Segmentation (BraTS) challenge dataset is the benchmark you will use in this course. Understanding its construction helps you understand its limitations.

BraTS aggregates data from multiple academic medical centres across the US and Europe. Each centre contributed cases with full four-sequence MRI and expert manual segmentations. The labels were created by multiple annotators and underwent quality control. The multi-institutional design was deliberate: the challenge organisers wanted a dataset that would force algorithms to generalise across scanner types, acquisition protocols, and patient populations.

Key design choices in BraTS:

- **Four MRI modalities per case**: T1, T1-contrast-enhanced, T2, FLAIR — each provides complementary tissue contrast
- **Three hierarchically-nested label regions**: WT contains TC, TC contains ET
- **Expert annotation**: not crowd-sourced, not automated — trained neuroradiologists and neurosurgeons
- **Multi-institutional**: specifically to test generalisation

What BraTS does not capture: paediatric patients, low-quality scans, post-treatment changes in the early weeks after surgery, patients with implants. These are real clinical scenarios your model will eventually face.

---

## Dataset Bias from Patient Selection

If your training data comes only from one academic centre with a tertiary neurosurgery programme, your dataset will over-represent:

- Large, clearly delineated tumours (small or subtle tumours get referred elsewhere or are caught incidentally)
- Younger patients with favourable performance status
- Well-characterised GBM and grade II/III glioma (unusual histologies are rarer)
- High-quality 3T MRI (tertiary centres invest in scanner quality)

A model trained on this data deployed at a district general hospital will encounter: older patients with comorbidities, lower-quality scans, more post-treatment imaging, and atypical presentations. This is distribution shift — the test population differs systematically from the training population. It is the most common cause of performance degradation after clinical deployment.

The lesson is not that biased datasets are useless. It is that you must know who your training data represents, and be explicit about who your model will and will not generalise to.

---

## The Key Principle

A rigorous AI study starts with a clinical question, defines the AI task that answers it, specifies the population and outcomes before looking at data, and constructs or curates a dataset that reflects the intended deployment context. Starting from the data and working backwards is technically possible but produces models whose clinical utility is unclear and whose failure modes are unknown.

!!! note "Connect to Lab Mission"
    **Now do the lab — M0 (Environment Setup) and M1 (Data Exploration).**

    Before you write a single line of model code, you will set up your environment (M0) and inspect the BraTS dataset structure (M1). As you explore, keep these questions in mind: What clinical question does this dataset answer? Which patient populations were included or excluded? What would happen if you deployed a model trained on this data in a setting different from a US/European academic medical centre? These questions are not rhetorical — write your answers in your lab notebook.
