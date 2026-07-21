<p align="center">
  <img src="assets/logo-banner.png" alt="radar-datatree — Cloud-native, time-aware weather radar datasets" width="800">
</p>

<p align="center"><em>An open-source project by <a href="https://atmoscale.ai">AtmoScale</a> — radar data infrastructure for institutions.</em></p>

<p align="center">
  <a href="https://atmoscale.ai"><img src="https://img.shields.io/badge/by-AtmoScale-0F2F4D.svg" alt="By AtmoScale"></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"></a>
  <a href="https://doi.org/10.48550/arXiv.2510.24943"><img src="https://img.shields.io/badge/arXiv-2510.24943-b31b1b.svg" alt="arXiv"></a>
  <a href="https://atmoscale.github.io/radar-datatree/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue" alt="Documentation"></a>
  <a href="https://github.com/AtmoScale/radar-datatree/actions"><img src="https://github.com/AtmoScale/radar-datatree/actions/workflows/render-notebooks.yml/badge.svg" alt="CI"></a>
  <a href="https://registry.opendata.aws/nexrad-arco/"><img src="https://img.shields.io/badge/AWS-Open%20Data-orange" alt="AWS Open Data"></a>
</p>

---

Reproducing a published radar figure used to mean downloading hours of NEXRAD Level II files, decoding them, and stitching sweeps by hand. With **radar-datatree**, it's one `xarray` call against the cloud archive.

> Reproduce **[Ryzhkov et al. (2016)](https://doi.org/10.1175/JTECH-D-15-0020.1) Fig. 4** on a laptop — **hours of file preparation become seconds of analysis**, reading a fraction of the bytes. [Notebook 3](https://atmoscale.github.io/radar-datatree/3.QVP-Workflow-Comparison.html) runs both workflows, asserts they agree, and measures the gap on your machine.

<p>
  <a href="https://colab.research.google.com/github/AtmoScale/radar-datatree/blob/main/notebooks/1.NEXRAD-KLOT-Demo.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open Notebook 1 in Colab"></a>
  &nbsp;·&nbsp;
  <a href="https://atmoscale.github.io/radar-datatree/quickstart.html"><strong>5-line quickstart →</strong></a>
</p>

## Choose your path

| If you want to… | Start here |
|---|---|
| **Analyze your own event** | [Notebook 1 — KLOT demo](https://atmoscale.github.io/radar-datatree/1.NEXRAD-KLOT-Demo.html) opens the live archive in 5 lines and visualizes a polarimetric scan. The [quickstart](https://atmoscale.github.io/radar-datatree/quickstart.html) is the 30-second version. |
| **Grab the low sweep** | [Notebook 2 — KLOT low sweeps](https://atmoscale.github.io/radar-datatree/2.KLOT-LowSweeps.html) gets `sweep_0` across every VCP two ways: glob-and-concatenate, or open the pre-stitched `KLOT-lowsweeps` virtual archive. |
| **Reproduce paper results** | [Notebook 3 — QVP workflow comparison](https://atmoscale.github.io/radar-datatree/3.QVP-Workflow-Comparison.html) reproduces Ryzhkov et al. (2016). Then [Notebook 4 — QPE scaling](https://atmoscale.github.io/radar-datatree/4.QPE-Scaling-Benchmark.html) extends it to Marshall–Palmer rainfall accumulation. |
| **Understand the data model** | [About](https://atmoscale.github.io/radar-datatree/about.html) covers the DataTree / Icechunk / Zarr stack and the parent platform. [Glossary](https://atmoscale.github.io/radar-datatree/glossary.html) defines every radar acronym in one place. |

## Notebooks

| Notebook | Description | Open |
|---|---|---|
| [**1. NEXRAD KLOT demo**](https://atmoscale.github.io/radar-datatree/1.NEXRAD-KLOT-Demo.html) | Open weather radar archives in 5 lines — AWS Open Data Registry entry point. | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AtmoScale/radar-datatree/blob/main/notebooks/1.NEXRAD-KLOT-Demo.ipynb) |
| [**2. KLOT low sweeps**](https://atmoscale.github.io/radar-datatree/2.KLOT-LowSweeps.html) | Grab `sweep_0` across every VCP: glob-and-concatenate vs. the pre-stitched `KLOT-lowsweeps` virtual archive. | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AtmoScale/radar-datatree/blob/main/notebooks/2.KLOT-LowSweeps.ipynb) |
| [**3. QVP workflow comparison**](https://atmoscale.github.io/radar-datatree/3.QVP-Workflow-Comparison.html) | **Paper reproduction.** Reproduce Ryzhkov et al. (2016); benchmark ARCO vs file-based access. | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AtmoScale/radar-datatree/blob/main/notebooks/3.QVP-Workflow-Comparison.ipynb) |
| [**4. QPE scaling benchmark**](https://atmoscale.github.io/radar-datatree/4.QPE-Scaling-Benchmark.html) | Marshall–Palmer rainfall accumulation, 1 day live + 7d/30d/6mo cluster-recommended templates. | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AtmoScale/radar-datatree/blob/main/notebooks/4.QPE-Scaling-Benchmark.ipynb) |

**Available archives:** `nexrad-arco/KLOT` (Chicago) and `nexrad-arco/KVNX` (Vance AFB, OK) on AWS `us-east-1`. More NEXRAD radars are published to the same bucket as they're processed.

## Reproducing the paper

[Notebook 3 — QVP Workflow Comparison](https://atmoscale.github.io/radar-datatree/3.QVP-Workflow-Comparison.html) is the laptop-runnable companion to *Ladino-Rincón et al.* (2026, submitted to *IEEE Transactions on Big Data*; earlier preprint: [arXiv:2510.24943](https://doi.org/10.48550/arXiv.2510.24943)). It reproduces Figure 4 of [Ryzhkov et al. (2016)](https://doi.org/10.1175/JTECH-D-15-0020.1) for the May 20 2011 KVNX MCS, computing the QVP via two paths in one notebook and asserting numerical equivalence between them.

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

**Journal article (submitted):**

> Ladino-Rincón, A., et al. (2026). *Radar DataTree: A Cloud-Native AI-Ready Data Model for Accessible, Time-Aware Weather Radar Datasets.* Submitted to *IEEE Transactions on Big Data*.

**Earlier preprint:**

> Ladino-Rincón, A., & Nesbitt, S. W. (2025). *Radar DataTree: A FAIR and Cloud-Native Framework for Scalable Weather Radar Archives.* arXiv:2510.24943. https://doi.org/10.48550/arXiv.2510.24943

---

[Apache License 2.0](LICENSE) · [Alfonso Ladino-Rincón](https://github.com/aladinor) · [Stephen Nesbitt](https://github.com/swnesbitt) · University of Illinois Urbana-Champaign
