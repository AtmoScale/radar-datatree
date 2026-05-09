# Installation

Get **radar-datatree** running locally in two minutes. Requires **Python ≥ 3.12**.

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

```{note}
Verification snippet lands in the next PR — for now, the easiest check is to launch Jupyter (above) and open {doc}`Notebook 1 <1.NEXRAD-KLOT-Demo>`. If its first code cell runs without errors, your install is healthy.
```
