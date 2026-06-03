# Roles, Tools, and Skills

Directing Claude effectively in a research session requires understanding three distinct concepts: **roles** (how to frame Claude's reasoning), **tools** (what Claude can act on), and **skills** (reusable workflows that combine roles and tools to accomplish recurring research tasks). This page covers all three in the context of the lab missions.

---

## Roles

A role is an explicit framing that tells Claude what kind of thinking to do, what to prioritize, and what to omit. The same underlying information — your model's error maps, your metric files, your training script — produces systematically different outputs when presented to Claude under different roles.

Roles are not decorative. They constrain what Claude produces and make the output predictable. A developer role will produce code; a data inspector role will produce observations; a skeptical reviewer role will produce objections. If you do not specify a role, Claude will try to do all three simultaneously and produce a confused mixture.

---

### Developer

**What it does:** implements code from your specification.

**When to use in the lab:** Mission 2 (building the first detector), Mission 4 (implementing the single-change improvement), any time you need a specific, well-scoped implementation task executed.

**The constraint:** the developer role works only when your specification is complete. If you are unclear about what to implement, use the Data Inspector role first to establish what you are working with, then switch to Developer once you know what change to make.

```
You are implementing a data augmentation function.
Add random horizontal flipping to the DataLoader in scripts/dataloader.py.
Do not change any other file.
Set numpy seed to 42.
After implementing, print the shapes of 3 augmented batches to confirm it works.
Before writing any code, describe your plan in numbered steps and wait for my approval.
```

---

### Data Inspector

**What it does:** reads files, reports findings, takes no action.

**When to use in the lab:** at the start of any new mission, before making any changes to the pipeline. Mission 2 begins with data inspection before any training code is written. Mission 3 begins with reading the validation metrics before generating any figures.

**The constraint:** the data inspector role must be explicitly limited to observation. Without a "do not write training code" instruction, Claude will begin implementing solutions before you have established what the data actually contains.

```
Act as a data analyst. Do not write training code.
Read all files in data/sample/ and report:
- number of NIfTI files present
- dimensions and voxel spacing of the first case
- whether labels are present for every case
- any unusual values in the label files (e.g., values other than 0 and 1)
Do not take any other action.
```

---

### Visual Debugger

**What it does:** generates and interprets diagnostic figures.

**When to use in the lab:** Mission 3 (error analysis), any time you need to understand a failure pattern that is not visible in a scalar metric. Error maps, confusion maps, and overlay visualizations are the primary outputs.

**The constraint:** the observation step must precede the hypothesis step. The visual debugger role generates figures and describes what is visible. Only after you have reviewed the figures does the session move to hypothesis generation.

```
Create error maps for the 3 worst-performing validation cases.
For each case: show the MRI slice, ground truth mask, predicted mask,
and a colour-coded error map (green=TP, red=FP, blue=FN) in a 2x2 labelled panel.
Save each figure to outputs/figures/error_case_<rank>.png.
Then describe in plain language what you see in the worst case.
Do not propose any hypothesis yet. Only describe what you observe.
```

---

### Algorithm Engineer

**What it does:** runs controlled single-variable experiments.

**When to use in the lab:** Mission 4. This is the primary role for the improvement experiment. The algorithm engineer role enforces the most important constraint in Mission 4: exactly one change, with all other parameters held constant.

**The constraint:** the algorithm engineer role requires an explicit "one change only" instruction and an explicit list of what must not change. Without these, Claude will interpret "improve the model" as permission to change multiple things.

```
Make exactly one change to scripts/run_train.py:
add Dice loss to complement the existing BCE loss (weighted equally, 0.5 each).
Do not change: the model architecture, learning rate (0.001), batch size (4),
random seed (42), or data augmentation.
After training, compare the new Dice to the baseline (0.67 from val_metrics.json).
Save the comparison to outputs/metrics/model_swap_comparison.json.
```

---

### Skeptical Reviewer

**What it does:** stress-tests your claims, identifies weaknesses.

**When to use in the lab:** Mission 5 (study design critique). After completing a study plan or report, switch to the skeptical reviewer role to identify the weakest assumptions and the strongest objections before presenting the work.

**The constraint:** the skeptical reviewer role is adversarial by design. Claude in this role should not be asked to defend the current approach — only to attack it. If Claude produces a balanced "strengths and limitations" section rather than a pointed critique, redirect: "Focus only on the weaknesses. Do not describe strengths."

```
Act as a skeptical peer reviewer.
Read reports/challenge_plan.md and identify the three strongest objections
to the proposed study design. For each objection:
1. State the specific weakness
2. Explain why it threatens the validity of the proposed conclusions
3. Suggest a specific change that would address it
Do not describe strengths. Only critique.
```

---

### Clinical Translator

**What it does:** rewrites technical results for clinical audiences.

**When to use in the lab:** Mission 6. After generating technical results, switch to the clinical translator role to produce a plain-language summary suitable for a clinical collaborator who understands medicine but not machine learning.

**The constraint:** the clinical translator role requires an explicit vocabulary prohibition and an explicit honesty requirement. Without the vocabulary prohibition, Claude will use ML terminology. Without the honesty requirement, Claude will write a promotional summary rather than an accurate one.

```
Write a summary of our model results for a clinical radiologist who understands
MRI but not machine learning.
Do not use the words: epoch, loss function, tensor, batch, architecture, or weights.
State what the model can and cannot do in plain language.
Include at least 3 specific limitations.
Do not overstate what was demonstrated. If the model was evaluated on teaching data
only, say so explicitly.
```

---

## Tools

Tools are the actual capabilities Claude can act on in your project. In Claude Code, the relevant tools are:

**File reading.** Claude reads any file in the project directory by path. Reading is always safe — it does not modify the project. Use it liberally for inspection and verification.

**File writing.** Claude creates or overwrites files at paths you specify (or paths it selects if you do not specify). This is consequential: a file written to the wrong path may not be found by the autograder. Always specify exact paths in your prompts.

**Terminal command execution.** Claude can run shell commands — including Python scripts, pip installs, evaluation scripts, and git operations. This is the capability that makes training experiments possible in a single session. It is also the capability that requires the most careful supervision: a command Claude runs cannot be un-run.

**Python script execution.** Claude can invoke Python directly to compute metrics, generate figures, and inspect data files without writing a separate script. Useful for quick data inspection tasks.

**Git operations.** Claude can stage files, write commit messages, and commit to git. This creates a version-controlled record of what changed and when. The `CLAUDE.md` file governs which git operations Claude is permitted to perform.

The permissions governing each of these tools are set in `CLAUDE.md`. If you have not reviewed what permissions your project grants Claude, do so before your first session.

---

## Skills

A skill is a reusable prompt pattern — a template for a recurring research task that can be adapted to new problems by substituting the specific dataset, file paths, and research question. The value of a skill is that it encodes a validated workflow: you have used it before, you know what output to expect, and you know how to verify that it worked.

### MRI Data Inspection Skill

This skill is used at the start of any new dataset or mission to establish ground truth about what you are working with. It produces a structured report covering file count, dimensions, class distribution, and anomalies. It explicitly prohibits training code, ensuring Claude remains in observation mode. The output is a markdown report in `reports/data_inspection.md` and a JSON summary in `outputs/status/data_inspection.json`. Use this skill before writing any model code or making any training decisions.

### Segmentation Error Analysis Skill

This skill ranks all validation cases by Dice score, identifies the worst performers, generates four-panel error map figures, and produces a structured hypothesis report. It enforces the two-phase sequence (observation before hypothesis) that is the core scientific discipline of Mission 3. The output is two PNG figures and a markdown report. Use this skill whenever you need to understand where a model fails, not just how much it fails on average.

### Clinical Translation Memo Skill

This skill converts a technical result into a plain-language memo for a specified clinical audience. It requires audience definition (who reads this and what they know), vocabulary constraints (what terms are prohibited), a honesty declaration (what the model was and was not evaluated on), and a limitations section (minimum three items). The output is a markdown memo in `reports/clinical_memo.md`. Use this skill at the end of any mission to produce the clinical-facing summary required in Mission 6.

### Study Design Critique Skill

This skill reads a proposed study plan and produces an adversarial critique identifying the three weakest assumptions and suggesting specific changes. It is used in Mission 5 after completing the study plan, to simulate peer review before submission. The output is a structured critique in `reports/study_critique.md`. Use this skill for any research proposal before presenting it to a collaborator or supervisor.

---

## Subagents and MCP (Advanced Concepts)

These concepts are not required for the lab, but they are relevant to future research infrastructure.

**Subagents** are specialized AI agents delegated specific subtasks within a larger workflow. In an advanced clinical AI research pipeline, you might spawn one subagent to handle data quality checking on an incoming imaging batch while another handles model evaluation and a third handles report generation. Each subagent operates in its own context window with its own tools and its own task specification. The orchestrating system — another Claude instance or a workflow script — coordinates the results. This enables parallel, composable research workflows that scale beyond what a single linear session can accomplish.

**MCP (Model Context Protocol)** is Anthropic's standard for connecting Claude to external data sources and tools beyond the local file system. With MCP, Claude can connect to institutional imaging servers, clinical databases, research registries, and real-time analysis pipelines. This enables agentic workflows that span multiple systems — for example, a Claude agent that retrieves patient imaging from a PACS system, runs a segmentation model, stores the result in a research registry, and generates a radiologist-facing report, all within a single coordinated workflow.

Neither of these capabilities is implemented in this course. The lab operates on local files with a single Claude session. But understanding these concepts prepares you to design more sophisticated agentic research infrastructure in your own work after the course.

!!! note "Role switching mid-session"
    The roles described on this page are not mutually exclusive within a session — they are sequential. A productive Mission 3 session might move through: Data Inspector (read the metrics) → Visual Debugger (generate error maps) → Skeptical Reviewer (challenge the hypothesis). The key discipline is making each transition explicit in the prompt. See the Role Switching for Research page for the detailed protocol.

!!! tip "Naming the role in every prompt"
    Even if you are continuing a task from a previous prompt, begin each new prompt with the role declaration: "Act as a data inspector..." or "You are now an algorithm engineer..." This prevents role drift, which is the tendency for Claude's outputs to become a mixture of multiple roles when the role is not explicitly re-stated.
