<p align="center">
  <img src="assets/logo-banner.png" alt="radar-datatree — Cloud-native, time-aware weather radar datasets" width="800">
</p>

<p align="center">
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"></a>
  <a href="https://doi.org/10.48550/arXiv.2510.24943"><img src="https://img.shields.io/badge/arXiv-2510.24943-b31b1b.svg" alt="arXiv"></a>
  <a href="https://atmoscale.github.io/radar-datatree/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue" alt="Documentation"></a>
  <a href="https://github.com/AtmoScale/radar-datatree/actions"><img src="https://github.com/AtmoScale/radar-datatree/actions/workflows/render-notebooks.yml/badge.svg" alt="CI"></a>
  <a href="https://registry.opendata.aws/nexrad-arco/"><img src="https://img.shields.io/badge/AWS-Open%20Data-orange" alt="AWS Open Data"></a>
</p>

---

**radar-datatree** is a FAIR and cloud-native framework that turns fragmented NEXRAD Level II archives — millions of standalone binary files — into hierarchical, time-indexed, analysis-ready datasets queryable directly from object storage. Built on [xarray.DataTree](https://docs.xarray.dev/en/stable/user-guide/hierarchical-data.html), [Zarr v3](https://zarr.dev), and [Icechunk](https://icechunk.io).

## Start here

**[Notebook 1 — open weather radar archives in 5 lines of code →](https://atmoscale.github.io/radar-datatree/1.NEXRAD-KLOT-Demo.html)**

Connect to the public [`s3://nexrad-arco`](https://registry.opendata.aws/nexrad-arco/) bucket on AWS, open the NEXRAD KLOT (Chicago) archive as one `xarray.DataTree`, and visualize a polarimetric scan. No downloads, no credentials.

**Available archives:** `nexrad-arco/KLOT` on AWS (us-east-1). More NEXRAD radars are published to the same bucket as they're processed.

## Notebooks

| | |
|---|---|
| [**1. NEXRAD KLOT demo**](https://atmoscale.github.io/radar-datatree/1.NEXRAD-KLOT-Demo.html) | Open weather radar archives in 5 lines — AWS Open Data Registry entry point. |
| [**2. QVP workflow comparison**](https://atmoscale.github.io/radar-datatree/2.QVP-Workflow-Comparison.html) | **Paper reproduction.** Reproduce Ryzhkov et al. (2016); benchmark ARCO vs file-based access. |

## Reproducing the paper

[Notebook 2 — QVP Workflow Comparison](https://atmoscale.github.io/radar-datatree/2.QVP-Workflow-Comparison.html) is the laptop-runnable companion to [Ladino-Rincón & Nesbitt (2025)](https://doi.org/10.48550/arXiv.2510.24943). It reproduces Figure 4 of [Ryzhkov et al. (2016)](https://doi.org/10.1175/JTECH-D-15-0020.1) for the May 20 2011 KVNX MCS, computing the QVP via two paths in one notebook and asserting numerical equivalence between them.

| Path | What it does | Wall-clock (laptop) |
|---|---|---|
| **Traditional** | Downloads ~55 NEXRAD Level II files, decodes, concatenates | ~6 min |
| **ARCO streaming** | `engine="rustytree"` over `s3://nexrad-arco/KVNX` | ~10 s |

The paper reports 6.5 s ARCO / 308 s file-based on EC2 `m5.xlarge` — laptop numbers come in roughly the same shape.

## Install

Requires Python ≥ 3.12.

```bash
git clone https://github.com/AtmoScale/radar-datatree.git
cd radar-datatree
uv sync
```

Recommended: [uv](https://docs.astral.sh/uv/). Conda alternative: `conda env create -f environment.yml`.

## Citation

> Ladino-Rincón, A., & Nesbitt, S. W. (2025). *Radar DataTree: A FAIR and Cloud-Native Framework for Scalable Weather Radar Archives.* arXiv:2510.24943. https://doi.org/10.48550/arXiv.2510.24943

---

[Apache License 2.0](LICENSE) · [Alfonso Ladino-Rincón](https://github.com/aladinor) · [Stephen Nesbitt](https://github.com/swnesbitt) · University of Illinois Urbana-Champaign
