# Quickstart

Five lines of Python — every NEXRAD KLOT (Chicago, IL) scan ever published to the public archive, in one `xarray.DataTree`. No downloads, no decoders, no waiting.

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

That's it. `dt` is a hierarchical, time-indexed view of the entire KLOT archive on the [AWS Open Data Registry](https://registry.opendata.aws/nexrad-arco/), grouped by {term}`Volume Coverage Pattern <VCP>` and {term}`sweep`. Every variable is lazy — only the {term}`Zarr v3` chunks you slice into are fetched from S3.

## What's next

- {doc}`Notebook 1: NEXRAD KLOT Demo <1.NEXRAD-KLOT-Demo>` — the full access walkthrough: narrow the tree to one VCP and sweep, select a scan, plot its reflectivity.
- {doc}`Notebook 2: KLOT low sweeps <2.KLOT-LowSweeps>` — if you only need the lowest cuts, open the `KLOT-lowsweeps` virtual archive and get the 2×2 polarimetric view (Z, ZDR, RhoHV, PhiDP).
- {doc}`Tutorials <tutorials>` — paper reproduction and large-scale rainfall accumulation.
- {doc}`Installation <installation>` — if `import icechunk` failed, start here.

```{note}
`engine="rustytree"` is a Rust-backed `xarray.DataTree` backend (`rustytree-xarray` on PyPI) recommended for radar-datatree archives. Drop-in replacement for `engine="zarr"`, ~10× faster on icechunk repos served from object storage.
```
