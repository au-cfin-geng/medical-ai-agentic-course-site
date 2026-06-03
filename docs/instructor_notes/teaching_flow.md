!!! warning "Instructor Resource"
    This section is for instructors and teaching assistants. Students may read it, but it is not required course content.

# Teaching Flow

This document describes the recommended pacing and facilitation approach for the full two-day course. It is written for instructors who are running the course for the first time, but experienced instructors will also find it useful as a pacing sanity check.

---

## Day 1: Getting Hands On First

### Opening the Course (20 minutes maximum)

Resist the temptation to open with a long lecture about what AI is, what large language models do, or what the history of brain tumour segmentation looks like. Students already know some version of this. The opening should answer three questions in under 20 minutes:

1. **Why is this course different from other courses about AI in medicine?** The honest answer: most courses teach you to use AI as a user of existing tools (APIs, pre-trained models, point-and-click interfaces). This course teaches you to work with AI as a research collaborator — where you are responsible for the scientific judgment and the AI is responsible for scaffolding the implementation. That is a different cognitive stance and it requires practice.

2. **What is "prompt-first research" and why does it matter?** The framing that works well in practice: a prompt is a protocol. In wet lab research, a protocol describes exactly what you will do, in what order, with what materials, so that someone else can reproduce it. A prompt to an AI coding assistant serves the same function. If your prompt is vague, your protocol is vague, and your results are not reproducible. If your prompt is precise, you have a record of what you asked for, what you got, and why.

3. **What will we actually do over the next two days?** Walk through the 7 missions on the mission overview page. Do not explain each mission in detail — just name them and describe the arc: set up, first results, understand failures, try to improve, design a study, translate to a clinical context. Students should understand they are doing end-to-end research in miniature, not isolated exercises.

Keep this to 20 minutes. If you run over, cut the detail, not the framing. The framing is the course.

### Why to Do Mission 0 Without Lecture First

Send students directly to Mission 0 before any further instruction. Do not explain how Claude Code works, what a CLAUDE.md file is, or what a "good prompt" looks like. Let them experience the tool cold.

The pedagogical reason: students who have never used an agentic coding tool need to encounter the discomfort of a vague prompt before they can appreciate the principle of a specific one. If you explain the principle first, they nod and move on. If they type "set up the lab" and get a generic response, and then watch the instructor type a contextualised, scoped prompt and get exactly what was needed — they understand the principle through contrast, not description.

Mission 0 is short by design. It should take 20-30 minutes for most students. Let it run in parallel with the live demo (see Live Demo Script).

### Debriefing Mission 0

After most students have finished Mission 0, bring the room together for a 10-minute debrief. The only two questions you need:

- "What did Claude do that you expected?"
- "What did Claude do that surprised you?"

The answers you are listening for (but should not say first): students will notice Claude reads files before responding; students will notice it writes real code, not pseudocode; students will notice that when they gave it a vague prompt, it either asked a clarifying question or guessed incorrectly. These observations set up the rest of the course.

If no one mentions the CLAUDE.md file, point to it explicitly: "Did anyone look at this file? This is your project's instruction manual for the AI. The better this file describes your project, the more useful Claude becomes. Think of it as onboarding documentation for a new collaborator."

### MRI Lecture Approach

Use the MRI Cheat Sheet rather than a slide deck. The reason: a slide deck tempts you to lecture at the class; a cheat sheet forces you to ask what students already know and build from there.

Open with a question: "Who here has read an MRI scan in a clinical context?" Wait for hands. "Who here has used MRI data in a research context?" Wait again. "Who has never worked with MRI data before?" All three groups will be in the room. You now know your audience distribution and can calibrate accordingly.

Cover the three concepts that are genuinely needed for the lab missions:
1. What FLAIR, T1, T1ce, and T2 sequences show, and why tumour segmentation uses multiple sequences together.
2. What a label/mask is and how it relates to the original scan — specifically, that the mask is the same size as the scan in voxels, and that each voxel has a class label.
3. What voxel spacing means and why it matters for preprocessing.

Everything else in the cheat sheet is reference material. Students do not need to memorise MRI physics to run the lab; they need enough conceptual grounding to interpret what they are seeing in the data dashboard.

The lecture should take 20-25 minutes. If clinical students are asking deep questions about MRI sequences, invite them to explain to the group — they will often give better explanations than you can.

### Pacing Mission 1 and Mission 2

Mission 1 (environment setup and data inspection) will take very different amounts of time depending on background:

- **Technical students** (computational biology, CS, bioinformatics): typically 20-30 minutes including the extension exercises.
- **Clinical students** (medical doctors, nurses, clinical researchers): often 45-60 minutes, and may need help distinguishing a file path error from a conceptual misunderstanding.

Do not wait for everyone to finish Mission 1 before starting Mission 2. Instead, pair fast-finishing technical students with clinical students who are still working through Mission 1. This is deliberate: technical students practice explaining; clinical students get timely help; both benefit.

Mission 2 (training the first model) has a natural waiting period while the model trains. Use that time for a mini-lecture or discussion. Do not fill the waiting time with more content — students need it to review what they have submitted to the training script and to start thinking about what they expect to see in the results.

### Framing Mission 2 Results

