# Mission 1 — Receive the Signal

Systematically inspect and document the MRI dataset before any modelling action begins.

---

## Why This Matters Clinically

Data provenance is not an administrative formality in clinical AI — it is a scientific requirement. Before training any model on patient imaging data, you must verify what data you actually received, which modalities are present, whether labels are complete and aligned, and whether anything looks anomalous. A model trained on corrupted labels, misregistered modalities, or an unrecognised class distribution does not fail with an obvious error message; it trains normally, evaluates plausibly, and produces results that look real. Errors discovered at the data inspection stage cost minutes. The same errors discovered at model evaluation cost weeks — and errors that reach clinical deployment may harm patients.

---

## Traditional Bottleneck

Students who skip systematic data inspection typically discover their dataset's actual properties at the worst possible moment. Missing files reveal themselves as file-not-found errors mid-training. Wrong class distributions reveal themselves as unexpected loss behaviour that looks like a learning rate problem. Misaligned labels reveal themselves as Dice scores that are consistently lower than expected, with no obvious cause. None of these problems are visible without looking at the data before modelling. The standard shortcut — "download the data, assume it is correct, start modelling" — transfers a documentation debt from Mission 1 to every subsequent mission. Mission 1 closes that debt explicitly: inspect first, document what you found, then proceed.

---

## Claude / Agentic Method

This mission introduces Claude in the **data steward** role — a specific stance distinct from the coder or analyst role. As data steward, Claude's primary obligation is honest documentation: it produces a data receipt that records exactly what was received, what was verified, and what is uncertain or anomalous. Claude is not asked to fix the data, interpret the data scientifically, or proceed to modelling. It is asked only to look, describe, and report.

The core habit introduced here is **inspect before you model**: assign Claude the inspection task with a defined output contract, review the data receipt before doing anything else, and treat any anomaly flagged in the receipt as a prerequisite investigation before Mission 2 begins. This mirrors the data curation discipline expected in clinical AI research, where a data receipt is a governance document, not a convenience.

---

## Anthropic Academy / Claude Reading Connection

!!! info "Academy Alignment — Disclaimer"
    The Anthropic Academy modules listed here are independent courses created by Anthropic. This course is not affiliated with Anthropic, and the connections described below are the course author's interpretation of how those public resources relate to the skills practiced in this lab. Always consult the original Academy content directly.

    Relevant modules:

    - **Claude Code 101** — demonstrates using Claude Code to run file inspection and reporting tasks. The data steward role in Mission 1 is a direct application of this pattern to a research dataset.
    - **Claude Code in Action** — shows Claude generating structured reports from directory inspection. The `data_notes.md` deliverable follows the report-generation workflow shown in this module.
    - **AI Fluency: Framework & Foundations** — introduces the concept of AI as a tool that requires human specification of what to look for. Mission 1 practices this by writing an explicit inspection protocol rather than asking Claude to "look at the data."

---

## Prompt Pattern Practiced

**Context before action — Inspector role**

Two patterns are combined in Mission 1. First, **context before action**: tell Claude what you are looking for before asking it to look. The prompt names the specific properties to check (modality presence, case count, class distribution, anomalies) rather than asking Claude to determine what matters on its own. Second, **inspector role**: explicitly assign Claude the data analyst role, not the developer role, and instruct it that its output is a receipt, not a plan. This prevents Claude from treating data inspection as a prelude to code generation.

---

## What You Will Build

By the end of Mission 1, the project record will contain:

- **`data/sample/`** — the teaching MRI dataset confirmed present on disk, with all expected case directories and modality files accessible.
- **`reports/data_notes.md`** — a data receipt documenting: dataset name and source, case count, modality listing (T1, T1ce, T2, FLAIR), class distribution summary (what fraction of voxels are tumour versus background), QC notes on any anomalies found, and a clear statement of what was verified versus assumed.
- **`outputs/status/stage_01_fetch_sample.json`** — a machine-readable status file confirming the fetch and inspection completed, with at minimum the keys `status` and `dataset`.
- A written confirmation from you (in the lab dashboard) of the three most important properties you learned about the dataset from reading `data_notes.md`.

---

## What to Do in the Lab Studio

1. Open the course dashboard and navigate to the **Mission 1** tab.
2. Copy the Layer A prompt from `prompts/stage_01_fetch_sample.md` in the student classroom repo.
3. Paste the prompt into Claude Code (`claude` from the project root).
4. Watch Claude inspect the data directory. Notice whether Claude mentions all four modalities by name — this tells you whether the context before action pattern is working.
5. When Claude finishes, open `reports/data_notes.md` and read it fully before doing anything else.
6. Open `outputs/status/stage_01_fetch_sample.json` and confirm `status` is `"ok"`.
7. Return to the dashboard and enter your three-sentence summary of what the data receipt told you about the dataset.

---

## Expected Artifact

| Filename | Content | How to know it is correct |
|---|---|---|
| `data/sample/` | Teaching MRI dataset, directory accessible | `ls data/sample/` returns case directories, not an empty listing |
| `reports/data_notes.md` | Dataset summary: case count, modalities, class distribution, QC notes, anomaly flags | Mentions all four modalities by name; reports a specific tumour voxel fraction (e.g., "2.3% of voxels labelled as tumour"); flags any missing files or unexpected values |
| `outputs/status/stage_01_fetch_sample.json` | `{"status": "ok", "dataset": "..."}` | `status` is `"ok"`, `dataset` names the actual dataset used |

---

## How to Inspect the Result

1. Open `reports/data_notes.md`. Does it mention all four modalities — T1, T1ce, T2, and FLAIR — by name? If only one or two modalities are named, Claude inspected only part of the data structure.
2. Does `data_notes.md` report a class distribution? You should see a specific number or percentage for tumour versus background voxels. A generic statement like "class distribution is imbalanced" without numbers is not a data receipt — it is a template.
3. Does `data_notes.md` flag any anomalies, or does it read as an all-clear? A genuine inspection of a real dataset almost always finds something worth noting — a case with slightly different dimensions, a file that is larger or smaller than expected, or a label file with an unexpected value range. If `data_notes.md` reports no anomalies at all, ask Claude to re-inspect with explicit instructions to look for outliers.
4. Compare the case count in `data_notes.md` to the number of subdirectories in `data/sample/`. Do they match?

---

## Reflection Question

What did you learn about your dataset that you could not have known without inspecting it? Specifically: how does the class distribution you found affect how you should interpret the Dice score you will compute in Mission 2? Would a model that predicts all-background on every voxel perform better or worse than random chance on this dataset, and why?

---

## Extension Challenge

Ask Claude to visualise one representative MRI slice with its label overlay using the Layer C prompt. Open the resulting figure and inspect whether the label overlay correctly aligns with the tumour region — do the coloured voxels in the overlay sit inside the visually distinct region of the scan, or are they offset? If the overlay is misaligned, that is clinically significant and should be documented in `reports/data_notes.md` as an anomaly before Mission 2 begins.

---

## Transfer to Your Own Research

For your own PhD dataset, what would a data receipt look like? Identify five specific properties you would want Claude to verify before beginning any analysis: the things that, if wrong, would silently corrupt your results. Draft the inspection protocol you would include in your context-before-action prompt — naming each property, how to measure it, and what range of values would count as normal versus anomalous.
