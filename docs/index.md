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
Companion code for *Ladino-Rincón et al.* (2026, in preparation). An open-source project by [AtmoScale](https://atmoscale.ai).
:::

:::

```{epigraph}
**The problem isn't NEXRAD data. It's the infrastructure around it.**

Open the full archive in five lines of Python — no downloads, no decoders, no waiting.
```

<div class="rdt-stat-bar">
  <div class="rdt-stat"><strong>60×</strong><span>faster than file-based</span></div>
  <div class="rdt-stat"><strong>22×</strong><span>less RAM</span></div>
  <div class="rdt-stat"><strong>100 TB</strong><span>queryable from a laptop</span></div>
</div>

## Choose your path

````{grid} 1 1 3 3
:gutter: 3

```{grid-item-card}
:link: 1.NEXRAD-KLOT-Demo
:link-type: doc
:class-card: rdt-cta-card

**Analyze your own event**
^^^

Open the live KLOT archive, slice a single severe-weather scan, and plot the polarimetric signature — in 5 lines.

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
