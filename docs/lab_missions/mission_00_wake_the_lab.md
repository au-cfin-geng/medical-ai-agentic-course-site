# Mission 0 — Wake the Lab

Before any science can happen, the environment must work. This mission is about getting oriented, verifying that your tools are in order, and making your first intentional prompt to Claude Code. You will not produce a model or a figure here — you will produce confidence that the rest of the course can proceed.

---

## Scientific Purpose

Every computational experiment depends on a functioning environment. In real research, environment failures waste hours: a wrong package version produces silent numerical differences; a missing data path causes a script to silently skip cases; a GPU that is not detected slows training by 50x. Experienced researchers verify their environment before they write a single line of model code. This mission instils that habit. You will produce a structured verification report that documents your exact environment — so that when something goes wrong later (and it will), you have a baseline to compare against.

---

## Required Background Reading

Before starting this mission, read the following pages on this site:

- [What Is Agentic Coding](../agentic_research/what_is_agentic_coding.md) — understand what Claude Code is and how it differs from a chatbot
- [Claude Code Workflow](../agentic_research/claude_code_workflow.md) — understand the read-plan-act-verify cycle
- [Prompt as Protocol](../agentic_research/prompt_as_experimental_protocol.md) — understand why precision in prompts matters
- [Prompt Best Practices](../agentic_research/prompt_best_practices.md) — the practical rules you will apply in every mission

---

## What You Will Ask Claude to Build

Your goal is to direct Claude Code to produce a complete environment verification report for the Medical AI Lab. The report should confirm that all required Python packages are installed at the expected versions, that the dataset paths described in the repository README are accessible and contain the expected number of files, that the results and checkpoints directories exist or can be created, and that GPU availability is detected and reported. Claude should read the project's `CLAUDE.md` and `requirements.txt` before writing any code, and the output should be a formatted document that another researcher could read to understand exactly what environment you are working in.

Think about what information a colleague would need if they had to reproduce your results from scratch on a different machine. The report should answer their questions before they ask them.

You are not evaluating Claude's output blindly — after it produces the script, you should run it and check the output yourself. If something is missing or the format is hard to read, ask Claude to revise it.

---

## Expected Artifacts

| Filename | Contents | What Correct Looks Like |
|---|---|---|
| `environment_check.py` | A Python script that performs all verification checks | Runs without errors; uses `importlib.metadata` or `pkg_resources` for version checks |
| `environment_check.txt` or `environment_check.md` | The output of running the verification script | Lists all packages with installed vs required version; shows ✓ or MISSING; reports dataset file counts; reports GPU availability |

The report should be machine-readable but also human-readable. If you open it and cannot tell within 10 seconds whether the environment is healthy, ask Claude to improve the formatting.

---

## How to Inspect Results

Run the verification script yourself and read the output line by line:

1. Are all packages in `requirements.txt` listed? Are any marked as missing?
2. Do the dataset paths match what is described in the README? Are the file counts plausible (e.g., 369 BraTS training cases)?
3. Is the GPU status reported? If you have a GPU and it shows `No GPU detected`, something is wrong with your CUDA installation — note this now.
4. Open the saved `.txt` or `.md` file and check that it is a complete record, not just console output.

If any check fails, do not skip it and move on. Ask Claude to help you diagnose the failure before proceeding to Mission 1. An environment problem ignored in Mission 0 will cost you two hours in Mission 2.

---

## Prompt Principle

**Always provide project context before asking Claude to do anything.**

Claude Code does not know your project unless you tell it. The single most common mistake in this course is issuing a one-line instruction and getting a generic answer that does not fit your codebase.

Compare these two prompts:

!!! failure "Weak prompt"
    ```
    Check if all packages are installed.
    ```
    Claude has no idea what packages, what project, or what to do with the result.

!!! success "Strong prompt"
    ```
    I am working on the Medical AI Agentic Lab. My repository is at /path/to/repo.
    Read CLAUDE.md and README.md first to understand the project structure.
    Then read requirements.txt to get the list of required packages.
    Write a Python script called environment_check.py that:
    1. Checks each required package is installed and reports its version
    2. Checks that the data paths described in the README exist and reports file counts
    3. Checks for GPU availability using torch.cuda.is_available()
    4. Saves a formatted summary to environment_check.md
    Run the script and show me the output.
    ```
    Claude now has role, project context, file locations, a specific task breakdown, and an explicit output format.

The pattern is: **Context → Files to read → Task breakdown → Output specification.**

---

## Reflection Questions

1. What would happen if you ran the Mission 2 training script without noticing that `torch` was installed but CUDA was not available? How would the training behave, and how long might it take before you noticed?

2. The verification script produces a snapshot of your environment at one point in time. When would it be useful to re-run it? What events might change your environment in ways that are hard to notice?

3. You gave Claude a detailed prompt and it produced a script. You are responsible for understanding what that script does. Read through it: does it check everything you asked for? Is there anything it missed?

4. Compare the output of your verification report with a classmate's. If the outputs differ (different package versions, different GPU), what implications does this have for reproducing each other's results?

5. The `CLAUDE.md` file in the lab repository tells Claude Code about the project. What information does it contain? Why is it better practice to put this information in a file rather than repeating it in every prompt?

---

## Optional Challenge

Extend the verification script to also check that the dataset files are not corrupted. For each NIfTI file in the first 5 training cases, load the file with `nibabel`, check that the image dimensions are as expected (e.g., 240x240x155 for BraTS), and check that the label file contains only the expected integer values (0, 1, 2, 3 for BraTS). Report any anomalies. This is a minimal data integrity check — the kind a real clinical AI pipeline would run before every training run.

---

## Common Failure Modes

**Claude does not find CLAUDE.md.** This means you ran Claude Code from the wrong directory. Always launch Claude Code from the root of your lab repository. Verify with `pwd` before starting.

**Package version check reports wrong versions.** If you have a conda environment that is not activated, Claude may be checking the base Python installation. Ask Claude to print `sys.executable` and `sys.prefix` at the start of the script — if these do not point to your project environment, you need to activate it first.

**Dataset paths not found.** The data may not have been downloaded, or the path in CLAUDE.md may use a placeholder like `/data/brats`. Ask Claude to also print the directory tree one level deep at the expected data location, so you can see what is actually there.

**Script runs but output file is empty or not created.** This usually means the script wrote to stdout but the redirect failed, or there was a silent exception. Ask Claude to add explicit error handling and to print a confirmation message when the file is saved.

**Student skips the verification and goes straight to Mission 1.** You will encounter a mysterious error in Mission 2 and spend 45 minutes discovering it was a version incompatibility that Mission 0 would have caught in 2 minutes.

---

## Expected Learning Outcome

After completing this mission you can: launch Claude Code from a project directory; give Claude a context-first, structured prompt; verify that Claude's output actually does what you asked; read and run Python code that you directed Claude to write; produce a reproducible environment record. You are ready to do science.
