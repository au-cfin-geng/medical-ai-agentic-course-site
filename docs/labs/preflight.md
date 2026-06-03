# Preflight — Set Up Your Agentic Research Workstation

Before any experiment begins, the laboratory must be verified. This page is your pre-flight checklist for the agentic research environment you will use throughout this course.

---

## Why This Matters Clinically

Reproducible science starts with a reproducible environment. In clinical AI research, a result that cannot be reproduced is a result that cannot be trusted. If your Python version, library versions, or file paths differ between machines — or between runs on the same machine — your model's behaviour may change in ways you cannot explain or defend.

In clinical AI workflows, environment configuration is treated as an experimental variable, not an administrative afterthought. This preflight exercise trains that habit from the first minute of the course.

---

## Traditional Bottleneck

In traditional workshop settings, environment setup is assigned as homework before day one, or handed to students as a README with twenty steps and no verification mechanism. The result: on day one, a significant fraction of students discover silently broken environments at the moment they are supposed to be learning something else. Students reach Mission 3 before discovering that their data path was wrong all along. These failures are not the student's fault — they are the result of a setup process that does not verify itself.

---

## Claude / Agentic Method

In this course, you use Claude Code as your setup assistant. Instead of following a twenty-step README and hoping each step worked, you give Claude a single natural-language prompt that instructs it to perform a comprehensive environment check and write the results to a structured output file.

Claude Code can run Python version and package checks, verify that required directories exist and are writable, confirm compute availability, write a structured JSON file with every check result, and write a human-readable report summarizing the verification. You then inspect the output files. If any check fails, you know before you reach Mission 0.

The key habit being practiced: do not trust that something works until you have verified output that proves it works.

---

## Anthropic Academy / Claude Reading Connection

> **Disclaimer:** The Anthropic Academy modules listed here are independent courses created by Anthropic. This course is not affiliated with Anthropic, and the connections described below are the course author's interpretation of how those public resources relate to the skills practiced in this lab. Always consult the original Academy content directly.

Relevant modules:
- **Claude Code 101** — introduces Claude Code as an agentic coding assistant and explains how to start a session, give context, and inspect outputs.
- **Introduction to Claude Cowork** — covers using Claude as a collaborative research partner rather than a one-shot query tool.

---

## Prompt Pattern Practiced

**Explicit checklist + explicit output file + honest failure reporting**

Three components:
1. **Explicit checklist:** enumerate every check in the prompt itself. Claude cannot guess what "ready" means for your project; you must define it.
2. **Explicit output file:** specify the exact file path and key names for the output JSON to prevent Claude from writing to an unexpected location or inventing its own schema.
3. **Honest failure reporting:** instruct Claude to write `false` or a specific error message for any check that fails, rather than silently skipping failed checks.

Example prompt structure:
```
Read CLAUDE.md first. Then perform the following environment checks:
1. Python version (must be 3.10 or higher)
2. Required packages: torch, monai, nibabel, matplotlib, numpy
3. Directory outputs/status/ must exist and be writable
4. Directory data/ must exist
Write results to outputs/status/preflight_complete.json with keys:
  python_ok: bool, packages_ok: bool, outputs_writable: bool, data_dir_exists: bool
If any check fails, write false and include a "failures" key listing what failed.
Also write a summary to reports/preflight_report.md.
Do not write placeholder values. Only write what was actually verified.
```

---

## What You Will Build

By the end of this preflight exercise, you will have created two verified artifacts:

1. **`outputs/status/preflight_complete.json`** — a machine-readable JSON file with boolean values for each environment check. Every key must reflect the actual state of the environment.

2. **`reports/preflight_report.md`** — a human-readable markdown report summarizing what was checked, what passed, what failed, and any remediation steps Claude recommends.

---

## What to Do in the Lab Studio

1. Open your terminal and navigate to the course repository root.
2. Start a Claude Code session: `claude`
3. Give Claude the preflight prompt (use the pattern above or the one in your lab repo's CLAUDE.md).
4. Watch Claude run the checks. Read what it outputs to the terminal.
5. When Claude finishes, open `outputs/status/preflight_complete.json` in a text editor.
6. Open `reports/preflight_report.md`.
7. If any value is `false`, follow Claude's remediation instructions or ask Claude a follow-up question.
8. Do not proceed to Mission 0 until all required checks show `true`.

---

## Expected Artifact

`outputs/status/preflight_complete.json` with structure similar to:

```json
{
  "python_ok": true,
  "python_version": "3.11.4",
  "packages_ok": true,
  "packages_checked": ["torch", "monai", "nibabel", "matplotlib", "numpy"],
  "outputs_writable": true,
  "data_dir_exists": true,
  "failures": []
}
```

`reports/preflight_report.md` with a human-readable summary of each check result and the date/time of verification.

---

## How to Inspect the Result

Open `outputs/status/preflight_complete.json` and verify:
- Every boolean value is `true` or `false`, not a string like `"true"` or `"unknown"`.
- The `python_version` field contains a real version string from your machine, not a placeholder.
- The `failures` array is empty if all checks passed.

If you see a value like `"check_not_run"` or `null` for any key, Claude did not actually run that check. Ask Claude to redo the check and write the real result.

---

## Reflection Question

What would have gone wrong if you had started Mission 0 without running this verification?

Think specifically: which of the checks you just ran would have been the first to cause a visible failure? At what point in the lab would you have discovered it? How much time would you have spent debugging something that could have been caught in 30 seconds?

---

## Extension Challenge

Extend the preflight to check for disk space availability. Add a check that verifies at least 2 GB of free space in the project directory. Write the available space in GB to the JSON output under a key called `disk_space_gb`. What prompt would you write to add this check without rewriting the entire preflight from scratch?

---

## Transfer to Your Own Research

For your own PhD research environment, write a preflight checklist from scratch. Consider:
- What Python packages does your project require?
- What data directories must exist before any analysis can run?
- What compute resources (GPU memory, CPU count) does your pipeline assume?
- What external tools must be installed and on the PATH?

Draft a prompt you could give Claude Code at the start of every new project or every new collaborator onboarding session.
