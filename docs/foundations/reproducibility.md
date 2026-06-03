# Reproducibility in Medical AI

Reproducibility is not a bureaucratic requirement. It is the difference between science and anecdote. In medical AI, where claims about model performance may influence clinical adoption decisions that affect patients, the stakes of irreproducible results are not merely academic.

## The Reproducibility Crisis in Machine Learning

The broader scientific community has grappled with a reproducibility crisis for over a decade — most prominently in social psychology (where large-scale replication efforts found that only ~40% of published findings replicated), but also in preclinical biomedical science, neuroscience, and economics. Machine learning has its own version of this problem, with distinctive features.

A 2019 survey of NeurIPS and ICML papers found that fewer than 6% provided code sufficient to reproduce their results. A study of clinical AI publications found that the majority could not be fully replicated from the information in the paper alone — missing preprocessing details, unspecified hyperparameters, unclear train/test splits. The problem is not generally one of deliberate fraud; it is one of incomplete reporting, optimistic selection of results, and the enormous practical difficulty of capturing all the decisions that go into producing a result.

In machine learning research, the reproducibility problem has specific manifestations that differ from wet lab science. Code that runs today may not run in six months because dependencies have updated. A random seed that was not fixed leads to different results on every run. A model that was the best of fifty runs, reported as a single result, benefits from a multiple comparison problem that is rarely acknowledged. These are not exotic edge cases; they are common practice.

!!! clinical "Clinical Relevance"
    When a published study claims that an AI model detects lung cancer on CT with 94% sensitivity and 88% specificity, a hospital considering adoption needs to trust that number. If the result was achieved by selecting the best of many experimental runs, by allowing test-set leakage, or by evaluating on a dataset that is not representative of the hospital's patient population, the number is misleading. Clinicians and hospital administrators typically cannot audit the code, verify the splits, or re-run the analysis. They rely on the scientific community's standards of rigorous reporting. When those standards are not upheld, clinical decisions may be based on inflated estimates — with consequences for real patients.

## Data Leakage: The Silent Inflator of Performance

Data leakage is the single most common cause of inflated performance metrics in AI research. It occurs when information from the test set contaminates the training process, allowing the model to perform better on the evaluation than it would on genuinely unseen data.

**Test set contamination** occurs when examples from the test set are included in training data. This can happen inadvertently when datasets are assembled from multiple sources without careful de-duplication. It can also happen when preprocessing steps (such as normalisation statistics or feature scaling) are computed across the entire dataset rather than fit only to training data and then applied to the test set.

**Temporal leakage** occurs in prediction tasks that have a temporal structure. If a model is trained to predict 30-day readmission and the training data includes information recorded after admission (which a truly predictive model would not have access to), test-set performance will be inflated. If the dataset is randomly split by encounter rather than by time, future encounters may train the model and past encounters evaluate it — the opposite of how deployment works.

**Patient-level leakage** is particularly important in imaging studies and is frequently mishandled. A 3D brain volume contains many 2D slices or 3D patches. If the dataset is split at the slice or patch level — randomly assigning each slice to train, validation, or test — then slices from the same patient will appear in all three sets. The model sees nearly every patient during training. When it is evaluated on "test" slices from patients it has partially trained on, it performs far better than it would on truly unseen patients.

This is not a subtle problem. The performance difference between slice-level splitting and patient-level splitting can be dramatic — sometimes 10-15 Dice points. Patient-level splitting is the only valid approach for evaluating medical image segmentation models intended for clinical use: in deployment, you will encounter patients the model has never seen, not slices from patients the model has been partially trained on.

!!! warning "Common Misconception"
    **Reporting the best result from many experimental runs is standard practice.**

    It is common practice, but it is not scientifically defensible without acknowledgment. If you train five models with different random seeds and report the best Dice score, you have not demonstrated that your method achieves that Dice score — you have demonstrated a lower bound on the result that can be obtained with luck and multiple attempts. The appropriate practice is to report results over multiple seeds with mean and standard deviation, to pre-specify the evaluation protocol before running experiments, and to account for the multiple comparisons problem when comparing many methods.

## Random Seeds, Determinism, and Reproducibility

Neural network training is stochastic: weight initialisation, data augmentation, and (unless careful steps are taken) GPU operations introduce randomness. Setting a random seed controls this randomness but does not guarantee identical results across hardware, operating systems, or library versions. A seed that produces one result on an NVIDIA A100 running PyTorch 2.0 may produce a different result on an RTX 3090 running PyTorch 1.13, even with the same code.

True computational reproducibility — obtaining bit-identical results — requires pinning not just the random seed but the entire software environment: package versions, CUDA version, and (in some cases) disabling non-deterministic GPU operations that trade speed for determinism. In practice, the goal is typically *statistical* reproducibility: results that agree within expected variance across independent runs, hardware platforms, and research groups.

