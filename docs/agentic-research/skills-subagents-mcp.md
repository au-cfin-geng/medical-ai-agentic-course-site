# Skills, Subagents, and MCP

As agentic AI workflows become more sophisticated, the individual prompt — powerful on its own — becomes a component in a larger architecture. This page introduces three concepts that structure complexity in agentic research workflows: **skills** (reusable prompt patterns), **subagents** (delegated AI instances), and **MCP** (the protocol for connecting Claude to external systems).

Skills are used throughout this course. Subagents and MCP are advanced concepts introduced here to give you a complete picture of the agentic research landscape, even though they are not implemented in the lab.

---

## Reusable Research Skills

A skill is a proven prompt pattern — a template with specified inputs, a specified role, a specified output contract, and a specified validation step — that can be applied to new research problems by substituting the specific dataset, file paths, and research question.

The value of a skill is cumulative. Each time you apply a skill and get a good result, you refine the template slightly based on what worked and what did not. Over time, a skill becomes a reliable research tool: you know what input it needs, you know what output it produces, and you know how to verify that it worked.

The following four skills are the core reusable workflows of this course.

---

### Data Inspection Skill

**Purpose:** establish ground truth about a new dataset before writing any model code.

**When to use:** at the start of Mission 2, or any time you receive a new dataset and need to understand its structure before modeling.

**Prompt template:**

```
Act as a data analyst. Do not write training code.
Read all files in [dataset directory] and report:
- Total number of files and their file types
- Dimensions and voxel spacing of the first case
- Whether labels are present for every case
- Class distribution in the label files (e.g., proportion of foreground voxels)
- Any unusual values, missing files, or formatting inconsistencies

Save a structured report to reports/data_inspection.md with these sections:
## Summary
## File Inventory
## Dimensions and Spacing
## Label Analysis
## Anomalies

Save a machine-readable summary to outputs/status/data_inspection.json with keys:
{
  "n_cases": <integer>,
  "has_labels_all_cases": <boolean>,
  "mean_foreground_fraction": <float>,
  "anomalies_found": <boolean>
}

After writing both files, read them back and confirm all sections and keys are present.
```

**What it produces:** a structured report and a machine-readable summary that can be referenced in all subsequent sessions.

**Validation step:** check that `has_labels_all_cases` is `true` and `anomalies_found` is `false` before beginning any training. If either is `false`, do not proceed until the anomaly is understood.

---

### Segmentation Error Analysis Skill

**Purpose:** identify where a segmentation model fails, at the case level and the pixel level.

**When to use:** Mission 3, or any time you have a trained model and need to understand its failure modes rather than just its average performance.

**Prompt template:**

```
Phase 1 — Observation (do not generate any hypothesis):
Load outputs/metrics/val_metrics.json.
Rank all validation cases by Dice score from lowest to highest.
Generate the following figures and save them to outputs/figures/:
  - error_analysis_best.png: the highest-Dice case, 4-panel figure
    (T1ce slice, ground truth mask, predicted mask, error map: green=TP, red=FP, blue=FN)
  - error_analysis_worst.png: the lowest-Dice case, same 4-panel layout

After saving, describe in plain language what you observe in the worst case.
Do not propose any hypothesis yet.

---

Phase 2 — Hypothesis (after I confirm observation is complete):
Based on the observed failure pattern, propose one specific and testable hypothesis.
The hypothesis must name:
(1) The specific failure pattern (e.g., "the model predicts false positives along tumour boundaries")
(2) A plausible mechanistic cause
(3) A specific intervention for Mission 4

Write the hypothesis to reports/error_analysis.md.
Save outputs/status/stage_03_error_analysis.json with keys:
{
  "best_case_dice": <float>,
  "worst_case_dice": <float>,
  "hypothesis_stated": <boolean>,
  "hypothesis_testable": <boolean>
}
```

**What it produces:** two PNG error map figures and a structured hypothesis report.

**Validation step:** read the hypothesis. Does it name a specific failure pattern, a mechanistic cause, and a testable intervention? If not, ask Claude to revise until all three elements are present.

---

### Clinical Translation Memo Skill

**Purpose:** convert technical model results into plain-language documentation for a clinical collaborator.

**When to use:** Mission 6, or any time you need to communicate AI model results to a clinician, hospital administrator, or regulatory reviewer.

**Prompt template:**

```
Act as a clinical AI communicator.
Your audience: a clinical radiologist who understands MRI and tumour anatomy
but has no machine learning background.

Read [metric files and report files].

Write reports/clinical_memo.md with these sections:
## Current Status
  (What the model can do, in plain language. No ML jargon.)
## What Was Demonstrated
  (What was shown on the teaching dataset, stated conservatively.)
## What Was Not Demonstrated
  (What this evaluation does not prove — clinical generalizability,
   prospective performance, safety for unseen populations.)
## Key Limitations
  (At least 3 specific limitations a clinician should know.)
## Human Oversight Requirements
  (Specific description of what a radiologist must check in every model output.)

Prohibited vocabulary: epoch, loss function, tensor, batch, architecture,
weights, gradient, backpropagation, hyperparameter.

Do not claim clinical readiness. The model was evaluated on teaching data only.
State this explicitly in the first paragraph.
```

