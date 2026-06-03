# Anthropic Academy Reading Map for This Course

!!! note "Disclaimer — No Course Content Reproduced"
    This course creates original clinical AI research exercises and does not reproduce or contain content from Anthropic Academy courses. The table below maps selected public Anthropic learning resources to points in this course where their concepts are practised. Students who complete the recommended reading before each mission will have a richer conceptual foundation. All resource titles listed here are public Anthropic Academy course titles; no lesson text, exercises, or proprietary materials from those courses appear anywhere in this site.

---

## About This Map

This reading map exists for one reason: to help you build mental models before you need them. Every mission in this course asks you to do something genuinely unfamiliar — write a structured prompt that controls the behaviour of an AI agent, evaluate the output of that agent against a clinical standard, and communicate your findings with appropriate uncertainty. These are not skills that come from reading alone, but reading in advance makes the doing much faster.

The Anthropic Academy courses listed below are self-paced and mostly short. None of them are prerequisites — you can complete any mission without having read anything — but students who have engaged with the relevant Academy material consistently write cleaner prompts, waste less time on role confusion, and produce more useful output contracts. The efficiency gain is real and is worth the investment of an hour or two before each day of lab work.

A second reason for this map: clinical AI sits at the intersection of technical skill and responsible practice. The Anthropic Academy resources on AI limitations and safety are not background noise. They are directly relevant to Mission 6 and to every time you make a claim about what your model can or cannot do. A researcher who has read carefully about what AI does reliably and where it makes mistakes will write a more honest translation brief than one who has not.

The map is structured in three tiers: what to read before the course begins, what to read before each block of missions, and optional advanced reading for students who want to go further. You do not need to read everything. The minimum viable reading for each mission is indicated.

---

## Before the Course Begins

These three resources build the conceptual foundation that all missions draw on. We recommend completing them in the week before the course starts, or during the preflight async period if you are reading this just before Day 1.

**Claude 101**
What Claude is, how to have productive conversations, its basic capabilities and limitations. This is the starting point for all interactions you will have in this course. Why it matters here: every mission begins with a conversation with Claude Code. Students who have completed Claude 101 arrive with a working mental model of how Claude processes instructions, which means they waste far less time writing prompts that Claude cannot act on. Relevant across all missions, but especially Missions 0, 1, and 2 where you are building your first interaction patterns.

**AI Fluency: Framework and Foundations**
A conceptual grounding in what AI can and cannot do, and how to work with AI productively. This course introduces the idea that AI fluency is a skill — learnable, improvable, and distinct from either technical expertise or general technological enthusiasm. Why it matters here: Mission 6 asks you to translate your findings to a clinical collaborator. The framework from this course gives you vocabulary for explaining AI capabilities and limitations without overselling or underselling what you built. Also relevant to the framing of every mission: you are practising AI-assisted research, not AI-automated research.

**AI Capabilities and Limitations**
What AI does reliably, where it makes mistakes, and the importance of human oversight. This is the most directly relevant pre-reading for clinical applications. Clinical AI failures are rarely random — they cluster around known patterns of model weakness. Why it matters here: critical for Mission 6, where you must document what your model cannot do. Also useful throughout for calibrating your expectations when Claude produces code or analysis that looks plausible but may be wrong. The principle of human oversight that runs through this course begins with understanding why it is necessary.

---

## During Preflight and Mission 0

**Claude Code 101**
Using Claude Code as an agentic coding partner, how CLAUDE.md works as project memory, understanding project context, and the approval loop. This is the most practically immediate reading in the map. Why it matters here: Preflight and Mission 0 are exactly about setting up the conditions for effective Claude Code use. Students who have read Claude Code 101 understand why we write CLAUDE.md the way we do, what the approval loop means for research integrity, and how to structure a first message that gives Claude enough context to work effectively. Directly applied in Preflight and Mission 0.

**Introduction to Claude Cowork**
Collaborative workflows with Claude Code, session management, and effective project context. Where Claude Code 101 introduces the tool, this resource extends it into multi-session collaborative work. Why it matters here: Missions 0 through 2 each produce artifacts that the next mission builds on. Students who understand session management maintain continuity across missions; those who do not often find that Claude loses context and repeats work or makes contradictory suggestions. Relevant to Missions 0–2 in particular, and to the overall practice of maintaining CLAUDE.md throughout the course.

