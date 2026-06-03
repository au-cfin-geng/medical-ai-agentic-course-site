# Mission 3 — Investigate Failure

A model that sometimes fails is more informative than one that always succeeds. Find where it fails.

---

## Why This Matters Clinically

In clinical AI, the distribution of model failures matters as much as the average performance. A model with a mean Dice score of 0.65 might be performing brilliantly on 90% of cases and catastrophically on 10% — and that 10% might be the patients who need the model most, such as those with atypical tumour morphology, post-surgical anatomy, or low-contrast lesions.

False positives and false negatives have asymmetric clinical consequences. A false positive in tumour segmentation — predicting tumour where there is none — may lead to unnecessary biopsy or treatment, with associated risk and patient anxiety. A false negative — missing a region of true tumour — may leave a lesion untreated. Understanding which failure mode dominates, and in which case types it occurs, is prerequisite knowledge for responsible deployment decisions.

Error maps — visualizations that show where the model is wrong, pixel by pixel — are the primary tool for this investigation. They reveal spatial patterns of failure that aggregate metrics cannot: does the model consistently fail at tumour boundaries? Does it fail in a particular anatomical region? Does it fail on slices with small lesion sizes? Each of these patterns suggests a different remediation strategy.

---

## Traditional Bottleneck

The most common shortcut in computational AI courses is to treat the aggregate metric as the complete evaluation. "Dice score is 0.65" becomes the final word on model performance, and the analysis moves directly to the next experiment.

What this misses:

- **Best and worst cases are invisible.** The best-performing case might be trivial (a large, well-contrasted tumour). The worst-performing case might reveal a systematic failure mode.
- **Error patterns are invisible.** Whether the model fails at boundaries, in the tumour core, or in a specific anatomical region cannot be read from a single scalar metric.
- **Hypotheses are generated without evidence.** Students who do not look at their failure cases often propose improvements that do not address the actual failure mode. They change the loss function when the real problem is data quality; they increase model capacity when the real problem is class imbalance.
- **The qualitative-quantitative connection is broken.** Good scientific practice requires that you can look at a failing prediction and describe, in plain language, why it is failing.

Mission 3 restores the qualitative-quantitative connection by requiring that you look at the actual failure cases and generate hypotheses from what you see.

---

## Claude / Agentic Method

Claude plays two roles in Mission 3: visual debugger and hypothesis generator. These are applied sequentially, not simultaneously.

As **visual debugger**, Claude generates scripts that:
- Rank all validation cases by Dice score
- Load the best-performing and worst-performing cases
- Generate error maps showing true positive, false positive, and false negative voxels in distinct colours
- Save the figures to the outputs directory

As **hypothesis generator**, Claude is prompted to observe the figures first — to describe what it sees in the error maps — before generating any hypothesis about why the model failed. This sequence is enforced by the prompt structure: observation before hypothesis.

This is a specific application of scientific discipline: you should not know why something fails before you have looked at how it fails. The hypothesis should emerge from the evidence, not precede it.

---

## Anthropic Academy / Claude Reading Connection

> **Disclaimer:** The Anthropic Academy modules listed here are independent courses created by Anthropic. This course is not affiliated with Anthropic, and the connections described below are the course author's interpretation of how those public resources relate to the skills practiced in this lab. Always consult the original Academy content directly.

Relevant Anthropic Academy modules:

- **AI Fluency for Students** — discusses how to critically evaluate AI outputs, including model predictions. Mission 3's error analysis framework is a direct application of critical evaluation habits.
- **AI Capabilities and Limitations** — addresses the limits of what AI models can reliably do. Understanding your model's failure cases is how you discover those limits empirically.
- **Claude Code in Action** — demonstrates Claude generating visualization code. Mission 3 uses this to produce error map figures that would take significant manual coding effort.

---

## Prompt Pattern Practiced

**Ask Claude to observe first, then explain. Never hypothesis before evidence.**

This is the scientific method applied to prompt engineering. The pattern enforces two phases:

