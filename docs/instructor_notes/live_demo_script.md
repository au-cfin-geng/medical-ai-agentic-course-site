!!! warning "Instructor Resource"
    This section is for instructors and teaching assistants. Students may read it, but it is not required course content.

# Live Demo Script

This document provides word-for-word guidance for the three live demonstrations delivered during the course. Each demo is timed and scripted at the level of detail that lets a first-time instructor run it confidently. Adapt the phrasing to your own voice — the goal is the principle, not the script.

All demos assume you are projecting your terminal on a screen large enough to be readable from the back of the room. Increase your font size before the session (18pt minimum in the terminal; 20pt is better for a large room).

---

## Demo 1: Mission 0 Opening Demo

**When**: Immediately after the course opening, before students start Mission 0.
**Duration**: 10 minutes.
**Goal**: Show the contrast between a vague prompt and a well-contextualised prompt. Set up the concept that will run through the entire course.

### Setup (before students arrive)

Have the lab repo cloned and the terminal positioned in the repo root. Have the CLAUDE.md file visible in a text editor in another window. Do not open Claude Code yet.

### Step 1: Open the terminal (1 minute)

Say: "Let me show you what this tool actually looks like before you use it. Everything I'm going to do, you will do yourself in the next 30 minutes."

Navigate to the repo:
```
cd ~/medical-ai-lab
ls
```

Say: "Here is what the lab repository looks like. There are directories for data, models, scripts, and a file called CLAUDE.md. Before I open Claude, I want you to look at this file for a moment."

Switch to the text editor showing CLAUDE.md.

Say: "This file is the project's instruction manual for Claude. It describes what the project is, what the existing code does, and what conventions to follow. When you open Claude in this directory, it reads this file first. Think of it as onboarding documentation for a new collaborator."

### Step 2: Bad prompt (3 minutes)

Return to the terminal. Open Claude:
```
claude
```

Wait for the prompt. Type slowly so the audience can read:
```
help me set up the lab
```

Press Enter. Let Claude respond. Do not interrupt while it is running.

When the response appears, say: "Look at what happened. Claude gave me something — probably some generic setup steps. But did it actually help? Let me ask: does this response mention our specific data directory? Does it mention the specific model architecture we're using? Does it mention the BRATS dataset?"

Pause. The answer will be no, or only vaguely.

Say: "This is what a vague prompt produces. The response is not wrong. It is just not about our project. Claude has no way of knowing what 'set up the lab' means unless we tell it."

### Step 3: Good prompt (4 minutes)

Clear the session or start a new one. Say: "Now let me show you what a specific prompt looks like."

Type (slowly, talking through each element as you type):
```
I am working on the brain tumour segmentation lab. The lab repo is at ~/medical-ai-lab. I need to verify that:
1. The Python environment is active and the correct packages are installed
2. The training data directory contains the expected BraTS subject folders
3. The model file at models/unet.py can be imported without errors

Check each of these three things and tell me which ones pass and which ones fail. Do not install anything or change any files.
```

Press Enter. While Claude is reading files and running checks, narrate what it is doing.

Say: "Notice what it is doing right now — it is reading files, not 'thinking.' When Claude appears to pause, it is typically reading a file, running a command, or waiting for a subprocess. It is not generating text. This matters because it means you can look at what it is reading and check whether it is looking at the right thing."

Point to the output as it appears: "Look at this — it found the data directory and listed the subject folders. It imported the model and there was no error. It checked the package versions. This is a verification report, not a generic suggestion."

Say: "The difference between those two prompts is not about vocabulary or tricks. It is about being specific: what project are you in, what do you want to check, what are the constraints? That is the principle we will use for the whole course."

### Step 4: What to say next (1 minute)

Say: "Now you will do this yourself. Mission 0 walks you through your first interaction with Claude Code. The goal is not to produce a perfect prompt — the goal is to notice the difference between a specific prompt and a vague one. You have 25-30 minutes. I will be walking around. Go."

---

## Demo 2: Planner Role (Mission 2 Introduction)

**When**: Before students start Mission 2 (writing the training script).
**Duration**: 5 minutes.
**Goal**: Introduce the Planner pattern — asking Claude to describe a plan before writing any code, and reviewing the plan as a team before approving it.

### Context

By this point, students have completed Mission 0 and Mission 1. They understand basic Claude interaction. Mission 2 asks them to use Claude to write a training script. The risk: students will immediately ask Claude to write the entire training script in one shot, accept the first version, run it, and then not understand what it did.

The Planner pattern prevents this.

### Demo script

Say: "Before any of you types 'write me a training script' — stop. I want to show you a different way to approach this."

Open a new Claude session in the terminal. Say: "The pattern I'm going to show you is called the Planner pattern. The idea is: before Claude writes any code, it describes what it is going to do, step by step. You review the plan. You approve it. Then it executes."

Type the following prompt, reading it aloud as you type:

