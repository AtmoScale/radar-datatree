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
Query decades of weather radar straight from object storage. An open-source project by [AtmoScale](https://atmoscale.ai).
:::

:::

```{epigraph}
**The problem isn't NEXRAD data. It's the infrastructure around it.**

Open the full archive in five lines of Python — no bulk downloads, no file-by-file decoding, no manual archive assembly.
```

<div class="rdt-highlights">
  <a class="rdt-highlight rdt-highlight--speed" href="3.QVP-Workflow-Comparison.html">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><polyline points="12 7 12 12 15.5 14"></polyline></svg>
    <strong>Hours &rarr; seconds</strong>
    <span>Preparation collapses into analysis. The benchmark measures the gap on your machine.</span>
  </a>
  <a class="rdt-highlight rdt-highlight--open" href="about.html">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 7 4 12 9 17"></polyline><polyline points="15 7 20 12 15 17"></polyline></svg>
    <strong>Open formats</strong>
    <span>Zarr v3, Icechunk and CfRadial2 all the way down. Nothing proprietary, no lock-in.</span>
  </a>
  <a class="rdt-highlight rdt-highlight--one" href="1.NEXRAD-KLOT-Demo.html">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="12 3 21 7.5 12 12 3 7.5 12 3"></polygon><polyline points="3 12.5 12 17 21 12.5"></polyline><polyline points="3 17 12 21.5 21 17"></polyline></svg>
    <strong>One dataset</strong>
    <span>Every VCP and sweep on a single time axis, instead of a directory of binary files.</span>
  </a>
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

The design and its benchmarks are described in *Ladino-Rincón et al.* (2026), *Radar DataTree: A Cloud-Native AI-Ready Data Model for Accessible, Time-Aware Weather Radar Datasets*, submitted to *IEEE Transactions on Big Data*. [Notebook 3](3.QVP-Workflow-Comparison) and [Notebook 4](4.QPE-Scaling-Benchmark) reproduce its two case studies — see [About](about.md) for the full citation.

```{toctree}
:hidden:
:maxdepth: 1
:caption: User guide

installation
quickstart
tutorials
glossary
about
changelog
```