**What it produces:** a clinical-facing memo that can be shared with a clinical collaborator or included in an ethics or regulatory submission.

**Validation step:** read the memo. Count the prohibited vocabulary violations. Confirm the "What Was Not Demonstrated" section is substantive. Confirm the limitations are specific (not "the model may not generalize" but "the model was not evaluated on post-surgical anatomy or patients with prior treatment").

---

### Study Design Critique Skill

**Purpose:** adversarially review a proposed study plan to identify weaknesses before the plan is presented to a collaborator or supervisor.

**When to use:** Mission 5, or any time you have drafted a study design and want to stress-test it before sharing.

**Prompt template:**

```
Act as a skeptical methods reviewer at a top medical imaging journal.
Read [study plan file].

Identify the 3 weakest assumptions in this study design.
For each assumption:
1. State the assumption explicitly
2. Explain why it is weak (what evidence challenges it, what it overlooks)
3. Suggest a specific change to the study design that would address the weakness

Do not describe strengths. Only identify weaknesses.
Do not suggest "collect more data" as a solution without specifying
what additional data and why it would address the specific weakness.

Write your critique to reports/study_critique.md.
```

**What it produces:** a structured critique that can be used to revise the study plan before submission or presentation.

**Validation step:** read the critique. For each weakness, confirm: (a) the assumption is stated clearly enough to be falsifiable; (b) the explanation names a specific threat to validity; (c) the suggested change is specific enough to implement.

---

## Subagents (Advanced Concept)

A subagent is a specialized AI agent instance delegated a specific subtask within a larger workflow. In advanced research infrastructure, a top-level orchestrating agent coordinates multiple subagents, each with its own task, context, and tools.

Consider a clinical AI research pipeline that processes a new patient imaging study. Rather than a single sequential session — inspect, evaluate, generate report — an advanced workflow might spawn:

- **Subagent 1:** data quality checker — reads the incoming imaging files, confirms DICOM compliance, checks for motion artefacts, outputs a quality report
- **Subagent 2:** model evaluator — runs the segmentation model on the new study, computes per-lesion metrics, identifies the three highest-risk regions
- **Subagent 3:** report generator — reads the quality report and the evaluation output, writes a radiologist-facing summary

Each subagent operates in its own context window with its own instructions and its own output contract. The orchestrating agent coordinates the results, handles failures in individual subagents, and produces a final coordinated output.

The advantage of subagents over a single sequential session is parallel execution and isolated context. Subagent 1 and Subagent 2 can run simultaneously. A failure in Subagent 1 (bad data) can be handled without aborting the session entirely.

This architecture is relevant to clinical AI research infrastructure — particularly for high-throughput scenarios like processing a queue of incoming imaging studies or running multi-site model evaluations. The Anthropic documentation on subagents provides the technical foundation.

---

## MCP — Model Context Protocol (Advanced Concept)

MCP (Model Context Protocol) is Anthropic's standard for connecting Claude to external data sources and tools beyond the local file system. With MCP, Claude can connect to:

- **Institutional imaging servers** — retrieve DICOM studies from a PACS system for direct analysis without manual download
- **Clinical databases** — query patient-level metadata to contextualize model outputs
- **Research registries** — read from and write to multi-site study databases
- **Real-time analysis pipelines** — send images to a running model server and receive predictions

An MCP-enabled clinical AI workflow might look like this: a radiologist flags an incoming study for AI-assisted triage. An MCP-connected Claude agent retrieves the study from the PACS server, runs the segmentation model via a model server connection, queries the patient registry for prior studies, generates a comparative report, and saves the result to the radiologist's worklist — all without manual file transfer.

This represents a qualitatively different capability from the local-file agentic research practiced in this course. The clinical implications are significant: MCP-enabled workflows can be embedded in clinical infrastructure rather than operating as standalone research tools.

The appropriate caution: MCP-connected systems that interact with real patient data require institutional data governance, regulatory compliance, and clinical oversight that are far beyond the scope of this course. MCP is introduced here as a technical concept, not as a tool ready for deployment.

!!! info "Anthropic resources for advanced concepts"
    For subagents: see the Anthropic documentation on multi-agent architectures and agent coordination patterns. For MCP: see the Model Context Protocol specification and the Anthropic documentation on tool use and external integrations. These are the primary technical references for building agentic research infrastructure beyond what this course implements.

!!! note "Skills vs. subagents"
    The distinction matters for practical planning. A skill is a prompt pattern you apply in your current session — no additional infrastructure required. A subagent requires orchestration code, multiple Claude instances, and coordination logic. For individual research tasks, skills are almost always the right tool. Subagents become relevant when the task has clear parallel components that would each benefit from their own context window.
