# Mission 0 — Wake the Lab

Orient Claude Code to your project context and verify that the end-to-end pipeline is operational before any analysis begins.

---

## Why This Matters Clinically

A research environment that cannot be verified cannot produce trustworthy results. In clinical AI, the credibility of every downstream finding — every Dice score, every failure analysis, every translation recommendation — depends on the integrity of the pipeline that produced it. Before any patient data is analysed, a clinical AI team confirms that the environment is operational, the output directories are writable, and the package versions are known and recorded. This mission trains that discipline from the first prompt.

---

## Traditional Bottleneck

Without an explicit orientation step, students begin working in an environment whose state is unknown. Hidden dependency conflicts, unverified directory structures, and implicit assumptions about what "ready" means create a diffuse failure mode: problems appear later, in the wrong place, with misleading symptoms. A student whose output directory does not exist will receive a cryptic file-not-found error in Mission 2 rather than a clean "directory missing" error in Mission 0. Environment chaos costs time at the worst possible moment — when something scientifically interesting is happening and a debugging detour destroys the learning arc.

---

## Claude / Agentic Method

This mission introduces two foundational agentic habits that will persist for the entire course. First, **CLAUDE.md as project memory**: Claude reads the project context file before taking any action, so that its behaviour is shaped by the specific research environment rather than generic defaults. You will observe how Claude's responses differ when given project context versus a cold-start prompt. Second, **explicit output contracts**: the prompt specifies exact file paths, exact JSON keys, and exact content requirements before any code is written. This makes the result machine-checkable — you do not need to read the output carefully to know whether Mission 0 succeeded; you run a check against the specified schema.

---

## Anthropic Academy / Claude Reading Connection

!!! info "Academy Alignment — Disclaimer"
    The Anthropic Academy modules listed here are independent courses created by Anthropic. This course is not affiliated with Anthropic, and the connections described below are the course author's interpretation of how those public resources relate to the skills practiced in this lab. Always consult the original Academy content directly.

    Relevant modules:

    - **Claude Code 101** — introduces Claude Code as an agentic coding assistant: how to start a session, give context, and inspect outputs. Mission 0 is a direct application of the session-startup workflow demonstrated in this module.
    - **Introduction to Claude Cowork** — explains using Claude as a collaborative research partner rather than a one-shot query tool. The CLAUDE.md orientation habit practiced here is the foundation of that collaboration model.
    - **Claude Code in Action** — demonstrates Claude performing file and environment operations in a real project context. The env_check.md and status JSON produced in this mission follow the pattern shown there.

---

## Prompt Pattern Practiced

**Explicit task + expected output + exact file paths**

Specify what Claude must do (check the environment), what Claude must produce (two output files), and exactly where to write them (full relative paths from the project root) — all in a single prompt before any code is written. This removes ambiguity about what "done" means and makes the result verifiable by inspection rather than trust.

---

## What You Will Build

By the end of Mission 0, the project record will contain:

- **`reports/env_check.md`** — a human-readable environment report describing the Python version, platform, and package status for this specific machine. Must describe your machine, not a template.
- **`outputs/status/stage_00_bootstrap.json`** — a machine-readable JSON status file with at minimum the keys `status`, `python_version`, and `platform`.
- The output directories `outputs/status/` and `reports/` must exist and be confirmed writable by Claude.
- A completed CLAUDE.md reading — Claude's response should reference specific content from the project context file, demonstrating that it read and processed the context rather than ignoring it.

---

## What to Do in the Lab Studio

1. Open the course dashboard and navigate to the **Mission 0** tab.
2. Copy the Layer A prompt from `prompts/stage_00_bootstrap.md` in the student classroom repo.
3. Paste the prompt into Claude Code in your terminal (`claude` from the project root).
4. Before approving any file writes, read Claude's plan: does it mention CLAUDE.md? Does it list the correct output paths?
5. Approve the plan and let Claude run the environment checks.
6. When Claude finishes, open `reports/env_check.md` in a text editor.
7. Open `outputs/status/stage_00_bootstrap.json` in a text editor.
8. Return to the dashboard and mark Mission 0 complete if both files exist and describe your actual machine.

---

## Expected Artifact

| Filename | Content | How to know it is correct |
|---|---|---|
| `reports/env_check.md` | Python version, platform string, list of package versions checked | Version numbers match what `python --version` and `pip show` report on your machine |
| `outputs/status/stage_00_bootstrap.json` | `{"status": "ok", "python_version": "...", "platform": "..."}` | `status` is `"ok"`, `python_version` is a real version string, `platform` names your operating system |

---

## How to Inspect the Result

1. Open `reports/env_check.md`. Does it name a Python version that matches your machine? Does it list the packages you know are installed? If you see generic placeholder text like "Python version: X.Y.Z", Claude did not run the check — it templated the output.
2. Open `outputs/status/stage_00_bootstrap.json`. Is `status` the string `"ok"` (not `"true"`, not `null`, not `"unknown"`)? Does `python_version` contain a real version string from your interpreter?
3. Check that both `reports/` and `outputs/status/` directories exist. Run `ls reports/` and `ls outputs/status/` in your terminal to confirm.
4. Read Claude's session output. Did Claude quote something specific from CLAUDE.md? If Claude's response contains no reference to the project context, it did not read CLAUDE.md — give it the prompt again with an explicit instruction to read the context file first.

---

## Reflection Question

What does CLAUDE.md tell Claude that changes how it responds compared to a cold-start prompt with no context? Think about which specific pieces of information in your project's CLAUDE.md are load-bearing for Mission 0's result — and which would matter more in later missions.

---

## Extension Challenge

Add hardware context to `env_check.md` using the Layer C prompt: GPU availability (with VRAM if present), total RAM in GB, and available disk space in the project directory. Note that GPU detection via PyTorch is environment-dependent; if the check returns `No GPU detected` on your machine, that is a correct and honest result — do not ask Claude to fake a different answer.

---

## Transfer to Your Own Research

What would you put in a CLAUDE.md for your own PhD project? Identify three things Claude needs to know to be useful in your specific research context: the structure of your data, the vocabulary of your domain, and the output conventions you expect. Draft the first three lines of a CLAUDE.md for your own project.
