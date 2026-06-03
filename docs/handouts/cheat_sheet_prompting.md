# Prompting Cheat Sheet

> **For print:** use browser Print → Save as PDF. Recommended: A4, portrait.

---

## The 10 Prompt Principles

1. **Assign a role first.** "Act as a data analyst" gives Claude a consistent cognitive stance before it reads the rest of the prompt.
2. **State the objective in one sentence.** If you cannot, your goal is not clear enough yet.
3. **Specify the output format.** Tell Claude whether you want a table, a code block, prose, bullet points, or a structured report.
4. **Add constraints.** What should Claude NOT do? What scope limits apply? ("Do not write code yet." "Maximum 200 words.")
5. **Provide just enough context.** Too little: Claude guesses. Too much: Claude buries the key instruction.
6. **Ask for a plan before code.** "Plan, then wait for approval" is more reliable than "implement this."
7. **End with a verification step.** "After writing, run the script and confirm it executes without error."
8. **One objective per prompt.** If the task has multiple parts, chain prompts rather than combining them.
9. **Name the failure you are preventing.** "Ensure that Dice is computed per-case, not batch-averaged" prevents a specific bug.
10. **Update the prompt when the output is wrong.** Rephrasing randomly is not debugging. Diagnose which principle was violated.

---

## Role Templates

| Role | Use Case | Prompt Starter |
|---|---|---|
| **Data Analyst** | Summarising, counting, describing data | "Act as a data analyst. Inspect the dataset at [path] and produce..." |
| **Planner** | Any implementation task — design before code | "Act as a Planner. Produce a step-by-step plan for [task]. Do not write any code yet." |
| **Implementer** | Writing code after a plan is approved | "Act as an Implementer. Based on the approved plan, write [file] that..." |
| **Inspector** | Finding patterns in failures or data | "Act as an Inspector. Examine [cases/results] and identify patterns in..." |
| **Critic / Devil's Advocate** | Challenging your conclusions | "Act as a Critic. Argue as forcefully as possible against the conclusion that..." |
| **Code Reviewer** | Checking correctness and reproducibility | "Act as a peer code reviewer. Review [file] for correctness, reproducibility, and medical imaging conventions." |
| **Tutor** | Building understanding, not just getting answers | "Act as a tutor. Teach me [concept] using a concrete example. Then ask me 3 questions to check my understanding." |
| **Regulatory Consultant** | Navigating FDA/CE pathways | "Act as a regulatory affairs consultant for SaMD. Assess the regulatory pathway for [device description]." |
| **Scientific Writer** | Producing or reviewing text for reports | "Act as a scientific writer. Write a methods section for [study]. Every claim must be supported by [evidence]." |
| **Results Auditor** | Sanity-checking outputs before conclusions | "Act as a results auditor. Check these metrics for internal consistency before I draw any conclusions." |

---

## Prompt Anatomy

A strong prompt has six parts:

```
[CONTEXT]
Who you are, what project this is, what has happened so far.

[ROLE]
What cognitive role Claude should adopt for this task.

[OBJECTIVE]
One clear sentence: what must Claude produce or do?

[CONSTRAINTS]
What Claude must NOT do. Scope limits. Format restrictions. Hard rules.

[EXPECTED OUTPUT]
Describe the output precisely: format, length, structure, file path if saving.

[VALIDATION]
How will you (or Claude) verify the output is correct?
```

---

## Bad vs Good Prompt Example

**Bad prompt:**

```
Write a training loop for my brain tumour model.
```

Problems: no context, no architecture details, no constraint on loss function, no logging specification, no file to write to, no verification step.

**Good prompt:**

```
Act as an Implementer.

Context: I have a verified UNet2D model (scripts/model.py, in_channels=4, num_classes=4)
and a working DataLoader (scripts/dataset.py). Hardware: CPU only. Dataset: BraTS 2020,
70 training cases, label convention 0/1/2/4.

Objective: Write a training loop in scripts/train.py.

Constraints:
- Use DiceCELoss (combined Dice + CrossEntropy)
- Remap BraTS label 4 → index 3 before loss computation, remap back after
- Do not use GPU-specific code
- Do not modify model.py or dataset.py

Expected output:
- scripts/train.py with argparse for: --epochs (default 50), --lr (default 1e-4),
  --batch_size (default 8), --output_dir (default results/)
- Logs epoch-level metrics to results/training_log.csv
- Saves best checkpoint to results/best_model.pt

Validation:
After writing, run: python scripts/train.py --epochs 2 --output_dir results/smoke_test/
Confirm: (1) no errors, (2) training_log.csv has 2 rows, (3) best_model.pt exists.
```

---

## Common Prompting Mistakes

| Mistake | What Happens | Fix |
|---|---|---|
| **No context** | Claude assumes a generic project; file paths and conventions are wrong | Provide project root, current mission, key file names |
| **No constraints** | Claude makes architectural or methodological choices you did not approve | State explicitly what Claude must NOT do |
| **Too much in one prompt** | Claude completes some parts well and ignores others | Break into sequential prompts; chain them |
| **Not verifying output** | A correct-looking but wrong result proceeds silently | End every prompt with a verification step |
| **Accepting without understanding** | You run code you cannot explain; debugging becomes impossible | Use the "Teach Me" prompt after any output you accept but do not understand |
| **Not updating CLAUDE.md** | Next session starts from scratch | Update CLAUDE.md at the end of every session |

---

## Quick Starters by Mission

| Mission | Suggested Opening |
|---|---|
| **M0: Wake the Lab** | "Act as a QA engineer. Verify my Python environment. Check that these packages are installed and working: [list]. Report PASS/FAIL for each." |
| **M1: Receive the Signal** | "Act as a data analyst. Inspect the dataset at [path]. Report: case count, label class frequencies, any missing modalities, any cases I should inspect manually." |
| **M2: Build the First Detector** | "Act as a Planner. Before any code, produce a step-by-step plan for implementing a 2D U-Net on BraTS data. Do not write code. Wait for my approval." |
| **M3: Investigate Failure** | "Act as an Inspector. Load the per-case metrics from [path]. Identify the 10 worst cases and find patterns that distinguish them from the 10 best cases." |
| **M4: Improve With Intent** | "Act as an Implementer. Based on the root cause identified in Mission 3 ([cause]), implement [specific change] in [file]. Do not change anything else." |
| **M5: Design the Next Study** | "Act as a clinical trials methodologist. Design a validation study for our brain tumour segmentation model. Research question: [question]. Calculate the required sample size." |
| **M6: Translate Responsibly** | "Act as a regulatory affairs consultant. Given our model's intended use ([use]), what is the most likely FDA device class and clearance pathway?" |
