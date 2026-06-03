!!! warning "Instructor Resource"
    This section is for instructors and teaching assistants. Students may read it, but it is not required course content.

# Student Showcase Ideas

The showcase is the closing activity of the course. Its purpose is not to declare a winner or rank performance — it is to give students practice communicating scientific results under the same constraints that apply in real research settings: limited time, a mixed audience, and the requirement to be honest about both what worked and what did not.

This page describes three format options, a set of judging criteria grounded in scientific thinking rather than metric performance, and notes on how the showcase connects to career development.

---

## Format Options

### Format 1: Dashboard Walkthrough (5 minutes per group)

Each group navigates their course dashboard live in front of the room and walks through their artifacts in order.

**Structure**:
1. Open the dashboard. Show the overview: how many missions completed, what artifacts were produced.
2. Click to the best artifact. Explain: what is this, why is this the best one, and what did you learn from producing it?
3. Click to the most interesting failure. Explain: what failed, why was this failure interesting or informative, and what does it tell you about where the model or your analysis fell short?
4. One-sentence summary: "If we had three more days and unlimited compute, the next thing we would do is ___."

**Why it works**: The dashboard walkthrough is fast, shows the complete arc of what each student or group did, and naturally rewards breadth of engagement (students who completed more missions have more to show). It also rewards quality of reflection — a student who can articulate their most interesting failure clearly is demonstrating the scientific literacy the course is designed to develop.

**Limitation**: Five minutes is tight if groups have complex artifacts. Brief the groups in advance: "You have five minutes. Practise. If you cannot describe your best artifact and your best failure in five minutes, you are describing too much detail."

**Works best for**: cohorts of 8-16 students, where 5-6 groups means 25-30 minutes total.

---

### Format 2: Scientific Poster Session

Each group prepares a one-page poster (A4 or A3) in advance of the showcase. Posters are pinned around the room. The instructor and any visiting faculty circulate for 20-30 minutes. Groups stand by their poster and explain it to whoever visits.

**Poster structure** (all on one page):
- **Question**: what was the central scientific question they investigated? (This should be their Mission 3 failure mode framed as a question: "Does data augmentation with elastic deformation improve boundary accuracy for the whole tumour sub-region?")
- **Method**: what one change did they make and why? What was the hypothesis?
- **Key result**: what did the metrics show? One figure maximum (training curves or a before/after Dice comparison).
- **Key failure**: what went wrong, or what surprised them? This can be a failure in the model, a failure in the prompt, or a failure in the experimental design.
- **What next**: if they continued this work, what would the next experiment be?

**Why it works**: The poster format is the format of academic conferences. Students practise a skill they will use repeatedly in their careers. Preparing the poster requires them to synthesise their work into a coherent narrative, which is harder than executing individual missions but more valuable as a transferable skill.

**Limitation**: Preparation time. Students need 30-45 minutes to produce a poster. Either schedule this during the final lab period (Mission 6 can be shortened to allow poster production time) or ask students to complete the poster the evening before Day 2.

**Works best for**: cohorts that include clinical researchers or PhD students who are already familiar with scientific posters; courses with a longer Day 2 schedule.

---

### Format 3: Lightning Talk (3 minutes + 2 minutes Q&A)

Each group presents exactly three slides. No exceptions. The constraint is enforced strictly — the timer is visible and groups stop at three minutes.

**Slide structure**:
1. **What we built**: one sentence describing the model or analysis, one figure showing the key result.
2. **What failed**: the most instructive failure, described specifically and honestly.
3. **What we learned**: one sentence about what changed in their understanding of medical AI between Day 1 morning and Day 2 afternoon.

**Why it works**: The three-slide constraint forces prioritisation, which is itself a form of scientific communication skill. Students who have done excellent work often struggle to distil it to three slides — this discomfort is productive. The Q&A period (2 minutes) is also excellent preparation for conference talks.

**Limitation**: Students who are less comfortable with public speaking may find the format stressful. Mitigate this by pairing students for the presentation (both stand up, one presents, the other handles questions).

**Works best for**: cohorts where students have some presentation experience; courses that explicitly connect to conference preparation.

---

## Judging Criteria That Reward Scientific Thinking

