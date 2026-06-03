# Classroom Workflow

## The Basic Loop

Every mission in this course follows the same cycle:

**Dashboard → Prompt → Claude Code → Artifact → Dashboard**

You open the dashboard to read the mission. You write or adapt a prompt. You paste the prompt into Claude Code. Claude Code takes actions — reading files, running scripts, writing outputs. You inspect the artifact Claude produced. You return to the dashboard to proceed.

This loop is not a coincidence. It reflects how agentic research workflows actually operate: a human specifies intent, an AI agent executes, the human inspects and judges, and the cycle continues. The course structure is itself a model of the research workflow you are learning.

---

## The Action Environment: VS Code + Claude Code

Your primary working environment is VS Code with the Claude Code extension active. This is where you type prompts and where Claude Code operates.

Claude Code is not a chatbot. It does not answer questions in a conversation window and wait for you to copy the answers somewhere. When you give Claude Code a prompt, it reads files in your project directory, runs terminal commands, writes files, and reports what it did. It takes actions on your behalf in the project environment.

This distinction matters. When you ask Claude Code to produce a data inspection report, Claude Code will:

1. Read the CLAUDE.md file to understand the project context
2. Navigate to the data directory and read the relevant files
3. Run a Python script to extract the statistics you asked for
4. Write the report to the specified output path
5. Confirm what it did

You do not need to copy and paste. You do not need to switch between a chat window and a terminal. The work happens in your project directory, and the artifacts are real files.

---

## The Dashboard: Navigation, Not Chat

The course website (this site) is your navigation interface, not your primary work interface. It contains:

- Mission descriptions and objectives
- Required prompts for each layer (Layer A, B, and C)
- Explanations of what each mission teaches
- Instructions for inspecting artifacts
- Optional extension exercises

The dashboard does not replace Claude Code. You do not type prompts into the dashboard. You read the mission here, then act in VS Code.

Think of the relationship this way: the dashboard is your research brief. Claude Code is your lab environment. You move between them, but you do your work in the lab.

---

## What CLAUDE.md Does

Every project that uses Claude Code should have a CLAUDE.md file at the project root. This file is Claude's memory of the project. When Claude Code starts a new session, it reads CLAUDE.md to understand:

- What this project is about
- Where the important files and directories are
- What it is allowed to do and what it must not do
- What the required artifact paths are
- What honesty standards apply to this project

Without a CLAUDE.md, Claude Code starts each session without context. It may write files to the wrong locations, make assumptions about the dataset that are not true, or generate reports that do not conform to the required structure.

The CLAUDE.md for this lab is pre-written and included in the project. You should read it before your first mission. Understanding what it contains will help you understand why Claude behaves the way it does and what you would need to write if you were setting up your own research project.

---

## The Student as Junior Clinical Investigator

The framing that underpins this entire course is this: you are a junior clinical investigator, not a student completing exercises.

A junior clinical investigator does not simply write code and submit it. They:

- Understand why each step is necessary before executing it
- Inspect outputs critically, not just confirmingly
- Catch errors before they propagate into downstream analyses
- Communicate findings honestly, including limitations
- Maintain a paper trail of decisions and results

This course gives you the tools to do all of these things. Claude Code handles execution. Your job is everything that requires scientific judgment.

In practice, this means: when Claude produces a data inspection report, you do not simply accept it. You open the report, read the statistics, and ask: do these numbers make sense for this dataset? Is anything missing? Is anything surprising? Only when you are satisfied that the report is accurate and complete do you proceed to the next mission.

This inspection habit is the single most important thing you will practise in this course. It is also the habit that distinguishes a competent clinical AI researcher from someone who produces impressive-looking outputs that contain silent errors.

---

## Prompts: Layer A, B, and C

The course provides three layers of prompts for each mission:

- **Layer A** prompts are ready to use. Paste them directly into Claude Code. They are fully specified with output contracts, role assignments, and validation steps. Use these if you are moving quickly or if you are new to prompting.
- **Layer B** prompts are partially specified. They give you the structure and the output contract but leave the role assignment and some specifics for you to fill in. Use these once you are comfortable with Layer A.
- **Layer C** prompts are starting points only. They describe the mission objective and leave the design of the prompt entirely to you. Use these if you want to practise prompt engineering from scratch.

You should not feel obligated to progress to Layer B or C. The mission outcomes are identical regardless of which layer you use. The difference is in how much prompting practice you get. If you have extra time, try running the same mission with a Layer A prompt and then with your own Layer C prompt, and compare the outputs.

---

## Session Structure

Each session follows a consistent rhythm:

1. **Brief (10 min)** — The instructor introduces the mission objective and clinical context. Key prompting concepts for this mission are explained.
2. **Mission work (45-60 min)** — Pairs or individuals work through the mission using Claude Code. Instructors circulate to review CLAUDE.md files, check output contracts, and ask students to articulate their hypothesis before any code change.
3. **Debrief (15 min)** — The cohort compares prompt strategies and results. Bring your best prompt and your most interesting failure.

The debrief is the most important part of each session. Comparing prompts reveals that identical tasks can produce very different outputs depending on how they are specified. This is the point — you are learning to see prompts as experimental instruments.
