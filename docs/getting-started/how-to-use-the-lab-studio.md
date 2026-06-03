# How to Use the Lab Studio

## The VS Code + Claude Code Environment

The Lab Studio is VS Code with the Claude Code extension, opened on the lab repository. It is not a web app, a notebook, or a browser-based IDE. It is a full local development environment where Claude Code can read and write files, run terminal commands, and execute Python scripts on your machine.

This matters because it means Claude Code has real agency in your project. When Claude writes a file, that file exists on your disk. When Claude runs a script, that script runs in your Python environment with your data. The outputs are real. The errors are real. The artifacts you produce are genuine files, not screenshots of text.

---

## What the Dashboard Shows

The course website (this site) is your mission dashboard. For each mission, the dashboard shows:

- **Objective** — The clinical question this mission addresses
- **Traditional bottleneck** — What this step looks like without agentic AI (slow, error-prone, manual)
- **Claude method** — How the agentic approach changes this step
- **Required artifact** — The exact file Claude must produce for this mission
- **Layer A, B, C prompts** — Ready-to-use prompts at different levels of specification
- **Inspection checklist** — What to verify in the artifact before proceeding
- **Optional exploration** — Extension exercises for students who finish early

The dashboard tells you what to do and what to look for. Claude Code does the work.

---

## How to Navigate Between Missions

Missions must be completed in order. Each mission depends on artifacts from the previous one. You cannot run the error analysis (Mission 3) without the baseline results (Mission 2). You cannot write the study design critique (Mission 5) without understanding the improvement results (Mission 4).

The navigation path is simple:

1. Read the current mission on the dashboard
2. Check that the required artifacts from the previous mission exist
3. Select the prompt layer you want to use (A, B, or C)
4. Run the prompt in Claude Code
5. Inspect the artifact against the inspection checklist
6. Mark the mission complete and proceed

If an artifact is missing or fails the inspection checklist, do not proceed. The inspection step is not optional — it is the scientific judgment step that validates your work before you build on it.

---

## What the `prompts/` Directory Contains

The lab repository includes a `prompts/` directory with pre-written prompt files for each mission. These are the same prompts shown on the dashboard but in plain text files you can open and edit in VS Code.

Structure:
```
prompts/
  preflight/
    layer_a.txt
  mission_01/
    layer_a.txt
    layer_b.txt
    layer_c.txt
  mission_02/
    ...
```

You can edit these files before pasting them into Claude Code. This is especially useful for Layer B and C prompts, where you are expected to add your own role assignment or refine the output contract. Editing the file in VS Code before pasting gives you a record of the exact prompt you used, which is good scientific practice.

---

## How to Inspect Artifacts

Every required artifact has a specified format. Here is what to check for the main artifact types:

**JSON files** (e.g., `baseline_results.json`, `preflight_report.json`):
- Open in VS Code and verify all required keys are present
- Check that numeric values are plausible (Dice scores between 0 and 1, not negative or above 1)
- Check that file paths referenced inside the JSON actually exist

**Markdown reports** (e.g., `data_inspection_report.md`, `error_analysis_report.md`):
- Open and read — not skim, read
- Verify that all required sections are present
- Check that statistics cited in the text match the data files
- Look for hedging language Claude may have added; ask whether that hedging is scientifically appropriate

**Figure files** (e.g., `failure_cases.png`):
- Open and look at them
- Verify that the figure shows what it claims to show
- Check axis labels, colour bars, and figure titles

The inspection step is where you exercise scientific judgment. Claude produces the artifact. You validate it.

---

## How Layer A, B, and C Prompts Differ

**Layer A** prompts are fully specified. They include:
- An explicit role assignment ("Act as a Data Steward...")
- A background context section explaining the project
- A detailed task description with no ambiguity
- An output contract specifying the exact file path, format, and required fields
- A validation step telling Claude what to check before finishing

Layer A prompts should work without modification. They are calibrated for the lab dataset and directory structure.

**Layer B** prompts omit the role assignment and leave the output contract partially specified. You add the role you think is most appropriate and complete the output format specification.

**Layer C** prompts describe the objective in one or two sentences and ask you to write the full prompt yourself. Use them as a test of what you have learned.

---

## When to Use Exploration vs Base Prompts

Use base prompts (Layer A or B) when:
- You are working through a mission for the first time
- You are under time pressure
- You want a reliable, reproducible artifact

Use exploration prompts (Layer C or custom prompts) when:
- You have completed the base mission and want to push further
- You want to test whether a different prompt produces a better or worse result
- You are developing a prompt you could use in your own research

The optional exploration exercises at the bottom of each mission page are designed for students who finish the base mission early. They introduce extensions that are clinically interesting but not required for the course grade.
