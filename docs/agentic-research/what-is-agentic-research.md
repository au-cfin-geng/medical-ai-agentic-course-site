# What Is Agentic Research?

Agentic research is what happens when an AI system moves beyond answering questions and starts taking actions in the world on your behalf — reading your files, running your scripts, inspecting the outputs, writing new files, and iterating based on what it observes. In this course, that agent is Claude Code, and the world it acts in is your clinical AI research project.

Understanding what "agentic" actually means — and what it does not mean — is the foundational concept you need before you write a single prompt.

---

## Single-Turn Prompting vs. Agentic Interaction

The simplest use of an AI assistant is single-turn: you ask a question, you receive an answer. "What is Dice loss?" produces an explanation. "Write me a Python function that computes Dice loss" produces a code block. The interaction is complete. Nothing has changed in the world — no files have been created, no scripts have run, no data has been examined.

Agentic interaction is different in kind, not just degree. When you give Claude Code an agentic task, the following can happen in a single session:

1. Claude reads your `CLAUDE.md` file to understand the project context
2. Claude reads your training script to understand how it is currently structured
3. Claude proposes a modification and waits for your approval
4. After approval, Claude writes the modified script to disk
5. Claude executes the training script in the terminal
6. Claude reads the output metrics file that the script produced
7. Claude writes a structured comparison report to a specified path
8. Claude commits the changes to git with a descriptive message

That is eight distinct actions with real consequences. Files were written. Code was executed. Outputs were produced. The project record changed. This is agentic research.

---

## What Claude Code Actually Does

Claude Code is not a chatbot with a code syntax highlighter. It is an agent with tool access. Concretely, in the context of this course, Claude Code can:

- **Read files** — any file in your project directory, including Python scripts, JSON metric files, NIfTI image headers, markdown reports, and configuration files
- **Execute terminal commands** — run Python scripts, install packages, call evaluation scripts, list directories, check file sizes
- **Write files** — create new scripts, overwrite configuration values, produce JSON output files, generate markdown reports
- **Run Python** — execute data inspection scripts, compute metrics, generate matplotlib figures, save them to specified paths
- **Commit to git** — stage files, write commit messages, create a version-controlled record of what changed and when

Each of these capabilities is governed by the permissions you set in `CLAUDE.md` and by your approval during the session. Claude proposes; you approve or redirect. You are never passive.

---

## Why This Matters for Research

The bottleneck in traditional computational research is implementation: can I write the code to test this hypothesis? This produces a well-known problem in science — researchers with strong programming skills have an inherent advantage that is unrelated to the quality of their scientific thinking.

Agentic AI shifts this bottleneck. The question is no longer "can I implement this?" The question becomes: **can I describe my research intent precisely enough for Claude to implement it correctly?**

This is a different skill — and it is a scientific skill, not a programming skill. It requires you to think clearly about:

- What exactly you want to test (the hypothesis)
- What data and files are relevant (the materials)
- What constraints must hold (what must not change)
- What output you need and in what exact format (the output contract)
- How you will verify the result (the validation step)

These are the same elements that make a scientific protocol reproducible. The researcher who cannot write a precise protocol cannot do reproducible science, regardless of whether a human or an AI is implementing it.

---

## The Lab Context: Describing What Training Must Accomplish

In this course, you do not write Python training loops line by line. You describe what the training loop must accomplish, what artifacts it must produce, and what the acceptance criteria are. Claude implements the loop. You evaluate the output against your specification.

This is not a shortcut. It is a reframing of where the intellectual work happens.

Consider Mission 4 — Improve With Intent. The task is to make exactly one change to the training pipeline, retrain, and determine whether the change improved the Dice score. A student working without agentic tools might spend three hours changing the loss function, debugging the training script, and manually extracting metrics. The intellectual work — which hypothesis to test, what constitutes a controlled experiment, what "improvement" means statistically — might occupy twenty minutes.

With Claude Code, the implementation work takes twenty minutes. The intellectual work — formulating a testable hypothesis from the error analysis in Mission 3, writing a prompt that specifies exactly one change and preserves the baseline, verifying that the comparison is valid — now occupies the full session.

The research has not been automated. The bottleneck has moved.

---

## This Does NOT Remove the Need for Scientific Judgment

Claude makes mistakes. It misunderstands context. It hallucinates plausible-sounding values that it did not actually compute. It edits files you did not ask it to edit. It writes optimistic reports that overstate what the evidence shows.

None of this is unusual or alarming — it is a description of a capable but imperfect research assistant who needs supervision. The appropriate response is not to distrust Claude entirely, and not to trust Claude uncritically. It is to verify every consequential output.

In the lab, that means:

- Every metric Claude reports: open the actual JSON file and read the actual number
- Every figure Claude claims to have generated: open the PNG file and look at it
- Every report Claude writes: compare the numbers in the report against the raw metric files
- Every code change Claude makes: read the diff before approving it

The verification requirement is not a workaround for a broken tool. It is the scientific standard that applies to any research assistant, human or AI.

---

## "Prompt-First" Does Not Mean "AI-First"

The methodology of this course is sometimes described as "prompt-first" research. This phrase can be misread.

**Prompt-first does not mean**: generate prompts and let Claude decide what research to do.

**Prompt-first means**: your research intent — the hypothesis, the evaluation criteria, the constraints, the output specification — leads every interaction. The prompt is the instrument through which your scientific thinking is transmitted to Claude. If the prompt is vague, the research is vague. If the prompt is precise, the research is precise.

The analogy is to a well-specified experiment. A researcher with a clear protocol can hand it to a lab technician and expect consistent results. A researcher with a vague intention cannot. Prompt-first research asks you to develop the discipline of clear experimental specification, because Claude cannot compensate for an underspecified research question.

!!! warning "Common misconception"
    "Claude will do my research for me." Claude will help you execute a well-specified research task. The science — the hypothesis, the evaluation criteria, the interpretation, the clinical judgment — remains yours. An AI that independently decides what research to do and what conclusions to draw is not a research assistant. It is an unreviewed paper.

!!! note "In the lab"
    Each mission in this course is structured around a specific prompt pattern that practices one agentic research skill. Mission 2 practices the data inspection role — prompting Claude to read files and report findings without taking action. Mission 3 practices the visual debugger role — generating diagnostic figures and observing before hypothesizing. Mission 4 practices the algorithm engineer role — implementing exactly one change and producing a controlled comparison. Mission 5 practices the skeptical reviewer role — attacking your own study plan. Mission 6 practices the clinical translator role — converting technical results into clinical language. Each role requires a different prompt structure, and each produces a different kind of output. The agentic research pages in this section explain the concepts behind those structures.

!!! info "A note on reproducibility"
    Because prompts are text, they are archivable. A researcher who records every prompt they used — along with the outputs those prompts produced — has created a partially reproducible record of their AI-assisted research workflow. This is analogous to a lab notebook. The Prompts as Experimental Instruments page develops this idea further.
