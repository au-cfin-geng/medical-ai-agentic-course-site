# Prompt Patterns for Clinical AI

> **For print:** File → Print → Save as PDF. Eight patterns, each self-contained. Bring this sheet to every lab session.

Eight reusable prompt structures for clinical AI research. Each pattern is domain-tested: it produces outputs that are verifiable, reproducible, and fit for clinical research purposes.

---

## Pattern 1: Context-First

**What it does:** Establishes all session context before any task is issued, preventing Claude from making assumptions about data location, output format, or research scope.

**When to use:** The first message of every session. Mission 0 setup. Any time you resume after a break.

```
Research context: I am studying [research question] using [dataset] at [data path].
Output convention: all results go to outputs/ as JSON unless specified otherwise.
Constraints: do not modify files in data/. Use only [approved libraries].
Today's objective: [one sentence describing this session's goal].
Confirm you have understood this context before I send the first task.
```

---

## Pattern 2: Inspector Role

**What it does:** Directs Claude to observe and describe data without immediately writing code or drawing conclusions. Separates the observation phase from the analysis phase.

**When to use:** Mission 1 (data inspection). Any time you need structured observations before forming a hypothesis. Mission 3 (failure characterisation before proposing fixes).

```
Acting as a data analyst with expertise in medical imaging:
Inspect the dataset at [path] and report the following observations only —
do not write code, do not propose solutions, do not draw conclusions:
1. [specific property to observe, e.g. voxel spacing per case]
2. [specific property to observe, e.g. label coverage as % of total voxels]
3. [specific property to observe, e.g. presence of missing modalities]
Format: one bullet per observation. Flag anomalies with [ANOMALY].
```

---

## Pattern 3: Output Contract

**What it does:** Specifies the exact output file, format, and key names before Claude writes anything, then requires self-verification. This is the single pattern most reliably associated with reproducible results.

**When to use:** Every task that produces a file artifact. Missions 1, 2, 3, 4. Any time you will load the output programmatically.

```
Write results to outputs/[mission]_[descriptor].json with exactly these keys:
  { "case_id": string, "dice_wt": float, "sensitivity_wt": float,
    "specificity_wt": float, "failure_mode": string or null }
Include one object per case. Include an "aggregate" key with mean and std
for each float field.
After writing: read the file back. Confirm all keys are present.
If any key is missing, rewrite the file before responding.
```

---

## Pattern 4: Plan-Before-Code

**What it does:** Requires Claude to produce a numbered implementation plan in plain language before writing any code. Prevents Claude from solving the wrong problem efficiently.

**When to use:** Mission 2 (baseline implementation). Mission 4 (algorithmic improvement). Any task where the implementation approach is non-obvious or where multiple approaches exist.

```
Acting as a Python developer implementing a medical image processing pipeline:
Before writing any code, produce a numbered implementation plan with:
1. What the code will read and from where
2. The algorithm steps in order
3. What the code will write and where
4. How you will verify correctness
I will approve the plan or request changes before you write any code.
```

---

## Pattern 5: Observation Before Hypothesis

**What it does:** Requires Claude to list all observable evidence before proposing any explanation. Prevents premature hypothesis commitment — the most common failure mode in AI-assisted analysis.

**When to use:** Mission 3 (error analysis). Mission 4 (before proposing an improvement). Any time you are looking at an unexpected result.

```
Acting as a data analyst:
Look at the error map at [path] for case [case_id].
List every observable feature of the error pattern:
- Location (anatomical region or relative position)
- Shape (diffuse / focal / boundary-localised)
- Relationship to tissue type visible in [modality]
- Magnitude (how many voxels affected)
Do not propose an explanation until I ask you to.
```

---

## Pattern 6: Controlled Experiment

**What it does:** Enforces the one-variable rule: explicitly states the hypothesis, names the single change being made, and requires the output to include a before/after comparison.

**When to use:** Mission 4 (improvement with intent). Any time you are making a change to the pipeline and want to know whether the change caused the improvement.

```
Hypothesis: [specific, falsifiable prediction, e.g. "increasing the threshold
from 0.3 to 0.5 will reduce false positives in the ventricle region,
increasing specificity_wt by at least 0.03 without reducing dice_wt below baseline"]
Single change: [exact modification, nothing else]
Task: implement this change and re-run the evaluation.
Output contract: write to outputs/m04_comparison.json with keys:
  baseline_dice_wt, intervention_dice_wt, baseline_specificity_wt,
  intervention_specificity_wt, hypothesis_supported (boolean), interpretation (string)
```

---

## Pattern 7: Skeptical Reviewer

**What it does:** Invokes a critical role that finds weaknesses without proposing solutions. The solutions come in a separate, subsequent prompt. Separates criticism from implementation to prevent Claude from immediately fixing problems it has just identified.

**When to use:** Mission 5 (before finalising study design). Mission 6 (before writing the translation brief). Any time you want to find the weaknesses in your own work before a collaborator or reviewer does.

```
Acting as a rigorous peer reviewer of a clinical AI study:
Review the following result / study design / translation brief:
[paste your artifact]
List the three most serious methodological weaknesses in order of severity.
For each weakness: state the problem, state what evidence would be needed to address it.
Do NOT propose fixes. Do NOT rephrase the artifact. Only critique it.
```

---

## Pattern 8: Honesty Constraint

**What it does:** Applies explicit epistemic guardrails to translation or communication tasks, requiring Claude to name what was not demonstrated and to flag any overconfident language in its own output.

**When to use:** Mission 6 (translation brief). Any time you are communicating results to a clinical collaborator. Study design limitations sections.

```
Acting as a clinical AI consultant advising on deployment readiness:
Write a translation brief for the following result: [summary of your findings].
Apply these honesty constraints:
1. Do not use the phrase "ready for clinical use" or any equivalent.
2. For every claim about performance, state the population and conditions
   under which it was measured.
3. Include a "What this did not demonstrate" section with at least three items.
4. Specify what additional evidence would be required before deployment.
5. After writing, review your own output for overconfident language and correct it.
```
