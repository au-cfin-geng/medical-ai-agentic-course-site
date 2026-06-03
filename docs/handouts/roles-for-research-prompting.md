# Roles for Research Prompting

> **For print:** File → Print → Save as PDF. Reference during every lab session. Switch roles explicitly — do not combine roles in one prompt.

Each role activates a different mode of reasoning in Claude. The role is declared in the first line of your prompt. Switching between roles across prompts — rather than asking Claude to "be everything at once" — is the single most effective technique for producing usable, verifiable research outputs.

---

## Role Reference Table

| Role | When to use | Example prompt starter | Mission |
|---|---|---|---|
| **Developer** | Implementing a specific algorithm, script, or data pipeline. You know what you want built. | "Acting as a Python developer implementing a medical image processing pipeline..." | M0–M4 |
| **Data Inspector** | Observing data structure, statistics, or quality without drawing conclusions or writing code. | "Acting as a data analyst with expertise in medical imaging, inspect and describe..." | M1, M3 |
| **Visual Debugger** | Producing error maps, slice overlays, intensity histograms, or annotated visualisations. | "Acting as a medical imaging visualisation expert, create a plot showing..." | M3 |
| **Algorithm Engineer** | Proposing and implementing exactly one algorithmic change in the context of a controlled experiment. | "Acting as an ML engineer specialising in segmentation, implement the following single change..." | M4 |
| **Skeptical Reviewer** | Finding weaknesses in your approach, your results, or your study design. No solutions — only critique. | "Acting as a rigorous peer reviewer of a clinical AI study, identify the three most serious weaknesses in..." | M5 |
| **Clinical Translator** | Converting technical findings into plain language suitable for a clinical collaborator. No ML jargon without definition. | "Acting as a clinical AI consultant advising on deployment readiness, write a translation of..." | M6 |
| **Devil's Advocate** | Challenging your hypothesis before you commit to implementing it. Argues for why you might be wrong. | "Acting as devil's advocate, argue against the following hypothesis before I implement it..." | M5 |

---

## How Roles Work

A role prefix tells Claude which type of reasoning to prioritise and which outputs to avoid. Without a role, Claude will try to be helpful in whatever way seems most natural — which often means mixing observation, code, and interpretation in a single response that is difficult to verify.

**Developer role** suppresses unnecessary explanation and produces code with a concrete output. Use it when you know exactly what you want built and you will verify the result against your output contract.

**Data Inspector role** suppresses code and solution proposals. Use it when you want to see what is in your data before you have formed a hypothesis. The observation → hypothesis → implementation sequence only works if you genuinely observe first.

**Visual Debugger role** suppresses written analysis and produces an image or plot. Use it to see failure patterns that are invisible in a table of Dice scores. A spatial error map showing that false positives cluster near the lateral ventricles is a finding that a table cannot convey.

**Algorithm Engineer role** suppresses broad exploration and focuses on one change. Use it in Mission 4 when your hypothesis is already formed and you want exactly one implementation, not a menu of options.

**Skeptical Reviewer role** suppresses positive framing and solution proposals. Use it after you have a result you are pleased with — this is when you are least likely to find your own flaws. The output should be a ranked list of concerns, not suggestions for improvement. If you want suggestions, that is a subsequent prompt with a different role.

**Clinical Translator role** suppresses technical framing and enforces plain language. Use it when writing for a clinical audience. Pair it with the Honesty Constraint pattern (see Prompt Patterns handout) to ensure the translation does not overstate what your system can do.

**Devil's Advocate role** suppresses agreement. Use it before you commit to Mission 4's controlled experiment. A devil's advocate prompt asking "why might my hypothesis be wrong?" before you implement the change is a low-cost way to discover whether your hypothesis is well-formed. If Claude can easily generate three strong counterarguments, your hypothesis probably needs sharpening.

---

## Role Switching Protocol

1. Finish the current task and confirm the artifact is written.
2. Explicitly signal the role switch in the next prompt's first line.
3. Do not assume Claude remembers which role it was in. State it every time.
4. Never ask Claude to "switch to reviewer while also fixing the code." Critique and implementation are separate prompts.

**Example switch sequence:**

```
[Prompt 1 — Developer role]
Acting as a Python developer, implement the Dice computation for case BraTS_001...
Output contract: write to outputs/m02_metrics.json...

[Prompt 2 — Data Inspector role, after confirming the file was written]
Acting as a data analyst, inspect outputs/m02_metrics.json.
Report: which case has the lowest whole tumour Dice? What is the Dice value?
Do not write code. Do not propose improvements.

[Prompt 3 — Skeptical Reviewer role]
Acting as a rigorous peer reviewer, identify the two most serious weaknesses
in the evaluation I just ran. Do not propose fixes.
```
