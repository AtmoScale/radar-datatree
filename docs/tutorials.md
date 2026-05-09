# Tutorials

Three progressive notebooks — each runs end-to-end on the public archives, no credentials needed.

```{note}
The repo is being refactored notebook-by-notebook against the new `engine="rustytree"` + xarray 2026.4 stack. The QPE / basin / rainfall tutorials return as each refactor lands.
```

````{grid} 1 1 2 2
:gutter: 3

```{grid-item-card}
:link: 1.NEXRAD-KLOT-Demo
:link-type: doc
:class-card: sd-bg-light

**1. Open weather radar archives in 5 lines of code**

Connect to NEXRAD on the [AWS Open Data Registry](https://registry.opendata.aws/nexrad-arco/), open the KLOT (Chicago, IL) archive as one `xarray.DataTree`, and visualize a polarimetric scan — modeled after Earthmover's [ERA5 sample-data demo](https://docs.earthmover.io/sample-data/era5).

- Anonymous icechunk session on `s3://nexrad-arco`
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

Paper reproduction. Compute QVPs for the May 20, 2011 KVNX MCS via both the traditional file-download workflow and ARCO streaming, and measure the gap. ~6 minutes traditional vs ~10 seconds ARCO on the same useful bytes.

- KVNX (MC3E campaign), OSN anonymous
- Traditional: 55 NEXRAD files downloaded + decoded
- ARCO: streaming via `engine="rustytree"`
- Numerical-equivalence assertion across both paths

+++
~7 min read + ~6 min run | Intermediate
```

```{grid-item-card}
:link: 3.QPE-Scaling-Benchmark
:link-type: doc
:class-card: sd-bg-light

**3. QPE scaling: from hours to months**

Marshall–Palmer Z–R rainfall accumulation over the May 20, 2011 KVNX MCS, run live for the 1-day window. Templates for 7-day, 30-day, and 6-month windows are included as cluster-recommended copy-paste blocks (the file-based 6-month run is ~10 hours).

- KVNX, sweep_0 (~0.5°), Marshall–Palmer (a=200, b=1.6)
- ARCO live: 1-day accumulation map (Cartopy)
- Cluster templates: 7d / 30d / 6mo + scaling figures

+++
~5 min read + ~1 min run | Intermediate
```

````

```{toctree}
:hidden:
:maxdepth: 1

1.NEXRAD-KLOT-Demo
2.QVP-Workflow-Comparison
3.QPE-Scaling-Benchmark
```
