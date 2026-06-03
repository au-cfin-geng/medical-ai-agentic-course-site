# Prompts as Experimental Instruments

The central claim of this course is that a prompt is not a request — it is an experimental instrument. This page explains what that means, why it matters for clinical AI research, and how to build prompts that function as scientific protocols.

---

## The Protocol Analogy

Every scientific experiment has a protocol: a documented specification of what you will do, with what materials, under what conditions, and what you will measure. A wet lab protocol specifies reagents, concentrations, incubation times, measurement instruments, and expected controls. A clinical trial protocol specifies the patient population, intervention, comparator, primary outcome, and analysis plan.

The protocol is what makes an experiment reproducible. Without a protocol, a colleague cannot replicate your result. With a protocol, they can follow your steps, observe whether they get the same outcome, and either confirm or challenge your finding.

A prompt to Claude is the protocol for your AI-assisted research step. Like a wet lab protocol, it should specify:

1. **Background** — what is the project and what have you done so far?
2. **Objective** — what specifically should happen in this step?
3. **Materials** — which files, datasets, and scripts are involved?
4. **Method constraints** — what must NOT be changed?
5. **Expected output** — exact file names, JSON keys, report structure
6. **Validation step** — how will you verify it worked?

When your prompt contains all six components, the result is reproducible, checkable, and transferable. When your prompt is missing components, you get ambiguous outputs that cannot be verified against your intent.

---

## What Makes a Protocol Reproducible

Consider what makes a wet lab protocol reproducible versus not. A protocol that says "add some of the enzyme and incubate" is not reproducible. A protocol that says "add 2 µL of RNase A (stock concentration 10 mg/mL) and incubate at 37°C for 30 minutes" is reproducible.

The same logic applies to prompts. A prompt that says "help me train a model" leaves every decision to Claude — which dataset, which script, which hyperparameters, which output path, which metric to report. A prompt that specifies the dataset location, the script to use, the exact parameter to change, the output path, and the exact keys in the output JSON leaves almost no room for variation.

Specificity is not pedantry. In research, specificity is how you distinguish "I ran the experiment" from "I ran an experiment." The former implies a controlled procedure. The latter implies you did something, you are not sure what, and you cannot reproduce it.

---

## Transforming a Vague Prompt into a Research Protocol

Here is the transformation in full detail. This is the most important practical exercise on this page.

**VAGUE:**

```
Help me train a model
```

This prompt leaves every consequential decision to Claude: which dataset to use, which script to run, which hyperparameters to apply, where to save the results, what format to save them in. Claude will make all of these decisions, and you will not know what it decided until you look at the output. You cannot reproduce this experiment, because you did not specify it.

**RESEARCH PROTOCOL PROMPT:**

```
I am working on brain tumour segmentation using the teaching data in data/sample/.
My baseline model achieved Dice 0.67, recorded in outputs/metrics/val_metrics.json.

I want to test whether adding random horizontal flipping augmentation improves Dice.

Please take the following steps in order:

(1) Read scripts/run_train.py and describe how augmentation is currently handled.
    Do not make any changes yet — only read and describe.

(2) Propose the minimal code change to add random horizontal flipping as a
    training augmentation. Do not implement anything yet — wait for my approval.

(3) After I approve, implement only that change. Do not alter the model
    architecture, learning rate, batch size, or random seed (seed = 42).

(4) Run the training script. After training completes, evaluate on the
    validation set using the same evaluation script as baseline.

(5) Save the result to outputs/metrics/augmentation_test.json with exactly
    this structure:
    {
      "dice": <float between 0 and 1>,
      "baseline_dice": 0.67,
      "delta": <new_dice - 0.67>,
      "change": "<one sentence describing what was changed>",
      "augmentation_supported": <true or false>
    }

(6) Report in plain language whether the change helped or not, citing the
    delta value from the JSON file.
```

This is a research protocol prompt. It specifies six numbered steps. It names the exact files involved. It states what must not change. It provides the exact output contract including key names and types. It requires a plain-language interpretation anchored to the specific computed value.

---

