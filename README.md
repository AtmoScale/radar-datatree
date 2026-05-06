<p align="center">
  <img src="assets/logo-banner.png" alt="radar-datatree — Cloud-native, time-aware weather radar datasets" width="800">
</p>

<p align="center">
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"></a>
  <a href="https://doi.org/10.48550/arXiv.2510.24943"><img src="https://img.shields.io/badge/arXiv-2510.24943-b31b1b.svg" alt="arXiv"></a>
  <a href="https://atmoscale.github.io/radar-datatree/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue" alt="Documentation"></a>
  <a href="https://github.com/AtmoScale/radar-datatree/actions"><img src="https://github.com/AtmoScale/radar-datatree/actions/workflows/render-notebooks.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/awslabs/open-data-registry/pull/3039"><img src="https://img.shields.io/badge/AWS-Open%20Data-orange" alt="AWS Open Data"></a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-notebooks">Notebooks</a> •
  <a href="#-citation">Citation</a>
</p>

---

## Overview

**Radar DataTree** transforms fragmented weather radar archives — millions of standalone binary files with no temporal indexing — into **FAIR-compliant, cloud-optimized datasets** built on [xarray.DataTree](https://docs.xarray.dev/en/stable/user-guide/hierarchical-data.html), [Zarr](https://zarr.dev), and [Icechunk](https://icechunk.io). This repository provides **examples and tutorials** for accessing and analyzing data in this format.

<p align="center">
  <img src="images/radar_datatree.png" alt="Radar DataTree Architecture" width="800"/>
</p>

| Metric | Traditional Workflow | Radar DataTree | Speedup |
|--------|---------------------|----------------|---------|
| **Load 92 GB metadata** | Minutes | **~1.5 seconds** | ~100x |
| **QVP generation (1 week)** | Hours | **Seconds** | **100x+** |
| **QPE accumulation (5 days)** | 30-60 minutes | **~12 seconds** | **70-150x** |

---

## Quick Start

NEXRAD KLOT (Chicago, IL) data is available on the **Open Storage Network** with anonymous access:

```python
import xarray as xr
import icechunk as ic

# Connect to cloud storage
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

# Open the entire archive (lazy loading - only metadata)
dtree = xr.open_datatree(
    session.store,
    zarr_format=3,
    consolidated=False,
    chunks={},
    engine="zarr",
    max_concurrency=5,
)

# Explore: 92 GB of data, loaded in ~1.5 seconds!
print(f"Dataset size: {dtree.nbytes / 1024**3:.2f} GB")

# Plot reflectivity from a specific time
dtree["VCP-34/sweep_0"].DBZH.sel(
    vcp_time="2025-12-13 15:36",
    method="nearest"
).plot(x="x", y="y", cmap="ChaseSpectral", vmin=-10, vmax=70)
```

---

## Installation

We strongly recommend [**uv**](https://docs.astral.sh/uv/) — a fast Python package and project manager written in Rust. Install it via the [official guide](https://docs.astral.sh/uv/getting-started/installation/) or run:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then clone and set up the project:

```bash
git clone https://github.com/AtmoScale/radar-datatree.git
cd radar-datatree
uv sync
```

<details>
<summary>Alternative: conda or pip</summary>

**conda:**
```bash
conda env create -f environment.yml
conda activate radar-datatree
```

**pip:**
```bash
pip install -e ".[dev]"
```

</details>

---

## Notebooks

| Notebook | Description |
|----------|-------------|
| [**1. Getting Started**](https://atmoscale.github.io/radar-datatree/1.NEXRAD-KLOT-Demo.html) | Data access, radar fundamentals, polarimetric visualization |
| [**2. QVP Workflow Comparison**](https://atmoscale.github.io/radar-datatree/2.QVP-Workflow-Comparison.html) | Reproduce a published QVP figure — ARCO vs file-based performance |
| [**3. QPE Snow Storm**](https://atmoscale.github.io/radar-datatree/3.QPE-Snow-Storm.html) | Snow accumulation estimation for the December 2025 Illinois storm |

Run locally: `cd notebooks && jupyter lab`

---

## Citation

> **Ladino-Rincón, A., & Nesbitt, S. W. (2025).** Radar DataTree: A FAIR and Cloud-Native Framework for Scalable Weather Radar Archives. *arXiv preprint arXiv:2510.24943 [cs.DC]*. https://doi.org/10.48550/arXiv.2510.24943

<details>
<summary>BibTeX</summary>

```bibtex
@article{ladino2025radardatatree,
  title={Radar DataTree: A FAIR and Cloud-Native Framework for Scalable Weather Radar Archives},
  author={Ladino-Rinc{\'o}n, Alfonso and Nesbitt, Stephen W.},
  journal={arXiv preprint arXiv:2510.24943},
  year={2025},
  doi={10.48550/arXiv.2510.24943}
}
```

</details>

---

## Contact

The conversion tool (**Raw2Zarr**) transforms raw radar files into the ARCO format. Contact us for access.

**[Alfonso Ladino-Rincón](https://github.com/aladinor)** · **[Stephen Nesbitt](https://github.com/swnesbitt)** · University of Illinois Urbana-Champaign

Built with [xarray](https://xarray.dev) · [xradar](https://xradar.dev) · [Zarr](https://zarr.dev) · [Icechunk](https://icechunk.io)

[Apache License 2.0](LICENSE)