**Phase 1 — Observation (no hypothesis permitted):**
```
Read CLAUDE.md first.
Load outputs/metrics/val_metrics.json to identify the validation cases.
Rank all validation cases by Dice score (lowest to highest).
Generate the following figures:
- outputs/figures/error_analysis_best.png: best case — show original T1ce slice,
  ground truth mask, predicted mask, and error map (green=TP, red=FP, blue=FN)
  in a 2x2 labelled panel
- outputs/figures/error_analysis_worst.png: same layout for the worst case

Save both figures. Then describe in plain language what you see in each figure.
Do not propose any hypothesis yet. Only describe what you observe.
```

**Phase 2 — Hypothesis (after observation):**
```
Now that you have described the error patterns, propose one specific and testable
hypothesis about why the worst case fails. The hypothesis must name:
1. The specific failure pattern observed
2. A plausible mechanistic cause
3. A specific intervention to test in Mission 4

Write findings to reports/error_analysis.md.
Write outputs/status/stage_03_error_analysis.json with keys:
  best_case_dice, worst_case_dice, hypothesis_stated (bool), hypothesis_testable (bool)
```

---

## What You Will Build

By the end of Mission 3, the project record will contain:

1. **`outputs/figures/error_analysis_best.png`** — a four-panel figure showing the best-performing validation case: original MRI slice, ground truth mask, predicted mask, and colour-coded error map.

2. **`outputs/figures/error_analysis_worst.png`** — the same four-panel layout for the worst-performing validation case. This is the primary artefact of Mission 3.

3. **`reports/error_analysis.md`** — a structured report containing: (a) a plain-language description of what is visually wrong in the worst case, (b) a specific and testable hypothesis about the cause, and (c) a proposed intervention for Mission 4.

---

## What to Do in the Lab Studio

1. Start a Claude Code session in the project root.
2. Give Claude the Phase 1 prompt — observation only, no hypothesis.
3. When Claude generates the figures, open them immediately. Look at the error map for the worst case before reading Claude's description.
4. Write down in your own words what you see wrong. What colour dominates the error map? Where spatially are the errors concentrated?
5. Compare your observation with Claude's. Do they agree?
6. Give Claude the Phase 2 prompt — hypothesis generation only after observation is complete.
7. Read the hypothesis in `reports/error_analysis.md`. Is it specific enough to test?

---

## Expected Artifact

`reports/error_analysis.md` should contain:
- A description of the best case (2-3 sentences)
- A description of the worst case (3-5 sentences describing the visual failure pattern)
- A specific and testable failure hypothesis naming the pattern, cause, and proposed intervention
- A clear statement of what experiment in Mission 4 would test this hypothesis

`outputs/figures/error_analysis_worst.png`: a four-panel matplotlib figure with clear titles and colour-coded error regions (TP green, FP red, FN blue).

---

## How to Inspect the Result

Open `outputs/figures/error_analysis_worst.png`. Can you describe in one sentence what is visually wrong? For example: "The model predicts a large region of tumour in the left hemisphere but the ground truth shows no tumour there" (false positive pattern). Or: "The model correctly identifies the tumour centre but misses the boundary completely" (boundary failure).

If you cannot describe in one sentence what is wrong, the figure is not informative enough. Ask Claude to regenerate with larger panels or a different colour scheme.

Open `reports/error_analysis.md`. Check the hypothesis: does it name a specific failure pattern, a plausible cause, and a testable intervention? "The model needs more data" is not a testable hypothesis. A testable hypothesis specifies what change you would make and what improvement you would expect to see.

---

## Reflection Question

Is your failure hypothesis specific enough that someone could design an experiment to test it?

Test your hypothesis against three criteria:
1. Is the failure pattern named precisely enough to be recognizable in a new figure?
2. Is the proposed cause mechanistically plausible?
3. Is the proposed intervention specific enough that someone could implement it from the description alone?

If any answer is no, revise the hypothesis with Claude before proceeding to Mission 4.

---

## Extension Challenge

Extend the error analysis to report failure statistics by slice position (axial slice index). Do the failure cases cluster near the top or bottom of the brain volume? Does the model perform worse on slices with small lesion areas? What prompt would you write to generate this spatial failure analysis?

---

## Transfer to Your Own Research

For your own model or analysis, how would you identify and visualize the worst-performing cases?

Define: what is your equivalent of a "case"? What metric ranks cases from best to worst? What visualization would make the failure pattern visible? Draft a prompt you would use to generate a failure analysis for one of your own research models.
