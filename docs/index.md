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
Companion code for *Ladino-Rincón et al.* (2026, in preparation).
:::

:::

## What is radar-datatree?

**radar-datatree** is a [FAIR](https://www.go-fair.org/fair-principles/) and cloud-native framework that turns fragmented weather radar archives — millions of standalone binary files with no temporal indexing — into hierarchical, time-indexed, analysis-ready datasets queryable directly from object storage. Built on the WMO FM-301/CfRadial 2.1 standard, [xarray.DataTree](https://docs.xarray.dev/en/stable/user-guide/hierarchical-data.html), [Zarr v3](https://zarr.dev), and [Icechunk](https://icechunk.io).

Instead of downloading and parsing thousands of binary files, you get direct access to time-indexed, multidimensional arrays — right from your Python session.

## Get started

````{grid} 1 1 3 3
:gutter: 3

```{grid-item-card}
:link: installation
:link-type: doc
:class-card: rdt-cta-card

**Install**
^^^

`uv sync` or conda — running locally in two minutes. Python ≥ 3.12.

+++
[Install →](installation.md)
```

```{grid-item-card}
:link: quickstart
:link-type: doc
:class-card: rdt-cta-card

**Quickstart**
^^^

Open the entire NEXRAD KLOT archive as one `xarray.DataTree` in 5 lines of code.

+++
[Quickstart →](quickstart.md)
```

```{grid-item-card}
:link: tutorials
:link-type: doc
:class-card: rdt-cta-card

**Tutorials**
^^^

Three runnable notebooks — from a beginner-friendly demo to paper reproduction and large-scale rainfall accumulation.

+++
[Tutorials →](tutorials.md)
```

````

```{toctree}
:hidden:
:maxdepth: 1
:caption: User guide

installation
quickstart
tutorials
about
```
