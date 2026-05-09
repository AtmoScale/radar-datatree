```{image} ../assets/logo-banner.png
:alt: radar-datatree — Cloud-native, time-aware weather radar datasets
:width: 800px
:align: center
```

```{div} text-center
*Companion code for [Ladino-Rincón & Nesbitt (2025), arXiv:2510.24943](https://doi.org/10.48550/arXiv.2510.24943).*
```

---

## What is radar-datatree?

**radar-datatree** is a [FAIR](https://www.go-fair.org/fair-principles/) and cloud-native framework that turns fragmented weather radar archives — millions of standalone binary files with no temporal indexing — into hierarchical, time-indexed, analysis-ready datasets queryable directly from object storage. Built on the WMO FM-301/CfRadial 2.1 standard, [xarray.DataTree](https://docs.xarray.dev/en/stable/user-guide/hierarchical-data.html), [Zarr v3](https://zarr.dev), and [Icechunk](https://icechunk.io).

Instead of downloading and parsing thousands of binary files, you get direct access to time-indexed, multidimensional arrays — right from your Python session.

---

## Get started

````{grid} 1 1 3 3
:gutter: 3

```{grid-item-card}
:link: installation
:link-type: doc
:class-card: sd-bg-light

**1 · Install**
^^^

`uv sync` or conda — running locally in two minutes. Python ≥ 3.12.

+++
[Install →](installation.md)
```

```{grid-item-card}
:link: quickstart
:link-type: doc
:class-card: sd-bg-light

**2 · Quickstart**
^^^

Open the entire NEXRAD KLOT archive as one `xarray.DataTree` in 5 lines of code.

+++
[Quickstart →](quickstart.md)
```

```{grid-item-card}
:link: tutorials
:link-type: doc
:class-card: sd-bg-light

**3 · Tutorials**
^^^

Three runnable notebooks — from a beginner-friendly demo to paper reproduction and large-scale rainfall accumulation.

+++
[Tutorials →](tutorials.md)
```

````

```{toctree}
:maxdepth: 1
:caption: User guide

installation
quickstart
tutorials
about
```
