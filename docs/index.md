```{image} ../assets/logo-banner.png
:alt: radar-datatree — Cloud-native, time-aware weather radar datasets
:width: 800px
:align: center
```

---

## What is radar-datatree?

**radar-datatree** is a [FAIR](https://www.go-fair.org/fair-principles/) and cloud-native framework that turns fragmented weather radar archives — millions of standalone binary files with no temporal indexing — into hierarchical, time-indexed, analysis-ready datasets queryable directly from object storage. Built on the WMO FM-301/CfRadial 2.1 standard, [xarray.DataTree](https://docs.xarray.dev/en/stable/user-guide/hierarchical-data.html), [Zarr v3](https://zarr.dev), and [Icechunk](https://icechunk.io).

Instead of downloading and parsing thousands of binary files, you get direct access to time-indexed, multidimensional arrays — right from your Python session.

---

## Start here

```{note}
The repo is being refactored notebook-by-notebook against the new `engine="rustytree"` + xarray 2026.4 stack. The QPE / basin / rainfall tutorials return as each refactor lands.
```

````{grid} 1 1 2 2
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

```{grid-item-card}
:link: 2.QVP-Workflow-Comparison
:link-type: doc
:class-card: sd-bg-light

**2. Reproduce Ryzhkov et al. (2016): traditional vs ARCO**

Paper reproduction. Compute QVPs for the May 20, 2011 KVNX MCS using both the traditional file-download workflow and the ARCO streaming workflow, and measure the gap. ~6 minutes traditional vs ~10 seconds ARCO.

- KVNX (MC3E campaign), OSN anonymous
- Traditional: 55 NEXRAD files downloaded + decoded
- ARCO: streaming via `engine="rustytree"`

+++
~7 min read + ~6 min run | Intermediate
```

````

```{toctree}
:hidden:
:maxdepth: 1

1.NEXRAD-KLOT-Demo
2.QVP-Workflow-Comparison
```

---

## Install

We strongly recommend [**uv**](https://docs.astral.sh/uv/) — a fast Python package manager — but conda works too. Requires Python ≥ 3.12.

`````{tab-set}

````{tab-item} uv
```bash
git clone https://github.com/AtmoScale/radar-datatree.git
cd radar-datatree
uv sync
uv run jupyter lab notebooks/
```
````

````{tab-item} Conda
```bash
git clone https://github.com/AtmoScale/radar-datatree.git
cd radar-datatree
conda env create -f environment.yml
conda activate radar-datatree
jupyter lab notebooks/
```
````

`````

No multi-gigabyte downloads required — data streams directly from the cloud.

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
| **rustytree-xarray** | Rust-backed DataTree backend (recommended engine) |

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
```{button-link} https://registry.opendata.aws/nexrad-arco/
:color: warning
:outline:

AWS Open Data
```
:::

:::{grid-item}
```{button-link} https://xarray.dev
:color: info
:outline:

xarray Docs
```
:::

::::

---

## Citation

> Ladino-Rincón, A., & Nesbitt, S. W. (2025). *Radar DataTree: A FAIR and Cloud-Native Framework for Scalable Weather Radar Archives.* arXiv:2510.24943. [doi:10.48550/arXiv.2510.24943](https://doi.org/10.48550/arXiv.2510.24943)
