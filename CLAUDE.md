# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

radar-datatree is a public-facing repository that provides examples and tutorials for accessing Analysis-Ready Cloud-Optimized (ARCO) weather radar data using the Radar DataTree framework.

**Important Context**: This is the public companion to `raw2zarr` (a private repository). The conversion tool is private due to licensing discussions with UIUC OTM. This repository focuses on **reading and analyzing** already-converted data, not converting raw data.

## Implementation Workflow (per-phase)

Plans for non-trivial work live in `.plan_out/<kebab-case-name>.md` at the repo root, structured as numbered phases with checkboxes (see `.plan_out/qvp-benchmark-integration.md` as a format reference).

**For every phase in such a plan, follow this exact sequence — no shortcuts:**

1. **Implement** all refactor code for the phase end-to-end. Do not interleave phases.
2. **Smoke test** — run the smallest realistic check that the change works (notebook executes, import resolves, helper returns expected shape, etc.).
3. **Audit** with these slash commands, in this order, addressing findings before moving on:
   - `/simplify`
   - `/xarray`
   - `/python-design-patterns`
   - `/python-code-review`
   - `/python-testing-patterns`
4. **Ask for explicit approval** before committing — never `git commit`/`push`/`gh pr create` autonomously.
5. **On approval**: commit, push, open the PR, then update the plan file by checking off the completed phase's items.
6. **Wait for the PR to merge** before starting the next phase. One PR per phase, not one mega-PR per plan.

## Architecture

The Radar DataTree framework uses:
- **xarray.DataTree**: Hierarchical data representation
- **Zarr v3**: Cloud-optimized storage format
- **Icechunk**: ACID-compliant transactional storage with version control
- **xradar**: Radar-specific I/O and analysis tools

Data is organized hierarchically by Volume Coverage Pattern (VCP) and sweep:
```
/VCP-34/sweep_0/  # Variables: DBZH, ZDR, RHOHV, PHIDP, VELOCITY
/VCP-34/sweep_1/
/VCP-12/sweep_0/
...
```

This is a documentation-focused repository. The actual library code under `src/radar_datatree/` is minimal — the primary content is four progressive, self-contained Jupyter notebook tutorials built with Sphinx + MyST-NB.

## Available Data

