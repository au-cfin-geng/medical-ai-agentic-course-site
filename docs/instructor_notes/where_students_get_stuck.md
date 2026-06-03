!!! warning "Instructor Resource"
    This section is for instructors and teaching assistants. Students may read it, but it is not required course content.

# Where Students Get Stuck

This document is a field guide for instructors and TAs. Each entry describes a problem type, how to recognise it, and the fastest path to resolution. Problems are organised by category: technical, conceptual, prompting, and scientific.

Use this document proactively — circulate during lab time and look for these patterns rather than waiting for students to raise their hands.

---

## Technical Problems

### Environment Setup Failures

**What it looks like**: Student cannot complete Mission 1. Error messages involving `ModuleNotFoundError`, `conda not found`, wrong Python version, or path errors that multiply when they try to fix the first one.

**Root cause**: Heterogeneous machines in a course setting are the norm. Students arrive with Windows, macOS, and Linux laptops in various states of package management configuration. Docker or Conda environments reduce this variance but do not eliminate it.

**Resolution**:
1. Have a pre-built Conda environment YAML file ready. Point students to it immediately rather than debugging their local Python installation: `conda env create -f environment.yml && conda activate medical-ai-lab`. This resolves 80% of environment problems in under 5 minutes.
2. If Docker is available on the machine, have a Docker pull command ready: `docker pull [course-image]`. This is the nuclear option but it reliably works.
3. For path errors: ask the student to run `pwd` and `ls` before anything else. Most path errors come from the student being in the wrong directory. Do not let them chase a complex error until you have confirmed they are in the right place.
4. GPU availability: some students will have machines without NVIDIA GPUs. The training scripts should run on CPU for Mission 2 — it will be slow (10-20 minutes versus 2-3 minutes on GPU) but it should work. Reduce the number of training epochs for CPU-only students: change `--epochs 30` to `--epochs 5` to get a result in reasonable time.

**Pre-emption**: Send environment setup instructions 48 hours before the course. Ask students to confirm they can run `python -c "import torch; print(torch.__version__)"` before arriving. This converts the first 30 minutes of lost lab time into a problem solved at home.

---

### Data Loading Failures

**What it looks like**: Training script starts, then fails with a FileNotFoundError, or loads successfully but produces all-zero labels, or crashes after the first batch with a shape mismatch.

**Root cause**: The BraTS dataset has a specific directory structure that the dataloader expects. A missing trailing slash, a renamed folder, or a partial download creates these failures. Shape mismatches typically mean the student has pointed at the wrong directory or the wrong modality.

**Resolution**:
1. Have a data check script ready that students can run before training: `python scripts/check_data.py --data-dir /path/to/data`. This script should verify: directory exists, expected number of subjects present, at least one subject can be loaded and has the right shape and non-zero labels. Providing this script saves 15-30 minutes of debugging per affected student.
2. For all-zero label errors: ask the student to run the data check script and inspect the output. The label file is often named differently than expected (`seg.nii.gz` versus `Segmentation.nii.gz`). The dataloader must handle both naming conventions, or the setup instructions must be very precise about which naming convention the downloaded data uses.
3. For shape mismatch: confirm the student is using the correct modality combination. The expected input to the model should be documented clearly in the CLAUDE.md file. If it is not, this is a site improvement to make.

---

### CUDA Memory Errors

**What it looks like**: `RuntimeError: CUDA out of memory` during training, typically in the first few batches.

**Root cause**: BraTS volumes are large (240 x 240 x 155 voxels). A batch size of even 2 can exhaust a GPU with less than 8GB VRAM.

**Resolution**:
1. Have a batch size reduction guide ready as a one-liner: add `--batch-size 1` to the training command. For very low-VRAM machines, also add `--patch-size 128` to switch from full-volume to patch-based training.
2. If the student is using a 3D model with full volumes and batch size 1 and still running out of memory, switch them to 2D slice training with `--mode 2d`. Results will be worse but the mission will complete.
3. Do not let students spend more than 10 minutes debugging a CUDA memory error. It is a configuration problem, not a conceptual one, and it has a known solution.

---

## Conceptual Problems

### Not Understanding What Dice Measures

**What it looks like**: Student asks "is 0.65 a good score?"; student compares Dice scores across tasks (brain tumour vs. liver segmentation); student is confused about why a very large tumour and a very small tumour get different Dice scores with the same boundary error.

