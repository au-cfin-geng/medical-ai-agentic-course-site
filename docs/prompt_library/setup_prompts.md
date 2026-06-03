# Setup and Context Prompts

These templates belong at the very beginning of your work. Use them before touching any code or data. A session without proper context-setting is the single most common cause of Claude producing plausible-looking but wrong outputs.

---

## 1. Initial Context-Setting Prompt

**When to use:** At the start of EVERY Claude Code session, before issuing any other instruction.

**Why it works:** Claude Code has no memory between sessions. This prompt re-establishes the project state, your current position in the workflow, and the constraints you care about — all in one step. It assigns Claude the role of a careful collaborator who must understand the situation before acting.

**Failure it prevents:** Claude making assumptions about file paths, data formats, or mission goals that were established in a previous session but are now lost. This is the most common cause of confidently wrong outputs.

**Customisation:** Update `[CURRENT_MISSION]`, `[LAST_COMPLETED_STEP]`, and `[NEXT_GOAL]` every time you start a session. If you have already created a `CLAUDE.md`, replace the manual summary with "Read my CLAUDE.md file first."

```
You are a research assistant helping me work through a brain tumour segmentation lab.

Project location: [PROJECT_ROOT]
Current mission: [CURRENT_MISSION]
Last completed step: [LAST_COMPLETED_STEP]
Next goal: [NEXT_GOAL]

Key constraints:
- We are using PyTorch on a CPU-only machine (no CUDA unless I confirm otherwise)
- The dataset is BraTS-format NIfTI files, 4 modalities per case
- Do not modify any file in the data/ directory
- All outputs (plots, metrics, checkpoints) go to results/

Before doing anything, please:
1. List the contents of [PROJECT_ROOT] so we both know what is there
2. Confirm you understand the current mission and next goal
3. State one assumption you are making that I should verify

Do not write any code yet.
```

---

## 2. CLAUDE.md Generation Prompt

**When to use:** Once at the start of Mission 0, after your environment is verified and working.

**Why it works:** Asking Claude to generate the `CLAUDE.md` from an actual inspection of the project means the file reflects reality rather than intention. The verification step forces Claude to check that the commands it writes actually run.

**Failure it prevents:** A `CLAUDE.md` that contains wrong paths, wrong commands, or aspirational content that does not match the codebase.

**Customisation:** Add any project-specific "do not touch" directories, custom environment variables, or known working commands before the final instruction.

```
I need you to create a CLAUDE.md file for this project. This file will be read at the start of every future session to restore context quickly.

Please do the following in order:
1. Inspect the directory structure at [PROJECT_ROOT] (list all files and directories, two levels deep)
2. Read the main Python scripts in scripts/ and note what each one does
3. Check requirements.txt (or environment.yml) and note the key dependencies
4. Try running: python scripts/check_env.py and capture the output
5. Identify the three most important files a new collaborator needs to know about

Then generate a CLAUDE.md with these sections:
- ## Project Summary (2-3 sentences, what this project does)
- ## File Map (annotated tree of key files)
- ## How to Run (working commands for: check environment, load data, train model, evaluate)
- ## Data (format, location, do-not-modify policy)
- ## Current Status (what has been completed, what is next)
- ## Do Not Touch (files/directories Claude must never modify)

Write the CLAUDE.md to [PROJECT_ROOT]/CLAUDE.md.
After writing it, read it back and confirm every command in "How to Run" is syntactically correct.
```

---

## 3. Environment Verification Prompt

**When to use:** Mission 0, before writing any code, and any time you suspect a dependency issue.

**Why it works:** This prompt instructs Claude to run actual checks rather than assuming packages are installed. It returns a structured report you can read in under 30 seconds.

**Failure it prevents:** Spending an hour debugging a model that fails because NumPy is the wrong version, or nibabel is not installed, or the GPU is not detected when you thought it was.

**Customisation:** Add any project-specific packages to the required list. If you are on a cluster, add a check for GPU availability and SLURM version.