Regardless of which format you choose, use criteria that reward scientific process, not metric performance. Communicate these criteria to students before the showcase begins.

### Criterion 1: Quality of Error Analysis

Not: "did they identify failures?" — every model has failures.

Yes: "did they identify a *pattern* of failure? Did they connect the pattern to a plausible cause? Did they describe what data or analysis would confirm or disconfirm that cause?"

A group that says "the model missed 7 of 42 enhancing tumours and we found that all 7 were under 5cm³ in volume, suggesting the loss function is dominated by the large edema class in small-tumour cases" should score higher on this criterion than a group that says "the model got some cases wrong."

### Criterion 2: Strength of Improvement Hypothesis

Not: "did the Dice go up?"

Yes: "was the improvement motivated by the error analysis? Was the prediction explicit before the experiment? Was the result interpreted in light of the prediction?"

A group that predicted "adding class weights to up-weight small enhancing tumours will improve Dice on the enhancing tumour sub-region" and tested exactly that — even if the result was inconclusive — scores higher than a group that tried five things and reports whichever one gave the best number.

### Criterion 3: Honest Assessment in Mission 6

Not: "did they list model strengths?"

Yes: "did they identify real gaps between their research result and clinical readiness? Did they name specific validation steps that would be needed before deployment? Were they specific about failure modes that would concern them clinically?"

A group that says "this model should not be used clinically because it has not been validated on data outside this dataset, has no comparison to radiologist performance, and our error analysis shows it misses small enhancing tumours, which are clinically significant" is demonstrating more scientific maturity than a group that describes a path to deployment without acknowledging these gaps.

### Criterion 4: Prompt Quality and Reproducibility

Not: "did they use a lot of prompts?"

Yes: "are their prompts specific and purposeful? Could another researcher reproduce their workflow from their prompt log? Did they use prompt principles (Planner, Critic, constraint specification) in ways that improved their results?"

This criterion can be assessed by asking one question: "If I wanted to reproduce exactly what you did, would your prompt log tell me enough to do it?" The honest answer from many groups will be "mostly, but not completely." That honest answer, accompanied by an explanation of what is missing, is itself evidence of scientific thinking.

### What Is Explicitly Not a Criterion

**Dice score is not a judging criterion.**

State this clearly before the showcase. Repeat it if necessary.

A group with a final Dice of 0.75 and an excellent error analysis, a clearly motivated hypothesis, and a clear-eyed assessment of clinical gaps should score higher than a group with a Dice of 0.88 who cannot explain their results and has not identified any failure modes.

The reason is both pedagogical and scientific: in real research, understanding your result matters more than the number itself. A researcher who produces a Dice of 0.88 without understanding why is not yet ready to write a methods section, handle peer review, or advise others on when their model is appropriate to use.

---

## Connecting to Career Development

Every artifact produced in this course represents publishable-quality material — not immediately, but with appropriate validation and expansion.

Be specific about this with students:

- **The Mission 5 study design** is a methods section. If the study design is detailed, appropriately powered, and uses a clinically meaningful primary endpoint, it is close to what would appear in the Methods section of a grant application or a protocol paper. Students with strong Mission 5 outputs should be encouraged to develop them further with their supervisors.

- **The Mission 3 error analysis** is the Limitations section of a paper — but more importantly, it is the justification for a follow-up study. "We found the model systematically misses small enhancing tumours; a targeted study comparing class-weighted and unweighted training on cases stratified by tumour volume would address this" is a research question grounded in preliminary data. That is how grant proposals are written.

- **The Mission 6 assessment** is the kind of structured analysis that clinical AI standards (FDA, CE marking, NICE Evidence Standards Framework) require at various stages of technology development. Students who have practised honest gap analysis are better prepared for the regulatory and health technology assessment processes they will encounter if they take research to clinical deployment.

- **The prompt log** is a methods documentation artefact. The growing norm in computational research is to include code and workflow documentation as part of published supplementary material. A well-maintained prompt log demonstrates transparency about how AI tools were used — which is increasingly expected by journals and funders.

If any students are interested in pursuing the study design from Mission 5, offer to connect them with relevant contacts at your institution's clinical research office or ethics board. The best outcome of this course is a student who leaves with a research question they want to pursue.
