# CLAUDE.md — Project Memory

`CLAUDE.md` is a markdown file at the root of your project repository that Claude Code reads at the start of every session. It is the most important file in your project for agentic research, and it is the one that students most commonly underestimate.

This page explains what `CLAUDE.md` does, what a good one contains, and what happens without one.

---

## The Problem It Solves

Claude Code has no memory between sessions. This is not a limitation that will be patched — it is a fundamental property of how large language models work. Each session begins with a blank context window. Nothing from your previous sessions — the code Claude wrote, the hypothesis you discussed, the metric value you reviewed, the constraint you corrected — persists unless it is encoded in a file that Claude can read.

Without `CLAUDE.md`, every session begins with the same question: what is this project and what have we done so far? You spend the first ten minutes of every session re-establishing context. Claude makes guesses based on the files it sees. Some guesses are right. Some are wrong. The session is built on an uncertain foundation.

With a good `CLAUDE.md`, the first session prompt can be: "Read CLAUDE.md, confirm you understand the project, and then proceed to Mission 4." Claude reads the file, has accurate context, and begins the task.

---

## What a Good CLAUDE.md Contains

A `CLAUDE.md` file for a clinical AI research project should contain the following sections.

**Project description.** One paragraph explaining what this project is and what it is trying to accomplish. Written for Claude, not for a human reviewer — assume Claude knows about brain tumour segmentation but does not know anything specific about this particular project, dataset, or research question.

Example:
```
This project develops a brain tumour segmentation model using a teaching subset
of MRI data. The research question is whether simple U-Net variants and standard
augmentation strategies can produce clinically informative segmentation masks
from limited training data. The project follows a structured sequence of missions,
each with specific artifact requirements.
```

**File map.** A list of the key directories and what they contain. Claude needs to know where to look for data, where to save outputs, and where the scripts live.

Example:
```
data/sample/         — Teaching dataset. NIfTI format. Do not modify.
scripts/             — Training and evaluation scripts.
outputs/metrics/     — JSON metric files. Required artifact location.
outputs/figures/     — PNG figures. Required artifact location.
outputs/status/      — Stage completion JSON files.
reports/             — Markdown reports. Required artifact location.
```

**What Claude should NOT do.** Explicit prohibitions that override Claude's default behaviour. Without these, Claude may edit files it was not asked to edit, use external libraries that are not approved, or delete files to "clean up."

Example:
```
MUST NOT:
- Modify any file in data/sample/
- Install packages not in requirements.txt
- Delete any file in outputs/ or reports/
- Change the random seed from 42
- Overwrite outputs/metrics/val_metrics.json (baseline, must be preserved)
```

**Required artifact paths.** The exact paths for every file that must exist for grading. This is the single most common cause of autograder failures — Claude saves a file at a reasonable-seeming path that is not the graded path.

Example:
```
REQUIRED ARTIFACTS (exact paths, case-sensitive):
outputs/metrics/val_metrics.json          — Mission 2 baseline evaluation
outputs/figures/error_analysis_worst.png  — Mission 3 error map
reports/error_analysis.md                 — Mission 3 hypothesis report
outputs/metrics/model_swap_comparison.json — Mission 4 improvement comparison
reports/challenge_plan.md                 — Mission 5 study design
reports/clinical_memo.md                  — Mission 6 translation memo
```

**Run commands.** How to execute the training script, evaluation script, and any other scripts Claude needs to run. Without this, Claude will try to infer the run command from the script contents, which sometimes produces the wrong invocation.

Example:
```
Training: python scripts/run_train.py --config configs/baseline.yaml
Evaluation: python scripts/evaluate.py --predictions outputs/predictions/ --labels data/sample/labels/
```

**Honesty requirements.** Explicit instructions about how Claude should handle uncertainty and what it must not do when generating reports.

Example:
```
HONESTY REQUIREMENTS:
- Do not report a metric value you have not read from an actual file.
- If a required output file does not exist, say so — do not generate a placeholder value.
- Do not use language that implies clinical validation when only teaching-data evaluation has been done.
- If the hypothesis was not supported, say so directly.
```

---

## A Simplified CLAUDE.md Template

This is a minimal template you can adapt for a new project. It is not the full lab `CLAUDE.md` — it is a starting structure.

```markdown
# Project: [Project Name]

## What This Is
[One paragraph: what you are building, what data you are using, what the
research question is]

## File Map
[Directory] — [What it contains and whether it can be modified]
...

## Do Not
- [Specific prohibition]
- [Specific prohibition]
...

## Required Outputs
[Exact file path] — [What it must contain]
...

## How to Run
Training: [exact command]
Evaluation: [exact command]

## Current State
Baseline Dice: [value, source file]
Current mission: [mission number]
Last completed artifact: [path]

## Honesty
If a file does not exist, say so. Do not fabricate metric values.
```

---

## How to Write Your Own CLAUDE.md for a Future Project

Start with one paragraph describing the project. Use the template above. Fill in the file map based on your actual directory structure. Fill in the prohibitions based on the mistakes you most want to prevent — if you know there are critical files that must not be edited, list them explicitly.

Update `CLAUDE.md` after every milestone. When you complete Mission 3 and have a confirmed baseline Dice and a confirmed failure hypothesis, add both to the "Current State" section of `CLAUDE.md`. The next session will start with that information already available.

Treat updating `CLAUDE.md` as part of completing each mission. It takes two minutes. It saves twenty minutes at the start of the next session.

---

## What Happens Without a CLAUDE.md

Consider the difference in Claude's first response under two conditions.

**Without CLAUDE.md:**

> "I can see you have a project with some Python scripts and a data directory. I'll start by exploring the directory structure to understand what you have. I see `scripts/`, `data/`, and `outputs/`. The data directory contains NIfTI files — are you working on medical imaging? I'll look at the scripts next. The training script uses PyTorch... What would you like to do today?"

Claude is exploring, guessing, and asking open-ended questions. It does not know what the project is, what has been done, or what the constraints are. This is not a reliable starting point for a research session.

**With a well-written CLAUDE.md:**

> "I've read CLAUDE.md. This is a brain tumour segmentation project using the teaching dataset in `data/sample/`. The baseline model from Mission 2 achieved Dice 0.42, recorded in `outputs/metrics/val_metrics.json`. Mission 3 is the error analysis phase — I should generate error map figures for the best and worst validation cases, save them to `outputs/figures/`, and write the hypothesis report to `reports/error_analysis.md`. I must not modify the baseline metric file or the data. The random seed is fixed at 42. Ready to proceed — would you like me to begin with the observation phase?"

Claude has correct project context, knows the current state, knows the constraints, and is ready to execute the task. The difference is entirely attributable to `CLAUDE.md`.

!!! tip "First thing to do in any new Claude Code session"
    Type: "Read CLAUDE.md and tell me in 2 sentences what this project is and what my role is." If Claude's answer is accurate, proceed. If Claude's answer is wrong or incomplete, correct it before giving any other instruction. A session built on wrong context produces wrong outputs.

!!! warning "CLAUDE.md must reflect reality"
    A `CLAUDE.md` that says the baseline Dice is 0.67 when the actual value in `val_metrics.json` is 0.42 is worse than no `CLAUDE.md` at all — it introduces a confident error. Keep `CLAUDE.md` updated and accurate. After each mission, update the "Current State" section to reflect what was actually accomplished.

!!! info "CLAUDE.md in your own research"
    For any project where you plan to use Claude Code across multiple sessions, create a `CLAUDE.md` at the start. The two minutes of writing pays back across every session. Think of it as the README that is also a standing instruction set for your AI research assistant.
