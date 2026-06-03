# Lab Commands Cheat Sheet

> **For print:** use browser Print → Save as PDF. Recommended: A4, portrait.

---

## Starting Claude Code

Open your terminal, navigate to your project directory, then:

```bash
cd /path/to/your/brats_lab
claude
```

Claude Code starts in the current directory. Everything Claude reads and writes will be relative to this directory. Always start Claude Code from your project root.

**Confirm it is working:** Claude Code will show a prompt. Type `hello` and press Enter. If it responds, you are ready.

---

## Key Sections of CLAUDE.md

Your `CLAUDE.md` file lives at the project root and is read at the start of every session. Keep it updated.

| Section | What to Put Here |
|---|---|
| `## Project Summary` | 2-3 sentences: what this project does, what stage it is at |
| `## File Map` | Annotated tree of key files — what each script does |
| `## How to Run` | Working shell commands for: check env, load data, train, evaluate |
| `## Data` | Where data lives, format, the rule "do not modify data/" |
| `## Current Status` | Last completed step, current mission, next action |
| `## Do Not Touch` | Files and directories Claude must never modify (e.g. `data/`, raw labels) |

**Template line for CLAUDE.md update:** At the end of each session, ask Claude: "Update the Current Status section of CLAUDE.md to reflect what we completed today."

---

## Common Shell Commands

### Navigation and inspection

```bash
ls -la                          # List all files with sizes and permissions
ls -la results/                 # List a specific directory
pwd                             # Print current working directory
find . -name "*.nii.gz" | head  # Find NIfTI files in the project
```

### Reading files

```bash
head -n 20 results/training_log.csv     # Show first 20 lines of a CSV
cat results/metrics_summary.json        # Print a JSON file
wc -l results/metrics_per_case.csv      # Count lines (= number of cases + header)
```

### Running scripts

```bash
python scripts/check_env.py                        # Verify environment
python scripts/train.py --epochs 2 --batch_size 4 # Smoke test training (2 epochs)
python scripts/evaluate.py --checkpoint results/best_model.pt --split test
python scripts/visualise.py --metrics results/eval/metrics_per_case.csv
```

### Checking results

```bash
ls -lh results/checkpoints/         # List checkpoints with human-readable sizes
ls -lh results/figures/             # List generated figures
cat results/eval/metrics_summary.json
```

### Git (if your project is version controlled)

```bash
git status                          # See what has changed
git add scripts/train.py            # Stage a specific file
git commit -m "add training loop"   # Commit with message
git log --oneline -10               # See last 10 commits
```

---

## Viewing the Dashboard

The course dashboard (`dashboard/index.html`) shows your mission progress and links to all resources.

**Option 1 — Open directly:**

```bash
open dashboard/index.html         # macOS
xdg-open dashboard/index.html     # Linux
```

**Option 2 — Use the URL given by your instructor** (if the dashboard is served on the course network).

---

## Student Project File Structure

```
brats_lab/
├── CLAUDE.md                   ← Read at the start of every session
├── data/
│   ├── train/                  ← Training cases (do not modify)
│   │   └── BraTS_[id]/
│   │       ├── t1.nii.gz
│   │       ├── t1ce.nii.gz
│   │       ├── t2.nii.gz
│   │       ├── flair.nii.gz
│   │       └── seg.nii.gz
│   ├── val/                    ← Validation cases (do not modify)
│   └── test/                   ← Test cases (do not modify)
├── scripts/
│   ├── check_env.py            ← Mission 0: verify environment
│   ├── audit_data.py           ← Mission 1: dataset summary
│   ├── dataset.py              ← DataLoader
│   ├── model.py                ← UNet2D architecture
│   ├── train.py                ← Training loop
│   ├── evaluate.py             ← Evaluation on test set
│   └── visualise.py            ← Plot generation
├── results/
│   ├── checkpoints/            ← Model checkpoints saved during training
│   ├── best_model.pt           ← Best checkpoint by val Dice
│   ├── training_log.csv        ← Epoch-level metrics from training
│   ├── eval/
│   │   ├── metrics_per_case.csv
│   │   └── metrics_summary.json
│   └── figures/                ← Generated plots (PNG)
└── session_handover_[date].md  ← End-of-session context document
```

---

## How to Recover from a Broken Claude Session

If Claude Code crashes, produces a confusing error, or gets stuck in a loop:

**Step 1 — Start a fresh session.**
Close the terminal tab or window. Open a new terminal and restart:

```bash
cd /path/to/brats_lab
claude
```

**Step 2 — Re-establish context.**
Paste the context-setting prompt from [Setup Prompts](../prompt_library/setup_prompts.md), or:

```
Read my CLAUDE.md file. Then read the most recent session_handover file.
Tell me what the current status is before doing anything else.
```

**Step 3 — Verify nothing was broken.**
Ask Claude to list the files in `results/` and confirm the most recent checkpoint is intact.

**Step 4 — Continue from the last known good state.**
Use the "next session starting point" from your session handover document.

**If a script is broken and you are not sure what Claude changed:**

```bash
git diff                         # If using git, see all changes since last commit
git checkout -- scripts/train.py # Revert a specific file to its last committed state
```

**Golden rule:** If in doubt, read before modifying. Ask Claude to explain what it is about to do before it does it.
