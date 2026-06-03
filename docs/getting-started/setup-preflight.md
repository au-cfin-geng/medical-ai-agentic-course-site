# Preflight Setup

## Why Environment Setup Matters for Reproducibility

In clinical AI research, a result that cannot be reproduced is not a result. This seems obvious, but it has a less obvious implication: reproducibility begins before you write a single line of analysis code. It begins with your environment.

Two researchers running the same code on different Python versions, with different library versions, on machines with different floating-point behavior, can get different numerical results. This is not a hypothetical. It has affected published clinical AI papers. The preflight setup is your first act of scientific discipline in this course: establishing a documented, verified environment that others could replicate.

---

## What the Preflight Assignment Does

The preflight is Mission 0 of this course. Its objective is not to teach you anything new about clinical AI. Its objective is to verify that your computational environment is correctly configured and to produce a documented record of that environment.

Specifically, the preflight:

1. Verifies that Python and all required libraries are installed at the correct versions
2. Verifies that the lab repository is cloned and the directory structure is intact
3. Verifies that the BraTS sample data can be loaded (correct file format, readable headers, correct shapes)
4. Verifies that basic Dice coefficient computation runs without error
5. Produces a `preflight_report.json` file documenting everything above

The preflight report is your first required artifact. It is also a model of what a good environment report looks like: it documents not just success or failure, but the specific versions, paths, and values that define your environment.

---

## The Agentic Setup Pattern

The preflight introduces the core pattern of this course: you specify intent, Claude executes, you inspect the output.

For the preflight, this pattern looks like:

1. You open Claude Code in VS Code with the lab repository open
2. You paste the preflight prompt (available in the Prompt Library under Setup Prompts)
3. Claude reads the CLAUDE.md file, checks the environment, loads a sample data file, runs a basic computation, and writes the report
4. You open `preflight_report.json` and inspect it

What you are practising here is not Python programming. You are practising the habit of directing an AI agent to do a well-specified task and then inspecting its work. This habit will serve you for every subsequent mission.

---

## How to Run the Preflight Prompt

Before running the preflight:

- Ensure Claude Code is installed and authenticated with your Anthropic account
- Ensure the lab repository is cloned to your machine
- Open the repository root in VS Code
- Verify that the CLAUDE.md file is present at the root

Then:

1. Open Claude Code in VS Code (Cmd+Shift+P → "Claude Code: Open")
2. Copy the preflight prompt from the Prompt Library
3. Paste it into the Claude Code input field and press Enter
4. Watch the output panel — Claude will report each step as it completes
5. When Claude finishes, it will tell you where it wrote the report

Do not proceed to Mission 1 until you have a complete `preflight_report.json` with no error flags.

---

## What to Inspect in the Output File

Open `preflight_report.json` and check:

- **python_version**: Should be 3.10 or higher
- **library_versions**: Check nibabel, numpy, matplotlib, scikit-learn, torch (if applicable) against the required versions listed in `requirements.txt`
- **data_path**: Should point to the correct location within the repository
- **sample_volume_shape**: Should match the expected BraTS volume dimensions
- **dice_test**: Should return `"passed": true`
- **errors**: Should be an empty list

If any field shows an error or unexpected value, consult the troubleshooting section in the lab repository README before Day 1. Do not wait until Day 1 to discover that your data path is wrong.
