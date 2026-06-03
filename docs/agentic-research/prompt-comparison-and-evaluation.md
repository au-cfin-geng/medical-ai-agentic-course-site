# Comparing and Evaluating Prompts

Prompts are not interchangeable. Two prompts for the same task can produce outputs that differ systematically in quality, specificity, scientific validity, and downstream usability. Understanding how to compare prompts — and how to evaluate which one produced the better output — is a transferable research skill.

This page covers the principles of prompt comparison, the criteria for evaluation, and how this practice connects to the lab missions.

---

## Why Prompts Are Comparable

A well-specified task can be executed by many different prompts. The choice of prompt is analogous to the choice of protocol in a wet lab: different protocols for the same experiment can produce different results, not because the underlying biology is different, but because the protocol shapes what is measured, how it is measured, and what is recorded.

Prompt comparison is therefore not about finding the "best" general-purpose prompt. It is about finding, for a specific research task, which prompt formulation produces output that most faithfully represents your research intent, is most verifiable, and is most reproducible.

This is a feature, not a bug. The fact that different prompts produce different outputs means that prompt design is a consequential choice — and consequential choices should be documented.

---

## How to Run a Prompt Comparison

A prompt comparison follows the same structure as any controlled experiment: identical task, two different prompts, compare the outputs on specific criteria.

**Step 1 — Define the task.** What is the specific research step you are prompting for? Be precise. "Evaluate the model" is not a task — "compute per-case Dice scores for all validation cases and save to `outputs/metrics/val_metrics.json`" is a task.

**Step 2 — Write two prompts.** The prompts should differ on one specific dimension — for example, one has an output contract and one does not. Or one specifies the role and one does not. Or one uses the plan-before-code pattern and one does not.

**Step 3 — Run both prompts** and save both outputs. Do not overwrite the first output when running the second — save them to separate files for comparison.

**Step 4 — Compare on specific criteria** (see the next section).

**Step 5 — Record the comparison.** Note which prompt produced better output, why, and what specific change made the difference. This is your prompt improvement log.

---

## Criteria for Evaluating a Prompt

Four criteria apply to any research prompt:

**Specificity.** Does the prompt leave room for ambiguity? Can Claude make a consequential decision that you did not intend to delegate? A high-specificity prompt names files, paths, parameters, and constraints explicitly. A low-specificity prompt leaves these to Claude's discretion. Evaluate: what decisions did Claude make that you did not specify? Were they the right decisions?

**Output contract.** Does the prompt name exact file paths and required formats? Can the output be graded by an autograder or compared against a previous run? A prompt with a complete output contract produces a specific, findable, verifiable output. A prompt without an output contract produces output that may or may not be findable and verifiable.

**Role clarity.** Does the prompt tell Claude what kind of thinking to do? Is Claude in developer mode, inspector mode, or critic mode? A prompt with clear role declaration produces output of a predictable type. A prompt without role declaration produces mixed output.

**Validation step.** Does the prompt ask Claude to verify its own output? Does it specify how Claude should confirm the output is correct? A prompt with a validation step produces self-checked output — not necessarily correct, but at least self-consistent. A prompt without a validation step may produce output that fails basic consistency checks.

Score each prompt on all four criteria (high / medium / low) before comparing outputs. The prompt that scores higher on all four criteria should produce better output. If it does not, examine the output carefully — you may be discovering a fifth criterion you had not considered.

---

## Mission 4 as a Prompt Comparison Experiment

Mission 4 — Improve With Intent — is, at a meta-level, a prompt comparison experiment. The improvement hypothesis you bring from Mission 3 is encoded in the prompt you use to run the experiment. A different hypothesis is a different prompt. The experiment evaluates the prompt as much as the algorithm.

Consider two prompt versions for Mission 4:

**Prompt Version A — vague hypothesis:**
```
The model needs better augmentation. Add some augmentation and see if it helps.
```

