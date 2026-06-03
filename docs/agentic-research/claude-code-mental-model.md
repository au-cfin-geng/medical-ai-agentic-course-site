# Claude Code — Your Research Partner

Working effectively with Claude Code requires a practical mental model of what Claude knows, what it can do, and where it will fail you. This page builds that mental model from the ground up. Read it before your first lab session, and revisit it when something goes wrong.

---

## What Happens When You Open Claude Code

When you start a Claude Code session in your project directory, the first thing Claude does is read your `CLAUDE.md` file. This file is the standing instruction set for the project — it tells Claude what the project is, what it has accomplished so far, what directories contain what, what files it must not touch, and what the required output paths are.

If `CLAUDE.md` is missing or empty, Claude starts with no project context. It will try to infer context from the files it can see, but it will be working without a map. The quality of that inference is unpredictable, and you will spend the first several minutes of every session correcting misunderstandings.

If `CLAUDE.md` is present and well-written, Claude begins with an accurate model of the project. The first prompt of every session can immediately address the research task at hand rather than establishing context from scratch.

This is why the very first step in the lab is to read and understand the `CLAUDE.md` file before you touch Claude Code.

---

## The Session Lifecycle: Context Is Fresh, Not Persistent

This is the most important practical fact about Claude Code: **Claude has no memory between sessions.** When you close a Claude Code session and open a new one, Claude starts from zero. It does not remember what you discussed, what files it modified, what hypotheses you considered, or what decisions you made.

The only memory that persists between sessions is the contents of the files in your project directory. Everything Claude needs to know about the project's history must be encoded in files — primarily in `CLAUDE.md`, but also in your reports, your metric files, and any session notes you keep.

This has practical consequences:

- If you want Claude to know that the baseline Dice score is 0.42, that value must be in a file Claude can read (such as `outputs/metrics/val_metrics.json`), or you must provide it in the first prompt of each session.
- If you made an important decision in a previous session — for example, to fix the random seed to 42 — that constraint must be in `CLAUDE.md`, or Claude will not know about it.
- If Claude makes a mistake in one session and you correct it, Claude will make the same mistake in the next session unless you record the correction somewhere Claude will read it.
- If you finish Mission 3 and come back the next day for Mission 4, Claude does not know Mission 3 happened. The `CLAUDE.md` file and the artifacts produced in Mission 3 are what Claude will learn from — nothing else.

The `CLAUDE.md` file exists precisely to solve this problem. It is the bridge between sessions.

---

## The Approval Loop: You Are Never Passive

Claude Code operates in an approval loop. Before taking any consequential action — writing a file, running a script, modifying existing code — Claude proposes the action and waits for your approval. You can approve, redirect, or ask for clarification.

This is the single most important safeguard in agentic research. The approval loop means that:

- Claude cannot modify files without your knowledge
- Claude cannot run scripts without your awareness
- You can catch misunderstandings before they become mistakes in the project record

The approval loop is only effective if you actually read the proposals. A common failure mode is approving Claude's plan quickly without reading it, because the session feels routine. This is how Claude edits a file you did not intend to touch, or runs an experiment with the wrong parameters, or generates an output at the wrong file path that the autograder will not find.

The habit to develop: before approving any action, read the specific files and parameters Claude has named. Make sure they match your intent.

---

## What Claude Is Good At

Claude performs reliably on tasks that are well-structured and verifiable:

**Running structured tasks.** "Read `scripts/run_train.py`, add exactly this one line of code at line 47, run the script, and save the output metrics to `outputs/metrics/augmentation_test.json`." Claude is excellent at this. The task is specific, the files are named, the output location is specified.

**Synthesizing information from multiple files.** "Read `outputs/metrics/val_metrics.json`, `outputs/metrics/model_swap_comparison.json`, and `reports/error_analysis.md`. Produce a summary table comparing the Dice scores across missions." Claude is good at reading multiple files and producing a coherent synthesis.

**Generating boilerplate.** "Generate a matplotlib figure with four panels, each labelled, with a colour bar on the error map panel." Claude writes good boilerplate for standard scientific visualization tasks.

**Explaining its own outputs.** "What does this error map tell us about the failure mode?" Claude is helpful for interpreting outputs it has generated, as long as you verify the interpretation against the actual figure.

**Formatting outputs.** "Reformat this JSON file with these exact keys in this exact structure." Claude handles output formatting reliably.

**Writing clinical translation prose.** As practiced in Mission 6, Claude is effective at rewriting technical results for a clinical audience, given explicit audience constraints and honesty requirements.

---

## What Claude Is Not Reliable For

Understanding Claude's failure modes is as important as understanding its capabilities.

**Novel clinical judgment.** Whether a model is ready for clinical deployment, whether a failure pattern poses serious patient risk, whether a Dice score of 0.65 is acceptable for a specific clinical application — these are questions that require clinical expertise, institutional context, and ethical judgment that Claude does not possess. Claude can synthesize relevant information. It cannot make the judgment.

