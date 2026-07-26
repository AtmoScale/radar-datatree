---
orphan: true
---

# Changelog

Notable changes to the tutorials, the published claims, and the data-access patterns.
Entries follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); dates are when the change
merged to `main`.

Because this is a documentation site rather than a released library, entries record **what a
reader would notice** — a notebook that behaves differently, a claim that changed, an access route
that moved — rather than every internal edit.

## Unreleased

### Changed

- The homepage hero now leads with what the project does — *"Query decades of weather radar
  straight from object storage"* — instead of announcing the accompanying manuscript. The paper
  reference moved into *What is radar-datatree?*, where it can say which notebooks reproduce its
  case studies ([#57](https://github.com/AtmoScale/radar-datatree/pull/57)).
- The three homepage highlights are now distinct cards, each with its own accent colour and icon.
  They previously rendered as three identical oversized headlines that wrapped awkwardly — the
  component had been designed for short numeric values like `60×` and did not survive being given
  phrases ([#57](https://github.com/AtmoScale/radar-datatree/pull/57)).

### Fixed

- **Corrected an overstated virtualization claim.** Notebook 2 said *"No bytes were copied to build
  it"* of `KLOT-lowsweeps`, and the glossary said it *"re-indexes the archive rather than copying
  it"*. Both are literally true and both invited the wrong conclusion: that repo references the
  **already-converted ARCO chunks**, so it avoids a *second* duplication, not the first. References
  that point straight at raw Level II — the stronger claim — need a NEXRAD codec at read time and
  are not demonstrated here yet ([#57](https://github.com/AtmoScale/radar-datatree/pull/57)).

## 2026-07-21

### Changed

- **Performance is now described qualitatively rather than with a fixed number.** The homepage
  advertised `60× faster`, `22× less RAM` and `100 TB queryable from a laptop`. Six runs of the
  same benchmark on one machine spanned 43×–145× — that variance is network-bound, not a property
  of the software — so the site says *hours of preparation become seconds of analysis* and
  [Notebook 3](3.QVP-Workflow-Comparison) measures the real ratio on your machine. `22× less RAM`
  was never a memory measurement; it is a decoded-byte ratio, now explained in the glossary
  ([#56](https://github.com/AtmoScale/radar-datatree/pull/56)).
- *"no downloads, no decoders, no waiting"* → *"no bulk downloads, no file-by-file decoding, no
  manual archive assembly"*. Queries do move bytes; the true distinction is that you never
  bulk-copy or hand-organize the archive ([#56](https://github.com/AtmoScale/radar-datatree/pull/56)).
- Notebooks 1 and 2 now show the **Arraylake** access route alongside the anonymous-S3 route that
  actually executes. Arraylake has no anonymous read — even a public repo requires login — so
  switching outright would have broken the AWS Open Data Registry promise on Notebook 1 and failed
  CI on fork PRs ([#55](https://github.com/AtmoScale/radar-datatree/pull/55)).
- **Notebook 1 is access-only**: connect, narrow the tree, select one scan, plot reflectivity. It is
  pinned to a fixed 2016 storm so it cannot age out of the live archive. **Notebook 2** now opens
  the `KLOT-lowsweeps` virtual archive directly and explains why `sweep_0`/`sweep_1` are a split cut
  at the same elevation; it owns the polarimetric panel
  ([#54](https://github.com/AtmoScale/radar-datatree/pull/54), [#55](https://github.com/AtmoScale/radar-datatree/pull/55)).
- Citation corrected repo-wide: the 2026 journal article is *Radar DataTree: A Cloud-Native
  AI-Ready Data Model for Accessible, Time-Aware Weather Radar Datasets*, submitted to **IEEE
  Transactions on Big Data**. The 2025 arXiv preprint keeps its own, different title
  ([#54](https://github.com/AtmoScale/radar-datatree/pull/54)).

### Added

- Glossary section **"How big is the archive?"**, separating the five numbers people call *size*:
  logical, compressed source, materialized, virtual reference, and bytes actually transferred
  ([#56](https://github.com/AtmoScale/radar-datatree/pull/56)).
- Weekly cold-cache CI run, so drift in the live public archives is caught without anyone touching
  the repo ([#54](https://github.com/AtmoScale/radar-datatree/pull/54)).

### Removed

- **`notebooks/demo_functions.py`.** Every notebook now carries the code it uses, so each runs
  standalone on Colab or from a copy-paste with no invisible import. The module was 1302 lines, but
  little of it was science — roughly 300 lines of formatted-print blocks became three small
  `pandas` tables ([#54](https://github.com/AtmoScale/radar-datatree/pull/54)).

### Fixed

- The QVP equivalence check used `.max()`, so a single all-NaN gate made the difference `NaN` and
  the assertion passed having compared nothing. Now `nanmax`, with NaN-mask and comparable-fraction
  guards and a scan-pairing check that tolerates the two paths' different clocks
  ([#54](https://github.com/AtmoScale/radar-datatree/pull/54)).
- Notebook 4 asserted nothing: a degenerate window produced 0 mm everywhere with a green build.
  Four scalar invariants added ([#54](https://github.com/AtmoScale/radar-datatree/pull/54)).
- Restored a dropped `plt.colorbar` and a `set_ylim` ordering that had shifted contour labels on
  three panels of the Ryzhkov figure ([#54](https://github.com/AtmoScale/radar-datatree/pull/54)).
- The social card baked `60× faster / 22× less RAM` into the `og:image`, so every link preview
  advertised claims the site had retired ([#56](https://github.com/AtmoScale/radar-datatree/pull/56)).
