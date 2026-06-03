# The Prompt as Experimental Protocol

## A Familiar Frame

Scientific research depends on protocols. A protocol is a documented, reproducible specification: what you intend to do, with what materials, under what conditions, and what you will measure. The protocol exists because reproducibility is a core value of science — another researcher should be able to follow the same steps and arrive at comparable results.

The same logic applies to prompting an AI coding agent. A prompt is an instruction set. If it is vague, the output will be arbitrary and difficult to reproduce. If it is precise — context established, objective stated, constraints defined, expected output described — then it functions as a specification that Claude can execute reliably, and that you can document, revise, and share.

This framing is not a metaphor for motivational purposes. It has a practical implication: your prompts are part of your research methods. If you used Claude Code to write the analysis pipeline in your dissertation, a thorough methods section would include the prompts you used, just as it would include the scripts and parameters.

## The Transformation: From Vague to Precise

Here is a request that a student might naturally type:

```
Can you help me with my model?
```

There is nothing wrong with this as a casual question between colleagues who share context. As a prompt to Claude, it fails on every dimension. Claude has no information about the project, the dataset, the model architecture, the current state of the work, what "help" means in this context, or what a satisfactory result looks like. Claude will make assumptions — and those assumptions may not align with your intentions at all.

Now consider a prompt that has been structured as a protocol:

```
I am working on brain tumour segmentation using the BraTS 2021 dataset. I have a
U-Net model in model/unet.py and a training script in scripts/train.py. The current
Dice score on the validation set is 0.67, which is lower than expected for this
architecture (we would expect approximately 0.80-0.85 for this dataset). I think the
issue might be in how the data loader handles class weights, because the tumour classes
are heavily underrepresented relative to background.

Please read scripts/train.py and scripts/dataloader.py. Identify whether class
weighting is implemented correctly for an imbalanced multi-class segmentation task.
If it is not, propose a specific fix. Do not edit any files yet — describe your
diagnosis and proposed fix first, so I can review it before you make any changes.
```

The difference in output quality between these two prompts will be substantial. The second prompt constrains Claude to a specific diagnosis task, gives it the files to work with, establishes a hypothesis to evaluate, prevents premature code changes, and requires a human review step before action.

## What the Better Prompt Provides

Breaking down the elements:

**Project context** — BraTS 2021, U-Net. Claude now knows the domain, dataset, and architecture, and can draw on relevant knowledge about their characteristics and typical failure modes.

**Current state** — Dice 0.67, lower than expected. Claude knows where you are and that there is a problem worth diagnosing. Without this, it does not know whether to fix something or optimise something that is already working.

**Hypothesis** — class weighting issue. You are not asking Claude to investigate everything; you are directing it toward a specific potential cause. This is exactly how you would direct a human research assistant: here is what I suspect, please investigate whether I am right.

**File constraints** — specific files named. Claude will read these files, not wander through your entire codebase. This saves time and prevents Claude from "fixing" things in files you did not want touched.

**Task type** — read and diagnose, not edit. Separating the diagnosis step from the implementation step means you can review Claude's reasoning before any changes are made. This is the most important structural safeguard you can build into a complex task.

**Output format** — description, not code. You asked for an explanation and a proposal, not a modified file. The output is something you can review and reason about.

**Validation step** — plan first, wait for approval. This turns the prompt into a two-stage interaction: diagnose and propose, then implement. The approval gate is yours.

## Protocol Elements for Any Prompt

When writing a prompt for a substantive task, work through these elements:

**Background** — what is the project, what have you already done, what is the current state?
Researchers are good at this: it is the "Methods so far" section of your lab notebook.

**Objective** — what specifically should Claude accomplish in this interaction?
Not "improve the model" but "implement per-case Dice scoring across the three tumour subregions and save results to results/per_case_metrics.csv with columns patient_id, dice_wt, dice_tc, dice_et."

**Materials** — which files, datasets, or scripts are involved?
Name them explicitly. Claude should not have to guess which file contains the evaluation logic.

**Method constraints** — what should Claude NOT do?
This is the constraint that students most often omit. "Only edit scripts/evaluate.py." "Do not change the model architecture." "Do not modify the data loader." Constraints prevent over-eager editing.

**Expected output** — what format should the result take?
A CSV? A printed summary? A modified script? A written explanation? An explicit output specification prevents Claude from producing something technically correct but in a format you cannot use.

**Validation step** — how should Claude verify its own output?
Ask Claude to sanity-check its results: "After writing the evaluation script, run it and report the mean Dice score for the whole tumour class. The expected range for this architecture on this dataset is 0.80-0.85."

## Why This Matters for Reproducibility

If you document your prompts, another researcher can reproduce your AI-assisted workflow. Not just re-run the code, but re-run the process by which the code was produced. This is an emerging question in research methodology: when AI tools contribute substantially to analysis pipelines, how do we document that contribution rigorously?

The answer follows from the protocol framing. Document your prompts in the same way you document your scripts: version them, annotate why you wrote them the way you did, record when you revised them and why. Your prompt library is not a convenience tool — it is a methodological record.

This does not mean every session requires exhaustive documentation. For exploratory work and quick checks, informal prompts are fine. But for the critical steps — the data split logic, the metric calculation, the final evaluation pipeline — document what you asked and what you got.

## A Practical Test

Before sending a prompt, ask yourself: if a knowledgeable colleague who had never seen this project read this prompt, would they be able to execute the task correctly? If the answer is no, add the missing information. That test is the protocol standard applied to prompting.
