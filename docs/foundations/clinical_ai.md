# What Is Clinical AI?

Clinical AI refers to the application of machine learning and related computational methods to clinical data — images, signals, text, genomics, structured records — for purposes that include supporting diagnosis, estimating prognosis, guiding treatment decisions, and flagging risk. The qualifier *clinical* is important: it signals that the system operates in, or in close proximity to, a medical context where errors carry real consequences for patients.

This definition deliberately excludes much of what is called "medical AI" in press releases. A natural language processing model that helps researchers mine the literature is not clinical AI in this sense. A segmentation model embedded in a radiotherapy planning workflow, advising oncologists on tumour margins before irradiating a patient — that is clinical AI.

## Narrow AI, Not General Intelligence

Every clinical AI system deployed today is a narrow AI: it does one thing in one domain under one distribution of inputs. A model trained to detect diabetic retinopathy in fundus photographs taken with a specific camera protocol under specific lighting conditions will degrade, sometimes catastrophically, when applied to images from a different camera or a different demographic. It does not "understand" the retina. It has learned a mapping from pixel patterns to labels that generalised within a training distribution.

This is not a failing unique to medicine. It is the fundamental character of contemporary supervised learning. Recognising this prevents a class of expensive errors — clinical integration of a model that was never validated on your patient population, your scanner, your hospital workflow.

!!! clinical "Clinical Relevance"
    FDA-cleared clinical AI tools already operate in radiology, ophthalmology, cardiology, and stroke care. IDx-DR for diabetic retinopathy screening was the first FDA-authorised AI diagnostic device requiring no physician oversight of the AI output itself. Viz.ai's stroke detection system alerts the neurovascular team before the patient leaves the CT scanner. These tools cleared regulatory hurdles not because they achieved high accuracy on a test set, but because they demonstrated prospective clinical utility under defined conditions of use. Understanding what those conditions are — and what lies outside them — is as important as understanding model architecture.

## The Supervised Learning Paradigm

Most clinical AI rests on supervised learning. The paradigm is conceptually simple: collect a large set of labelled examples (images with diagnoses, scans with segmentation masks, records with outcomes), train a model to predict labels from inputs, and evaluate generalisability on held-out data. The implicit promise is that the patterns the model learns will be clinically meaningful and will transfer to unseen cases.

This promise is kept more often than critics claim and less often than developers hope. Pattern recognition in images is a domain where supervised deep learning has proven genuinely powerful. Models that detect pneumonia on chest X-rays, identify skin lesions, or segment brain tumours have matched or exceeded radiologist performance under controlled benchmark conditions. The frontier failure modes are not primarily about accuracy within distribution — they are about robustness outside it.

What clinical AI does well:

- **Pattern recognition in images** at scales and speeds that exceed individual human reviewers
- **Risk stratification** from structured records when outcomes are frequent enough to generate signal
- **Anomaly detection** as a screening aid to prioritise expert review
- **Volumetric measurement** of structures that would take hours to measure manually

What it does not do well:

- **Causal reasoning**: a model that identifies a finding does not understand what caused it
- **Out-of-distribution generalisation**: performance degrades when inputs depart from the training distribution
- **Common sense**: a model can confidently segment an artefact as tumour because the pixel intensities matched the training distribution
- **Uncertainty calibration**: many models produce high-confidence predictions on inputs they should flag as uncertain

## Distribution Shift: The Central Problem in Clinical Deployment

If there is one concept that separates researchers who understand deployed AI from those who do not, it is distribution shift. A model trained at Hospital A on a particular scanner, with a particular patient mix, with labels from a particular group of radiologists, learns a distribution. Hospital B has different scanners, different contrast protocols, different demographics, and different annotation conventions. The model is now operating outside its training distribution, and its performance will be different — often substantially worse.

Distribution shift is not a software bug. It is a property of any system that learns from finite data. It means that a model validated at one institution cannot be assumed to generalise to another without prospective evaluation at the target site. It means that when a hospital upgrades its MRI scanner, existing AI tools must be re-evaluated. It means that a model trained on adult data may not transfer to paediatric patients.

!!! warning "Common Misconception"
    **High accuracy on a test set means the model is clinically ready.**

    It does not. A test set is only as good as the data it was drawn from. If the test set shares the same demographic composition, scanner, and annotation team as the training set, high accuracy is expected — but it tells you little about performance in a different clinical environment. The history of medical AI is littered with models that achieved headline-grabbing benchmark performance and then failed in prospective deployment because the test set was not representative of the target population. Regulatory submissions now require prospective validation data precisely because retrospective test-set performance is insufficient evidence of clinical utility.

## Research AI vs Deployed AI

There is a meaningful distinction between a research AI system optimised for publication metrics and a deployed AI system that must be safe, robust, and monitored over time. Research AI is typically evaluated on a fixed, curated benchmark under controlled conditions. Deployed AI must handle the messiness of real clinical data: missing sequences, acquisition artefacts, patients who do not match the training distribution, edge cases the developers never anticipated.

Deployed AI also requires monitoring infrastructure. A model that was performing well six months ago may be degrading because the hospital changed its imaging protocol, because the patient mix has shifted, or because a software update changed the preprocessing pipeline. Post-market surveillance — analogous to pharmacovigilance for drugs — is a regulatory requirement for AI as a medical device in both the US and EU, and a scientific necessity regardless of regulation.

## Key Terms

| Term | Definition |
|------|-----------|
| Supervised learning | Learning a mapping from inputs to outputs using labelled training examples |
| Training distribution | The statistical distribution of inputs the model was trained on |
| Distribution shift | Mismatch between training and deployment data distributions |
| FDA-cleared | Approved by the US Food and Drug Administration for a specific intended use |
| SaMD | Software as a Medical Device — the regulatory category for AI diagnostic tools |
| Prospective validation | Evaluating a model on data collected after model development, in the target clinical setting |
| Post-market surveillance | Ongoing monitoring of an AI tool's performance after deployment |

!!! example "Why This Matters for the Lab"
    In this course you will train a segmentation model on the BraTS dataset — a carefully curated, multi-institutional benchmark. Your model will achieve a certain Dice score. The lab is designed to help you reason critically about what that score means: what dataset it was measured on, what population it represents, what would happen if you deployed it on a different scanner, and what validation you would need before trusting it clinically. The point is not to train the best model. It is to understand what "best" means in context.

!!! question "Reflect"
    1. Suppose a clinical AI company reports 97% sensitivity for detecting intracranial haemorrhage on non-contrast CT. What additional information would you need before recommending this tool be adopted at your hospital?
    2. A model trained on data from three academic medical centres achieves excellent performance. Why might this model perform worse at a community hospital with a different patient mix?
    3. Who bears responsibility when an AI-assisted diagnosis is wrong — the developer, the hospital, or the clinician?

!!! note "Connect to Lab Mission"
    **M0 (Environment Setup) and M1 (Data Exploration):** Before you write a single line of model code, you will explore the BraTS dataset to understand its provenance: how many sites, what scanners, what patient population, what annotation protocol. This is not a warm-up exercise. It is the foundational scientific act of understanding your data's distribution before making claims about model performance.
