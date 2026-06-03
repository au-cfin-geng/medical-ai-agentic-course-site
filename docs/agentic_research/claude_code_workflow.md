# Working with Claude Code

## Starting a Session

Claude Code runs in your terminal. Open a terminal, navigate to your project directory, and type `claude`. This launches an interactive session. Claude can now read files in that directory and its subdirectories, run shell commands, and write or modify files — all within the scope of your current working directory.

The first thing you should do in any session is give Claude orientation. Do not start with your task; start with context:

```
I am working on a brain tumour segmentation project using the BraTS 2021 dataset.
The project root is here. Key files: model/unet.py contains the model architecture,
scripts/train.py contains the training loop, scripts/evaluate.py contains evaluation
logic, and data/ contains the preprocessed NIfTI volumes. Today I want to implement
per-class Dice scoring in the evaluation script.
```

This takes thirty seconds to write and substantially improves what Claude does next. Without it, Claude is working blind.

## Why Context Matters at the Start

Claude has no memory between sessions. Every time you start a new `claude` session, it begins with no knowledge of your project, your previous conversations, or what was decided yesterday. If you spent an hour yesterday establishing that you want patient-level validation splits — not slice-level — Claude does not know that today. You have to re-establish it.

This is a fundamental property of how large language models work, not a bug that will be fixed. Build it into your workflow: every session starts with context-setting, every time.

## The CLAUDE.md File

There is a solution to the context problem that does not require you to retype everything each session: the `CLAUDE.md` file. Place a file called `CLAUDE.md` in your project root. Claude reads this file automatically at the start of each session.

What to put in it:

- **Project description**: what is this project, what is the clinical problem, what dataset are you using
- **Key file paths**: where are the main scripts, where is the data, where do results go
- **How to run the pipeline**: the exact command to run training, the exact command to run evaluation
- **What Claude should not do**: do not modify the model architecture, do not change the data split logic, do not edit requirements.txt
- **Expected outputs**: what does a successful run produce, where does the output go, what is the expected range for key metrics
- **Project-specific conventions**: naming conventions, file format expectations, any unusual design decisions

A good `CLAUDE.md` is three to five paragraphs of plain prose. It does not need to be exhaustive — just enough to orient a knowledgeable but uninformed assistant on the first day.

## The Interaction Loop

Working with Claude Code is a loop, not a single transaction:

1. **Write a prompt** — describe the task clearly, including context, objective, constraints, and expected output
2. **Observe what Claude does** — watch which files it reads, what commands it runs, what code it writes
3. **Verify the output** — read the code, run it yourself, check the results
4. **Accept, correct, or iterate** — if correct, move on; if not, provide specific feedback and ask for a revision

The verification step is where many students create problems for themselves by skipping it. A Claude output is not verified until you have checked it. "Claude said it worked" is not verification.

## What Verification Means in Practice

Verification is not abstract. After Claude writes or modifies a script, you should:

- **Read the code Claude wrote.** Not skim — read. Look at the logic. Does it match what you asked for? Are there sections that seem unusual?
- **Run the script yourself.** Do not just check that Claude ran it during the session; run it in your own terminal and confirm the output.
- **Check that output files exist and contain sensible values.** If Claude wrote an evaluation script, open the output CSV. Are the columns right? Are the values in the expected range? Are there missing values?
- **Sanity-check metrics.** A Dice score of 0.0 on all cases is wrong. A Dice score of 1.0 on all cases is also wrong. A loss that increases monotonically over training is wrong. You need to know enough about your domain to catch these.

## When to Trust Claude and When to Be Sceptical

Not all code carries the same risk. Some tasks are relatively safe to accept with light verification:

- Boilerplate code (argument parsers, file I/O, logging setup)
- Data format questions ("how do I read a NIfTI file with NiBabel?")
- Plotting and visualisation
- Standard preprocessing steps like intensity normalisation
- Utility functions for renaming files or organising directories

Be more sceptical — meaning verify more carefully — when Claude touches:

- **Core model logic.** If Claude modifies your U-Net architecture, read every change.
- **Loss functions.** Incorrect loss implementations are common and often not obvious from the output.
- **Metric calculations.** Dice, Hausdorff distance, sensitivity, specificity — these are often implemented incorrectly in subtle ways that produce plausible-looking numbers.
- **Data splits.** Patient-level versus slice-level splits matter clinically. Confirm Claude implemented what you specified.
- **Anything involving ground truth labels.** Errors here invalidate all downstream results.

## Common Mistakes Students Make

**Accepting the first output without checking.** Claude is fast. That speed creates a temptation to keep prompting and building without verifying intermediate steps. Resist this. A pipeline built on an unverified step will produce wrong results that are hard to trace.

**Not specifying constraints.** "Fix the evaluation script" is ambiguous. Claude may change the data loader, the metric definitions, and the output format simultaneously. Instead: "Only edit scripts/evaluate.py. Do not change any other files. The change should only affect how per-case metrics are aggregated."

**Starting with no context.** "Help me with my project" or "Can you fix the bug?" tells Claude nothing. Every prompt needs enough context to be actionable by someone who has never seen your project before.

**Continuing a session that has gone wrong.** If Claude has made incorrect changes, contradicted itself, or produced a series of errors, the session context is polluted. Start a new session. Summarise the problem cleanly. Do not try to salvage a session in which the ground truth of what has been established is unclear.

## How the Lab Uses Claude Code

Each lab mission has a defined set of objectives. Your job is to write prompts that accomplish those objectives using Claude Code. Claude writes and runs the code; you inspect the results that appear in the dashboard.

This is not a passive experience. You are not watching Claude perform tasks. You are directing it, verifying its outputs, identifying when it has gone wrong, and deciding when the objective has been genuinely met. The lab is designed to give you structured practice in exactly this skill — because it is the skill that transfers to your own research.
