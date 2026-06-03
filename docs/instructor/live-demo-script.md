# Live Demo Script

!!! warning "Instructor Resource"
    This page is for instructors and teaching assistants. It contains exact prompts and demo sequences. Do not share with students before the demos are run.

Four scripted demonstrations, one per key teaching moment. Each demo is designed for a class audience watching a projected screen. Run each demo live, not from pre-recorded video — students need to see what happens when things take a moment to respond, and that realism is itself instructive.

**Before any demo:** Increase terminal font size to at least 18pt. Use a light terminal background if your room has strong ambient light. Have the lab repository open and Claude Code ready to start.

---

## Demo 1: Mission 0 — Claude Reading CLAUDE.md vs. Cold Start

**Purpose:** Show concretely why CLAUDE.md matters and what the context-setting first message does.

**Duration:** 8–10 minutes

**Setup:** Have two terminal windows open — one with CLAUDE.md in the repository, one in an empty directory (simulating a cold start). Start with the cold start window.

**Exact prompt to type (cold start — no CLAUDE.md):**

```
You are helping me with a brain tumour segmentation project.
Please list the MRI cases in my dataset and describe the first one.
```

**While Claude is running, say to the class:**
"Watch what Claude does when it has no context. It doesn't know where the data is, what format the cases are in, or what I mean by 'describe.' It will either ask me clarifying questions, or it will make assumptions — and those assumptions may be wrong."

**What to point out in the output:** Claude will either ask "where is your dataset?" or produce a generic description that does not reflect the actual data. Both are evidence of the cold-start problem. Say: "Every question Claude has to ask me is a turn I could have used for research. Every assumption it makes is a risk that the output is wrong."

---

**Now switch to the window with CLAUDE.md. Send the context-setting first message:**

```
I am beginning a lab session. My research context is in CLAUDE.md — please read it.
Confirm: (1) where the data is, (2) what my research question is, (3) what output conventions I am using.
Do not begin any task until I confirm your understanding is correct.
```

**While Claude is running, say to the class:**
"Now Claude has project memory. It knows the data path, the research question, and how I want outputs formatted. Watch how it confirms these before starting. That confirmation step is the approval loop — I am staying in control of the research."

**What to point out in the output:** Claude will correctly report the data path, research question, and output conventions from CLAUDE.md. Point out specifically: "If Claude gets any of these wrong, I correct it now — before any computation happens. This is vastly cheaper than discovering a misunderstanding after a 10-minute run."

**Closing remark:** "The first message of every session is the most important message. Write it with the same care you would write the first paragraph of a paper."

---

## Demo 2: Planner Role — Mission 2 Plan-Before-Code

**Purpose:** Show what happens when you ask Claude to plan before it codes, and why approving the plan before implementation matters.

**Duration:** 8–10 minutes

**Setup:** CLAUDE.md is set up. Data directory is visible. One BraTS case is pre-loaded.

**Exact prompt to type:**

```
Acting as a Python developer implementing a medical image processing pipeline:
Before writing any code, produce a numbered implementation plan for the following task:
Load the BraTS case at data/brats_sample/BraTS_001/. Compute the whole tumour Dice score
between the model prediction (threshold the FLAIR volume at intensity 500) and the
reference label (label values 1, 2, 4 combined). Write the result to outputs/m02_metrics.json
with keys: case_id (string), dice_wt (float), sensitivity_wt (float), specificity_wt (float).
Do not write any code until I have approved the plan.
```

**While Claude is running, say to the class:**
"I have asked for a plan, not code. Watch what Claude produces. The plan step tells me whether Claude has understood the task correctly before it writes 50 lines of Python."

**What to point out in the output:** The plan will typically include: (1) load the FLAIR volume, (2) threshold at 500 to create a binary mask, (3) load the label file, (4) binarise labels 1+2+4, (5) compute TP/FP/FN, (6) compute Dice, sensitivity, specificity, (7) write JSON. 

Say: "Now I can see the plan. Step 2 is where I should look most carefully: the threshold of 500 is my instruction, but Claude can tell me if that threshold is calibrated to the normalised intensities or the raw intensities. If I approve this plan without checking, I might get Dice scores that are meaningless because the threshold is wrong for the scale of the data. This takes me 30 seconds to catch in the plan; it would take me 10 minutes to diagnose in the code."

**Point out one deliberate issue in the plan (if Claude produces the plan correctly):** Ask the class: "Is there anything missing from this plan? What about the validation step — how will we confirm the JSON was written correctly with the right keys?" Then send a follow-up: "Please add a step: after writing the JSON, read it back and confirm all specified keys are present."

**After approval:** Send: "Plan approved. Please implement it now."