**Deciding whether a model is "clinically ready."** Claude will often write positive-sounding assessments if asked a leading question. "Is this model good enough to deploy?" is a question Claude should not be asked, and whose answer you should not trust.

**Fabricating metrics.** Claude can and does report plausible-sounding metrics that it did not actually compute. "The Dice score improved from 0.42 to 0.61" might be a real result Claude computed, or it might be a plausible-sounding number Claude generated based on its training data. Without opening the actual output file, you cannot tell which it is.

**Staying within scope in long sessions.** Given vague instructions and a long session, Claude may edit files it was not asked to edit, add features that were not requested, or drift away from the specified task. Mitigation: use the plan-before-code pattern and re-read `CLAUDE.md` at the start of each session.

**Knowing things outside its training cutoff.** Recent papers, clinical guidelines updated after Claude's training cutoff, and institution-specific protocols are not in Claude's knowledge. Do not ask Claude to assess whether your approach is consistent with current clinical standards — consult the primary sources.

---

## The Verification Imperative

Every consequential output Claude produces must be independently verified by you before it is recorded in the project or reported to anyone else. This is not optional, and it is not a workaround for a broken tool — it is the appropriate scientific standard.

Concretely:

- **Every file Claude claims to have written:** open the file in a text editor or viewer. Read it. Confirm it contains what Claude said it contains.
- **Every metric Claude reports:** find the source JSON file. Open it. Read the number. Confirm it matches what Claude reported.
- **Every figure Claude generates:** open the PNG file. Look at it. Confirm it shows what Claude described.
- **Every report Claude writes:** read the numbers in the report and cross-check them against the raw metric files. A discrepancy means Claude fabricated or misread a number.
- **Every code change Claude makes:** read the diff before approving it. Confirm the change matches your specification and does not touch files you did not intend to modify.

In Mission 4, this means opening `outputs/metrics/model_swap_comparison.json` and confirming that `baseline_dice` matches the value in `outputs/metrics/val_metrics.json` to at least two decimal places. If they differ, the comparison is not controlled, regardless of what Claude says.

---

## What the CLAUDE.md File Does

`CLAUDE.md` acts as a standing instruction set that shapes every session. Every time Claude Code starts a session, it reads this file first. A well-written `CLAUDE.md`:

- Establishes the project identity (what this is and what it is trying to accomplish)
- Maps the directory structure (what is in each key folder)
- States what Claude should not do (which files it must not edit, which directories it must not touch)
- States the required output paths (exactly where graded artifacts must be saved)
- States honesty requirements (Claude must not overstate what was demonstrated; if a metric file does not exist, it must say so)
- Records important decisions from previous sessions (the random seed, the baseline Dice score, the hypothesis being tested)

The `CLAUDE.md — Project Memory` page covers this in detail. For now, the key point is: the quality of your CLAUDE.md directly determines the quality of your sessions.

---

## The "Plan Before Code" Habit

This is the single most valuable habit you can develop in this course.

Before every code-writing task, start with a prompt that asks Claude to describe its approach in numbered steps without writing any code. This surfaces misunderstandings at the planning stage, before they are embedded in files and have to be undone.

The plan-before-code prompt looks like this:

```
Before writing any code, describe your plan in numbered steps:
1. Which files will you read?
2. What exactly will you change?
3. Which files will you create or modify?
4. What will you NOT touch?
5. How will you verify the output is correct?

Do not write any code until I approve this plan.
```

When Claude responds with a plan, read it carefully. Ask yourself: does this match my intent? Are there files named here that I did not expect? Is there a step missing that I expected to see? Are the output paths correct? If anything is off, redirect now — before a single line of code is written.

This adds perhaps five minutes to the start of a task. It saves twenty minutes of debugging and file-restoration later. In Mission 4, it is the primary mechanism for enforcing the "one change only" constraint — if Claude's plan describes two changes, you catch it before the code is written.

!!! tip "Before every session"
    Start with: "Read CLAUDE.md and summarize in two sentences what this project is and what I am trying to accomplish today." This confirms Claude has loaded the right context before you give it any task. If Claude's summary is wrong or incomplete, correct it before proceeding. A session built on wrong context produces wrong outputs.

!!! info "The research assistant analogy"
    Think of Claude Code as a highly capable research assistant who has read every paper in your project folder and can implement code quickly and accurately — but who needs clear instructions, cannot exercise clinical judgment, and will confidently report things that turn out to be wrong. A good PI gives a good RA clear protocols, reviews their outputs, and does not delegate scientific judgment to them. The same standards apply here.

!!! warning "Long session drift"
    After a session exceeds roughly 30-40 exchanges, Claude's attention to constraints in the original prompt weakens. If you are in a long session and Claude starts doing things that seem slightly off-specification, start a new session and re-establish context from `CLAUDE.md`. It is faster than trying to redirect a confused long session.
