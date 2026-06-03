# Medical AI + Agentic Coding Lab

**A PhD-level summer course on Clinical AI, MRI Analysis, and Prompt-First Research**

This repository contains the full source for the course website, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).
The site covers two intensive days of lectures, lab missions, and guided agentic-coding sessions
designed for PhD students and early-career researchers working at the intersection of clinical medicine
and machine learning.

---

## Prerequisites

- Python 3.9 or higher
- pip 21+
- Git

No Docker or conda environment is required — a plain virtual environment is sufficient.

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-org>/medical-ai-agentic-course-site.git
cd medical-ai-agentic-course-site

# 2. (Optional but recommended) Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate.bat   # Windows CMD
# .venv\Scripts\Activate.ps1   # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Local Preview

```bash
make serve
```

Then open your browser at **http://127.0.0.1:8000**.

The development server supports live-reload: any edits to Markdown files or `extra.css` will refresh
the browser automatically.

---

## Build

```bash
make build
```

The static site is written to the `site/` directory.

---

## Validate

Before committing or deploying, run the built-in validator to check that all nav entries resolve to
real files and that no file is accidentally empty:

```bash
make validate
```

The script exits with code `0` if everything passes, `1` otherwise.

---

## GitHub Pages Deployment

Deployment is automated via GitHub Actions (see `.github/workflows/deploy.yml`).
Every push to `main` triggers `mkdocs gh-deploy --force`, which pushes the built site to
the `gh-pages` branch.

### One-time setup

1. In your GitHub repository, go to **Settings > Pages**.
2. Set the source to **Deploy from a branch** and choose the `gh-pages` branch, root folder.
3. Save — GitHub will publish the site at `https://<your-org>.github.io/medical-ai-agentic-course-site/`.

### Manual deployment (if you need it)

```bash
# Build and push to gh-pages in one command
mkdocs gh-deploy --force
```

---

## Site Structure

| Directory | Purpose |
|---|---|
| `docs/` | All Markdown source pages |
| `docs/course_map/` | Schedule, learning outcomes, lab alignment |
| `docs/foundations/` | Clinical AI, imaging pipeline, ethics |
| `docs/mri/` | MRI textbook chapters |
| `docs/medical_ai_workflow/` | End-to-end AI workflow pages |
| `docs/agentic_research/` | Agentic coding and prompt-first research |
| `docs/lab_missions/` | Mission 0 – 6 lab guides |
| `docs/prompt_library/` | Reusable prompt templates by category |
| `docs/handouts/` | Print-ready cheat sheets and glossary |
| `docs/instructor_notes/` | Teaching flow, demo scripts, student FAQ |
| `docs/assets/stylesheets/` | Custom CSS (`extra.css`) |
| `docs/assets/images/` | Figures and diagrams |
| `scripts/` | Utility scripts (validate_site.py) |
| `.github/workflows/` | GitHub Actions CI/CD |
| `mkdocs.yml` | MkDocs configuration |
| `requirements.txt` | Python dependencies |
| `Makefile` | Common tasks (`install`, `serve`, `build`, `validate`, `clean`) |

---

## Contributing

Contributions are welcome — especially new prompt templates, additional mission briefs, and
corrections to the MRI textbook chapters.

1. Fork the repository and create a feature branch.
2. Make your changes in `docs/` (Markdown) or `docs/assets/stylesheets/extra.css`.
3. Run `make validate` to ensure all nav references resolve.
4. Run `make serve` to check the site renders correctly.
5. Open a pull request with a clear description of the change.

### Writing conventions

- Use sentence case for headings (not Title Case), except for proper nouns.
- Place clinical or prompt-principle admonitions with `!!! clinical "..."` or `!!! prompt-principle "..."`.
- Keep lab missions in the imperative voice ("Run the following command…").
- Cite sources with footnotes where claims are empirical.

---

## License

| Content | Code |
|---|---|
| All Markdown documentation under `docs/` is released under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) licence. | All scripts, configuration files, and CSS are released under the [MIT Licence](https://opensource.org/licenses/MIT). |

If you use this material in a course or publication, please attribute:
> "Medical AI + Agentic Coding Lab", Course Team. Available at https://github.com/<your-org>/medical-ai-agentic-course-site

---

## Acknowledgements

This course draws on publicly available clinical AI literature, the BraTS dataset family,
the MkDocs Material documentation, and the Claude Code agentic coding environment.
We are grateful to all contributors who have improved the content through feedback and corrections.