**What to point out in the output:** Show the code, then show the JSON output, then show Claude's self-verification. "Notice the three steps: plan, implement, verify. This is the minimum viable research cycle for a computational task."

---

## Demo 3: Critic Role — Mission 3 Observation to Hypothesis Prompting

**Purpose:** Show how the Inspector Role followed by the Skeptical Reviewer role produces a hypothesis, and how this differs from asking Claude to "fix the problem."

**Duration:** 8–10 minutes

**Setup:** outputs/m02_metrics.json exists with at least one case having low Dice. An error map PNG is available (pre-generated or generated live).

**Exact prompt to type (observation step):**

```
Acting as a data analyst with expertise in medical imaging:
Look at the error map image at outputs/m03_error_map_BraTS_001.png.
List every observable feature of the error pattern:
1. Location in the image (relative to brain anatomy)
2. Shape of the error regions (diffuse / focal / boundary)
3. Proportion of error that is false positive (red) vs false negative (blue)
4. Any visible relationship to specific tissue types or anatomical structures
Do not propose any explanation or fix. Only describe what you observe.
```

**While Claude is running, say to the class:**
"I am asking for observations, not explanations. This is the Inspector Role. Watch the output — Claude should produce structured observations only, no 'this is probably because' language. If it does propose an explanation, I will redirect it."

**What to point out in the output:** Point to specific observations (e.g., "FP clusters near the lateral ventricles" or "FN concentrated at the tumour boundary"). Say: "Now I have evidence. I didn't have to guess what the failure pattern was — I described it systematically."

---

**Send the hypothesis prompt:**

```
Based on the observations above, I am now forming a hypothesis.
Acting as a research advisor:
I observe that false positives cluster near the lateral ventricles.
My hypothesis is: the model is confusing the CSF-adjacent white matter signal on FLAIR
with peritumoral oedema, because both regions appear bright on FLAIR.
Is this hypothesis consistent with the observations? What additional observations
would confirm or refute it before I implement any change?
```

**While Claude is running, say to the class:**
"Now I switch from observation to hypothesis. Notice I am forming the hypothesis myself — Claude is checking it, not inventing it. This is the right division of labour: I am the scientist, Claude is a research partner who can tell me whether my hypothesis is coherent."

**What to point out in the output:** Claude should confirm or challenge the hypothesis and suggest additional checks (e.g., "look at the T1 at the same location to see if the signal pattern is distinguishable from oedema"). Say: "This is how you use the observer and critic roles together. You observe first, form a hypothesis second, and only then implement a change — in Mission 4."

---

## Demo 4: Role Switching — Mission 5 Developer to Skeptic Transition

**Purpose:** Show a complete role switch within a single session, demonstrating that the roles produce genuinely different output types and that the switch is explicit, not implicit.

**Duration:** 8–10 minutes

**Setup:** A Mission 5 study design draft exists (either a student artifact or the pre-prepared example in the instructor materials).

**Exact prompt to type (developer / study designer role, first):**

```
Acting as a clinical research study designer:
I have a brain tumour segmentation model with whole-tumour Dice 0.81 (3-case internal test).
Draft the patient population section of a prospective validation study for this model.
Include: age range, diagnosis, imaging protocol, inclusion criteria, exclusion criteria.
Write this as a methods section paragraph, not a bullet list.
```

**While Claude is running, say to the class:**
"I am in the study designer role. Watch Claude produce a methods paragraph — specific, structured, written in methods-section language. This is what the developer role does: it produces a thing. Now watch what happens when I switch to the skeptic."

**What to point out in the output:** Show the methods paragraph. Say: "This looks reasonable. But let's interrogate it."

---

**Send the role-switch prompt:**

```
Now I am switching roles. Acting as a rigorous peer reviewer of a clinical AI validation study:
Review the patient population section I just wrote above.
List the three most serious methodological weaknesses in that section.
For each weakness: state the problem and what evidence or specification would be needed to address it.
Do NOT rewrite the section. Do NOT propose solutions. Only critique.
```

**While Claude is running, say to the class:**
"Explicit role switch. Reviewer mode. Watch what happens — Claude will find problems with the methods paragraph it just wrote. This is not a bug; this is the point. The developer role optimises for producing something; the reviewer role optimises for finding what is wrong with it. You need both."

**What to point out in the output:** Claude will typically find: (1) the exclusion criteria are not specific enough (what counts as "prior treatment"?), (2) the imaging protocol is not pinned to a specific scanner or field strength, (3) there is no specification of who reads the reference labels or how inter-rater agreement is handled. Say: "Three problems. None of them would have been caught if I had just kept writing the study design without switching roles. The role switch is the quality control mechanism."

**Closing remark for the demo:** "Every time you switch from building to reviewing, you are doing peer review of your own work before anyone else sees it. It costs you two prompts. It saves you a referee report."
