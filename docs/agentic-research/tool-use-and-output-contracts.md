# Tool Use and Output Contracts

An output contract is the specification — written in your prompt — of the exact file path, file format, required contents, and validation criteria for every output Claude should produce. Output contracts are the single most effective mechanism for making agentic research reproducible, gradable, and trustworthy.

This page explains what output contracts are, why they are essential, how to write them, and what happens when they are missing.

---

## What an Output Contract Is

An output contract is a promise that you extract from Claude before it takes action. It states: "When you are done, I expect to find a file at exactly this path, in exactly this format, containing exactly these keys, with values of exactly these types."

The analogy is to a contract between a client and a contractor. A vague contract ("build me a house") produces a house that may or may not match what the client imagined. A specific contract ("build a three-bedroom house at 42 Oak Street, with the specifications in document A, by 1 June, for €250,000") produces a result that can be evaluated against specific criteria.

In agentic research, you are the client. Claude is the contractor. The output contract is the binding specification.

---

## Why Output Contracts Are Essential

Without an output contract, Claude will produce output. It will choose a file path that seems reasonable to it. It will choose a format it has seen frequently in similar tasks. It will choose key names based on convention. The output will exist, it will look plausible, and it will be wrong from the perspective of downstream use.

Consider the grading implications. The autograder for Mission 4 tests for the file at `outputs/metrics/model_swap_comparison.json` with keys `baseline_dice`, `new_dice`, `delta`, `change_description`, and `hypothesis_supported`. If Claude saves the file to `results/mission4.json` with keys `original_score`, `improved_score`, and `description`, the autograder finds nothing. Your experiment ran correctly. Your code produced the right numbers. You failed the autograder test, not because the science was wrong, but because the output contract was violated.

This is not a quirk of this course's autograder. In real research pipelines, downstream scripts, visualizations, and meta-analyses depend on specific file paths and specific key names. An output that does not match the expected contract breaks the pipeline at the point of consumption, not at the point of production. The bug is invisible until it is downstream.

---

## The Anatomy of an Output Contract

A complete output contract has four components:

1. **File path** — the exact path, relative to the repository root, including directory and filename. Case-sensitive. No substitutions.
2. **File format** — JSON, markdown, PNG, CSV. Each implies different validation criteria.
3. **Required keys or sections** — for JSON, the exact key names and value types. For markdown, the required section headers. For PNG, the required panels or labels.
4. **Minimum content requirement** — for reports, a minimum character or word count. For JSON, a constraint on value ranges (e.g., Dice is a float between 0 and 1). For figures, a description of what must be visually present.

All four components should appear in every output contract you write.

---

## Output Contract Precision: Three Levels

Here is the same task expressed as an output contract at three levels of precision.

**BAD — no contract:**

```
Save the results.
```

Claude will save something. You do not know where, in what format, or with what keys. The autograder will not find it. You will not be able to compare it against other results.

**BETTER — partial contract:**

```
Save the Dice score to a JSON file in the outputs directory.
```

Claude will save a JSON file. The directory is constrained. The format is specified. But the exact filename is not given, the key name is not specified, and there is no validation requirement. You will find a JSON file in the outputs directory, but it may be named `results.json`, `dice.json`, or `evaluation_result_mission4.json`, and the key inside may be `"score"`, `"dice_score"`, or `"val_dice"`. The autograder is looking for `"dice"` in `outputs/metrics/model_swap_comparison.json`. This file will not be found.

**GOOD — complete contract:**

```
Write to outputs/metrics/model_swap_comparison.json with exactly this structure:
{
  "baseline_dice": <float between 0 and 1, must match val_metrics.json exactly>,
  "new_dice": <float between 0 and 1>,
  "delta": <new_dice minus baseline_dice>,
  "change_description": "<one sentence describing the exact change made>",
  "hypothesis_supported": <true or false>
}

After writing, read the file back and confirm that:
(1) baseline_dice matches the value in outputs/metrics/val_metrics.json
(2) delta equals new_dice minus baseline_dice to 4 decimal places
(3) all five keys are present
```