## Component-by-Component Analysis

Let us trace each component of the research protocol example.

**Background:** "I am working on brain tumour segmentation using the teaching data in data/sample/. My baseline model achieved Dice 0.67, recorded in outputs/metrics/val_metrics.json."

This tells Claude what project it is operating in, where the data lives, and what the reference metric is. Without this, Claude might train on a different dataset or compare against a fabricated baseline.

**Objective:** "I want to test whether adding random horizontal flipping augmentation improves Dice."

This is a single testable hypothesis. It names one variable (horizontal flipping), one outcome (Dice), and one comparison (against baseline). A vague objective like "I want to improve the model" is not testable and does not specify what to measure.

**Materials:** "data/sample/, scripts/run_train.py, outputs/metrics/val_metrics.json."

Named files only. Claude is not asked to search for relevant data or decide which script to use.

**Method constraints:** "Do not alter the model architecture, learning rate, batch size, or random seed (seed = 42)."

This is the controlled experiment specification. Everything that is not the one variable being tested is explicitly held constant. This is the prompt equivalent of the control condition in an experiment.

**Expected output:** Step 5, specifying the exact file path, the exact JSON keys, the exact types, and the exact logic for `delta` and `augmentation_supported`.

This is the output contract. Without it, Claude will save results wherever it thinks is reasonable, with keys it chooses, in a format it selects. The autograder will not find them. You will not be able to compare them against other experiments.

**Validation step:** Step 6, requiring a plain-language interpretation "citing the delta value from the JSON file."

This requires Claude to ground its interpretation in the actual computed value, not in a general expectation. If the delta is negative, Claude must say the change did not help. This instruction makes it harder for Claude to write a vague or misleading summary.

---

## Why Specificity Matters for Reproducibility

If you document your prompts as part of your research record — alongside the outputs they produced — another researcher can reproduce your AI-assisted research workflow. They can run the same prompt against the same codebase and expect substantially the same output.

This is a new form of methods documentation that does not yet have established standards in the research community, but the principle is identical to the one that makes wet lab protocols reproducible: document what you asked for, document what you got.

In clinical AI research, where the stakes of irreproducibility are patient safety, this documentation practice is not optional — it is part of responsible research conduct.

---

## The Prompt Ledger

A prompt ledger is a record of every prompt you sent during a research session, along with the outputs those prompts produced and your assessment of whether the output met your research intent.

In this course, your prompts are part of your scientific record. Treat them accordingly. After each mission, review the prompts you used and note which versions produced better outputs. This record becomes a transferable methodology — a library of research protocol prompts you can adapt for future projects.

The minimum prompt ledger entry:
- The prompt text (verbatim)
- What output it produced (file paths and a brief description)
- Whether the output met your research intent (yes / partially / no)
- What you changed in the next prompt version if the first did not work

!!! example "Prompt anatomy"
    A research protocol prompt has six labeled components: **(1) Background** — project context and current state. **(2) Objective** — the specific, testable question being addressed. **(3) Materials** — exact file paths involved. **(4) Constraints** — what must not change. **(5) Output contract** — exact file path, format, key names, and types. **(6) Validation** — how Claude should verify and report whether it worked. A prompt missing any of these components is underspecified for research purposes.

!!! note "Connection to the lab missions"
    Every mission in this course supplies a prompt pattern to practice. Mission 2 practices the data inspection prompt — no training code, observation only. Mission 3 practices the two-phase observation-then-hypothesis prompt — enforcing that the hypothesis emerges from the evidence. Mission 4 practices the single-change protocol prompt — specifying exactly one variable to test. Mission 5 practices the study design critique prompt — asking Claude to attack rather than defend. Mission 6 practices the clinical translation prompt — specifying the audience, the prohibited vocabulary, and the required honesty language. Each of these is a research protocol prompt. Each practices one component of the methodology described on this page.

!!! tip "Document your prompts now"
    Keep a text file open during each lab session and paste every prompt you send into it, along with a brief note of what output it produced. After the lab, this file is the first draft of your methods section for any paper that uses this AI-assisted workflow.
