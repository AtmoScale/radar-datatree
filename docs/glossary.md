# Glossary

Quick reference for radar and infrastructure terms used across the tutorials.

## Radar terms

```{glossary}
ARCO
  **Analysis-Ready, Cloud-Optimized.** Data already chunked, compressed, and
  indexed so it can be queried directly from object storage without
  preprocessing or downloads.

DBZH
  Horizontal-polarization reflectivity factor, in decibels (dBZ). The primary
  radar variable — high values indicate intense precipitation, hail, or
  strong scatterers.

KLOT
  NEXRAD radar site near Chicago, IL. The public archive at
  `s3://nexrad-arco/KLOT` is the entry-point dataset for Notebook 1.

KVNX
  NEXRAD radar site near Vance AFB, OK. Used in Notebook 3 to reproduce
  Ryzhkov et al. (2016).

NEXRAD
  **Next Generation Weather Radar** — the U.S. national network of WSR-88D
  dual-polarization Doppler radars operated by NOAA/NWS.

PHIDP
  Differential propagation phase (Φ_DP), in degrees. Increases as the signal
  propagates through liquid precipitation; its range derivative (KDP) is
  used for rain-rate estimation.

Polarimetric
  A dual-polarization radar variable derived from comparing horizontal and
  vertical pulse returns. Includes ZDR, RHOHV, PHIDP, KDP. Used to classify
  hydrometeor type (rain, snow, hail) and improve QPE.

QPE
  **Quantitative Precipitation Estimation** — converting radar reflectivity
  into rainfall or snowfall rate using a Z–R or Z–S relationship.

QVP
  **Quasi-Vertical Profile** — an azimuthally averaged time-height
  cross-section of a polarimetric variable at fixed elevation, introduced by
  Ryzhkov et al. (2016).

RHOHV
  Co-polar correlation coefficient (ρ_HV), 0–1. High in pure liquid rain
  (≈ 0.98+); drops where hail, melting, or non-meteorological echoes are
  present.

Sweep
  A single 360° conical scan at a fixed antenna elevation. A NEXRAD VCP
  cycles through several sweeps (typically 5–16) at increasing elevations.

VCP
  **Volume Coverage Pattern** — a pre-defined sequence of sweeps that NEXRAD
  cycles through (e.g., VCP-12 general use, VCP-212 severe weather, VCP-34
  clear-air mode). Each VCP has different elevation angles and scan timing.

ZDR
  Differential reflectivity (Z_DR), in dB — the ratio of horizontal to
  vertical reflectivity. Sensitive to drop shape: large in oblate raindrops,
  near zero in tumbling hail or dry snow.
```

## Infrastructure terms

```{glossary}
DataTree
  Hierarchical container in xarray (`xarray.DataTree`) that holds multiple
  datasets in a tree of nodes — the model used here to organize radar
  volumes by VCP and sweep.

Icechunk
  ACID-compliant transactional storage layer over Zarr v3. Provides
  versioning, branches, and consistent reads against object storage. The
  `nexrad-arco` bucket is an Icechunk repository.

rustytree
  Rust-backed xarray DataTree backend (`rustytree-xarray` on PyPI). Drop-in
  replacement for `engine="zarr"`, ~10× faster on Icechunk repos served
  from S3. Used as `engine="rustytree"` in `xr.open_datatree(...)`.

Zarr v3
  Cloud-optimized chunked-array storage spec. Variables are split into
  independently compressed chunks; clients fetch only the chunks needed for
  a given query.
```
