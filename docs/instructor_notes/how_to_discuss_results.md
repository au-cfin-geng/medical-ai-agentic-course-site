!!! warning "Instructor Resource"
    This section is for instructors and teaching assistants. Students may read it, but it is not required course content.

# How to Discuss Results

This document provides a facilitation guide for the results discussion moments built into the course. Each mission has a natural discussion point: when students return from the lab, when results are posted to the dashboard, or when the class reconvenes after individual work. How you open and run these discussions shapes what students take away from the data they have produced.

The guiding principle for all results discussions: **the number is the starting point for the conversation, not the conclusion of it.**

---

## After Mission 2: First Results

Mission 2 produces each student's first Dice scores. This is often the most emotionally loaded moment in the course — students want to know if they "did well," and the reflex is to compare scores across the room.

### Opening the Discussion

Do not open with: "What was your Dice score?"

Open with: "What surprised you?"

This reframing has a specific purpose: it invites students to notice anything unexpected, positive or negative, about the training process or the result. Surprising things students commonly report:

- "It trained much faster than I expected" (good moment to discuss GPU parallelism)
- "The training loss went down but the validation loss went up" (introduce overfitting)
- "My model predicted mostly background and still got a Dice of 0.3" (introduce class imbalance)
- "I got the same result as my neighbour even though we used different hyperparameters" (introduce model robustness and the difference between noise and signal)

Each of these is a richer entry point than asking for the score.

### Making the Score Meaningful

After surfacing surprises, bring in the score — but contextualise it immediately.

Ask: "How do you know this number is meaningful? What would it mean if your Dice were 0.4?" Let students answer. Then: "What would it mean if your Dice were 0.99?"

The Dice-of-0.99 question reliably surfaces the overfitting concern without you having to lecture about it. Students who have completed Mission 1 (data inspection) will often say "if it's 0.99, something is wrong — either the data split is wrong, or we're memorising the training set." This is a correct intuition and worth affirming explicitly.

### Introducing the Baseline Reference

Before ending the Mission 2 discussion, introduce the baseline question: "What would a naive model score on this task? Specifically, if the model predicted 'all background' for every voxel — never predicting any tumour — what would its Dice be?"

The answer is 0 (or close to 0 for the tumour sub-regions, since Dice is undefined when both prediction and ground truth are empty and is typically set to 0 or 1 by convention — worth noting). But for the whole-tumour region, a model that always predicts background would get roughly a Dice of 0 on any case with a tumour.

The implication: any Dice score above 0 represents something learned. A score of 0.65 is not "only 65% good" — it is far above the naive baseline. But a score of 0.65 is also far below perfect, and Mission 3 will investigate why.

### What Not to Do

Do not rank students by Dice score. Do not put a leaderboard on the screen. Do not praise students with high scores or imply that students with low scores "need to do better." At this stage of the course, the primary outcome being assessed is whether students can explain their result, not whether the number is large.

---

## After Mission 3: Error Analysis

Mission 3 is the intellectual centre of the course. The discussion after Mission 3 is the most important discussion of the two days.

### Opening the Discussion

Ask each group (or each student, if working solo) to describe their primary failure mode in one sentence. Write all the failure modes on a whiteboard or shared document where everyone can see them.

You will often see a list like:
- "The model misses small enhancing tumours"
- "The model over-predicts edema at tumour boundaries"
- "The model fails on cases with ring-enhancing tumours"
- "The model's boundaries are accurate but consistently too large"

Now look at the list together.

### The Reproducibility Teaching Moment

Ask: "If we all trained the same model on the same data with the same code — did we find the same failure modes?"

If students all ran Mission 2 with identical configuration, they should have found similar (though not identical, due to random seed variation) failure patterns. If some students found very different failure modes: investigate together. Did they use a different training split? A different number of epochs? Did Claude generate different training scripts for different students?

This conversation — regardless of outcome — teaches something important. Either: (a) the same model fails in the same ways, which is a lesson in reproducibility; or (b) different configurations produce different failure modes, which is a lesson in experimental control.

Say: "This is why we document every decision in the prompt log. If two researchers using the same dataset find different failure modes, the first question a reviewer will ask is: what was different about your setup?"

### Clinical Grounding

After discussing failure modes technically, shift to the clinical grounding question.

Ask: "If you were a radiologist using this model, would you be worried about this failure mode? Why?"

The question of clinical concern is deliberately different from the question of statistical performance. A model that misses 10% of enhancing tumours might have a higher Dice than a model that gives systematically wrong boundaries — but the clinical implications of those two failure modes are very different. Missing a tumour entirely is different from slightly over-estimating its extent.

Students with clinical backgrounds will often lead this part of the discussion well. Invite them to explain to the group what the clinical consequence of a given failure mode would be.

