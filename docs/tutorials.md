# Tutorials

Four runnable notebooks — each end-to-end on the public archives, no credentials. Take them in order; each one builds on what the last one taught.

:::{tip}
Run [Verify your install](installation.md#verify-your-install) once before the first tutorial to confirm `import xarray, icechunk` and the connection to `s3://nexrad-arco` work in your environment.
:::

````{grid} 1 1 2 2
:gutter: 3

```{grid-item-card}
:link: 1.NEXRAD-KLOT-Demo
:link-type: doc
:class-card: rdt-tutorial-card

**Open weather radar archives in 5 lines of code**

Open the KLOT (Chicago) archive on the [AWS Open Data Registry](https://registry.opendata.aws/nexrad-arco/) as one `xarray.DataTree`, narrow it to a single VCP and sweep, and read back one scan of a July 2016 hailstorm as reflectivity.

+++
[Read]{.rdt-meta-label} 5 min · [Run]{.rdt-meta-label} ~1 min · {bdg-success}`Beginner`
```

```{grid-item-card}
:link: 2.KLOT-LowSweeps
:link-type: doc
:class-card: rdt-tutorial-card

**Get only the sweep you need**

Only need the cuts closest to the ground? Open the `KLOT-lowsweeps` **virtual reference** archive and get `sweep_0` and `sweep_1` as continuous time axes over the whole record — no VCP bookkeeping, and no bytes copied. See why both sit at the same 0.5° elevation (the split cut), then plot Z, ZDR, RHOHV and PHIDP.

+++
[Read]{.rdt-meta-label} 5 min · [Run]{.rdt-meta-label} ~1 min · {bdg-success}`Beginner`
```

```{grid-item-card}
:link: 3.QVP-Workflow-Comparison
:link-type: doc
:class-card: rdt-tutorial-card

**Reproduce Ryzhkov et al. (2016): traditional vs ARCO**

Compute the QVP for the May 20, 2011 KVNX MCS via the traditional file workflow vs ARCO streaming and measure the gap — **~6 min vs ~10 s** on the same bytes.

+++
[Read]{.rdt-meta-label} 7 min · [Run]{.rdt-meta-label} ~6 min · {bdg-warning}`Intermediate`
```

```{grid-item-card}
:link: 4.QPE-Scaling-Benchmark
:link-type: doc
:class-card: rdt-tutorial-card

**QPE scaling: from hours to months**

Marshall–Palmer Z–R rainfall accumulation, live for one day. Cluster-recommended copy-paste templates for **7d / 30d / 6mo** runs included.

+++
[Read]{.rdt-meta-label} 5 min · [Run]{.rdt-meta-label} ~1 min · {bdg-warning}`Intermediate`
```

````

```{toctree}
:hidden:
:maxdepth: 1

1.NEXRAD-KLOT-Demo
2.KLOT-LowSweeps
3.QVP-Workflow-Comparison
4.QPE-Scaling-Benchmark
```
