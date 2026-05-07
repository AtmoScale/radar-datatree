# Access 1 Day of Radar Data in 5 Seconds

**Stop waiting. Stop downloading. Start analyzing.**

```{image} ../images/radar_datatree.png
:alt: Radar DataTree Architecture
:width: 700px
:align: center
```

---

## What is Radar DataTree?

Radar DataTree is a **FAIR and cloud-native framework** that transforms fragmented weather radar archives into analysis-ready datasets. Built on the **WMO FM-301/CfRadial 2.1 standard**, it provides a dataset-level abstraction that aggregates millions of individual radar files into a single hierarchical structure optimized for scientific analysis.

Instead of downloading and parsing thousands of binary files, you get direct access to time-indexed, multidimensional arrays—right from your Python session.

---

## Try It Now

```python
import xarray as xr
import icechunk as ic

# Connect to NEXRAD KLOT (Chicago) — no credentials needed
storage = ic.s3_storage(
    bucket='nexrad-arco', prefix='KLOT-RT',
    endpoint_url='https://umn1.osn.mghpcc.org',
    anonymous=True, force_path_style=True, region='us-east-1',
)
repo = ic.Repository.open(storage)
session = repo.readonly_session("main")

# Load the entire archive (lazy — only metadata is fetched)
dtree = xr.open_datatree(session.store, zarr_format=3, consolidated=False, chunks={}, engine="zarr")

# Plot reflectivity
dtree["VCP-34/sweep_0"].DBZH.sel(vcp_time="2025-12-13 15:36", method="nearest").plot(
    x="x", y="y", cmap="ChaseSpectral", vmin=-10, vmax=70
)
```

**What just happened?** You opened an entire day of radar data in seconds. Only metadata was fetched—actual data loads on demand when you compute or plot.

---

## Start here

```{note}
The repo is being refactored notebook-by-notebook against the new `engine="rustytree"` + xarray 2026.4 stack. The full set (QVP workflow comparison, QPE products, basin monitoring, rainfall estimation) returns as each refactor lands. For now, start with the AWS Open Data demo:
```

````{grid} 1 1 1 1
:gutter: 3

```{grid-item-card}
:link: 1.NEXRAD-KLOT-Demo
:link-type: doc
:class-card: sd-bg-light

**1. Open NEXRAD radar archives in 5 lines with radar-datatree**

The AWS Open Data Registry demo. Connect to `s3://nexrad-arco`, open the NEXRAD KLOT (Chicago, IL) archive as one `xarray.DataTree`, and visualize a polarimetric scan — without downloading a file.

- Anonymous icechunk session on AWS
- Open with `engine="rustytree"`
- 2×2 polarimetric finale

+++
~5 min read | Beginner
```

````

```{toctree}
:hidden:
:maxdepth: 1

1.NEXRAD-KLOT-Demo
```

---

## Run Locally

`````{tab-set}

````{tab-item} Conda
```bash
git clone https://github.com/AtmoScale/radar-datatree.git
cd radar-datatree
conda env create -f environment.yml
conda activate radar-datatree
jupyter lab notebooks/
```
````

````{tab-item} uv
```bash
git clone https://github.com/AtmoScale/radar-datatree.git
cd radar-datatree
uv sync
uv run jupyter lab notebooks/
```
````

`````

No multi-gigabyte downloads required—data streams directly from the cloud.

---

## Why Radar DataTree?

### The Problem

Traditional weather radar archives present fundamental challenges:
- **Millions of standalone binary files** in proprietary formats
- **No temporal indexing** — each scan must be downloaded and parsed independently
- **Hours to days** required for multi-week analyses
- **Fundamentally misaligned** with FAIR data principles

### The Solution

A dataset-level abstraction that aggregates individual radar files into a single hierarchical dataset. Query by time, elevation, or variable—and load only what you need.

### Performance Impact

| Task | Traditional Workflow | Radar DataTree | Speedup |
|------|---------------------|----------------|---------|
| **Data Loading** | 38.5 minutes | 1.5 seconds | **100x faster** |
| **QVP Computation** | 38.7 minutes | 23 seconds | **100x faster** |
| **Total Time (1 week)** | 77.2 minutes | 24.5 seconds | **189x faster** |

*Benchmark: 1 week of NEXRAD KLOT data (92 GB, 3,888 files).*

---

## Technology Stack

```{dropdown} Built on proven open-source technologies
:color: info
:icon: tools

| Component | Purpose |
|-----------|---------|
| **WMO FM-301 / CfRadial 2.1** | Standardized radar data model ensuring interoperability |
| **xarray.DataTree** | Hierarchical data structures for multi-dimensional arrays |
| **Zarr v3** | Cloud-optimized storage with chunked compression |
| **Icechunk** | ACID-compliant transactional storage with version control |
| **xradar** | Radar-specific I/O, QC, and processing utilities |

The stack ensures compatibility with existing tools while enabling cloud-native workflows.
```

---

## Links

::::{grid} 2 2 4 4
:gutter: 2

:::{grid-item}
```{button-link} https://github.com/AtmoScale/radar-datatree
:color: primary
:outline:

GitHub Repository
```
:::

:::{grid-item}
```{button-link} https://doi.org/10.48550/arXiv.2510.24943
:color: secondary
:outline:

Research Paper
```
:::

:::{grid-item}
```{button-link} https://xarray.dev
:color: info
:outline:

xarray Docs
```
:::

:::{grid-item}
```{button-link} https://icechunk.io
:color: info
:outline:

Icechunk Docs
```
:::

:::{grid-item}
```{button-link} https://github.com/awslabs/open-data-registry/pull/3039
:color: warning
:outline:

AWS Open Data
```
:::

::::

---

## Citation

> Ladino-Rincón, A., & Nesbitt, S. W. (2025). *Radar DataTree: A FAIR and Cloud-Native Framework for Scalable Weather Radar Archives.* arXiv:2510.24943. [doi:10.48550/arXiv.2510.24943](https://doi.org/10.48550/arXiv.2510.24943)
