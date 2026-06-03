# From the Lab to Your Own Research

## What Transfers

The lab missions are built around one specific task: brain tumour segmentation on BraTS 2021. Your own research almost certainly involves a different dataset, a different clinical question, and possibly a different modality or task type. The specific knowledge you gain about BraTS does not transfer automatically. The workflow does.

The core skills you are practising — writing context-rich prompts, separating diagnosis from implementation, verifying outputs before accepting them, maintaining scientific judgment over AI-generated code — are domain-independent. They apply to any supervised learning project in life science research. They apply to clinical genomics, to longitudinal fMRI analysis, to pathology slide classification, to time-series prediction of patient deterioration.

What changes is the vocabulary and the context. The prompting discipline stays the same.

## Writing a CLAUDE.md for Your Own Research Project

The single highest-leverage thing you can do when starting a new AI-assisted research project is write a good `CLAUDE.md` before writing any code. This document is read automatically by Claude at the start of each session. It is your persistent context.

A useful `CLAUDE.md` for a research project contains:

**Project name and research question.** One or two sentences stating what you are investigating. This is not for Claude's benefit alone — writing it forces you to be precise about what you are doing.

**Dataset description.** Where the data is located, what format it is in, how many samples, what the class distribution is, any known issues or quirks. If there are preprocessing steps that have already been applied, document them here.

**Key scripts and what they do.** A brief description of each important file: what it is responsible for, what its inputs and outputs are, and how it fits into the pipeline. Do not list every file — list the ones Claude is likely to need.

**How to run the pipeline.** The exact commands. Not "run the training script" but `python scripts/train.py --config configs/experiment_01.yaml --output_dir results/experiment_01`. If there are environment setup steps (activating a conda environment, loading modules on an HPC cluster), document them.

**What Claude should not touch.** Any files or directories that should be treated as read-only. Preprocessed data directories. Configurations that have been validated and should not be modified without discussion.

**Expected outputs and where they go.** Where results files are written, what format they are in, and what the expected range of key metrics is. This gives Claude a basis for sanity-checking its own outputs.

**Domain vocabulary and conventions.** If your field uses specific abbreviations, metric names, or dataset conventions that might be ambiguous, define them. Do not assume Claude's general knowledge of your sub-field is current or accurate.

A `CLAUDE.md` does not need to be exhaustive. A focused, accurate two-page document is more useful than a ten-page document that is only partially accurate. Write it once, revise it as the project evolves.

## Adapting the Mission Workflow

The arc of the lab missions follows a pattern that recurs across almost all supervised learning projects in biomedical research:

**Mission 0 — Environment and infrastructure.** Get the compute environment working. Confirm dependencies are installed, data is accessible, and a minimal script runs without errors. Establish the `CLAUDE.md`.

**Mission 1 — Data inspection.** Before any modeling, understand your data. Count the samples, check the class distribution, visualise a representative subset, identify any anomalies or missing values. Decisions made here affect everything downstream.

**Mission 2 — Baseline.** Train the simplest reasonable model and evaluate it honestly. The baseline establishes your starting point and, crucially, tells you whether the pipeline is working correctly before you complicate it.

**Mission 3 — Error analysis.** Study where the baseline fails. Which cases are worst? Is there a pattern? What does the failure mode tell you about the problem? This step prevents the common mistake of improving model architecture before understanding what is actually going wrong.

**Mission 4 — Targeted improvement.** Based on the error analysis, make a specific, hypothesised improvement. Evaluate it fairly. Document whether the hypothesis was supported.

This arc works for classification, segmentation, survival prediction, dose estimation, and most other supervised tasks in life science research. The specific choices within each step change; the structure does not.

## What Stays the Same

Across domains, these principles hold:

**Protocol first.** Write your prompt as you would write a methods section — with enough specificity that someone else could reproduce what you did.

**Inspect before you model.** Time spent understanding your data before training is almost always recovered in debugging time saved later.

**Separate building from checking.** The prompt that builds the code and the prompt that verifies it serve different purposes. Merging them reduces your ability to catch errors.

**Evidence-based iteration.** Changes to the pipeline should be motivated by evidence from results, not by intuition about what might help. Intuition generates hypotheses; results confirm or refute them.

**Maintain scientific judgment.** Claude will not tell you if your research question is well-posed, if your dataset is appropriate for your claim, or if your evaluation is fair. Those judgments are yours.

## What You Will Need to Learn for Your Domain

The transferable skills are not a substitute for domain knowledge. For your own research, you will need to learn or deepen:

**The specific preprocessing pipeline.** Every imaging modality has its own conventions — bias field correction for MRI, windowing for CT, stain normalisation for pathology. These are not things Claude can determine from first principles for your specific dataset.

**The clinical context.** What does a false positive mean for a patient in your application? What is the clinical consequence of a missed finding? What level of performance would be required before a clinician would trust this tool? These answers come from your clinical collaborators and from the literature, not from a language model.

**The relevant evaluation metrics.** Dice coefficient is standard for volumetric segmentation. AUC is common for classification. For your specific clinical question, there may be domain-specific metrics or reporting standards (RECIST criteria, RANO criteria, survival analysis conventions) that must be respected.

**Regulatory and ethical considerations.** If your work is intended to contribute to a clinical tool, even eventually, there are regulatory frameworks (FDA, CE marking) and ethical requirements (IRB approval, data governance, privacy) that structure what you can and cannot do. Claude has no reliable knowledge of your specific institutional or regulatory context.

## Building Your Own Prompt Library

After each project, document the prompts that worked. Not every prompt — the ones that produced reliable, useful results for specific recurring tasks. Over time, this becomes a personal research toolkit: prompts for data inspection, prompts for baseline training, prompts for error analysis, prompts for generating figures for papers.

This is worth more than it might sound. Research workflows repeat across projects more than we often acknowledge. The prompt you wrote to generate a per-case metrics table for one project will work, with minor adaptation, for the next project. The Reviewer prompt that helped you identify failure mode patterns will transfer. Your prompt library is accumulated methodological knowledge.

Version your prompt library in a git repository alongside your code. You are more likely to actually maintain it that way, and it gives you a record of how your prompting practice evolves.

## A Final Note on Scientific Judgment

The most important thing to carry from this course into your own research is not a prompting technique. It is the habit of maintaining your own judgment over AI-generated output.

In medicine and biology, the cost of errors is not abstract. A data split that leaks patient information inflates performance estimates that affect clinical decision-making. A metric implemented incorrectly leads to wrong conclusions about model quality. An analysis pipeline that has not been verified by a human who understands the domain is not a reliable basis for scientific claims.

Claude Code is a capable research tool. Used with discipline, it can substantially accelerate your work. But it is a tool, not a collaborator who shares your scientific responsibility. The judgment about whether a result is valid, whether an analysis is appropriate, and whether a conclusion is warranted — that judgment is yours, and it is not one you can delegate to an AI system, however capable.

Use Claude Code to go faster. Use your scientific training to make sure you are going in the right direction.