This is a complete output contract. The file path is exact. The format is JSON. The keys are named. The types are specified. The validation step is specified. If Claude violates any part of this contract, it will be caught immediately — either by the validation step Claude is asked to perform, or by your own inspection of the file.

---

## The Grading Implication

The autograder for this course checks:

1. Whether the required file exists at the exact specified path
2. Whether the required keys are present in the JSON file
3. Whether the values are within expected ranges (e.g., Dice between 0 and 1)
4. Whether required sections are present in markdown reports

A contract violation at any of these levels fails the test. The most common contract violations in student sessions:

- **Wrong path:** Claude saves to `output/` instead of `outputs/`, or to `results/` instead of `outputs/metrics/`. This fails check 1.
- **Wrong key name:** Claude uses `"dice_score"` instead of `"dice"`. This fails check 2.
- **Missing key:** Claude omits `"hypothesis_supported"` from the comparison JSON. This fails check 2.
- **Wrong value type:** Claude saves the Dice score as a string (`"0.67"`) instead of a float (`0.67`). This fails check 3 for some tests.

All of these failures can be prevented by a complete output contract in the prompt.

---

## Output Contracts for Reports

Markdown reports require a different kind of output contract than JSON files.

For `reports/error_analysis.md` (Mission 3), the contract is:

```
Write reports/error_analysis.md with these sections in this order:
1. ## Best Case (2-3 sentences describing what is visually correct)
2. ## Worst Case (3-5 sentences describing the visual failure pattern, be specific)
3. ## Failure Hypothesis (must name: the specific failure pattern,
   a plausible mechanistic cause, and a specific intervention for Mission 4)
4. ## Proposed Mission 4 Experiment (one paragraph describing what you would test)

Minimum length: 300 words.
Do not use the phrase "further investigation is needed" without specifying what
investigation and what it would reveal.
```

This contract specifies section headers (which the autograder checks), section content requirements (which you check during verification), minimum length, and a prohibited filler phrase.

---

## How to Verify an Output Contract Was Met

After Claude reports that it has completed an output, do not accept that report without verification. Verification is a two-step process:

**Step 1 — Existence check:** Does the file exist at the exact path specified? Open a terminal and check. `ls outputs/metrics/model_swap_comparison.json` should return the file. If it does not exist, or if it exists at a slightly different path, the contract was violated.

**Step 2 — Content check:** Open the file. Read it. Confirm:
- For JSON: every required key is present; every value is of the correct type; values are in expected ranges; any derived values (like `delta`) are mathematically consistent with the source values.
- For markdown: every required section header is present; the content is substantive and not placeholder text; required specific claims are made.
- For PNG: the file opens without error; the figure shows the correct panels with correct labels.

If the verification fails, do not accept the output. Tell Claude specifically what was wrong and ask it to correct the specific violation.

!!! warning "Trust the file, not the report"
    If Claude says "I have saved the results to outputs/metrics/model_swap_comparison.json with all required keys," that is Claude's representation of what happened. Open the file and read it yourself. Claude can be wrong about what it saved, what keys it included, and what values it wrote. The file is the ground truth. Claude's report about the file is not.

!!! example "Verification checklist"
    After Claude completes any output task, run through this checklist:
    (1) Existence: does the file exist at the exact specified path?
    (2) Format: is it valid JSON / valid markdown / a viewable PNG?
    (3) Keys: are all required keys present with the correct names?
    (4) Values: are numeric values within expected ranges?
    (5) Derived values: are computed fields (delta, change_description) mathematically and logically consistent?
    (6) Report text: if a markdown report, does it make the required specific claims?

!!! tip "Add the verification step to every prompt"
    End every output contract specification with: "After writing, read the file back and confirm that all required keys are present with the correct names and value types. Report any discrepancy immediately." This makes verification automatic and surfaces violations before you discover them during grading.