**Root cause**: Dice is not intuitive. It is an overlap measure, and its properties (sensitivity to small structures, behaviour near 0 and 1) are not obvious.

**Resolution — the coin-flip analogy**: "Imagine the tumour is a coin on the floor. Dice measures how much your predicted coin overlaps with the real coin. If you predict a coin that's 20% bigger than the real coin but in the right place, you get roughly a Dice of 0.83. If you predict a coin in the completely wrong place with no overlap, you get a Dice of 0. If you predict a coin that's twice the size of the real coin, you get roughly 0.67 even if the real coin is fully inside your prediction."

**Follow-up**: "For small structures — like the enhancing tumour core in BraTS — a small absolute error in pixels becomes a large relative error in Dice. A 3-pixel boundary error on a 100-pixel structure is a very different Dice impact than a 3-pixel error on a 10,000-pixel structure. This is why enhancing tumour Dice is always lower than whole tumour Dice for the same model."

---

### Confused About What a Label/Mask Is

**What it looks like**: Student does not understand what the label image contains; asks "where are the labels?"; thinks the label is a different scan; confused about the relationship between the MRI image and the segmentation mask.

**Root cause**: For students without image analysis background, the concept of a voxel-wise label array is genuinely unfamiliar. It is not obvious that a "segmentation mask" is an image with integer values rather than a scan with intensity values.

**Resolution — the overlay visualisation**: Use the course dashboard to show a side-by-side of the MRI scan and the label overlay. Point out: "The label image is the same size as the MRI — 240 x 240 x 155 voxels. But instead of MRI intensity values, each voxel contains a class number: 0 for background, 1 for necrosis, 2 for edema, 4 for enhancing tumour. When we colour the overlay, we are just displaying those class numbers as colours."

If the dashboard is not yet running: show the label values directly in Python — `import nibabel as nib; label = nib.load('seg.nii.gz').get_fdata(); import numpy as np; print(np.unique(label))`. The output `[0. 1. 2. 4.]` makes the discrete nature of the labels concrete.

---

### Not Understanding Patient-Level Split

**What it looks like**: Student splits data randomly by file rather than by patient; student does not understand why this matters; student argues "the volumes are different so it's fine."

**Root cause**: The concept of data leakage through improper splits is abstract until students have a concrete example of what goes wrong.

**Resolution — the cheating analogy**: "Imagine you are a radiologist learning to read brain tumours. You study 100 patients. Then I test you by showing you the left hemisphere of one of those same 100 patients and asking you to identify the tumour. You already saw the right hemisphere during training — you know what this person's brain looks like. Your test score is inflated because you have already seen this patient. Patient-level split means: if any scan from a patient is in the training set, no scan from that patient can be in the validation or test set. The AI is in the same position as the radiologist in this analogy."

Follow up: "In BraTS, each patient has four modalities (FLAIR, T1, T1ce, T2) plus a segmentation label. If you split by file, you might put the FLAIR in training and the T1 in validation. The model has never seen the T1 of that patient in training — but it has learned the spatial structure of that person's tumour from the FLAIR. The test is not independent."

---

## Prompting Problems

### Prompts Too Vague

**What it looks like**: Student types "fix my code", "make it work", "improve the results", "help me with Mission 3". Gets a generic or unhelpful response. Is frustrated that Claude "doesn't understand."

**Approach**: Do not correct the student directly. Instead, ask: "What specific output do you expect from this prompt? What would Claude need to produce for you to say 'yes, that's what I asked for'?"

This question almost always causes the student to immediately realise their prompt was underspecified. They will revise it themselves. Your role is to ask the question, not to write the prompt for them.

If they struggle to answer the specificity question: "Think about the format of the output. Should it be a numbered list? A file? A code change? Should it describe what it's going to do before it does it? Describing the expected output format forces you to be specific about what you actually want."

---

### Not Checking Claude's Output

**What it looks like**: Student accepts the first response from Claude and moves on without verifying it. Training script runs but produces wrong results. Student is surprised when the error analysis in Mission 3 does not match what they thought they submitted.

**Root cause**: The cognitive reflex with AI tools is to treat the output as authoritative. This is the single most dangerous habit in a research context. An AI tool that writes plausible-looking code is not the same as a tool that writes correct code.

**Approach**: Ask: "How do you know this is correct? What would you expect to see if it worked? What would you expect to see if it didn't work?"

