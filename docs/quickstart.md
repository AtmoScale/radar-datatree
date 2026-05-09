# Quickstart

Open the public NEXRAD KLOT (Chicago, IL) archive as a single `xarray.DataTree` — no downloads, no parsing, no preprocessing.

```python
import xarray as xr
import icechunk

storage = icechunk.s3_storage(
    bucket="nexrad-arco",
    prefix="KLOT",
    region="us-east-1",
    anonymous=True,
)
session = icechunk.Repository.open(storage).readonly_session("main")

dt = xr.open_datatree(session.store, engine="rustytree", chunks=None)
print(sorted(dt.children))   # → ['VCP-12', 'VCP-212', 'VCP-34', ...]
```

That's it. `dt` is a hierarchical, time-indexed view of the entire KLOT archive on the [AWS Open Data Registry](https://registry.opendata.aws/nexrad-arco/), grouped by Volume Coverage Pattern (VCP) and sweep. Every variable is lazy — Zarr chunks load only when you slice into them.

## What's next

- {doc}`Notebook 1: NEXRAD KLOT Demo <1.NEXRAD-KLOT-Demo>` — the full walkthrough, including a 2×2 polarimetric visualization (Z, ZDR, RhoHV, PhiDP).
- {doc}`Tutorials <tutorials>` — paper reproduction and large-scale rainfall accumulation.
- {doc}`Installation <installation>` — if `import icechunk` failed, start here.

```{note}
`engine="rustytree"` is a Rust-backed `xarray.DataTree` backend (`rustytree-xarray` on PyPI) recommended for radar-datatree archives. Drop-in replacement for `engine="zarr"`, ~10× faster on icechunk repos served from object storage.
```