**Prompt Version B — specific hypothesis:**
```
The hypothesis from Mission 3 is: the model fails at tumour boundaries in
low-contrast slices because training examples with small tumour regions are
underrepresented. The proposed intervention is to add random horizontal flipping
to increase the diversity of boundary patterns in the training set.

Make exactly this one change. Fix random seed to 42. Do not change the learning
rate, model architecture, or any other training parameter.
Save the result to outputs/metrics/model_swap_comparison.json with keys
baseline_dice, new_dice, delta, change_description, hypothesis_supported.
```

Prompt Version A will produce some change to the training script, a retrain, and some result. Whether that result addresses the actual failure mode identified in Mission 3 is unknown — because the prompt did not specify which failure mode to address.

Prompt Version B produces a controlled test of a specific hypothesis. The output can be read as evidence for or against that hypothesis. The experiment is interpretable.

These are two different prompts for the "same task" (improve the model). They produce fundamentally different scientific value.

---

## Building a Prompt Library from Lab Experience

After each mission, you have at least one prompt that worked and at least one version that worked less well (or that you revised before running). Record both. Note what was different between them and why the better version was better.

Over the six missions of this course, you will accumulate a prompt library: a set of validated prompt templates for recurring research tasks, with notes on what makes each one work.

This library is transferable. The data inspection prompt you develop in Mission 2 can be adapted for any new dataset. The error analysis prompt from Mission 3 applies to any segmentation model. The study critique prompt from Mission 5 applies to any research proposal.

Researchers who treat prompt development as a methodological contribution — documenting their prompts, comparing versions, and recording what works — are developing a new form of methods expertise that will be increasingly valuable as AI tools become more embedded in research practice.

---

## The Prompt Iteration Cycle

No prompt is perfect on the first draft. The iteration cycle is:

1. **Draft the prompt** based on your understanding of the task and the criteria above.
2. **Run the prompt** and inspect the output against your intent and the output contract.
3. **Identify the weakness** in the output. Where did Claude's output diverge from your intent? Was it a specificity failure (Claude made a decision you did not intend to delegate)? An output contract failure (wrong path or key name)? A role failure (Claude mixed developer and critic outputs)?
4. **Improve the prompt** by adding the missing specification, correcting the output contract, or clarifying the role.
5. **Re-run and compare.** Does the improved prompt produce better output on the specific weakness you identified?
6. **Record the improvement.** What change made the difference?

Three iterations is a reasonable target for a mission-level prompt. A prompt that still produces poor output after three iterations has a deeper problem — usually an underspecified task or an incorrectly specified output contract. In that case, restart from the task definition.

---

## What to Record

A minimum prompt evaluation record for each mission contains:

- **Prompt text** — the verbatim text you sent
- **Output produced** — the file paths and a brief description of the content
- **Specificity score** — high / medium / low, and which decisions Claude made that you did not intend to delegate
- **Output contract compliance** — did the output appear at the correct path with the correct keys?
- **Your assessment** — did the output meet your research intent? If not, what was wrong?
- **Revised prompt** — if you iterated, what changed between versions?

This record is the first draft of a methods section for any paper that uses this AI-assisted workflow. Treat it accordingly.

!!! example "Prompt version control"
    Keep your prompt text in a file (e.g., `prompts/mission_04_v1.txt`, `prompts/mission_04_v2.txt`). After each mission, commit this file alongside the outputs it produced. This creates a version-controlled record of your prompt development, parallel to the version-controlled record of the code and outputs.

!!! tip "The five-minute audit"
    Before running any prompt, spend five minutes auditing it against the four criteria: specificity, output contract, role clarity, validation step. Add anything missing. This five minutes is more valuable than the time you would spend debugging a vague output.

!!! info "Prompts as methods"
    In conventional research, the methods section describes what you did. In AI-assisted research, the prompts you used are part of what you did. A paper that uses Claude Code to implement a training pipeline should ideally include the key prompts in supplementary materials. This is emerging practice, not yet standard — but it is the direction the field is moving.