If the student says "I don't know how to check it": walk them through one specific check. "The dataloader says it's loading 484 subjects. Does that match the number of subject folders in the data directory? Let's count." This concretises the verification habit.

Do not let students proceed to Mission 3 or Mission 4 without having checked their Mission 2 results. If they cannot explain what their training split contains, they cannot interpret their results.

---

### Letting Claude Go Too Far

**What it looks like**: Student asked Claude to improve one function; Claude rewrote three files; student is not sure what changed; model now does not run.

**Root cause**: Without explicit constraints, Claude will sometimes take initiative in ways that are counterproductive in a research setting where you need to understand every change.

**Resolution — the constraint principle**: Introduce this explicitly as a principle: "Claude's initiative is proportional to your prompt's scope. If your prompt has no scope limit, Claude assumes the scope is as large as needed to solve the problem."

Practical constraints to teach students:
- "Only modify the file `scripts/train.py`. Do not change any other file."
- "Make the smallest change that achieves the goal."
- "List every file you modified before making any changes, and wait for my approval."
- "Do not refactor anything. Only add the new functionality."

If the student's code is already in an unknown state from Claude's over-reach: use git to recover. `git diff` to see what changed; `git checkout -- .` to revert if needed. This is also a good moment to reinforce the habit of committing before each Claude session.

---

## Scientific Problems

### Accepting First Model Result Without Analysis

**What it looks like**: Student completes Mission 2, sees their Dice score, and immediately asks how to improve it. Has not done any error analysis. Wants to skip to Mission 4.

**Approach**: Do not let them skip Mission 3. The entire pedagogical arc depends on Mission 3 because it introduces the link between evidence and action. A student who goes from Mission 2 to Mission 4 directly is doing hyperparameter tuning, not research.

Ask: "What is failing? You have a Dice score, but that number doesn't tell you what the model is getting wrong. Is it missing small tumours? Is it getting the boundary wrong? Is it failing on specific patient subgroups? Without an error analysis, you're guessing at what to improve."

If the student says "I just want to try a different loss function and see if it helps": ask "What in your error analysis predicts that a different loss function would help? If you can't connect the change to the evidence, you're running a random experiment."

---

### Improvement Attempts Without Hypothesis

**What it looks like**: Student in Mission 4 tries five different changes without documenting a hypothesis for any of them. Changes things because they "read that it helps" or "seems like it might work."

**Approach**: Return to the error analysis. "What failure mode did you identify in Mission 3? What is the one change that your error analysis predicts should address that failure mode? Start there. Only there."

The discipline of one-change-at-a-time is uncomfortable for students who are used to empirical tuning. Explicitly acknowledge this: "I know this feels slow. In a real research setting, you would run multiple experiments in parallel. In this course, you are practising the discipline of making a testable prediction and testing it. The speed constraint is intentional."

If a student has already tried multiple changes: ask them to pick the one change they can best justify and treat that as their Mission 4 result. The others can be noted as "additional experiments not analysed."

---

### Claiming the Model Is Ready for Clinical Use

**What it looks like**: Student's Mission 6 concludes the model is "ready for clinical deployment." The evidence offered is a Dice score above some threshold. Clinical risks, failure modes, regulatory requirements, and validation requirements are absent from the analysis.

**Root cause**: Students conflate research performance with clinical readiness. This is a common and consequential error. A model with Dice 0.82 on a single-institution dataset has not demonstrated clinical readiness under any current regulatory framework.

**Resolution — the readiness checklist**: Use the Mission 6 readiness checklist to structure the discussion. Walk through each item with the student:

1. "Has this model been evaluated on data from a different institution than where it was trained?" (Almost certainly no, given the lab setup.)
2. "Has this model been evaluated in a prospective study, or only retrospectively on an archive?" (Only retrospective.)
3. "Has this model been compared to radiologist performance on the same cases?" (No.)
4. "Has this model been reviewed by a regulatory body?" (No — it is a research prototype.)
5. "Has a failure mode analysis been conducted and documented for clinical users?" (Only partially — Mission 3 started this.)

None of this means the model is bad or that the student did poor work. It means "research performance" and "clinical readiness" are different bars, and the purpose of Mission 6 is to understand why.

The teaching point: "A Dice score is a research metric. Clinical readiness requires evidence of generalisability, safety characterisation, regulatory clearance, and integration into clinical workflow. We have evidence for none of these yet. Mission 6 is about being honest about that gap — not to discourage you, but because being honest about evidence is the foundation of trustworthy medical research."
