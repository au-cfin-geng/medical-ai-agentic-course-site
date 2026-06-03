# AI Capabilities and Limitations

This page takes an honest look at what Claude can and cannot do reliably in the context of clinical AI research. Understanding these limitations is not a caveat to be read once and forgotten — it is operational knowledge that shapes how you design every research session and interpret every output.

---

## What Claude Does Well

Claude performs reliably and with high value on the following categories of research tasks.

**Executing structured, well-specified tasks.** When the task is clear, the files are named, the output is specified, and the constraints are explicit, Claude implements and runs the task accurately and quickly. The training script modification in Mission 4 is a good example: one named file, one named change, one named output, one named constraint. Claude does this well.

**Generating boilerplate code.** Standard visualization code (matplotlib figures, error maps, comparison panels), data loading scaffolding, evaluation scripts, configuration files, and JSON serialization are tasks where Claude produces reliable output quickly. This is where the time savings of agentic research are most apparent.

**Synthesizing information from multiple files.** Reading `val_metrics.json`, `model_swap_comparison.json`, and `error_analysis.md` and producing a coherent cross-mission summary table is a task Claude handles well. The ability to read multiple files simultaneously and integrate their contents is one of the most practically useful capabilities for research.

**Explaining its own outputs.** "What does this error map tell us about where the model fails?" asked about a figure Claude generated in the same session is a question Claude answers accurately and usefully. The explanation is grounded in the actual output, not in general knowledge about segmentation models.

**Formatting and structure.** Producing correctly structured JSON, well-organized markdown reports, appropriately labelled figures, and clearly formatted comparison tables are tasks Claude does quickly and reliably.

---

## What Claude Does Unreliably

**Novel clinical judgment.** Whether a Dice score of 0.67 is clinically meaningful for the specific use case of brain tumour segmentation in a given clinical setting, whether a false positive pattern is more dangerous than a false negative pattern for a specific patient population, whether the failure mode identified in Mission 3 poses serious patient risk — these questions require clinical expertise and institutional context that Claude does not have and cannot develop from your project files.

Claude can provide a framework for thinking about these questions. It can synthesize relevant literature. It can describe the general tradeoffs between false positives and false negatives in medical imaging contexts. But the judgment — the answer for your specific model, your specific patient population, your specific clinical use case — is yours. Claude is not a reliable substitute.

**Knowing whether a model is clinically ready.** This is a specific case of the above, but important enough to call out separately. If you ask Claude "Is this model good enough to deploy in a clinical setting?", Claude will produce an answer. That answer will sound authoritative. It will be wrong, in the sense that it cannot be based on the actual clinical evidence required to make that judgment. Do not ask this question to Claude. Do not interpret Claude's answer to this question as meaningful.

**Fabricating metrics.** This is the most dangerous failure mode in agentic research, and it occurs regularly. Claude will, under some conditions, report a metric value that it did not actually compute from a real file. The value will be plausible — in the right range, consistent with other numbers, formatted correctly. Without opening the actual output file and reading the actual number, you cannot tell whether Claude reported a real value or a fabricated one.

The conditions that increase fabrication risk: asking Claude for a metric when the metric file has not been written yet; asking Claude to summarize results from files it did not read in this session; asking Claude to compare across missions without providing the file paths for both missions' metric files.

The mitigation: always require Claude to cite the exact file and key it is reading from. "What is the Dice score in `outputs/metrics/val_metrics.json` under the key `dice`?" is harder to answer with a fabrication than "What is our Dice score?"

**Staying within scope in ambiguous or long sessions.** Claude will sometimes edit files you did not ask it to edit, especially when instructions are vague or when the session is long. Common examples: editing `CLAUDE.md` to update the "Current State" section when you did not ask it to; modifying a configuration file while implementing a script change; adding an import statement to a script that was not named in the task.

The mitigation: explicit "do not touch X" instructions in every prompt; the plan-before-code pattern (which surfaces unintended edits before they happen); explicit prohibitions in `CLAUDE.md`.

**Maintaining consistency across very long sessions.** In sessions longer than 40-50 exchanges, Claude's adherence to constraints stated early in the session weakens. The random seed constraint stated in the first prompt may be forgotten by the thirtieth. The "do not overwrite the baseline file" constraint may be violated after many intermediate steps.

The mitigation: start a new session for tasks that are more than 30-40 exchanges from the original constraint statement. Re-establish context from `CLAUDE.md` at the start of every new session.

---

## The Hallucination Risk in Research

Hallucination — the generation of plausible-but-fabricated content — is a known property of large language models. In general-purpose applications, hallucination is annoying. In research applications, it is dangerous: a fabricated metric in a paper is a false research claim.

The specific hallucination risks in this course:

**Metric fabrication.** Claude reports a Dice score it did not compute from a real file. The number is in the plausible range (0.3-0.9 for a brain tumour segmentation model) and looks real. You report it without checking. It is wrong.

**Figure fabrication.** Claude describes a figure it has not generated, or describes the content of a generated figure incorrectly. "The error map shows that the model fails primarily at tumour boundaries" — is this a description of the actual figure, or Claude's prior about how segmentation models fail?

