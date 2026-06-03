# Claude Code Workflow Cheatsheet

> **For print:** File → Print → Save as PDF. This page is designed to fit on one side of A4 or US Letter at 90% scale.

---

## 1. The Lab Loop

```
Dashboard (check artifacts from last session)
    ↓
Prompt (assign role + task + output contract)
    ↓
Claude Code (executes, writes output, confirms)
    ↓
Artifact (JSON / MD / PNG in outputs/ folder)
    ↓
Dashboard (record result, update CLAUDE.md)
```

Never skip the dashboard steps. The artifact is not complete until it is recorded.

---

## 2. Starting a Session

1. Open a terminal in the lab repository root.
2. Run `claude` to start Claude Code.
3. Send a **context-setting first message** — do not start with a task. Example:

```
I am resuming lab work. My research question is [from CLAUDE.md].
Last session I completed Mission 2 and wrote results to outputs/m02_metrics.json.
Today I am working on Mission 3: failure analysis of the worst-performing case.
My data is at data/brats_sample/. Do not modify any files in data/.
```

4. Wait for Claude to acknowledge context before issuing any task.

---

## 3. Layer A / B / C Structure

| Layer | Name | What it contains | Who writes it |
|---|---|---|---|
| **A** | Research context | CLAUDE.md: question, data path, output conventions, constraints | You (once per mission block) |
| **B** | Session role | Role assignment + task description | You (once per task) |
| **C** | Output contract | Exact file path, format, key names, validation step | You (every task with a file output) |

Every effective prompt activates all three layers. Missing Layer A means Claude may not know where your data is. Missing Layer C means you cannot verify the output.

---

## 4. Output Contract Syntax

Use this exact template for any task that writes a file:

```
Write to outputs/[filename].[ext] with keys:
  {
    "key_name": type,          // e.g. "case_id": string
    "key_name": type,          // e.g. "dice_wt": float
    "key_name": type           // e.g. "failure_mode": string
  }
After writing, read the file back and confirm:
(a) all specified keys are present,
(b) no additional unexpected keys were added,
(c) the file is valid JSON / parseable Markdown.
```

---

## 5. Role Switchers

| Role | Trigger phrase | What Claude does |
|---|---|---|
| **Developer** | "Acting as a Python developer..." | Writes code, runs it, writes output file |
| **Data Inspector** | "Acting as a data analyst..." | Produces structured observations, no code |
| **Visual Debugger** | "Acting as a visualisation expert..." | Produces plots, annotated images, slice comparisons |
| **Algorithm Engineer** | "Acting as an ML engineer..." | Proposes and implements one algorithmic change |
| **Skeptical Reviewer** | "Acting as a rigorous peer reviewer..." | Finds flaws, does NOT propose solutions in same prompt |
| **Clinical Translator** | "Acting as a clinical AI consultant..." | Converts findings to plain language, flags jargon |
| **Devil's Advocate** | "Acting as devil's advocate..." | Challenges your hypothesis before you implement it |

Switch roles explicitly between tasks. Do not combine roles in a single prompt.

---

## 6. When to Start a Fresh Session

- You have completed a full mission and produced a final artifact.
- Claude has made three or more consecutive errors on the same task.
- The conversation context is more than approximately 60 messages.
- You are moving from a coding task to a reviewing task (switch, do not continue).
- CLAUDE.md has been updated with new constraints or a new research question.

When starting fresh: update CLAUDE.md first, then send a new context-setting first message.

---

## 7. Key Files

| File / Folder | Purpose |
|---|---|
| `CLAUDE.md` | Persistent research context, updated between missions |
| `prompts/` | Your prompt log — save every prompt that worked |
| `outputs/` | All Claude-generated artifacts (JSON, Markdown, PNG) |
| `reports/` | Human-edited summaries, translation briefs, study designs |
| `data/` | Read-only source data — never modified by Claude |
| `fallback_outputs/` | Pre-computed results for use if live computation fails |