NEXRAD KLOT data on OSN:
- Bucket: `nexrad-arco`
- Prefix: `KLOT-RT`
- Endpoint: `https://umn1.osn.mghpcc.org`
- Access: Anonymous
- AWS Open Data Registry: Submitted via [PR #3039](https://github.com/awslabs/open-data-registry/pull/3039)

## Common Commands

### Environment Setup

```bash
# Conda (recommended)
conda env create -f environment.yml
conda activate radar-datatree

# uv
uv sync

# pip
pip install -e ".[dev]"
```

### Running Notebooks

```bash
cd notebooks
jupyter lab
```

### Linting and Formatting

CI runs all three checks — they must all pass:

```bash
ruff check .          # Linting (rules: E, W, F, I, B, UP; ignores E501; allows E402 in notebooks)
ruff format .         # Ruff formatting
black notebooks/      # Black formatting (notebooks directory)
ruff check --fix .    # Auto-fix linting issues
```

Pre-commit hooks (`.pre-commit-config.yaml`) run trailing-whitespace, end-of-file-fixer, check-yaml, check-added-large-files (max 1000KB), black, and ruff on commit.

### Building Documentation

```bash
sphinx-build -b html docs _build/html
```

Sphinx uses `myst_nb` in `cache` execution mode with a 600-second per-cell timeout (`nb_execution_timeout` in `docs/conf.py`). Notebooks are re-executed only when code changes.

## Pinned / Custom Dependencies

- **xarray**: Uses a custom async fork (`git+https://github.com/aladinor/xarray.git@async-dtreec`), not the official release
- **icechunk**: Pinned to a specific commit (`d11af22`) from git
- **zarr**: `>=3.1.2`
- **s3fs**: `>=2025.5.1`
- **uv**: Uses `unsafe-best-match` index strategy with `scientific-python-nightly-wheels` as extra index

## Quick Start (Programmatic Access)

```python
import xarray as xr
import icechunk as ic

# Connect to KLOT data
storage = ic.s3_storage(
    bucket='nexrad-arco',
    prefix='KLOT-RT',
    endpoint_url='https://umn1.osn.mghpcc.org',
    anonymous=True,
    force_path_style=True,
    region='us-east-1',
)
repo = ic.Repository.open(storage)
session = repo.readonly_session("main")

# Open DataTree (lazy loading)
dtree = xr.open_datatree(
    session.store,
    zarr_format=3,
    consolidated=False,
    chunks={},
    engine="zarr",
)
```

## Key Files

- `notebooks/1.NEXRAD-KLOT-Demo.ipynb`: AWS Open Data access demo — **access only**: connect, open the tree, narrow with `group_filter`/`group`, select one scan, plot `DBZH`. Pinned to a fixed pre-2020 event (KLOT VCP-212, 2016-07-27 13:01 UTC) so it cannot age out of the live archive. Deliberately does *not* plot the polarimetric quartet — that is NB2's job. **Filename is fixed**: this file is linked from the [AWS Open Data Registry page for nexrad-arco](https://registry.opendata.aws/nexrad-arco/). Never rename, move, or delete it; rewrites in place are fine.
- `notebooks/2.KLOT-LowSweeps.ipynb`: The `KLOT-lowsweeps` **virtual reference** archive — opens it directly (no glob-and-concatenate), explains why `sweep_0`/`sweep_1` are a split cut at the same 0.48° elevation, and plots the polarimetric panel for the same 2016 storm as NB1
- `notebooks/3.QVP-Workflow-Comparison.ipynb`: Intermediate — QVP reproduction, ARCO vs file-based performance comparison
- `notebooks/4.QPE-Scaling-Benchmark.ipynb`: Advanced — Marshall–Palmer QPE accumulation, 1-day live + cluster-scaling templates (`notebooks/3.QPE-Snow-Storm.ipynb` is retired/build-excluded)
- `docs/conf.py`: Sphinx configuration (myst_nb, sphinx_book_theme)

## Notebooks are self-contained

There is **no shared helper module** — `notebooks/demo_functions.py` was deleted. Each notebook
carries the code it uses so it runs standalone on Colab or from a copy-paste, and there is no
invisible import for readers to chase.

Self-containment is not licence for long notebooks. When code is needed in more than one notebook,
duplicate it in its simplest correct form rather than reaching for a module:

- keep scientific math verbatim (QVP azimuthal averaging, Z–R, equivalence tolerances);
- replace formatted-print blocks with a small `pandas` table;
- drop parameters and branches no notebook exercises;
- tag long figure builders `hide-input` so the rendered page stays readable.

Recurring inline helpers, by notebook:
- `plot_polarimetric_panel(scan)` — 2×2 Z/ZDR/RHOHV/PHIDP snapshot (NB2 only; NB1 plots `DBZH`
  alone so the two notebooks don't duplicate the same figure)
- `concat_sweep(dtree, sweep)` — stitch one sweep across `VCP-*` nodes along `vcp_time`. No longer
  executed anywhere: NB2 now reads the pre-stitched `KLOT-lowsweeps` virtual archive directly, and
  the only surviving copy is the non-executed cluster template in NB4. **Design rule if you
  reintroduce it: slice the time window *before* concatenating, never after.** Stitching the whole
  archive sorts ~1M scans onto one axis and gets slower every day the radar runs; that cost is
  exactly what the virtual low-sweep archive exists to remove. Use `join="exact"` so a mismatched
  azimuth/range grid raises instead of silently NaN-padding.
- `compute_qvp`, `list_nexrad_files`, `download_nexrad` (NB3)
- `rain_depth(z, a, b)` — Z–R depth; Marshall-Palmer rain a=200,b=1.6; Sekhon-Srivastava snow
  a=1780,b=2.21 (NB4)

## CI/CD

GitHub Actions workflow (`.github/workflows/render-notebooks.yml`):
- Triggers on push/PR to `main` when notebooks/, docs/, images/, or workflow files change
- Runs linting (ruff check, ruff format --check, black --check) before building
- Builds documentation with Sphinx (`sphinx-build -b html docs _build/html`)
- Deploys to GitHub Pages (main branch only)
- Uses uv with Python 3.12 and caches .venv
- 15-minute job timeout

There is no formal test suite — notebook execution via Sphinx serves as integration testing.

### Branch Protection

The `main` branch has protection rules enabled:
- **Pull requests required** — no direct pushes to main
- **1 approving review** required before merging
- **Stale reviews dismissed** — re-review needed after new commits
- **Enforce admins** — rules apply to org owners too
- **Force pushes and branch deletion blocked**

All changes must go through a feature branch and PR workflow.

## Reference Paper

Two distinct records — do not conflate them, and do not "correct" the preprint's title:

- **Journal article (submitted):** Ladino-Rincón et al. (2026). *Radar DataTree: A Cloud-Native
  AI-Ready Data Model for Accessible, Time-Aware Weather Radar Datasets.* Submitted to **IEEE
  Transactions on Big Data**. This is what the notebooks reproduce (NB3 Case Study I, NB4 Case
  Study II) and what "Cite this work" should point at.
- **Earlier preprint:** Ladino-Rincón & Nesbitt (2025). *Radar DataTree: A FAIR and Cloud-Native
  Framework for Scalable Weather Radar Archives.* arXiv:2510.24943 (28 Oct 2025). That really is
  the preprint's title on arXiv, so it stays verbatim wherever the preprint is cited.

## License

Apache License 2.0
