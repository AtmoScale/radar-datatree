# Contributing to radar-datatree

Thanks for your interest in `radar-datatree` — the open-source on-ramp to the [AtmoScale](https://atmoscale.ai) platform. This repo focuses on **tutorials, examples, and notebooks** for working with Analysis-Ready Cloud-Optimized (ARCO) weather radar data. Contributions that make the tutorials clearer, the helpers more reusable, or the science more reproducible are very welcome.

## Ways to contribute

- **Bug reports & questions** — open a [GitHub issue](https://github.com/AtmoScale/radar-datatree/issues). For radar-domain questions, please share the radar site, time window, and notebook involved.
- **Improvements to tutorials** — PRs that make notebooks clearer, add missing context, or improve plots are appreciated.
- **New examples** — if you've built a useful workflow on top of the `nexrad-arco` archive, propose it as a new notebook via an issue first.
- **Documentation** — typo fixes, glossary additions, and clarifying prose all welcome.

## Development setup

```bash
git clone https://github.com/AtmoScale/radar-datatree.git
cd radar-datatree
uv sync                       # recommended; alternative: conda env create -f environment.yml
uv run jupyter lab            # to edit notebooks
uv run sphinx-build -b html docs _build/html   # to preview the docs site
```

Python ≥ 3.12 required.

## Pull request workflow

1. Fork the repo and create a feature branch off `main`.
2. Make your changes; if you touch a notebook, restart the kernel and run it end-to-end before committing so outputs are populated.
3. Run the linters before pushing:
   ```bash
   uv run ruff check .
   uv run ruff format .
   uv run black notebooks/
   ```
4. Open a PR against `main`. The `render-notebooks.yml` CI will rebuild the docs site; an approving review is required before merge.

## Code style

- **Ruff** for linting + import sorting (rules: `E, W, F, I, B, UP`; line length 88; `E402` allowed in notebooks).
- **Ruff format** for Python files; **Black** for notebooks (kept consistent via pre-commit).
- **Notebooks are self-contained.** There is no shared helper module — each notebook carries the code it uses, so it runs standalone on Colab or from a copy-paste. Keep inlined helpers short: prefer a small `pandas` table over a formatted-print block, drop parameters nothing uses, and put long figure builders in a `hide-input`-tagged cell.

## Reporting security issues

Please don't open public issues for security concerns. Email `info@atmoscale.ai` instead.

## Code of conduct

This project adheres to the [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you agree to uphold it. Report issues to `info@atmoscale.ai`.

## Commercial / institutional support

For deployments, integrations, or institutional support beyond the open-source tutorials, talk to **[AtmoScale](https://atmoscale.ai)** — the parent platform behind `radar-datatree`.