When Mission 2 finishes and students see their Dice scores, the reflex response is to compare numbers. Redirect this immediately.

The framing that works: "The number is not your result. Your process is your result. Did you describe what you were going to do before you did it? Did you check that Claude actually did what you asked? Did you record what you changed and why? If yes, you have done research. If no, you have run a computation."

There is no such thing as a bad Dice score in Mission 2. A Dice of 0.45 and a Dice of 0.72 are both valid starting points for Mission 3. What matters is that the student can explain the number — what the model was trained on, what it was evaluated on, whether the split was correct. If they cannot explain it, they need to go back and check.

Explicitly: do not rank or compare Dice scores across groups at this stage. This is not a competition and treating it like one trains the wrong instinct.

---

## Day 2: Going Deeper

### Error Analysis Lecture

The error analysis lecture should be fully interactive. Do not describe failure modes in the abstract — show real examples and ask students to hypothesise before you reveal the explanation.

Suggested format:
1. Show a failure image (tumour boundary missed, false positive in white matter, complete miss of a small lesion).
2. Ask: "What do you think caused this? What would you look at to find out?"
3. Wait for responses. Write them on the whiteboard.
4. Then reveal: what the actual cause was (if known), and how you would investigate it systematically.

This models the core intellectual behaviour of Mission 3 — moving from observation to hypothesis to investigation. If students see you do it before they do it, they are more likely to do it well.

Common failure patterns that make excellent examples:
- Complete miss of small enhancing lesions (under-representation in training data, or loss function dominated by the large edema class).
- Boundary inaccuracy (the model is right about where the tumour is, wrong about how far it extends — often a training resolution issue).
- False positives in white matter lesion patients (the model has never seen non-tumour white matter lesions and over-activates).
- Generalisation failures across scanner manufacturers (a model trained on Siemens scanners failing on Philips scanners is a real and important failure mode).

### Mission 4: Holding Students to One Change

Mission 4 is the hardest mission pedagogically, not technically. Students who have completed a good error analysis arrive at Mission 4 with three to five potential improvements they want to try. They will try to implement all of them at once.

Hold them firmly to one change. The reason: if you change three things simultaneously and your Dice goes up by 0.03, you have learned nothing. You do not know which change caused the improvement, whether the changes interact, or whether you would get the same result on a different dataset. One change, clearly motivated by the error analysis, clearly documented, is a publishable observation. Three simultaneous changes is a noise experiment.

The phrasing that works: "Show me your error analysis. What is the single most important failure mode? If you could fix one thing, what would it be? Good. Change only that. If you have time after, we can talk about whether a second change is warranted."

If students push back and say "but what if the first change doesn't work?", that is fine — a negative result is a result. The hypothesis was tested and falsified. That is science.

### Missions 5 and 6 in Pairs or Small Groups

Missions 5 and 6 (study design and clinical translation) are the most intellectually demanding missions in the course, and they work significantly better in pairs or small groups than as solo exercises.

The reason: Mission 5 asks students to design a study to validate the model. This requires thinking about what "validation" means in a clinical context, what the appropriate comparator is, what outcome measures matter to clinicians, and what the power calculation would look like. Computational students typically have the methods vocabulary but not the clinical intuition. Clinical students have the reverse. The output is better when both perspectives are present.

Suggested grouping: if you paired technical and clinical students for Missions 3-5, keep those pairs together for Missions 5 and 6. If students worked solo, now is the time to form pairs explicitly.

### Showcase Format

The showcase is the conclusion of the course. It should take 30-45 minutes depending on group size.

The format recommendation: **each group presents their best artifact and their most interesting failure** — not their highest Dice score, not their most impressive chart. The best artifact is the thing they are most proud of having produced. The most interesting failure is the thing they learned the most from.

This framing has a specific purpose: it normalises failure as a source of learning, which is the correct scientific attitude toward negative results. It also rewards good analysis over lucky results.

See the Student Showcase Ideas page for specific format options and judging criteria.

### What to Prioritise If Time Is Short

If Day 2 is running behind:

- **Non-negotiable**: every student should reach Mission 3 (error analysis). This is the pedagogical core of the course. A student who sets up the environment, trains a model, and analyses its failures has completed the core learning arc. Everything else is extension.
- **Deprioritise**: the deep dive on Mission 5 or 6 can be assigned as async work after the course. The reflection questions in both missions are well-suited to independent work.
- **Do not rush Mission 3** to fit more in. A hurried error analysis teaches the wrong habit. If you have to cut time somewhere, cut from the showcase.
- The reflection questions throughout the course can always be completed asynchronously. They are designed for individual reflection and do not benefit from being rushed in the room.

---

## General Facilitation Notes

- **Move around the room** during lab time. Students who are stuck will not always raise their hand. Circulate every 15 minutes.
- **Read prompts over students' shoulders** (with permission). The most common issue is a vague prompt that gets an uninspiring result. A quick prompt review takes 60 seconds and redirects the student immediately.
- **Watch for students accepting Claude's first response** without verification. This is the most important bad habit to catch early. The correction: "How do you know that's correct? Did you check the output?"
- **Encourage students to narrate their reasoning to Claude** before asking for code. "Describe what you're about to ask before you type it. Then ask." This usually improves prompt quality immediately.
