# Debugging with Claude

## The Diagnostic Mindset

Debugging is not just fixing errors — it is understanding why something went wrong. This distinction matters more when working with an AI agent than in traditional programming. Claude can fix many bugs efficiently, often faster than you could. But if Claude fixes the bug without you understanding the cause, you lose the opportunity to learn something about your system that may be essential when the next, related bug appears.

The goal in this lab is not to produce a working pipeline by any means available. It is to produce a working pipeline that you understand. Keep this in mind as you use Claude for debugging.

## When Claude's Output Is Wrong: Be Specific

The most common mistake students make when debugging with Claude is reporting the error vaguely. "It does not work" or "the results look wrong" gives Claude almost nothing to work with. Be specific about what is wrong, what you expected, and what evidence you have.

**Vague:**
```
The training script has an error. Can you fix it?
```

**Specific:**
```
The training script you wrote in the last step produces NaN loss after exactly 3
training steps. Here is the full traceback:

[paste full traceback here]

Before your changes, the training script ran successfully to completion with a final
loss of 0.34. The only change you made was in the data loader's normalisation function.
What did you change there that might cause NaN loss to appear after 3 steps?
```

The second version gives Claude a timeline (worked before, fails after your changes), a specific symptom (NaN after step 3, not random), a candidate cause (normalisation function), and access to the exact error. This is enough to diagnose most bugs.

## Always Paste the Full Traceback

When an error occurs, paste the complete traceback into your prompt — not just the last line. The last line tells you the type of error. The traceback tells you where in the call stack the error occurred, which is usually where the real problem is.

Include:
- The exact command you ran (`python scripts/train.py --config config/baseline.yaml`)
- The complete output from that command, including warnings before the error
- The full traceback, from the first "Traceback (most recent call last)" to the final error line
- Your Python and CUDA versions if the error might be environment-dependent

## Hypothesis-Driven Debugging

Research training gives you a useful habit: form a hypothesis before running the experiment. Apply the same approach to debugging. Before asking Claude to find the bug, form your own hypothesis about where it is and why.

This is not just good practice — it produces better prompts:

```
I think the NaN loss is caused by the normalisation step in the data loader, because:
1. The NaN appears after step 3, which is when a new batch is loaded
2. This dataset has some slices with very low intensity values (near zero) that could
   cause division by zero if we normalise by mean intensity

Please read scripts/dataloader.py and specifically check the normalisation function
for any division operation that could produce infinity or NaN when the input intensity
is near zero. Confirm or refute my hypothesis, and if confirmed, propose a fix.
```

Even if your hypothesis is wrong, framing the question this way gives Claude a structured starting point. And if Claude refutes your hypothesis, it must explain why — which teaches you something.

## When to Stop Prompting and Start Fresh

There is a point in some sessions when continuing in the same session becomes counterproductive. Signs that you have reached this point:

- Claude gives contradictory answers to the same question
- Claude proposes changes that clearly reverse something it did earlier
- You have lost track of what state the code is in because of multiple edits
- Claude confidently describes code that does not match what is in the file
- The error messages are changing in ways that suggest multiple overlapping problems

When you reach this point, start a new session. Write a clean summary of the problem:

```
New session. Starting from a clean state.

I am working on brain tumour segmentation using the BraTS 2021 dataset. The project
structure is: [brief description].

Here is the specific problem I am trying to solve: [precise description of the bug,
the error, the symptom].

Here is the relevant code: [paste the relevant function or file].

Here is the full error message: [paste].

Please diagnose the problem and propose a fix. Do not make any changes yet.
```

A fresh session with a clear problem statement will outperform a polluted session with lost context almost every time.

## Common Debugging Scenarios in the Lab

These are the most frequent problems students encounter in the lab missions, with guidance on how to approach each.

**CUDA out of memory error**

Symptom: `RuntimeError: CUDA out of memory. Tried to allocate X GiB`

Common causes in 3D medical imaging: batch size too large, patches too large, model too wide for the available VRAM. Less common but worth checking: gradients accumulated over too many steps, tensors not freed between validation steps.

Debugging approach: ask Claude to read your training loop and identify where large tensors are held in memory during validation. Specifically check whether `torch.no_grad()` is used correctly during validation and whether tensors are being moved back to CPU after validation.

**NaN loss after a few steps**

Symptom: loss is finite for 2-3 steps, then becomes NaN and stays NaN.

Common causes: learning rate too high (gradient explosion); normalisation producing division by zero; labels containing values outside the expected class range; loss function receiving invalid input (e.g., log of zero in cross-entropy with softmax values that underflow).

Debugging approach: add gradient norm logging and learning rate logging to confirm they are in expected ranges. Ask Claude to read the data loader's normalisation code specifically for division operations.

**Dice score of 0.0 on validation, high on training**

Symptom: training Dice improves normally, validation Dice stays at or near zero.

Common causes: evaluation threshold too high (segmentation map all background); wrong activation function at output (sigmoid instead of softmax for multi-class, or missing any activation); data split implemented at slice level rather than patient level, with easy patients in training and hard patients in validation.

Debugging approach: ask Claude to read the evaluation script and confirm what activation function is applied at inference and what threshold is used to convert probabilities to binary masks.

**Empty or near-zero segmentation output**

Symptom: the model outputs a segmentation mask that is almost entirely background for every case.

Common causes: threshold too high; model not converged (all predictions pushed toward majority class by class imbalance); inference-time preprocessing different from training-time preprocessing.

Debugging approach: ask Claude to print the raw output probability distribution for one validation case — specifically, what is the maximum predicted probability for each foreground class? If max probabilities are very low (below 0.5), the model is uncertain everywhere, suggesting a convergence problem, not an evaluation bug.

## The Understanding Requirement

The distinction that matters: asking Claude to diagnose and fix a bug is legitimate and efficient. Accepting the fix without understanding what was wrong is a liability.

If Claude tells you the bug was a missing `dim=-1` argument in a softmax call, understand why that argument matters. If Claude tells you the class weights were not normalised, understand what unnormalised weights do to the loss landscape. These are not trivia — they are the knowledge that will help you recognise similar problems in your own research, where Claude may not be available or may give you a wrong diagnosis.

Use Claude to accelerate debugging. Use your own thinking to understand the bugs.
