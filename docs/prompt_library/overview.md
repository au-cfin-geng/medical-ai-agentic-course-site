# Prompt Library

## What This Library Is

This is a curated collection of reusable prompt templates covering every stage of the brain tumour segmentation lab. Each template has been written to assign Claude a specific cognitive task — inspection, planning, critique, communication — rather than just asking it to "write some code."

Think of this library as the reagents shelf in a wet lab. You do not improvise a new buffer every time you run a gel. You use a proven recipe, adjust the parameters for your sample, and document what you changed. Prompts work the same way.

## Why Templates Help

**Reduce cognitive load.** During a two-day lab, your attention is better spent on the science than on phrasing the question. A template gives you a reliable starting point so you can focus on interpreting results.

**Encode best practices.** The templates in this library embed the lessons from the agentic research section — role assignment, constraint specification, output verification — so those practices are active even when you are moving fast.

**Ensure reproducibility.** A prompt is part of your experimental record. A vague prompt produces results that cannot be reproduced even by you. A template makes the prompt an artefact you can version, share, and report.

**Prevent common failures.** Each template documents the failure mode it was designed to prevent. Knowing why the template exists helps you adapt it correctly.

## The Core Philosophy

> A good prompt is a research protocol: specific, reproducible, and verifiable.

A protocol specifies who does the work (role), what they must do (objective), what constraints apply (limits, scope, assumptions), and what counts as a valid result (expected output and how to check it). Every template in this library follows that structure.

When you deviate from a template, do it deliberately and document the change — just as you would note a protocol modification in a lab notebook.

## How to Use the Templates

1. **Identify your stage.** Use the table below to find the right file.
2. **Select the template** that matches your immediate goal.
3. **Replace `[BRACKETS]`** with your specific values — file paths, metric names, case IDs, thresholds.
4. **Add project context** if you are starting a new session: paste the CLAUDE.md summary or state the mission number and current step.
5. **Paste into Claude Code** (terminal, not a chat window).
6. **Verify the output** before proceeding. Each template tells you what to check.

### What to Put in `[BRACKETS]`

| Placeholder | Replace With |
|---|---|
| `[PROJECT_ROOT]` | Absolute path, e.g. `/home/user/brats_lab` |
| `[MISSION_NUMBER]` | e.g. `Mission 2` |
| `[MODALITY]` | e.g. `T1ce`, `FLAIR` |
| `[METRIC]` | e.g. `Dice`, `HD95` |
| `[N]` | A specific number, e.g. `10`, `3` |
| `[THRESHOLD]` | A numeric threshold, e.g. `0.5` |
| `[CASE_ID]` | A specific patient or file ID |
| `[YOUR QUESTION]` | A specific scientific question you want investigated |

## Template Index

| Category | File | When to Use |
|---|---|---|
| Setup and Context | [setup_prompts.md](setup_prompts.md) | Start of every session, creating CLAUDE.md, verifying the environment |
| Data Inspection | [data_prompts.md](data_prompts.md) | Mission 1 — understanding the dataset before modelling |
| Visualisation | [visualisation_prompts.md](visualisation_prompts.md) | Any mission — generating plots to inspect data or results |
| Modeling | [modeling_prompts.md](modeling_prompts.md) | Mission 2 — planning and implementing the U-Net pipeline |
| Error Analysis | [error_analysis_prompts.md](error_analysis_prompts.md) | Mission 3 — understanding where the model fails and why |
| Reviewer and Critic | [reviewer_prompts.md](reviewer_prompts.md) | Any mission — checking code quality, results validity, scientific claims |
| Translation and Communication | [translation_prompts.md](translation_prompts.md) | Missions 5 and 6 — study design, clinical framing, regulatory context |
| Bonus and Advanced | [bonus_prompts.md](bonus_prompts.md) | When you want to go beyond the mission brief |

## A Note on Session Continuity

Claude Code does not remember previous sessions. At the start of each session, use the [context-setting template](setup_prompts.md#1-initial-context-setting-prompt) to re-establish your project state. Keep your `CLAUDE.md` file updated so this step takes under 60 seconds.