```
Before writing any code, describe in steps how you would implement a training script for brain tumour segmentation using the existing model in models/unet.py and the dataloader in data/dataloader.py.

For each step, list:
- What the step does
- Which existing file it uses or modifies
- Any decision you are making that I should know about (for example, which loss function, which optimizer, what learning rate)

Do not write any code yet. Wait for my approval before proceeding.
```

Press Enter. While Claude responds, say: "Watch the output. It is describing a plan, not writing code. This is deliberate."

When the plan appears, turn to the audience. Say: "Now I want you to do what a research supervisor would do: review this plan. Does the loss function make sense for multi-class segmentation? Does the optimizer choice need justification? Are there any decisions Claude made that you would make differently?"

Take 1-2 responses from the audience. Engage with them briefly.

Say: "This is the conversation you should have with Claude before it writes a single line. Your role here is scientific: you are the person who knows whether the plan is sensible. Claude's role is implementation. You review; it executes. This is how you stay in control of the research."

Close the demo. Say: "When you start Mission 2, use this pattern. Ask for a plan first. Review it. Then approve it. Mission 2 walks you through the exact prompts to use."

---

## Demo 3: Critic Role (Mission 3 Introduction)

**When**: Before students start Mission 3 (error analysis).
**Duration**: 5 minutes.
**Goal**: Introduce the Critic pattern — asking Claude to analyse evaluation metrics and identify failure patterns, then critically examining Claude's analysis together.

### Context

Students now have Mission 2 results: a Dice score, some training curves, and a trained model. Mission 3 asks them to analyse the model's failures. The risk: students will either (a) accept a low Dice score and move on without analysis, or (b) ask Claude to "improve the model" without first understanding what is failing.

The Critic pattern is the corrective.

### Demo script

Prepare a short paste of example evaluation metrics. Use fabricated but realistic numbers:

```
Evaluation results:
- Mean Dice (whole tumour): 0.71
- Mean Dice (tumour core): 0.58
- Mean Dice (enhancing tumour): 0.41
- Worst cases: subjects BraTS_001, BraTS_047, BraTS_112
- Best cases: subjects BraTS_023, BraTS_056, BraTS_099
- Training loss at convergence: 0.31
- Validation loss at convergence: 0.44
```

Say: "Here are some example results. I'm going to ask Claude to be a critic — not to celebrate what worked, but to identify what failed and why."

Type the following:

```
Here are the evaluation results from a brain tumour segmentation model trained on BraTS 2021 data:

[paste the metrics above]

Act as a critical scientific reviewer. For each sub-region (whole tumour, tumour core, enhancing tumour):
1. Is this Dice score acceptable for clinical use? Why or why not?
2. What are the most likely explanations for the performance difference between sub-regions?
3. What would you look at first to investigate the worst-performing cases?

Be specific. Do not describe what Dice measures — assume I know that. Focus on what these particular numbers tell us about where the model is failing.
```

Let Claude respond. When it finishes, say: "Now let me ask you: is this a good analysis? What is Claude getting right? What is it missing?"

Wait for responses. Common correct observations from students:
- Claude correctly notes the gap between whole tumour and enhancing tumour performance.
- Claude may correctly identify that enhancing tumour is the hardest sub-region to segment.
- Claude may miss that the training/validation loss gap (0.31 vs 0.44) suggests some degree of overfitting.
- Claude cannot know what the worst-case subjects look like — that requires human inspection of the actual images.

Say: "This is the key limitation you will encounter throughout Mission 3. Claude can analyse numbers. It cannot look at an image. It cannot see whether the failure on BraTS_001 is a boundary error or a complete miss. That requires you — the researcher — to open those images in the dashboard and look."

Say: "Mission 3 uses this Critic pattern throughout. You give Claude the metrics; Claude gives you a structured analysis; you go verify the claims by looking at the actual failure cases. That combination — AI analysis plus human inspection — is more powerful than either alone."

Close the demo. Say: "When you open Mission 3, you'll find the specific prompts built into the mission steps. But the underlying pattern is always: give Claude structured data, ask for a critical analysis, then verify the claims yourself."

---

## General Demo Notes

- **Font size**: 18pt minimum in the terminal. Check from the back of the room before starting.
- **Typing speed**: type slowly enough that the audience can read what you are typing. Narrate each element as you type it.
- **Do not edit typos in real time**: if you make a small error while typing, finish the prompt and note the error. Editing mid-prompt breaks the audience's reading flow. Use the typo as a teaching moment: "I just made an error — does that matter? Let's see what Claude does with it."
- **Let Claude run fully before commenting**: do not start talking over Claude's output. Wait for it to finish, then respond. This models the behaviour you want from students: read the full output before reacting.
- **Keep a backup**: have the prompts above saved in a text file you can paste from if you lose your place. A live demo that stalls for 90 seconds while you reconstruct a prompt from memory is not a good use of time.
- **If Claude gives an unexpected response**: treat it as a teaching moment. "That's not what I expected. Let me look at why. What did I ask for? What did I get? What's different?" This models the correct research behaviour: interrogate unexpected results, do not ignore them.