For the lab, you will fix the random seed in all training scripts. This ensures that your results are consistent within the lab environment, and that when you share your configuration with a classmate, they can reproduce your results.

## What to Save and Why

A reproducible ML experiment requires preserving more than the model weights. The complete set of artifacts needed to reproduce and audit a result includes:

- **Code** at the exact version used (commit hash, not just "the main branch")
- **Training configuration**: all hyperparameters, architecture choices, loss function, optimiser settings
- **Data splits**: which patients were in train, validation, and test — saved as a list, not just a random seed
- **Preprocessing parameters**: normalisation statistics fitted on training data, resampling parameters
- **Model checkpoint**: best weights by validation metric, with epoch and validation score recorded
- **Training logs**: loss curves, metric histories, per-epoch summaries
- **Random seeds**: all seeds used (Python, NumPy, PyTorch)
- **Environment specification**: requirements.txt or conda environment file with pinned versions

This is not an aspirational standard; it is the minimum required to answer the question "did this model really achieve this result?" and to hand the project to a new researcher or engineer six months later.

## Version Control for Code and Data

Git is the standard for code version control. Every significant change to analysis code should be committed. Every experiment should be tagged with a commit hash, so that the exact code used to produce a result is recoverable. "Works on my machine" is not a reproducibility standard.

Data versioning is harder. Data files are often too large for standard git repositories. Tools like DVC (Data Version Control) address this by tracking data files and their hashes in git while storing the actual files in object storage (S3, GCS, or local cache). This enables the same workflow for data as for code: every version of the dataset is tracked, every preprocessing step is logged, and any state of the pipeline can be reconstructed.

In the context of public benchmarks like BraTS, data versioning is simplified: the dataset has a canonical version (identified by challenge year and release) and any preprocessing applied to it should be fully documented and reproducible from the raw release.

## Reporting Standards in Medical AI

The medical AI community has developed reporting standards analogous to CONSORT for clinical trials:

**TRIPOD-AI (Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis):** Standards for reporting prediction model studies. Covers study design, data sources, predictors, outcomes, statistical methods, and model performance.

**CONSORT-AI:** An extension of the CONSORT randomised trial reporting standard for trials involving AI interventions. Addresses the unique reporting challenges of AI in clinical trials: training data description, model version control, failure mode reporting.

**STARD (Standards for Reporting of Diagnostic Accuracy):** Applies when an AI model is being evaluated as a diagnostic test. Requires specification of patient population, reference standard, and the conditions under which the index test and reference standard were applied.

These standards matter not as compliance boxes to tick, but as checklists of the methodological details that must be reported for a result to be scientifically evaluable. A paper that does not specify its train/test split methodology, or that does not report confidence intervals on performance metrics, is providing incomplete evidence regardless of how impressive the headline number looks.

## Key Terms

| Term | Definition |
|------|-----------|
| Data leakage | Contamination of training by test-set information, inflating apparent performance |
| Patient-level split | Train/validation/test split performed at patient level, preventing any patient from appearing in multiple sets |
| Random seed | Initial value for pseudo-random number generation; fixing it enables reproducible stochastic computation |
| DVC | Data Version Control; tool for versioning large data files alongside code in git |
| TRIPOD-AI | Reporting standard for AI prediction model studies |
| CONSORT-AI | Reporting standard for clinical trials of AI interventions |
| Model checkpoint | Saved model state (weights + configuration) at a specific training step |

!!! example "Why This Matters for the Lab"
    The lab is deliberately designed around reproducibility practices. Dataset splits are provided as fixed files — you do not generate your own random split. All training scripts use fixed seeds. Preprocessing parameters are fitted only on the training set. Your experiment configurations are saved alongside results. At the end of the course, you will be able to hand your results directory to another researcher who can reproduce your Dice scores exactly. This is not perfectionism; it is the baseline standard for scientific credibility.

!!! question "Reflect"
    1. A published paper reports Dice 0.91 on brain tumour segmentation but does not specify how train/test splitting was performed. List three different splitting strategies that could lead to this result, and estimate how they might differ in performance if the split were done correctly at patient level.
    2. You train a model five times with different random seeds and obtain Dice scores of 0.81, 0.84, 0.79, 0.86, 0.83. You report "our model achieves Dice 0.863 ± 0.025." What is wrong with reporting 0.863, and how should you report this result?
    3. Six months after a model is deployed, a hospital's IT department upgrades the imaging system. What aspects of the trained model's artefacts do you need to preserve to assess whether the performance change (if any) is attributable to the software upgrade vs the imaging system upgrade?

!!! note "Connect to Lab Mission"
    **M5 (Experiment Tracking and Reproducibility):** You will set up MLflow or Weights & Biases logging for your training runs, implement proper patient-level splits, save all artifacts needed to reproduce your best run, and write a brief methods section in TRIPOD-AI style. Claude Code will help you implement the logging infrastructure. The goal is to produce a result that you could defend under peer review — not just in a demo.