If no students have clinical backgrounds: use the thought experiment of "what decision would change if the radiologist saw this output?" A complete miss of an enhancing lesion might cause a radiologist to recommend watchful waiting rather than aggressive treatment. A boundary over-prediction might cause the radiation oncology team to plan a larger treatment volume. These are not equivalent errors.

---

## After Mission 4: Improvement

Mission 4 produces a second result: the improved model (or the model after one specific change). The results discussion here should focus entirely on the hypothesis, not the score.

### Opening the Discussion

Ask: "Was your hypothesis correct?"

Not: "Did your Dice go up?"

A student whose Dice went from 0.65 to 0.68 after a theoretically motivated change is in a better scientific position than a student whose Dice went from 0.65 to 0.72 after a change they cannot explain. Affirm this explicitly.

### Evidence for a Real Improvement

When a student reports an improvement, ask: "What would you need to see to be convinced the improvement is real — and not just random variation due to a different random seed?"

This opens the discussion of statistical testing and multiple runs. The expected answer includes:
- Running the same experiment with multiple random seeds and showing consistent improvement
- Testing on a held-out set that was not used to guide the improvement decision
- Reporting a confidence interval, not just a point estimate

Students will often acknowledge they have none of this evidence. The response: "That is correct. What you have is a promising preliminary result. In a real paper, that would be a figure in the preliminary data section of a grant proposal, not the main result. The course is not designed for you to produce a definitive result — it is designed for you to understand what a definitive result would require."

### When the Hypothesis Was Wrong

A hypothesis that was tested and disproved is scientifically valid. Make this explicit and normalise it.

Say: "If you predicted that adding class weights would fix your boundary errors and the Dice went down — that is not a failure. You have learned something. What did you learn? What does the negative result tell you about what was actually causing the boundary error?"

This is often the most productive discussion when it happens. Students who tried an evidence-based change and got a negative result typically understand their model better than students who tried an unmotivated change and got a slight improvement.

### The Multiple-Change Problem

Some students will have made multiple changes in Mission 4 despite being asked to make one. When they report results, ask: "Which change do you think caused the improvement? How would you find out?"

The answer — separate experiments for each change — is the lesson. You cannot extract it if you do not ask the question.

---

## After Mission 6: Clinical Translation

Mission 6 is the final analytic mission. The discussion after Mission 6 is the most reflective and often the most revealing discussion of the course.

### Opening the Discussion

Ask each group: "Would you use this model if you were the radiologist? If yes, under what conditions? If no, what would it need to have?"

Do not give examples before hearing from students. The range of answers is the material for discussion.

Typical range of answers:
- "Yes, as a screening tool to flag suspicious cases for human review" — this is a reasonable and specific use case; probe what "suspicious" means and what the threshold should be.
- "Yes, for research studies where I just need a consistent boundary, not a perfect one" — also reasonable; this is the current main use of AI segmentation tools.
- "No, the model hasn't been validated on patients outside this dataset" — correct concern; probe what validation would look like.
- "No, the model completely misses some tumours and I cannot know which ones" — this is the most important answer and the hardest one to give. Affirm it.

### The Gap Between Research Standards and Clinical Standards

The Mission 6 discussion almost always surfaces the gap between what is published in research papers and what is required for clinical deployment. Make this gap explicit.

Say: "The majority of medical AI papers report results on retrospective datasets from a single institution. A reviewer for a medical AI journal might accept this. A regulatory body reviewing for clinical deployment would not. What is required for clinical deployment that is typically absent from even high-quality research papers?"

Expected answers: prospective validation, multi-site validation, comparison to clinical standard of care, failure mode documentation for clinical users, integration testing in real clinical workflow, regulatory submission, post-market surveillance plan.

This is not meant to be discouraging. It is meant to be accurate. The purpose of Mission 6 is to understand the gap — and to ensure that students, when they eventually publish or present research, are honest about where they are in the pipeline from research result to clinical tool.

### Using Outlier Results

If one group's model performed substantially better or worse than the others — investigate together.

This is one of the most valuable teaching moments in the course, because the investigation models exactly the scientific process you want students to use.

Ask:
1. "What was different about their setup?" (Check: random seed, training split, augmentation, number of epochs, loss function)
2. "Is the performance difference likely to reproduce? Or is it sensitive to the configuration?"
3. "If we ran the same configuration five times with different random seeds, what would we expect to see?"

If the outlier result is high: the group may have accidentally introduced data leakage, or they may have genuinely found a better configuration. Both outcomes are instructive.

If the outlier result is low: the group may have a configuration error, a data loading problem, or they may have encountered a genuinely difficult subset of the data. All three are instructive.

The point is not to "correct" the outlier result but to demonstrate that variability is information — and that understanding the source of variability is the researcher's job. A single result without context (from what configuration, with what random seed, on what exact data split) is not a result; it is an observation waiting to be explained.
