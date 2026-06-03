# Mission 2 — Build the First Detector

Implement a trustworthy baseline segmentation model with a pre-specified evaluation contract before any code is written.

---

## Why This Matters Clinically

Every clinical AI comparison depends on a trustworthy baseline. Without a baseline computed with fixed settings and a pre-specified evaluation metric, you cannot know whether any future change — more data, a different architecture, a different loss function — is a genuine improvement, a regression, or noise in a small validation set. The baseline is not a throwaway step on the way to something more interesting; it is the most scientifically important artefact of Day 1. A poorly defined baseline makes every subsequent experiment uninterpretable. In clinical AI, uninterpretable comparisons become unsafe deployment decisions.

---

## Traditional Bottleneck

Students who approach Mission 2 without a pre-specified evaluation contract make two common errors. First, they begin with complex models or optimised settings, meaning the "baseline" is already several experimental steps away from the simplest possible implementation. When Mission 4 improvements are compared against this baseline, the gains are ambiguous — was the improvement due to the new technique or the departure from a true baseline? Second, students run training without defining in advance how success will be measured, then choose the metric that looks best after seeing the results. Post-hoc metric selection is a form of p-hacking: it makes any result look better than it is. Both errors trace back to the same root cause — starting to build before specifying what "built" means.

---

## Claude / Agentic Method

This mission introduces Claude in two sequential roles: **planner** then **builder + evaluator**. The roles are explicitly separated by the prompt structure, and this separation is non-negotiable. Claude must describe its implementation approach in numbered steps and receive approval before writing any code. This is the **plan-before-code** pattern: it forces the student to engage with the approach before the implementation exists, when changing course is still easy.

The evaluation contract is the second key concept. Before any code is written, the prompt specifies the evaluation metric (Dice coefficient), its formula, its expected range on this dataset, the exact output file path, and the exact JSON schema — including field names and types. When the training run completes, the output is either correct or not, verifiable by schema check rather than subjective judgment. This mirrors the pre-registration practice in clinical trial design: outcomes are specified before data collection, not after.

---

## Anthropic Academy / Claude Reading Connection

!!! info "Academy Alignment — Disclaimer"
    The Anthropic Academy modules listed here are independent courses created by Anthropic. This course is not affiliated with Anthropic, and the connections described below are the course author's interpretation of how those public resources relate to the skills practiced in this lab. Always consult the original Academy content directly.

    Relevant modules:

    - **Claude Code in Action** — demonstrates Claude generating, running, and debugging Python code in a project context. The training and evaluation pipeline in Mission 2 is a direct application of the pattern shown in this module.
    - **Claude Code 101** — introduces the plan-approval workflow: Claude proposes an approach, the user reviews it, then Claude executes. Mission 2 enforces this workflow explicitly for both the visualisation step and the training step.
    - **AI Capabilities and Limitations** — addresses what AI models can and cannot reliably do. Mission 2 introduces the Dice metric as a tool for measuring where this specific model's capabilities end — grounding the abstract discussion in an empirical measurement.

---

## Prompt Pattern Practiced

**Plan-before-code + evaluation contract**

Two patterns are combined in Mission 2.

**Plan-before-code**: "Describe your approach in numbered steps and wait for my approval before writing any code." This single sentence changes Claude's behaviour from implementation-first to design-first. Review the plan before approving it — this is where you catch architectural choices you would want to change.

**Evaluation contract**: Specify the metric (Dice), its formula (2·TP / (2·TP + FP + FN)), its expected range on this dataset (likely 0.3–0.7 for a simple baseline), and the exact output format (`{"dice": float, "n_slices": int}` at path `outputs/metrics/val_metrics.json`) — all in the prompt, before any code is written. The output contract is part of the experimental design, not an afterthought.

---

## What You Will Build

By the end of Mission 2, the project record will contain:

- **`outputs/figures/sample_overlay.png`** — a visualisation of one representative MRI case showing the T1ce slice, ground truth label, and predicted label in a labelled multi-panel figure.
- **`outputs/figures/loss_curve.png`** — the training loss curve showing loss versus epoch for the baseline training run.
- **`outputs/metrics/val_metrics.json`** — the primary evaluation output, with schema `{"dice": float, "n_slices": int}`. The `dice` field must be a real floating-point number between 0 and 1.
- **`reports/train_notes.md`** — a training report describing the model architecture, training settings, Dice result, and an honest assessment of what the result means.
- **`outputs/status/stage_02_load_visualize.json`** and **`outputs/status/stage_03_train_baseline.json`** — status files confirming each stage completed.

