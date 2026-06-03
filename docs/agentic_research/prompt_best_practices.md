# Prompt Best Practices

## Ten Principles with Examples

These principles apply to any substantive interaction with Claude Code in a research context. Each one addresses a common failure mode observed in AI-assisted research workflows. For each principle, a before/after example shows the difference in practice.

---

### Principle 1: Give Context First

Before stating your task, tell Claude what project you are in, what the overall goal is, and what you have already done. Claude has no memory between sessions and no access to your intentions. Every prompt that omits context forces Claude to guess.

**Before:**
```
Fix the evaluation script.
```

**After:**
```
I am working on a brain tumour segmentation project using BraTS 2021. The evaluation
script is at scripts/evaluate.py. It currently computes a single Dice score averaged
across all cases. I want to change it to compute per-case Dice scores and save them
to results/per_case_metrics.csv. Fix the evaluate.py script to implement this.
```

---

### Principle 2: Define the Role

Explicitly assign Claude a role appropriate to the task. This shapes the mode of thinking Claude applies and helps you clarify what kind of output you actually need.

**Before:**
```
Look at my model and tell me if it is good.
```

**After:**
```
Act as a code reviewer with expertise in medical image segmentation. Read model/unet.py
and evaluate whether the architecture is appropriate for 3D brain tumour segmentation.
Identify any implementation choices that seem unusual or potentially problematic. Do not
make any changes — produce a written assessment only.
```

---

### Principle 3: State the Objective Specifically

Vague objectives produce arbitrary outputs. State exactly what Claude should produce, to what level of detail, and in what form.

**Before:**
```
Calculate the Dice score.
```

**After:**
```
Calculate the per-case Dice score for all 50 validation cases across the three BraTS
subregions: whole tumour (WT), tumour core (TC), and enhancing tumour (ET). Save
the results to results/per_case_metrics.csv with the following columns:
patient_id, dice_wt, dice_tc, dice_et. Also print the mean and standard deviation
for each subregion to the console.
```

---

### Principle 4: Constrain File Edits

If you do not specify which files Claude may change, it may change files you did not intend. Unrequested edits in adjacent files can introduce bugs that are hard to trace.

**Before:**
```
Add class weighting to handle the class imbalance.
```

**After:**
```
Add class weighting to handle class imbalance. Only edit scripts/train.py. Do not
modify scripts/dataloader.py, model/unet.py, or any other file. The class weights
should be defined as a parameter at the top of the training function, not hardcoded
in the loss call.
```

---

### Principle 5: Specify Expected Output Format

Claude will choose an output format if you do not specify one. The chosen format may not be compatible with your downstream pipeline.

**Before:**
```
Summarise the evaluation results.
```

**After:**
```
Produce a CSV file saved to results/summary_metrics.csv with the following columns:
metric, mean, std, min, max. Rows should correspond to: dice_wt, dice_tc, dice_et,
hd95_wt, hd95_tc, hd95_et. Values should be rounded to four decimal places. Also
print the CSV to the console so I can verify it.
```

---

### Principle 6: Ask for a Plan First

For any task involving multiple files or significant logic changes, ask Claude to describe its approach before writing any code. A plan you can review is safer than code that executes immediately.

**Before:**
```
Implement patch-based training in the training script.
```

**After:**
```
Before writing any code, describe in steps how you would implement patch-based training
in scripts/train.py. For each step, specify what change is required, which file is
affected, and what the expected outcome of that change is. Identify any design
decisions I need to make before implementation begins. Wait for my approval before
making any changes.
```

---

### Principle 7: Require Validation

Ask Claude to verify its own output before presenting it to you. This catches obvious errors before you spend time reviewing code that does not even run.

**Before:**
```
Write the evaluation script.
```

**After:**
```
Write the evaluation script in scripts/evaluate.py. After writing it, run it on the
first 5 validation cases and print the per-case Dice scores. Verify that the scores
are in the range 0.0 to 1.0 and that no cases have a score of exactly 0.0 or 1.0,
which would suggest an implementation error. Report what you find before I review
the full output.
```

---

### Principle 8: Ask Claude to Inspect Artefacts

After generating output files, ask Claude to open and inspect them. This catches formatting errors, empty outputs, and implausible values before you discover them later.

**Before:**
```
Generate the results CSV and we are done.
```

**After:**
```
After writing the evaluation script and running it, open the output CSV file at
results/per_case_metrics.csv. Print the first 10 rows and the shape of the DataFrame.
Confirm that the patient_id column contains valid BraTS IDs, that the Dice columns
contain values between 0 and 1, and that there are no NaN or missing values. Report
your findings.
```

---

### Principle 9: Separate Building from Checking

Do not ask Claude to implement something and verify it in a single prompt. Separation gives you a natural review point and makes it easier to identify where things went wrong.

**Before:**
```
Implement the Dice loss function and check that it works correctly.
```

**After — Prompt 1 (Build):**
```
Implement a Dice loss function for multi-class segmentation in model/losses.py.
The function should accept softmax predictions and one-hot encoded labels, both
as PyTorch tensors of shape (B, C, H, W, D). Return a scalar loss value. Do not
implement any other functions. Do not run it yet.
```

**After — Prompt 2 (Check, sent after reviewing the code):**
```
Now test the Dice loss function you just wrote. Create a small synthetic test:
predictions and labels of shape (2, 4, 32, 32, 32), with labels being one-hot
encoded. Run two cases: (1) perfect predictions (loss should be 0), and (2)
predictions and labels completely mismatched (loss should be 1). Report whether
the function produces the expected values in each case.
```

---

### Principle 10: Iterate Based on Evidence

When results are wrong, describe the evidence precisely. Do not just say "it did not work." State what the current metric is, what you expected, and ask for hypotheses ordered by likelihood.

**Before:**
```
The Dice score is bad. Can you fix it?
```

**After:**
```
The validation Dice score for the whole tumour class is 0.45. For this architecture
on BraTS 2021, we would expect approximately 0.80-0.85. The training loss decreases
normally over 100 epochs, reaching 0.21 by epoch 100. However, the validation Dice
does not improve beyond 0.45 after epoch 20. This pattern suggests either (a) a
data leakage issue where the validation cases are too similar to training cases, or
(b) overfitting. Please examine scripts/train.py and specifically the patient-level
split logic. List possible causes of this behaviour in order of likelihood, with your
reasoning for each.
```

---

## Quick Reference Summary

| Principle | One-line summary |
|---|---|
| 1. Context first | Tell Claude the project, the state, and the goal before stating the task |
| 2. Define the role | Name the type of thinking you need: Builder, Inspector, Reviewer, Planner |
| 3. Specific objective | State the exact deliverable, not the general direction |
| 4. Constrain edits | Name which files Claude may and may not change |
| 5. Output format | Specify file name, columns, structure, and precision |
| 6. Plan before code | Ask for a step-by-step plan and approve it before implementation |
| 7. Require validation | Ask Claude to verify its output against expected ranges |
| 8. Inspect artefacts | Ask Claude to open and read the output files after generating them |
| 9. Separate build/check | Use two prompts: one to build, one to verify |
| 10. Evidence-based iteration | When results are wrong, describe the evidence and ask for ordered hypotheses |

These are not rules to follow mechanically. They are habits that reduce the frequency of wasted work. With practice, they become the natural structure of how you communicate with an AI coding agent.
