# Roles for Claude

## Why Roles Work

When you write a prompt, you are not just specifying a task — you are implicitly specifying a mode of thinking. "Look at this data and tell me what you see" requires a different cognitive posture than "implement this function" or "argue against my conclusion." These are genuinely different tasks that benefit from different framings.

Role-based prompting makes that framing explicit. You tell Claude upfront what kind of thinking you need. This is not manipulation or performance — it is precision. Explicitly naming the role helps Claude select the appropriate approach and helps you clarify what you actually want before you start.

The roles described here are not exhaustive. They are the ones most useful for the lab missions and for research workflows in general. You can combine, modify, or invent roles as your work demands.

---

## The Builder

**What it does:** Implements code from your specification.

**When to use:** When you know precisely what you want — the logic is clear in your head, you just need someone to write it in Python. The Builder is not the right role when you are still working out what you need.

**Key requirement:** Your specification must be complete before you invoke the Builder. If you use a Builder role without a complete specification, Claude will fill the gaps with its own assumptions.

**Example prompt fragment:**

```
You are an expert Python developer working in a medical imaging research context.
Implement a function in scripts/evaluate.py called compute_dice_per_case that takes
a directory of prediction NIfTI files and a directory of ground truth NIfTI files,
computes the Dice score for each tumour subregion (whole tumour, tumour core, enhancing
tumour) for each case, and returns a pandas DataFrame with columns: patient_id, dice_wt,
dice_tc, dice_et. Do not modify any other functions in the file. Use NiBabel to load
the files.
```

---

## The Inspector

**What it does:** Reads data, code, or results and reports findings without making any changes.

**When to use:** Before any modeling step. Before trusting output. When you want to understand your starting point without risking changes to a working system. The Inspector is also the right role when you inherit someone else's code and need to understand it.

**Key requirement:** Tell Claude explicitly that it should not modify anything. Inspectors inspect; they do not intervene.

**Example prompt fragment:**

```
Act as a data analyst. Your task is to inspect the dataset, not to change anything.
Read the dataset at data/brats2021/train/ and report the following:
1. Total number of patient cases
2. Whether all four MRI modalities (T1, T1ce, T2, FLAIR) exist for each case
3. Volume dimensions (should be consistent across cases — flag any that are not)
4. Whether segmentation label files are present for each case
5. Any anomalies or missing files

Do not make any changes to the data or the directory structure. Produce a summary report.
```

---

## The Reviewer / Critic

**What it does:** Assesses output quality, identifies problems, and proposes improvements. Specifically focused on evaluating something that already exists.

**When to use:** After you have initial results. After Claude or you have written code that needs a second read. When you want a quality check before reporting results.

**Key requirement:** Give the Reviewer access to the specific artefact to review. A Reviewer without access to the output being reviewed cannot do its job.

**Example prompt fragment:**

```
Review the evaluation results in results/baseline_metrics.csv. For each patient case:
1. Identify the 10 worst-performing cases by Dice score for the whole tumour subregion
2. Describe any pattern in the failures — are they concentrated in particular cases,
   or distributed randomly?
3. Suggest three hypotheses for why the model performs poorly on these cases

Do not propose code changes yet. Focus on interpreting the data and generating hypotheses.
```

---

## The Planner

**What it does:** Proposes a step-by-step approach before any code is written.

**When to use:** Always, for any task of moderate complexity. The Planner role is the most underused and the most protective. A plan you can review is always safer than code that executes immediately.

**Key requirement:** Explicitly tell Claude to wait for your approval before writing or executing anything. The Planner's output is a plan, not code.

**Example prompt fragment:**

```
Before writing any code, describe in detail how you would implement patch-based training
for the U-Net model. Your description should:
1. List each step in order
2. For each step, specify which file it affects
3. For each step, specify what the expected output or change is
4. Flag any step where there is genuine uncertainty or where a design decision must be made

Do not write any code yet. Wait for my review and approval of this plan before proceeding.
```

---

## The Explainer

**What it does:** Translates technical output into plain language, oriented toward a specific audience.

**When to use:** To sanity-check results by forcing a plain-language description. When you need to communicate results to a clinical collaborator. When you are uncertain what a metric actually means in your context.

**Key requirement:** Specify the audience. "Explain this to a clinician" produces a different output than "explain this to a statistician" or "explain this to me as if I have not seen these results before."

**Example prompt fragment:**

```
Read the evaluation output in results/final_metrics.csv. Explain what these results
mean for a clinician who will decide whether this model is suitable for use in pre-
surgical planning. Avoid statistical jargon where possible. Focus on:
1. What the model can reliably detect
2. Where the model's errors are concentrated
3. What the clinical consequences of these errors might be
4. Whether you would recommend this model for clinical use based on these results alone
```

---

## The Devil's Advocate

**What it does:** Challenges your assumptions, identifies weaknesses in your claims, and presents the strongest objections to your conclusions.

**When to use:** Before declaring success. Before writing up results. When you feel confident — confidence is precisely when critical scrutiny is most valuable.

**Key requirement:** Ask for the strongest version of the objection, not a softened one. Weak devil's advocacy is not useful.

**Example prompt fragment:**

```
Take the role of a sceptical peer reviewer at a top medical imaging conference. I am
claiming that our U-Net model achieves clinically useful performance on the BraTS 2021
validation set. Based on the results in results/final_metrics.csv and the model
description in CLAUDE.md, argue against this claim. What are the three strongest
objections a rigorous reviewer would raise? Do not soften the objections.
```

---

## The Supervisor

**What it does:** Verifies that what was built matches what was specified. Reads implementation against requirements and reports deviations.

**When to use:** After major code changes. After a complex implementation to confirm that all requirements were met. When you want an independent check before running an expensive training job.

**Key requirement:** Provide both the specification and the implementation. The Supervisor compares the two.

**Example prompt fragment:**

```
Read scripts/train.py and confirm whether it implements all of the following requirements:
1. Patch-based training with patch size 128x128x128
2. Dice loss combined with cross-entropy loss (weighted 0.5 each)
3. 100 training epochs with early stopping based on validation Dice
4. Patient-level train/validation split (no patient appears in both sets)
5. Model checkpoints saved every 10 epochs

For each requirement, state whether it is implemented correctly, partially, or not at all.
If partially or not, quote the relevant code and explain the gap.
```

---

## Combining Roles

In practice, a complex task often moves through several roles in sequence. A disciplined workflow looks like:

1. **Inspector** — understand the data and current state
2. **Planner** — design the approach before any code is written
3. **Builder** — implement the approved plan
4. **Supervisor** — verify the implementation matches the plan
5. **Reviewer** — assess the results
6. **Devil's Advocate** — stress-test your conclusions before reporting them

You do not need all six for every task. A simple data inspection needs only the Inspector. A complex model change needs most of them. The judgment about which roles to use — and when — is part of the scientific discipline you are developing.