---

## What to Do in the Lab Studio

1. Open the course dashboard and navigate to the **Mission 2** tab.
2. This mission uses two prompts. Start with Stage 02: copy the Layer A prompt from `prompts/stage_02_load_visualize.md`.
3. Paste into Claude Code. Read Claude's plan before approving. Does it mention the specific output path for the overlay figure?
4. Approve and let Claude generate the visualisation. Open `outputs/figures/sample_overlay.png` immediately and inspect it before running training.
5. Copy the Stage 03 Layer A prompt from `prompts/stage_03_train_baseline.md`.
6. Paste into Claude Code. Read Claude's plan — verify that the evaluation contract matches what the prompt specified (Dice, exact output path, exact schema). Approve only after reviewing the plan.
7. Let training run. When it finishes, open `outputs/metrics/val_metrics.json` and `outputs/figures/loss_curve.png`.
8. Return to the dashboard and record your Dice score. You will use it as a reference point for every subsequent mission.

---

## Expected Artifact

| Filename | Content | How to know it is correct |
|---|---|---|
| `outputs/figures/sample_overlay.png` | Multi-panel figure: T1ce slice, ground truth, prediction | Three panels are visibly distinct; labels are present; the ground truth and prediction panels show the same anatomical slice |
| `outputs/figures/loss_curve.png` | Training loss vs. epoch | Curve is not flat; loss decreases over at least some epochs, indicating training actually occurred |
| `outputs/metrics/val_metrics.json` | `{"dice": float, "n_slices": int}` | `dice` is a real float between 0.0 and 1.0; `n_slices` is a positive integer; neither field is null, "N/A", or a placeholder string |
| `reports/train_notes.md` | Model description, training settings, Dice result, honest assessment | Names the specific architecture and loss function used; states the Dice score explicitly; includes a sentence about what this result means for patient data |

---

## How to Inspect the Result

1. Open `outputs/metrics/val_metrics.json`. Is `dice` a real float between 0 and 1? A value of exactly 0.0 or exactly 1.0 almost certainly indicates an error — a model that predicts all-background will have a Dice near 0, not exactly 0.
2. Open `outputs/figures/loss_curve.png`. Does the curve show a genuine decrease in loss, or is it flat from epoch 1? A flat loss curve means training did not update the weights. This is not a minor issue — it means the Dice score reflects random initialisation, not learned behaviour.
3. Open `reports/train_notes.md`. Does it honestly describe the model and its result, or does it read as aspirational? A phrase like "this baseline provides a strong foundation" is not an honest assessment of a model that has not been compared to anything. A phrase like "Dice of 0.52 on the validation set indicates the model is learning to segment but misses tumour boundaries" is honest.
4. Check that both status files exist: `outputs/status/stage_02_load_visualize.json` and `outputs/status/stage_03_train_baseline.json`. If either is missing, the corresponding stage did not complete with a verified output.

---

## Reflection Question

What does your Dice score mean in practical terms for a patient whose scan this model would analyse? Is a model with this Dice score good enough to use clinically, and if not, what would "good enough" require — a specific number, a comparison to radiologist performance, or something else?

---

## Extension Challenge

Try one hyperparameter variation using the Layer C prompt — for example, changing the number of training epochs or the learning rate. Save the result to `outputs/metrics/baseline_exploration.json` using a different key structure that includes the hyperparameter value alongside the Dice score. Do not overwrite `val_metrics.json`. This is your first controlled experiment: one variable changed, everything else held fixed.

---

## Transfer to Your Own Research

For a different medical AI task in your own PhD research, what would "the simplest measurable baseline" look like? Think about: what is the naive approach that requires no learned model (a threshold, a rule-based method, or a nearest-neighbour lookup)? What metric would you use to measure performance? Draft the evaluation contract you would include in the training prompt — the metric, its formula, and the exact output schema — before writing any code.
