# radar-datatree

:::{div} rdt-hero

```{image} /_static/logo-banner.png
:alt: radar-datatree — Cloud-native, time-aware weather radar datasets
:class: only-light rdt-hero-banner
```

```{image} /_static/logo-banner-dark.png
:alt: radar-datatree — Cloud-native, time-aware weather radar datasets
:class: only-dark rdt-hero-banner
```

:::{div} rdt-tagline
Companion code for *Ladino-Rincón et al.* (2026, submitted to *IEEE Transactions on Big Data*). An open-source project by [AtmoScale](https://atmoscale.ai).
:::

:::

```{epigraph}
**The problem isn't NEXRAD data. It's the infrastructure around it.**

Open the full archive in five lines of Python — no bulk downloads, no file-by-file decoding, no manual archive assembly.
```

<div class="rdt-stat-bar">
  <div class="rdt-stat"><strong>Hours → seconds</strong><span><a href="3.QVP-Workflow-Comparison.html">preparation becomes analysis</a></span></div>
  <div class="rdt-stat"><strong>Open formats</strong><span><a href="about.html">Zarr v3 · Icechunk · no lock-in</a></span></div>
  <div class="rdt-stat"><strong>One dataset</strong><span><a href="1.NEXRAD-KLOT-Demo.html">every VCP and sweep, time-indexed</a></span></div>
</div>

:::{note}
No fixed speedup is quoted here on purpose. The gap depends on your network and hardware — repeat runs of the same benchmark on one machine spanned more than a threefold range — so [Notebook 3](3.QVP-Workflow-Comparison) measures it on *your* machine and prints the result, rather than asking you to trust ours. For what "the whole archive" does and does not mean in storage terms, see [how big is the archive](glossary.md#how-big-is-the-archive).
:::

## Choose your path

````{grid} 1 1 3 3
:gutter: 3

```{grid-item-card}
:link: 1.NEXRAD-KLOT-Demo
:link-type: doc
:class-card: rdt-cta-card

**Analyze your own event**
^^^

Open the KLOT archive, slice a single severe-weather scan straight from object storage, and plot it — in 5 lines.

+++
[Notebook 1 →](1.NEXRAD-KLOT-Demo) · [Quickstart →](quickstart.md)
```

```{grid-item-card}
:link: 3.QVP-Workflow-Comparison
:link-type: doc
:class-card: rdt-cta-card

**Reproduce paper results**
^^^

Reproduce Ryzhkov et al. (2016) Fig. 4 in `~10 s` on a laptop. Then push to seasonal scale with Marshall–Palmer QPE.

+++
[Notebook 3 →](3.QVP-Workflow-Comparison) · [Notebook 4 →](4.QPE-Scaling-Benchmark)
```

```{grid-item-card}
:link: about
:link-type: doc
:class-card: rdt-cta-card

**Understand the data model**
^^^

The DataTree / Icechunk / Zarr stack, the AtmoScale parent platform, and a glossary of every radar acronym in one place.

+++
[About →](about.md) · [Glossary →](glossary.md)
```

````

## What is radar-datatree?

**radar-datatree** is a [FAIR](https://www.go-fair.org/fair-principles/) and cloud-native framework that turns fragmented weather radar archives — millions of standalone binary files with no temporal indexing — into hierarchical, time-indexed, analysis-ready datasets queryable directly from object storage. Built on the WMO FM-301/CfRadial 2.1 standard, [xarray.DataTree](https://docs.xarray.dev/en/stable/user-guide/hierarchical-data.html), [Zarr v3](https://zarr.dev), and [Icechunk](https://icechunk.io).

Instead of downloading and parsing thousands of binary files, you get direct access to time-indexed, multidimensional arrays — right from your Python session.

```{toctree}
:hidden:
:maxdepth: 1
:caption: User guide

installation
quickstart
tutorials
glossary
about
```