```
Please verify my Python environment for this brain tumour segmentation project.

Run the following checks and report the result for each as PASS or FAIL:

Core packages:
- python --version (need 3.8 or higher)
- import torch; print(torch.__version__) (need 1.12 or higher)
- import torchvision; print(torchvision.__version__)
- import nibabel; print(nibabel.__version__)
- import numpy; print(numpy.__version__)
- import matplotlib; print(matplotlib.__version__)
- import sklearn; print(sklearn.__version__)
- import pandas; print(pandas.__version__)

GPU check:
- torch.cuda.is_available() — report True or False
- If True: torch.cuda.get_device_name(0)

Data access:
- List the first 3 files in [DATA_DIRECTORY]
- Load the first NIfTI file found and print: shape, affine dtype, voxel spacing

Report format:
| Check | Result | Notes |
|-------|--------|-------|

At the end, summarise: ready to proceed / blocked by [issue].
If any check fails, propose the exact command to fix it before we continue.
```

---

## 4. Read-and-Confirm Prompt

**When to use:** Before asking Claude to modify, evaluate, or extend any existing file it has not yet read in this session.

**Why it works:** This prompt forces an explicit comprehension step. Claude must demonstrate understanding by producing a structured summary before it is permitted to act. This surfaces misunderstandings before they become bugs.

**Failure it prevents:** Claude modifying a file based on filename and context guesses rather than actual content — producing changes that are syntactically valid but logically wrong.

**Customisation:** Replace `[FILE_PATH]` with the specific file. Add any questions that matter for your context (e.g. "What metric does it optimise?", "Which classes does it predict?").

```
Before we make any changes, I need you to read and demonstrate understanding of a file.

Please:
1. Read the file at [FILE_PATH]
2. Write a structured summary covering:
   - Purpose: what this file is designed to do
   - Inputs: what data or arguments it expects
   - Outputs: what it produces (files, return values, side effects)
   - Key decisions: any non-obvious design choices (loss function, normalisation strategy, etc.)
   - Potential issues: anything that looks fragile or that might fail on edge cases
3. Answer these specific questions:
   - [QUESTION_1]
   - [QUESTION_2]

Do not modify the file. Do not write any new code.
Only proceed to the next step after I confirm your summary is correct.
```

---

## 5. Project Structure Survey Prompt

**When to use:** The first time you open a new or unfamiliar project, before Mission 0 begins.

**Why it works:** A structured survey forces Claude to build a complete map of the project before attempting any task. This prevents the common failure of Claude operating on an incomplete mental model of the codebase — for example, writing a training script that ignores a preprocessing pipeline that already exists.

**Failure it prevents:** Duplicate work (rewriting something that already exists), broken imports (referencing a module with the wrong path), and incorrect assumptions about data location.

**Customisation:** Specify the depth of the file tree if the project is large. Add domain-specific questions at the end (e.g. "What label convention does this project use?").

```
I am starting work on a new project and need a full orientation survey.

Project root: [PROJECT_ROOT]

Please perform the following survey:

1. Directory structure
   - List all files and directories to depth 3
   - Flag any directory you cannot read

2. Entry points
   - Which Python files can be run directly (have if __name__ == "__main__" or are invoked in a Makefile/README)?
   - What does each entry point do?

3. Data
   - Where is the data stored?
   - What format is it in?
   - How many cases/files are present?
   - Are there train/validation/test splits defined anywhere?

4. Configuration
   - Is there a config file (YAML, JSON, argparse defaults)?
   - What are the key hyperparameters?

5. Results
   - Where does output go?
   - Are there any existing results files I should know about?

6. Dependencies
   - What is in requirements.txt or environment.yml?
   - Are there any non-standard imports (domain-specific libraries)?

7. Gaps
   - What is missing that I would need to complete a standard training run?
   - Are there any TODO comments in the code?

Present the results as a structured report, not prose. At the end, recommend which file I should read first.
```

---

## Quick Reference

| Template | Key Cognitive Task Assigned to Claude | Session Stage |
|---|---|---|
| Context-Setting | Re-establish shared state before acting | First prompt every session |
| CLAUDE.md Generation | Inspect and document reality, not intention | Mission 0, once |
| Environment Verification | Run checks, report structured pass/fail | Mission 0, troubleshooting |
| Read-and-Confirm | Comprehend before modifying | Any time a file is touched |
| Project Survey | Build a complete map before taking action | First time on any project |