---

## During Missions 1–3

**Claude Code in Action**
Hands-on application of Claude Code to real computational tasks: running code, interpreting output, debugging failures, writing output contracts. Why it matters here: Missions 1, 2, and 3 are the most computationally intensive sessions in the course. Mission 1 requires structured data inspection; Mission 2 requires implementing and evaluating a segmentation baseline; Mission 3 requires directed failure analysis. Students who have seen how Claude Code handles real computational tasks — and how it can produce plausible-looking but incorrect code — approach these missions with the right combination of trust and verification. Relevant to Missions 1, 2, and 3.

---

## During Missions 4–5

**Introduction to Agent Skills**
What agentic AI can do in multi-step research contexts: planning, tool use, delegating subtasks, and maintaining coherent behaviour across a sequence of steps. Why it matters here: Mission 4 is a controlled experiment — you propose a hypothesis, implement exactly one change, and measure the outcome. This is an agentic research cycle in miniature. Understanding the agent skill concept helps you see the mission not as a coding exercise but as a structured scientific inquiry. Mission 5, which asks you to design a prospective validation study, draws on the same multi-step planning logic at a higher level of abstraction.

**Introduction to Subagents**
Delegating specialised subtasks to AI subagents, understanding what information a subagent needs to operate effectively, and how to compose subagent outputs into a coherent result. Why it matters here: Mission 5 introduces role switching in its most explicit form — you move deliberately from developer to skeptical reviewer to clinical translator within a single session. This is conceptually analogous to working with specialised subagents, and the framework from this resource gives you a principled way to think about why role switching improves output quality.

**AI Fluency for Students**
Applying AI fluency in a learning and research context: how to use AI as a thinking partner rather than an answer machine, how to verify AI outputs, and how to maintain intellectual ownership of your work. Why it matters here: Missions 3 and 5 are the missions where students most often over-rely on Claude — asking it to interpret results without first forming their own interpretation, or asking it to design a study without first writing their own research question. This resource reinforces the student's role as the scientist and Claude's role as the instrument.

**Teaching AI Fluency**
Frameworks for thinking about AI in educational settings, including how to design activities that build genuine AI fluency rather than AI dependency. Why it matters here: Mission 5 asks you to design a study in which a human evaluator and an AI-assisted evaluator assess the same segmentation results. This is itself a study of AI in a quasi-educational setting. The frameworks from this resource are directly applicable to designing that comparison fairly.

---

## Optional Advanced Reading

These resources are not required for any mission but are recommended for students who want to extend the methods of this course into their own research.

**Building with the Claude API**
Programmatic access to Claude for research automation: calling the API directly, managing conversation context, batching requests, and handling tool use programmatically. Relevant for students who want to run large-scale evaluations using Claude as a scorer or analyst rather than through the Claude Code interactive interface.

**Introduction to Model Context Protocol**
Connecting Claude to external data sources and tools through a standardised protocol. Relevant for students who want to extend their lab pipeline to include external databases, imaging repositories, or clinical data systems.

**Model Context Protocol: Advanced Topics**
Advanced MCP patterns for research infrastructure: multi-tool composition, secure data access, and building reproducible agentic pipelines. Relevant for students building production research infrastructure beyond the scope of this two-day course.

---

## What This Course Adds

Anthropic Academy provides excellent conceptual grounding in Claude's capabilities and in the principles of agentic AI work. What this course adds is a complete clinical research context in which those concepts are exercised against real-world constraints. Rather than generic prompting exercises, every mission in this course asks you to solve a problem with clinical stakes: how do you evaluate a segmentation model fairly, communicate its limitations honestly, and design a study that would actually justify the claims you want to make? The Anthropic Academy resources tell you what these tools can do; this course asks you to discover what responsible, reproducible clinical AI research looks like when you are the researcher using them. The combination — conceptual foundation plus structured clinical practice — is the full learning objective.
