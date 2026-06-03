# Mission 4 — Improve With Intent

Change one thing. Measure the effect. Know what you did and why.

---

## Why This Matters Clinically

In clinical AI research, the value of an improvement is inseparable from the evidence that the improvement is real and attributable. A model that performs better than the baseline is interesting. A model that performs better because of a specific, documented, single-variable change is scientifically credible.

This distinction matters at every stage of the clinical AI development pipeline. When you submit a paper to a medical imaging journal, reviewers will ask: how do you know the improvement came from the component you changed, not from a lucky random seed, a confounded comparison, or an implicit change you did not notice? When you present a model to a clinical team, they will ask: what exactly changed, and what is the evidence that the change caused the improvement?

Controlled improvement — making one change, preserving the baseline, and comparing with the same evaluation protocol — is how you build evidence that survives scrutiny.

---

## Traditional Bottleneck

The most common failure pattern in model improvement exercises is simultaneous multi-variable change: a student reads their error analysis, decides the model needs a better architecture AND a different loss function AND more training epochs AND a different preprocessing strategy, and implements all four changes at once.

The result: the Dice score improves by 0.08. But which change caused it? The student cannot say. Worse, one of the four changes may have actually hurt performance — its negative effect was masked by the positive effects of the others. If the student drops one change later (because it is expensive), they may unknowingly remove the change that was responsible for the improvement.

This is not a failure of intelligence or effort. It is a failure of experimental design. The antidote is simple: change one thing. But it requires discipline, and it requires a workflow that enforces the constraint.

---

## Claude / Agentic Method

Claude plays the role of algorithm engineer in Mission 4: a precise implementer who makes exactly the change you specify, preserves the baseline artefact, and produces a comparison that makes the effect of the change legible.

The key constraint is built into the prompt: Claude is instructed to make one specific change and to verify that the baseline Dice score in the comparison file matches the value in `val_metrics.json` from Mission 2. This verification is automatic evidence that the comparison is controlled.

The output contract names both the baseline value and the new value, requiring Claude to explicitly report the delta and attribute it to the specific change made.

---

## Anthropic Academy / Claude Reading Connection

> **Disclaimer:** The Anthropic Academy modules listed here are independent courses created by Anthropic. This course is not affiliated with Anthropic, and the connections described below are the course author's interpretation of how those public resources relate to the skills practiced in this lab. Always consult the original Academy content directly.

Relevant Anthropic Academy modules:

- **Claude Code in Action** — demonstrates Claude making targeted code modifications. Mission 4's single-variable change is a focused application of this capability.
- **Introduction to Agent Skills** — introduces the concept of Claude as a specialized agent for a specific task. The algorithm engineer role is an example of a tightly scoped agent.
- **AI Fluency: Framework and Foundations** — discusses the conditions under which AI-assisted analysis produces reliable results. Controlled experiments are one of those conditions.

---

## Prompt Pattern Practiced

**Change one thing; preserve baseline; compare with output contract naming both Dice values**

This prompt pattern has three non-negotiable constraints:

1. **Change one thing:** the prompt specifies exactly one change. It does not say "improve the model." It says "change the loss function from binary cross-entropy to Dice loss. Make no other changes."

2. **Preserve baseline:** the prompt explicitly requires that the baseline evaluation result (from Mission 2) is not overwritten. The baseline Dice score must be readable for comparison.

3. **Compare with output contract:** the output file must contain both the baseline Dice and the new Dice, with the change explicitly described. This prevents ambiguity about what was compared.

Example prompt:
```
Read CLAUDE.md first.
The hypothesis from Mission 3 is: [paste your specific hypothesis here].
Make exactly ONE change to the baseline pipeline: [describe the single change].

Constraints:
- Do not change any other parameter.
- Do not retrain on more data.
- Fix random seed to 42 (same as baseline).
- Do not overwrite outputs/metrics/val_metrics.json.

After retraining and re-evaluating, write:
outputs/metrics/model_swap_comparison.json with keys:
  {
    baseline_dice: [must match val_metrics.json exactly],
    new_dice: [new result],
    change_description: "[one sentence describing the exact change made]",
    delta: [new_dice - baseline_dice],
    hypothesis_supported: bool
  }
outputs/figures/model_swap_comparison.png: side-by-side overlay comparison
reports/model_swap.md: description of the change, the result, and whether the hypothesis was supported

Before writing any code, describe your plan and wait for my review.
```

---

## What You Will Build

By the end of Mission 4, the project record will contain:

1. **`outputs/metrics/model_swap_comparison.json`** — a comparison file containing both the baseline Dice score and the new Dice score, with the change explicitly described. The `baseline_dice` value must match `val_metrics.json` exactly.

2. **`outputs/figures/model_swap_comparison.png`** — a side-by-side figure showing the baseline prediction and the new prediction for the same validation case, allowing visual inspection of whether the change produced a qualitative improvement.

3. **`reports/model_swap.md`** — a lab notebook entry stating: the hypothesis from Mission 3, the specific change made, the baseline Dice score, the new Dice score, the delta, and whether the hypothesis was supported, partially supported, or refuted.

---

## What to Do in the Lab Studio

1. Before starting: re-read `reports/error_analysis.md` from Mission 3. Identify the one change you will make.
2. Start a Claude Code session.
3. Give Claude the algorithm engineer prompt with the plan-before-code constraint.
4. Read Claude's plan. Verify: does it describe exactly one change? Does it preserve the baseline result?
5. Approve the plan. Let Claude implement and run.
6. When done, open `outputs/metrics/model_swap_comparison.json`.
7. Verify: is `baseline_dice` the same value as in `val_metrics.json`? If not, the comparison is invalid.
8. Open `reports/model_swap.md`. Does it explicitly state whether the hypothesis was supported?

---

## Expected Artifact

`outputs/metrics/model_swap_comparison.json`:
```json
{
  "baseline_dice": 0.42,
  "new_dice": 0.51,
  "change_description": "Replaced binary cross-entropy loss with Dice loss",
  "delta": 0.09,
  "hypothesis_supported": true
}
```

`reports/model_swap.md`: a 250-400 word lab notebook entry. The most important sentences are: "The hypothesis was [supported / partially supported / refuted]. The evidence is: [specific numbers]. An alternative explanation for this result is: [honest consideration of confounds]."

---

## How to Inspect the Result

Open `outputs/metrics/model_swap_comparison.json`. Check that `baseline_dice` matches the value in `outputs/metrics/val_metrics.json` to at least two decimal places. If they differ, the comparison is not controlled — ask Claude to identify the discrepancy.

Check that `change_description` is a specific sentence, not a vague phrase. "Changed the model" is not a valid description. "Replaced binary cross-entropy with Dice loss, keeping all other hyperparameters identical" is valid.

---

## Reflection Question

How do you know your improvement was real and not noise from a lucky random seed?

If you ran the experiment with random seed 43 instead of 42, would you expect the same direction of improvement? What would you need to do to be confident that the improvement is consistent across seeds and not a single lucky outcome?

---

## Extension Challenge

Run the same experiment with two additional random seeds (43 and 44). Report the mean and standard deviation of the Dice score across three seeds for both the baseline and the new model. Does the improvement persist across seeds? What does the variance tell you about the reliability of the result?

---

## Transfer to Your Own Research

In your own research, how would you design a controlled experiment to test one specific change?

Define: what is your baseline? What is the one variable you would change? What is your pre-specified success criterion (minimum improvement to count as "supported")? What would it mean if the hypothesis were refuted?

Write a one-paragraph experimental design for one improvement you have been considering in your own research.