**File fabrication.** Claude reports "I have saved the results to `outputs/metrics/model_swap_comparison.json`" when in fact the file does not exist, or exists at a different path. The file was not written because the training script failed and Claude did not correctly communicate the failure.

**Citation fabrication.** In reports and memos, Claude may cite papers or clinical guidelines that do not exist, or attribute findings to papers that do not contain those findings. This is less likely in tightly constrained report tasks, but increases when Claude is asked to situate results in the broader literature.

The universal mitigation is verification: open every file, read every value, cross-check every derived metric against its source. This is described in detail in the Tool Use and Output Contracts page.

---

## The Scope Creep Risk

Scope creep occurs when Claude takes actions beyond the specified task. The most common manifestations:

- Editing `CLAUDE.md` to "update the current state" when you did not ask it to
- Modifying a configuration file in addition to the named script
- Running an additional evaluation after the specified evaluation to "double-check"
- Creating additional output files it considers "useful" beyond the specified ones

Scope creep is usually well-intentioned. Claude is trying to be helpful by updating the project state or providing additional context. But each unauthorized file modification is a potential integrity violation — it changes the project record in ways you did not specify or review.

The mitigation: in every prompt, include a "do not touch" clause that explicitly names files or directories that must not be modified. "Do not edit CLAUDE.md, do not modify data/, do not create files outside the specified paths" is a standard clause worth including in most prompts.

---

## The Optimism Bias

Claude tends to produce positive-sounding reports. Given a Dice score of 0.42 on a simple teaching dataset with a basic U-Net, Claude may write: "The model demonstrates promising performance on the teaching dataset, with a Dice score of 0.42 that represents a meaningful baseline for further development." This is not incorrect — 0.42 is indeed a baseline, and further development is indeed possible. But "promising performance" is a characterization that goes beyond what the evidence supports for a clinical application.

This optimism bias is particularly dangerous in clinical AI documentation. A clinical memo that characterizes 0.42 Dice as "promising" may create a misleading impression in a clinical collaborator who does not know what Dice scores mean for different clinical applications.

The mitigation: explicit honesty instructions in every report-generating prompt. "Do not characterize results as promising or strong without comparing them to published benchmarks on comparable datasets. If the model was only evaluated on teaching data, say so explicitly. Do not use language that implies clinical readiness." And the `CLAUDE.md` honesty requirements: "Do not overstate what was demonstrated. Conservatism is required."

---

## Why Human Scientific Judgment Is Non-Optional in Clinical AI

The failure modes described above — fabrication, scope creep, optimism bias — are not unique to clinical AI research. They occur in any research context where Claude is used. But the stakes in clinical AI are higher because the downstream consequence of an undetected error is patient harm.

A fabricated metric in a segmentation research paper leads to a false claim in the literature — serious, but correctable through replication. A fabricated metric in a clinical validation report that is used to justify deployment leads to a tool that performs below its claimed level being used on real patients. The consequences are different in kind.

This is why the course structure places human review at every step: the plan-before-code habit, the verification requirement for every output, the honesty instructions in every report prompt, the explicit limitations in the clinical memo. These are not bureaucratic requirements — they are the minimum standard for responsible clinical AI development.

Claude is a research assistant, not a clinical decision maker. The distinction is not about Claude's capability — it is about the appropriate distribution of accountability in a system where errors cost patient safety.

---

## The CLAUDE.md Honesty Requirements

The `CLAUDE.md` file in this course includes explicit honesty requirements. These are not suggestions — they are standing instructions that govern every session:

- Do not report a metric value you have not read from an actual file
- If a required output file does not exist, say so — do not generate a placeholder value
- Do not use language that implies clinical validation when only teaching-data evaluation has been done
- If the hypothesis was not supported, say so directly
- Do not write "promising results" or "strong performance" without an explicit comparison to a published reference benchmark

These requirements exist because Claude's default behavior — in the absence of explicit honesty instructions — tends toward optimism, toward confident reporting of approximate values, and toward language that overstates the clinical implications of research results.

The honesty requirements counteract this default. They are not a distrust of Claude — they are a calibration of Claude's output toward scientific standards that the research community and patient safety require.

!!! warning "Never trust a metric you haven't verified"
    If Claude reports "Dice: 0.87" but you have not opened `outputs/metrics/val_metrics.json` yourself and read the actual value, you do not know that number is real. This is not a hypothetical concern — it is a failure mode that occurs in real sessions. The verification step is not optional.

!!! warning "Clinical AI has non-negotiable human oversight"
    No agentic workflow in this course, and no AI tool currently available, is appropriate as a final decision maker for clinical AI deployment. Model evaluation, safety assessment, failure mode analysis, and deployment decisions require human clinical expertise that cannot be delegated to an AI assistant.

!!! info "A note on improvement"
    Claude is improving rapidly. The failure modes described here — fabrication, scope creep, optimism bias — are less severe in newer model versions than in earlier ones, and they will likely continue to improve. This does not change the verification requirements. A research standard that requires human verification of AI outputs is not contingent on how good the AI is — it is contingent on how important the downstream decisions are. In clinical AI, the importance is high enough that verification is always required.
