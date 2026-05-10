# Installation

Get **radar-datatree** running locally in two minutes.

## Prerequisites

- **Python ≥ 3.12** — required by `xarray ≥ 2026.4` and the rest of the stack.
- **Network access** to `s3://nexrad-arco` on AWS `us-east-1` (anonymous reads — no AWS credentials needed).

## Install

We strongly recommend [**uv**](https://docs.astral.sh/uv/) — a fast Python package manager — but conda works too.

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

## Verify your install

Run the {doc}`Quickstart <quickstart>` snippet in a Python session (or a fresh notebook cell). If it prints a list of `VCP-*` nodes, your install is healthy — every dependency loaded, anonymous S3 reads work, and you're already streaming from the public archive. Then jump straight into {doc}`Notebook 1 <1.NEXRAD-KLOT-Demo>` for the full polarimetric walkthrough.

## What got installed

```{dropdown} Core radar-datatree stack
:color: info
:icon: package

| Package | Version | Why it matters |
|---|---|---|
| **xarray** | `≥ 2026.4` | Hierarchical `DataTree` data model. |
| **xradar** | `≥ 0.12` | Radar-specific I/O on top of xarray (CfRadial, NEXRAD Level II readers, QC). |
| **zarr** | `≥ 3.1.2` | Cloud-optimized chunked storage; required for the v3 spec used in `nexrad-arco`. |
| **icechunk** | `≥ 2.0.4` | ACID-compliant transactional layer over Zarr — opens the archive as a versioned repo. |
| **rustytree-xarray** | `≥ 0.2` | Rust-backed `DataTree` backend (`engine="rustytree"`); ~10× faster than `engine="zarr"` on icechunk repos served from object storage. |
| **s3fs** | `≥ 2025.5.1` | Anonymous S3 reads against the AWS Open Data bucket. |

Full dependency tree (including visualization extras for individual tutorials) lives in [`pyproject.toml`](https://github.com/AtmoScale/radar-datatree/blob/main/pyproject.toml).
```
