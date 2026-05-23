# About

## Parent platform

`radar-datatree` is the open-source on-ramp to **[AtmoScale](https://atmoscale.ai)** — the institutional platform for turning radar, satellite, and model data into cloud-native, decision-ready products. Use this repository to learn the data model, reproduce published results, or analyze events on your own. Talk to AtmoScale when you need it operationalized for your institution.

```{button-link} https://atmoscale.ai
:color: primary

Visit AtmoScale →
```

## Technology Stack

```{dropdown} Built on proven open-source technologies
:color: info
:icon: tools

| Component | Purpose |
|-----------|---------|
| **WMO FM-301 / CfRadial 2.1** | Standardized radar data model ensuring interoperability |
| **xarray.DataTree** | Hierarchical data structures for multi-dimensional arrays |
| **Zarr v3** | Cloud-optimized storage with chunked compression |
| **Icechunk** | ACID-compliant transactional storage with version control |
| **xradar** | Radar-specific I/O, QC, and processing utilities |
| **rustytree-xarray** | Rust-backed DataTree backend (recommended engine) |

The stack ensures compatibility with existing tools while enabling cloud-native workflows.
```

## Links

::::{grid} 2 2 4 4
:gutter: 2

:::{grid-item}
```{button-link} https://github.com/AtmoScale/radar-datatree
:color: primary
:outline:

GitHub Repository
```
:::

:::{grid-item}
```{button-link} https://doi.org/10.48550/arXiv.2510.24943
:color: secondary
:outline:

arXiv Preprint
```
:::

:::{grid-item}
```{button-link} https://registry.opendata.aws/nexrad-arco/
:color: warning
:outline:

AWS Open Data
```
:::

:::{grid-item}
```{button-link} https://xarray.dev
:color: info
:outline:

xarray Docs
```
:::

::::

## Citation

**Forthcoming paper (in preparation):**

> Ladino-Rincón, A., et al. (2026). *Radar DataTree: A FAIR and Cloud-Native Framework for Scalable Weather Radar Archives.* (Manuscript in preparation.)

**Earlier preprint:**

> Ladino-Rincón, A., & Nesbitt, S. W. (2025). *Radar DataTree: A FAIR and Cloud-Native Framework for Scalable Weather Radar Archives.* arXiv:2510.24943. [doi:10.48550/arXiv.2510.24943](https://doi.org/10.48550/arXiv.2510.24943)
