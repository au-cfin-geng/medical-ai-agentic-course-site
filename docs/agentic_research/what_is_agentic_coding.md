# What Is Agentic Coding?

## Beyond Autocomplete

Most researchers encounter AI assistance in the form of autocomplete — suggestions that appear while typing, syntax hints, or tools that finish a line of code based on what comes before it. These tools are useful, but they are fundamentally passive. They respond to what you are currently writing; they do not take action on your behalf.

Agentic coding is something different in kind, not just degree. An agentic AI system can take actions: it can read files in your project, execute shell commands, write or modify code, run a training script, inspect the output, and then decide what to do next — all as part of a single task. The word "agentic" refers to this capacity for purposeful, multi-step action.

Claude Code, developed by Anthropic, is a command-line tool that brings this capability to researchers. You open a terminal in your project directory, run `claude`, and interact with it in natural language. Claude can read your entire codebase, run your scripts, check results, and make targeted edits. It is not browsing the web or accessing external services; it is working directly with the files and environment on your machine.

## An Analogy That Might Resonate

Think of it this way. Suppose you have access to a highly skilled research assistant. This person learns fast, can write Python fluently, knows the medical imaging literature, and works without complaint at 3 in the morning. They will do exactly what you ask, very quickly.

Now the important caveat: this assistant has no prior knowledge of your project. Every morning they arrive with no memory of yesterday's work. They will follow your instructions precisely — which means that if your instructions are ambiguous, they will make a reasonable guess, and it may not be the guess you wanted. Crucially, they will not push back on a bad research design. If you ask them to implement a method that will not answer your scientific question, they will implement it anyway. They are not checking whether your question is well-posed; they are only checking whether your instruction is actionable.

That is Claude Code. The scientific judgment remains yours.

## What Changes When Coding Becomes Agentic

Traditional programming puts the bottleneck at implementation: do you know the syntax? Do you know the right library? Can you debug the stack trace? For researchers without a software engineering background, this bottleneck is real and often painful.

Agentic coding shifts the bottleneck. The question is no longer "can I write this code?" The question becomes: "do I know precisely what I need, can I describe it clearly, and do I know how to verify that what I got is correct?"

This is actually a different kind of skill — and it is a skill that maps well onto scientific training. Researchers are accustomed to thinking carefully about what they want to measure, what conditions should be controlled, and what a valid result looks like. These habits of mind directly transfer to writing effective prompts.

What does not transfer automatically is the content of your domain expertise. Claude needs that as context, explicitly provided. It will not infer that your dataset has class imbalance, that your institutional protocol requires a specific train/validation split, or that the clinical meaning of a false negative in your task is far more serious than a false positive. You have to tell it.

## Three Things That Do Not Transfer Automatically

**Your domain expertise.** Claude knows medical imaging in general terms — it has been trained on a large body of text — but it does not know your specific dataset, your cohort, your acquisition protocol, or the clinical constraints of your problem. If you do not provide this context, Claude will make reasonable generic assumptions that may not apply to your situation.

**Your research goals.** Claude has no access to your scientific question, your hypotheses, your grant objectives, or the gap in the literature you are trying to fill. It only knows what you put in the prompt. A vague instruction produces output that is technically functional but scientifically arbitrary.

**Your quality standards.** What does "good enough" mean for your task? What Dice score is acceptable for your clinical application? What false positive rate would be clinically dangerous? Claude will not apply these standards unless you state them explicitly.

## AI Failure Modes You Must Know

Before you begin working with Claude Code, you should understand its known failure modes. These are not rare edge cases; they occur regularly.

**Hallucination.** Claude can produce output that is confidently stated but factually wrong. This includes fabricated citations, incorrect API function signatures, and plausible-sounding but incorrect explanations of what a piece of code does. In medical contexts, this is not a minor inconvenience; it can propagate errors into your pipeline.

**Context loss.** A Claude session has a context window — a limit on how much text it can hold in working memory at once. In a long session involving many file reads and code outputs, earlier instructions and context can effectively "drop out." Claude may contradict something it told you an hour ago without flagging the inconsistency.

**Over-eager editing.** Claude sometimes modifies files beyond the scope of what was requested. If you ask it to fix a bug in one function, it may also "improve" adjacent code you did not ask it to touch. These unrequested changes can introduce new problems.

**Plausible but logically wrong code.** This is the most dangerous failure mode for researchers. Claude can write code that is syntactically valid, runs without errors, and produces numbers — but implements the wrong logic. A metric calculation that is off by a factor, a normalisation applied in the wrong order, a data split that leaks patient information between train and validation sets. The code runs; the science is wrong.

## The Implication

Every Claude output requires human review. This is not a disclaimer to gloss over — it is the central discipline of working with agentic AI as a researcher. The goal of this course is not to teach you to generate code quickly. It is to teach you to work with Claude Code as a research partner: one that amplifies your capability while your judgment keeps the work scientifically sound.
