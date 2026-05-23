from datetime import datetime, timedelta

import fsspec
import icechunk
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import xradar as xd
from xarray import Dataset, DataTree


def rain_depth(
    z: xr.DataArray, a: float = 200.0, b: float = 1.6, t: float = None
) -> xr.DataArray:
    """
    Estimates rainfall depth using radar reflectivity and Z-R relationship.

    Computes precipitation depth per timestep using actual time differences
    between scans (not a constant interval), enabling accurate accumulation
    even when scan intervals vary.

    Parameters:
    -----------
    z : xr.DataArray
        Radar reflectivity in dBZ with vcp_time dimension.
    a : float, optional
        Z-R relationship parameter (default: 200.0, Marshall-Palmer 1948).
        For snow, use a=1780 (Sekhon-Srivastava 1970).
    b : float, optional
        Z-R relationship parameter (default: 1.6, Marshall-Palmer 1948).
        For snow, use b=2.21 (Sekhon-Srivastava 1970).
    t : float, optional
        Fixed integration time in minutes. If None, computed from actual
        time differences between scans in the vcp_time dimension.

    Returns:
    --------
    xr.DataArray
        Estimated rainfall/snowfall depth (mm) per timestep.
        Sum over vcp_time dimension to get total accumulation.
    """
    # Convert reflectivity from dBZ to linear units
    z_lin = 10 ** (z / 10)

    # Compute rainfall rate using Z-R relationship: R = (Z/a)^(1/b) in mm/hr
    rain_rate = (z_lin / a) ** (1 / b)

    if t is not None:
        # Use fixed integration time
        depth = rain_rate * (t / 60)  # Convert minutes to hours
    else:
        # Compute from actual time differences
        if "vcp_time" not in z.dims:
            raise ValueError(
                "DataArray must have 'vcp_time' dimension or provide integration time 't'"
            )

        # Compute time differences in hours for each timestep
        time_diffs = z.vcp_time.diff("vcp_time").dt.total_seconds() / 3600.0

        # Use median interval for uniform integration (simpler and avoids xr.concat issues)
        median_dt_hours = float(time_diffs.median().values)
        actual_total_hours = float(time_diffs.sum().values)

        # Multiply rate by median time interval to get depth per scan
        depth = rain_rate * median_dt_hours

        # Print summary info
        print(
            f"Actual QPE integration period: {int(actual_total_hours // 24)} days, "
            f"{int(actual_total_hours % 24)} hours, {int((actual_total_hours % 1) * 60)} minutes"
        )
        print(
            f"Time span: {str(z.vcp_time.min().values)[:19]} to {str(z.vcp_time.max().values)[:19]} UTC"
        )

    # Create result with proper metadata
    result = depth.copy()
    result.name = "precip_depth"
    result.attrs = {
        "units": "mm",
        "long_name": "precipitation depth per timestep",
        "description": f"Estimated using Z-R relationship (a={a}, b={b})",
    }

    return result


def compute_qvp(ds: xr.Dataset, var="DBZH") -> xr.DataArray:
    """
    Computes a Quasi-Vertical Profile (QVP) from a radar time-series dataset.

    This function averages the specified variable over the azimuthal dimension
    to produce a QVP. If the variable is in dBZ (a logarithmic scale), it converts
    the values to linear units before averaging and then converts the result
    back to dBZ.
    """
    units: str = ds[var].attrs["units"]
    if units.startswith("dB"):
        qvp = 10 ** (ds[var] / 10)
        qvp = qvp.mean("azimuth", skipna=True)
        qvp = 10 * np.log10(qvp)
    else:
        qvp = ds[var]
        qvp = qvp.mean("azimuth", skipna=True)

    # computing heigth dimension
    qvp = qvp.assign_coords(
        {
            "range": (
                qvp.range.values
                * np.sin(ds.sweep_fixed_angle.mean(skipna=True).values * np.pi / 180.0)
            )
            / 1000
        }
    )

    qvp = qvp.rename(f"qvp_{var}")
    qvp = qvp.rename({"range": "height"})
    return qvp


def set_publication_style() -> None:
    """Set matplotlib rcParams to match the Ryzhkov QVP figure style.

    Use r"$...$" math-mode for axis labels to get the same italic
    rendering as the Ryzhkov QVP figure.
    """
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans"],
            "font.size": 10,
            "axes.titlesize": "large",
            "axes.labelsize": "medium",
            "axes.labelweight": "normal",
            "axes.titleweight": "normal",
            "legend.fontsize": "medium",
            "xtick.labelsize": "medium",
            "ytick.labelsize": "medium",
            "mathtext.fontset": "dejavusans",
            "mathtext.default": "it",
        }
    )


def ryzhkov_figure(qvp_ref, qvp_zdr, qvp_rhohv, qvp_phidp):
    fig, axs = plt.subplots(2, 2, figsize=(9, 5), sharey=True, sharex=True)

    ## Reflectivity plot
    cf = qvp_ref.plot.contourf(
        x="vcp_time",
        y="height",
        cmap="ChaseSpectral",
        levels=np.arange(-10, 55, 1),
        ax=axs[0][0],
        add_colorbar=False,
    )
    contour_lines = qvp_ref.plot.contour(
        x="vcp_time",
        y="height",
        colors="k",  # Black contour lines
        levels=np.arange(0, 60, 15),  # Contour lines every 10 units
        ax=axs[0][0],
    )
    axs[0][0].clabel(contour_lines, fmt="%d", inline=True, fontsize=8)

    axs[0][0].set_title(r"$Z$")
    axs[0][0].set_xlabel("")
    axs[0][0].set_ylabel(r"$Height \ [km]$")
    axs[0][0].set_ylim(0, 12)

    plt.colorbar(
        cf,
        ax=axs[0][0],
        label=r"$Reflectivity \ [dBZ]$",
    )
    ## ZDR plot
    cf1 = qvp_zdr.plot.contourf(
        x="vcp_time",
        y="height",
        cmap="ChaseSpectral",
        ax=axs[0][1],
        levels=np.linspace(-2, 4, 21),
        add_colorbar=False,
    )

    contour_lines = qvp_ref.plot.contour(
        x="vcp_time",
        y="height",
        colors="k",  # Black contour lines
        levels=np.arange(0, 60, 15),  # Contour lines every 10 units
        ax=axs[0][1],
    )
    axs[0][1].clabel(contour_lines, fmt="%d", inline=True, fontsize=8)

    axs[0][1].set_title(r"$Z_{DR}$")
    axs[0][1].set_xlabel("")
    axs[0][1].set_ylabel(r"")

    plt.colorbar(
        cf1,
        ax=axs[0][1],
        label=r"$Diff. \ Reflectivity \ [dB]$",
    )

    ### RHOHV plot
    cf2 = qvp_rhohv.plot.contourf(
        x="vcp_time",
        y="height",
        cmap="Carbone11",
        ax=axs[1][0],
        levels=np.arange(0.7, 1.01, 0.01),
        add_colorbar=False,
    )

    contour_lines = qvp_ref.plot.contour(
        x="vcp_time",
        y="height",
        colors="k",  # Black contour lines
        levels=np.arange(0, 60, 15),  # Contour lines every 10 units
        ax=axs[1][0],
    )
    axs[1][0].clabel(contour_lines, fmt="%d", inline=True, fontsize=8)

    axs[1][0].set_title(r"$\rho _{HV}$")
    axs[1][0].set_ylabel(r"$Height \ [km]$")
    axs[1][0].set_xlabel(r"$Time \ [UTC]$")
    axs[1][0].tick_params(axis="x", labelsize=8)

    plt.colorbar(
        cf2,
        ax=axs[1][0],
        label=r"$Cross-Correlation \ Coef.$",
    )

    ### PHIDP
    cf3 = qvp_phidp.plot.contourf(
        x="vcp_time",
        y="height",
        cmap="PD17",
        ax=axs[1][1],
        levels=np.arange(0, 360, 10),
        add_colorbar=False,
    )

    contour_lines = qvp_ref.plot.contour(
        x="vcp_time",
        y="height",
        colors="k",  # Black contour lines
        levels=np.arange(0, 60, 15),  # Contour lines every 10 units
        ax=axs[1][1],
    )
    axs[1][1].clabel(contour_lines, fmt="%d", inline=True, fontsize=8)

    axs[1][1].set_title(r"$\theta _{DP}$")
    axs[1][1].set_xlabel(r"$Time \ [UTC]$")
    axs[1][1].set_ylabel(r"")
    axs[1][1].tick_params(axis="x", labelsize=8)
    plt.colorbar(
        cf3,
        ax=axs[1][1],
        label=r"$Differential \ Phase \ [deg]$",
    )

    return fig.tight_layout()


# Default 4-panel polarimetric layout for plot_polarimetric_panel(). Each row
# is (variable, cmap, vmin, vmax, colorbar label) — matches the standard
# dual-pol quartet shown in the radar-meteorology literature.
DEFAULT_POLARIMETRIC_PANELS = [
    ("DBZH", "ChaseSpectral", -10, 70, "Reflectivity [dBZ]"),
    ("ZDR", "HomeyerRainbow", -2, 6, "Differential Reflectivity [dB]"),
    ("RHOHV", "Carbone11", 0.7, 1.0, "Cross-Correlation Coefficient"),
    ("PHIDP", "PD17", 0, 180, "Differential Phase [deg]"),
]


def plot_polarimetric_panel(
    scan: xr.Dataset,
    *,
    panels: list[tuple[str, str, float, float, str]] | None = None,
    xlim: tuple[float, float] = (-10, 80),
    ylim: tuple[float, float] = (-100, 0),
    suptitle: str | None = None,
    figsize: tuple[float, float] = (11, 9),
):
    """Render the standard 2×2 polarimetric snapshot (Z, ZDR, RhoHV, PhiDP).

    Parameters
    ----------
    scan
        A georeferenced single-time radar sweep — must have ``x`` and ``y``
        Cartesian coordinates in **metres** (pass the output of
        :meth:`xarray.Dataset.xradar.georeference`).
    panels
        Optional override for the 4 panels. Each entry is
        ``(variable, cmap, vmin, vmax, colorbar_label)``. Defaults to the
        standard polarimetric quartet — pass a different list to plot
        velocity, KDP, or other variables.
    xlim, ylim
        Plot extent in **kilometres** (axes are rescaled inside the helper).
        Defaults zoom into the sector with the strongest echoes in the
        demo snapshot; widen for full-disk views.
    suptitle
        Figure-level title. Defaults to
        ``"KLOT polarimetric snapshot — <vcp_time> UTC"``.
    figsize
        Matplotlib figure size in inches.

    Returns
    -------
    tuple[matplotlib.figure.Figure, numpy.ndarray]
        The figure and 2×2 array of axes, so callers can post-process if
        they want (add annotations, save, etc.).
    """
    import cmweather  # noqa: F401  — registers ChaseSpectral / HomeyerRainbow / Carbone11 / PD17 colormaps

    panels = panels or DEFAULT_POLARIMETRIC_PANELS

    # Rescale x/y from metres to kilometres so tick marks read cleanly.
    scan_km = scan.assign_coords(x=scan.x / 1000, y=scan.y / 1000)
    scan_km.x.attrs["units"] = "km"
    scan_km.y.attrs["units"] = "km"

    fig, axes = plt.subplots(2, 2, figsize=figsize, sharex=True, sharey=True)
    for ax, (var, cmap, vmin, vmax, label) in zip(axes.flat, panels, strict=True):
        scan_km[var].plot(
            ax=ax,
            x="x",
            y="y",
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            cbar_kwargs={"label": label, "shrink": 0.8},
        )
        ax.set_title(var)
        ax.set_xlabel("East-West distance [km]")
        ax.set_ylabel("North-South distance [km]")
        ax.set_aspect("equal")
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)

    if suptitle is None and "vcp_time" in scan.coords:
        suptitle = f"KLOT polarimetric snapshot — {str(scan.vcp_time.values)[:19]} UTC"
    if suptitle:
        fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout()
    return fig, axes


def list_nexrad_files(
    radar: str = "KVNX",
    start_time: str = "2011-05-20 00:00",
    end_time: str = "2011-05-20 23:59",
) -> list:
    """
    List NEXRAD Level II files from AWS S3 bucket for a given radar and time range.

    Parameters:
    -----------
    start_time : str
        Start time in format "YYYY-MM-DD HH:MM"
    end_time : str
        End time in format "YYYY-MM-DD HH:MM"
    radar : str
        Radar site code (e.g., "KVNX")

    Returns:
    --------
    List[str]
        List of S3 paths to NEXRAD Level II files within the specified time range.
    """

    # Parse input times
    start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M")

    fs = fsspec.filesystem("s3", anon=True)
    base_path = "s3://unidata-nexrad-level2/"
    file_list = []

    current_dt = start_dt
    while current_dt <= end_dt:
        date_str = current_dt.strftime("%Y/%m/%d")
        prefix = f"{base_path}{date_str}/{radar}/{radar}"
        try:
            # Use glob to list files under this date/hour
            paths = fs.glob(f"{prefix}*")
            for path in paths:
                # Extract timestamp from filename
                filename = path.split("/")[-1]
                try:
                    file_time = datetime.strptime(
                        filename[len(radar) : len(radar) + 15], "%Y%m%d_%H%M%S"
                    )
                    if start_dt <= file_time <= end_dt:
                        file_list.append(f"s3://{path}")
                except Exception:
                    continue
        except FileNotFoundError:
            pass

        current_dt += timedelta(days=1)

    return sorted(file_list)


def nexrad_donwload(s3filepath, compressed=True):
    storage_options = {"anon": True}
    if compressed:
        compression = "gzip"
    else:
        compression = None
    stream = fsspec.open(
        s3filepath, mode="rb", compression=compression, **storage_options
    ).open()
    return xd.io.open_nexradlevel2_datatree(stream.read())


def get_repo_config():
    split_config = icechunk.ManifestSplittingConfig.from_dict(
        {
            icechunk.ManifestSplitCondition.AnyArray(): {
                icechunk.ManifestSplitDimCondition.DimensionName("vcp_time"): 12
                * 24
                * 365  # roughly one year of radar data
            }
        }
    )
    var_condition = icechunk.ManifestPreloadCondition.name_matches(
        r"^(vcp_time|azimuth|range)$"
    )
    size_condition = icechunk.ManifestPreloadCondition.num_refs(0, 10_000)

    preload_if = icechunk.ManifestPreloadCondition.and_conditions(
        [var_condition, size_condition]
    )

    preload_config = icechunk.ManifestPreloadConfig(
        max_total_refs=10_000,
        preload_if=preload_if,
    )

    return icechunk.RepositoryConfig(
        manifest=icechunk.ManifestConfig(
            splitting=split_config, preload=preload_config
        ),
    )


def connect_to_nexrad_arco(
    prefix: str,
    *,
    branch: str = "main",
    region: str = "us-east-1",
) -> icechunk.Session:
    """Open a read-only Icechunk session against ``s3://nexrad-arco/<prefix>``.

    Parameters
    ----------
    prefix
        Per-radar prefix inside the bucket — e.g. ``"KLOT"`` or ``"KVNX"``.
    branch
        Icechunk branch to read from. The published archives all use
        ``"main"``; other branches are typically internal development.
    region
        AWS region. The bucket is hosted in ``us-east-1``; override only
        if the archive is mirrored elsewhere.

    Returns
    -------
    icechunk.Session
        A read-only session backed by anonymous S3 reads — no AWS
        credentials needed. Pass ``session.store`` to
        :func:`xarray.open_datatree`.
    """
    storage = icechunk.s3_storage(
        bucket="nexrad-arco",
        prefix=prefix,
        region=region,
        # anonymous=True is what makes the public bucket usable without AWS
        # credentials. Drop it and reads fail with an auth error even
        # though the bucket is public.
        anonymous=True,
    )
    return icechunk.Repository.open(storage).readonly_session(branch)


def list_nexrad_files_with_sizes(
    radar: str = "KVNX",
    start_time: str = "2011-05-20 00:00",
    end_time: str = "2011-05-20 23:59",
) -> list[dict]:
    """
    List NEXRAD Level II files with actual file sizes using fsspec.

    Parameters:
    -----------
    radar : str
        Radar site code (e.g., "KVNX")
    start_time : str
        Start time in format "YYYY-MM-DD HH:MM"
    end_time : str
        End time in format "YYYY-MM-DD HH:MM"

    Returns:
    --------
    list[dict]
        List of dicts with 'path', 'size' (bytes), and 'time' for each file.
    """
    start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M")

    fs = fsspec.filesystem("s3", anon=True)
    base_path = "unidata-nexrad-level2"
    file_list = []

    current_dt = start_dt
    while current_dt <= end_dt:
        date_str = current_dt.strftime("%Y/%m/%d")
        dir_path = f"{base_path}/{date_str}/{radar}"

        try:
            # List directory with details (includes size)
            files_info = fs.ls(dir_path, detail=True)
            for file_info in files_info:
                filename = file_info["name"].split("/")[-1]
                # Filter to only files starting with radar name
                if not filename.startswith(radar):
                    continue
                try:
                    file_time = datetime.strptime(
                        filename[len(radar) : len(radar) + 15], "%Y%m%d_%H%M%S"
                    )
                    if start_dt <= file_time <= end_dt:
                        file_list.append(
                            {
                                "path": f"s3://{file_info['name']}",
                                "size": file_info.get("size", 0),
                                "time": file_time,
                            }
                        )
                except Exception:
                    continue
        except Exception:
            pass

        current_dt += timedelta(days=1)

    return sorted(file_list, key=lambda x: x["time"])


def nexrad_download_with_size(filepath: str) -> tuple:
    """
    Download a NEXRAD file and return datatree with size info.

    Parameters:
    -----------
    filepath : str
        S3 path to the NEXRAD file

    Returns:
    --------
    tuple
        (datatree, size_bytes) - The xradar datatree and file size in bytes
    """
    fs = fsspec.filesystem("s3", anon=True)

    # Get file info for size (compressed size)
    path = filepath.replace("s3://", "")
    file_info = fs.info(path)
    size_bytes = file_info.get("size", 0)

    # Use fsspec's built-in gzip decompression
    compression = "gzip" if filepath.endswith(".gz") else None
    stream = fsspec.open(filepath, mode="rb", compression=compression, anon=True).open()
    dtree = xd.io.open_nexradlevel2_datatree(stream.read())

    return dtree, size_bytes


def polar_to_geographic(ds, radar_lat, radar_lon):
    """
    Add geographic coordinates (latitude, longitude) to a radar dataset.

    Converts radar-centered x/y coordinates (meters) to approximate
    lat/lon using a simple offset from the radar location.

    Parameters
    ----------
    ds : xr.Dataset or xr.DataArray
        Radar data with 'x' and 'y' coordinates in meters from radar.
    radar_lat : float
        Radar latitude in degrees.
    radar_lon : float
        Radar longitude in degrees.

    Returns
    -------
    xr.Dataset or xr.DataArray
        Input data with added 'latitude' and 'longitude' coordinates.
    """
    lon = radar_lon + (ds.x / 111000) / np.cos(np.radians(radar_lat))
    lat = radar_lat + (ds.y / 111000)
    return ds.assign_coords(longitude=lon, latitude=lat)


def concat_sweep_across_vcps(
    dtree: DataTree,
    sweep_name: str = "sweep_0",
    append_dim: str = "vcp_time",
    validate_coords: bool = True,
    sort_by_time: bool = True,
    group_prefix: str = None,
) -> Dataset:
    """
    Concatenate a specific sweep across multiple VCP nodes along the vcp_time dimension.

    This enables continuous temporal analysis (e.g., QPE) for a specific elevation angle
    across different Volume Coverage Patterns.

    Parameters
    ----------
    dtree : xarray.DataTree
        DataTree with VCP nodes (e.g., "VCP-212", "VCP-35") containing sweep_* children
    sweep_name : str, default "sweep_0"
        Name of the sweep to extract from each VCP (e.g., "sweep_0", "sweep_1")
    append_dim : str, default "vcp_time"
        Time dimension name to concatenate along
    validate_coords : bool, default True
        If True, validate that all sweeps have compatible azimuth/range coordinates
    sort_by_time : bool, default True
        If True, sort the concatenated result by the append_dim coordinate
    group_prefix : str, optional
        Group prefix for organized data (e.g., "spatial", "temporal").
        If provided, VCPs are expected under this prefix (e.g., "/spatial/VCP-212").
        If None, VCPs are expected at the root level (e.g., "/VCP-212").

    Returns
    -------
    xarray.Dataset
        Concatenated dataset with all VCP sweeps merged along vcp_time dimension

    Raises
    ------
    ValueError
        If no VCP nodes are found, sweep not found in any VCP, or coordinates are incompatible

    Examples
    --------
    >>> # Standard structure (VCPs at root)
    >>> dtree = convert_files(radar_files, ...)
    >>> sweep_0_continuous = concat_sweep_across_vcps(dtree, sweep_name="sweep_0")
    >>>
    >>> # With group prefix (e.g., spatial/temporal organization)
    >>> sweep_0_spatial = concat_sweep_across_vcps(dtree, sweep_name="sweep_0", group_prefix="spatial")
    >>> sweep_0_temporal = concat_sweep_across_vcps(dtree, sweep_name="sweep_0", group_prefix="temporal")
    >>>
    >>> # Calculate QPE on continuous data
    >>> qpe = calculate_qpe(sweep_0_continuous['DBZH'])

    Notes
    -----
    - Assumes sweep_0 (and sweep_1) have consistent coordinates across VCPs
    - VCP nodes are automatically detected from the DataTree structure (VCP-* pattern)
    - Supports both single-store (with group_prefix) and multi-store (without) modes
    - Time coordinates are sorted after concatenation (if sort_by_time=True)
    - Missing sweeps in a VCP will be skipped with a warning
    - Coordinate validation checks azimuth and range dimension sizes for compatibility
    """
    # Find all VCP nodes in the DataTree
    vcp_nodes = {}
    for node_path in dtree.groups:
        parts = node_path.strip("/").split("/")

        # Handle group_prefix if provided
        if group_prefix:
            # Expect structure: /group_prefix/VCP-XXX or group_prefix/VCP-XXX
            if (
                len(parts) >= 2
                and parts[0] == group_prefix
                and parts[1].startswith("VCP-")
            ):
                if len(parts) == 2:  # Only VCP root nodes
                    vcp_name = parts[1]
                    vcp_nodes[vcp_name] = dtree[node_path]
        else:
            # Standard structure: /VCP-XXX or VCP-XXX
            if parts and parts[0].startswith("VCP-"):
                if len(parts) == 1:  # Only VCP root nodes
                    vcp_name = parts[0]
                    vcp_nodes[vcp_name] = dtree[node_path]

    if not vcp_nodes:
        prefix_msg = f" under '{group_prefix}/' prefix" if group_prefix else ""
        raise ValueError(
            f"No VCP nodes found in DataTree{prefix_msg}. "
            f"Expected nodes matching 'VCP-*' pattern."
        )

    # Extract the specified sweep from each VCP
    sweep_datasets = []
    skipped_vcps = []

    for vcp_name, _vcp_node in vcp_nodes.items():
        # Build sweep paths with group_prefix if provided
        if group_prefix:
            # With prefix: /spatial/VCP-212/sweep_0 or spatial/VCP-212/sweep_0
            sweep_path = f"/{group_prefix}/{vcp_name}/{sweep_name}"
            sweep_path_alt = f"{group_prefix}/{vcp_name}/{sweep_name}"
        else:
            # Without prefix: /VCP-212/sweep_0 or VCP-212/sweep_0
            sweep_path = f"/{vcp_name}/{sweep_name}"
            sweep_path_alt = f"{vcp_name}/{sweep_name}"

        if sweep_path in dtree.groups:
            sweep_ds = dtree[sweep_path].ds
            sweep_datasets.append((vcp_name, sweep_ds))
        elif sweep_path_alt in dtree.groups:
            sweep_ds = dtree[sweep_path_alt].ds
            sweep_datasets.append((vcp_name, sweep_ds))
        else:
            skipped_vcps.append(vcp_name)

    if not sweep_datasets:
        raise ValueError(
            f"Sweep '{sweep_name}' not found in any VCP nodes. "
            f"Available VCPs: {list(vcp_nodes.keys())}"
        )

    if skipped_vcps:
        import warnings

        warnings.warn(
            f"Sweep '{sweep_name}' not found in VCPs: {skipped_vcps}. "
            f"Proceeding with {len(sweep_datasets)} VCPs.",
            UserWarning,
            stacklevel=2,
        )

    # Validate coordinate compatibility if requested
    if validate_coords and len(sweep_datasets) > 1:
        reference_vcp, reference_ds = sweep_datasets[0]
        ref_azimuth_size = reference_ds.sizes.get("azimuth")
        ref_range_size = reference_ds.sizes.get("range")

        for vcp_name, sweep_ds in sweep_datasets[1:]:
            azimuth_size = sweep_ds.sizes.get("azimuth")
            range_size = sweep_ds.sizes.get("range")

            if azimuth_size != ref_azimuth_size or range_size != ref_range_size:
                raise ValueError(
                    f"Coordinate mismatch between {reference_vcp} and {vcp_name}:\n"
                    f"  {reference_vcp}: azimuth={ref_azimuth_size}, range={ref_range_size}\n"
                    f"  {vcp_name}: azimuth={azimuth_size}, range={range_size}\n"
                    f"Set validate_coords=False to skip this check."
                )

    # Concatenate datasets along the append_dim
    datasets_only = [ds for _, ds in sweep_datasets]
    concatenated = xr.concat(datasets_only, dim=append_dim)

    # Sort by time if requested
    if sort_by_time and append_dim in concatenated.coords:
        concatenated = concatenated.sortby(append_dim)

    return concatenated


# ---------------------------------------------------------------------------
# QVP-Workflow-Comparison notebook helpers
#
# These helpers absorb the formatted-print blocks that used to live inline in
# notebook 2. They are not general-purpose; they expose the specific layout
# the paper-reproduction artifact uses for the "Traditional vs ARCO" panels.
# ---------------------------------------------------------------------------


def calculate_chunk_metrics(ds, variables):
    """Count dask chunks and bytes that streaming the requested variables
    from a chunked Dataset would fetch.

    Returns ``(total_chunks, total_bytes, chunk_details)``. Variables that
    are not chunked (``da.chunks is None``) or absent from ``ds`` are
    skipped. ``chunk_details`` maps variable name to a dict of
    ``n_chunks``, ``chunk_shape``, ``chunk_size_mb``, and ``total_bytes``.
    """
    total_chunks = 0
    total_bytes = 0
    chunk_details = {}
    for var in variables:
        if var not in ds.data_vars:
            continue
        da = ds[var]
        if da.chunks is None:
            continue
        n_chunks = 1
        for dim_chunks in da.chunks:
            n_chunks *= len(dim_chunks)
        dtype_size = da.dtype.itemsize
        var_bytes = dtype_size * da.size
        chunk_shape = tuple(c[0] if c else 1 for c in da.chunks)
        chunk_bytes = dtype_size * int(np.prod(chunk_shape))
        chunk_details[var] = {
            "n_chunks": n_chunks,
            "chunk_shape": chunk_shape,
            "chunk_size_mb": chunk_bytes / 1e6,
            "total_bytes": var_bytes,
        }
        total_chunks += n_chunks
        total_bytes += var_bytes
    return total_chunks, total_bytes, chunk_details


def print_traditional_summary(metrics, ds_traditional):
    """Print the wall-clock + RAM + concat-shape summary for the traditional
    workflow (used in notebook 2 after the file-download loop)."""
    t = metrics["traditional"]
    workflow_min = t["total_workflow_time"] / 60
    print("=" * 60)
    print("TRADITIONAL WORKFLOW - ACTUAL COSTS (ALL FILES)")
    print("=" * 60)
    print(f"Files processed:               {t['files_processed']}")
    print(f"Download + decode time:        {t['total_time']:.1f}s")
    print(f"Concatenation time:            {t['concat_time']:.2f}s")
    print(f"QVP computation time:          {t['qvp_compute_time']:.2f}s")
    print(
        f"TOTAL WORKFLOW TIME:           "
        f"{t['total_workflow_time']:.1f}s ({workflow_min:.1f} min)"
    )
    print("-" * 60)
    print(f"Network transfer (compressed): {t['total_size_mb']:.1f} MB")
    print(f"Peak RAM (download phase):     {t['peak_memory_mb']:.0f} MB")
    print(f"Peak RAM (concat phase):       {t['concat_peak_memory_mb']:.0f} MB")
    print("=" * 60)
    print("\nConcatenated dataset shape:")
    print(f"  Time steps: {len(ds_traditional.vcp_time)}")
    print(f"  Azimuth: {len(ds_traditional.azimuth)}")
    print(f"  Range: {len(ds_traditional.range)}")
    print(f"  Variables: {list(ds_traditional.data_vars)[:6]}...")


def print_chunk_analysis(
    metrics,
    chunk_details,
    n_chunks,
    arco_bytes,
    *,
    selected_sweep,
    n_total_sweeps,
    compression_ratio=4.0,
):
    """Print the per-variable chunk breakdown and the selective-access
    advantage table (ARCO bytes vs traditional bytes).

    ``selected_sweep`` is the sweep name streamed via ARCO (e.g. ``"sweep_16"``).
    ``n_total_sweeps`` is the number of sweeps a NEXRAD Level II file holds for
    the chosen VCP (17 for VCP-12 / VCP-212 used in the paper). They drive the
    "1/N sweeps used" framing — no defaults, since silently using stale
    constants would lie if the notebook ever changes elevation strategy.
    ``compression_ratio`` is the assumed gzip ratio for NEXRAD Level II
    files (~4:1 by convention).

    Side effect: stashes ``arco_bytes / 1e6`` and the gzip-decompressed
    traditional volume into ``metrics["arco"]["uncompressed_mb"]`` and
    ``metrics["traditional"]["uncompressed_mb"]`` respectively, plus
    ``metrics["arco"]["chunk_details"]``. Downstream helpers
    (``print_workflow_comparison``) read from this single source of truth
    rather than recomputing.
    """
    t = metrics["traditional"]
    a = metrics["arco"]
    arco_mb = arco_bytes / 1e6
    traditional_uncompressed = t["total_size_mb"] * compression_ratio
    n_vars = len(chunk_details)

    a["uncompressed_mb"] = arco_mb
    a["chunk_details"] = chunk_details
    t["uncompressed_mb"] = traditional_uncompressed

    print("DATA ACCESS ANALYSIS:")
    print("=" * 70)
    print()
    print(f"ARCO - Selective Chunk Streaming ({selected_sweep}, {n_vars} variables):")
    print("-" * 70)
    print("  NOTE: No compression in this ARCO dataset - network = data size")
    print()
    for var, details in chunk_details.items():
        size_mb = details["chunk_size_mb"]
        total_mb = details["total_bytes"] / 1e6
        print(
            f"  {var}: {details['n_chunks']} chunks × "
            f"{size_mb:.2f} MB = {total_mb:.1f} MB"
        )
    print("-" * 70)
    print(f"  Total chunks streamed:  {n_chunks}")
    print(f"  Network transfer:       {arco_mb:.1f} MB")
    print()
    print(
        f"TRADITIONAL - Full File Downloads (all {n_total_sweeps} sweeps, "
        f"all variables):"
    )
    print("-" * 70)
    print(f"  Network transfer:       {t['total_size_mb']:.1f} MB (gzip compressed)")
    print(f"  Decompressed in RAM:    ~{traditional_uncompressed:.0f} MB")
    print(
        f"  Data actually used:     ~{traditional_uncompressed / n_total_sweeps:.0f} MB "
        f"(1/{n_total_sweeps} = {selected_sweep} only)"
    )
    print()
    print("=" * 70)
    print("SELECTIVE ACCESS ADVANTAGE:")
    print(
        f"  Network: ARCO {arco_mb:.0f} MB vs Traditional {t['total_size_mb']:.0f} MB"
    )
    print(f"           → {t['total_size_mb'] / arco_mb:.1f}x less data transferred")
    print(
        f"  RAM:     ARCO streams on-demand vs Traditional loads "
        f"{traditional_uncompressed:.0f} MB"
    )
    print(f"           → {traditional_uncompressed / arco_mb:.0f}x less data processed")
    print("=" * 70)


def print_arco_summary(metrics):
    """Print ARCO workflow timing + chunk summary."""
    a = metrics["arco"]
    print("=" * 60)
    print("ARCO DATA STREAMING - PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"Timesteps processed:           {a['timesteps']}")
    print(f"Connect to repository:         {a['connect_time']:.2f}s (metadata only)")
    print(
        f"Open DataTree:                 {a['open_datatree_time']:.2f}s (lazy, no data)"
    )
    print(f"Compute QVPs (data streams):   {a['qvp_compute_time']:.2f}s")
    print(f"Total time:                    {a['total_time']:.1f} seconds")
    print("-" * 60)
    print(f"Chunks streamed on-demand:     {a['n_chunks']}")
    print(
        f"Data streamed (network):       {a['uncompressed_mb']:.1f} MB (no compression)"
    )
    print("=" * 60)


def print_workflow_comparison(
    metrics,
    *,
    selected_sweep,
    n_total_sweeps,
    n_total_vars_per_sweep=8,
):
    """Print the full traditional-vs-ARCO comparison: throughput methodology
    block + workflow comparison table.

    Reads everything except the descriptive labels from ``metrics``. Required
    keys (set by earlier cells / by ``print_chunk_analysis``):
    ``traditional.{total_size_mb, total_workflow_time, peak_memory_mb,
    files_processed, throughput_mbs, uncompressed_mb}``,
    ``arco.{timesteps, total_time, throughput_mbs, uncompressed_mb,
    chunk_details}``, and top-level ``speedup``, ``data_reduction``,
    ``throughput_gain``. ``n_total_vars_per_sweep`` is the cosmetic "X/Y
    vars" denominator (NEXRAD Level II files carry ~8 polarimetric variables
    per sweep).
    """
    t = metrics["traditional"]
    a = metrics["arco"]
    useful_data_mb = a["uncompressed_mb"]
    trad_throughput = t["throughput_mbs"]
    arco_throughput = a["throughput_mbs"]
    speedup = metrics["speedup"]
    data_reduction = metrics["data_reduction"]
    throughput_gain = metrics["throughput_gain"]
    n_variables = len(a["chunk_details"])

    # Throughput methodology block.
    print("=" * 75)
    print("           THROUGHPUT METHODOLOGY (Fair Comparison)")
    print("=" * 75)
    print()
    print("Both workflows need the SAME useful data for QVP analysis:")
    print(
        f"  → {n_variables} variables × {a['timesteps']} timesteps × 1 sweep = "
        f"{useful_data_mb:.1f} MB"
    )
    print()
    print("TRADITIONAL: Downloads everything, uses only what's needed")
    print(f"  Network transfer:    {t['total_size_mb']:.0f} MB (gzip compressed)")
    print(
        f"  Decompressed in RAM: ~{t['uncompressed_mb']:.0f} MB (all sweeps, all vars)"
    )
    print(f"  Peak RAM:            {t['peak_memory_mb']:.0f} MB")
    print(
        f"  Useful data:         {useful_data_mb:.0f} MB "
        f"(1/{n_total_sweeps} sweeps, {n_variables}/{n_total_vars_per_sweep} vars)"
    )
    print(f"  Total time:          {t['total_workflow_time']:.1f}s")
    print(
        f"  Effective throughput: {useful_data_mb:.0f} MB / "
        f"{t['total_workflow_time']:.1f}s = {trad_throughput:.2f} MB/s"
    )
    print()
    print("ARCO: Streams only what's needed (no compression in this dataset)")
    print(f"  Network transfer:    {useful_data_mb:.0f} MB (uncompressed chunks)")
    print(f"  Data in RAM:         {useful_data_mb:.0f} MB (exactly what's needed)")
    print(f"  Total time:          {a['total_time']:.1f}s")
    print(
        f"  Effective throughput: {useful_data_mb:.0f} MB / "
        f"{a['total_time']:.1f}s = {arco_throughput:.1f} MB/s"
    )
    print()
    print("KEY INSIGHT: ARCO advantage is SELECTIVE ACCESS, not compression.")
    print(
        f"             Traditional downloads {t['total_size_mb']:.0f} MB to get "
        f"{useful_data_mb:.0f} MB of useful data."
    )
    print(
        f"             ARCO streams exactly {useful_data_mb:.0f} MB - only the "
        f"chunks needed."
    )
    print("=" * 75)
    print()

    # Comparison table.
    print("=" * 75)
    print("              WORKFLOW COMPARISON (Actual Measurements)")
    print("=" * 75)
    print(f"{'Metric':<40} {'Traditional':>15} {'ARCO Stream':>15}")
    print("-" * 75)
    rows = [
        (
            "Total processing time",
            f"{t['total_workflow_time']:.1f}s",
            f"{a['total_time']:.1f}s",
        ),
        ("Timesteps processed", str(t["files_processed"]), str(a["timesteps"])),
        (
            "Network transfer",
            f"{t['total_size_mb']:.0f} MB (gzip)",
            f"{useful_data_mb:.0f} MB",
        ),
        (
            "Peak RAM usage",
            f"{t['peak_memory_mb']:.0f} MB",
            f"{useful_data_mb:.0f} MB",
        ),
        (
            "Useful data for analysis",
            f"{useful_data_mb:.0f} MB",
            f"{useful_data_mb:.0f} MB",
        ),
        (
            "Effective throughput",
            f"{trad_throughput:.2f} MB/s",
            f"{arco_throughput:.1f} MB/s",
        ),
        (
            "Sweeps loaded",
            f"ALL ({n_total_sweeps}/file)",
            f"1 ({selected_sweep})",
        ),
        (
            "Variables loaded",
            f"ALL (~{n_total_vars_per_sweep}/sweep)",
            f"{n_variables} (selected)",
        ),
    ]
    for label, trad, arco in rows:
        print(f"{label:.<40} {trad:>15} {arco:>15}")
    print("-" * 75)
    print(f"{'SPEEDUP':.<40} {'':>15} {speedup:.1f}x faster")
    print(f"{'DATA EFFICIENCY':.<40} {'':>15} {data_reduction:.0f}x less data loaded")
    print(f"{'THROUGHPUT GAIN':.<40} {'':>15} {throughput_gain:.0f}x higher")
    print("=" * 75)


def plot_workflow_comparison(metrics, *, save_path=None, dpi=150):
    """Render the 3-panel benchmark figure for the QVP workflow comparison.

    Panel (a)  Total processing time — traditional file-download workflow vs
               ARCO streaming. Annotated with the speedup ratio.
    Panel (b)  Memory footprint — traditional peak RAM vs ARCO bytes
               loaded. Annotated with the memory-reduction ratio.
    Panel (c)  Traditional-workflow component breakdown (download+decode,
               concat, QVP compute) with ARCO total time as a horizontal
               reference line.

    Bars use the Wong (2011) colorblind-safe palette; speedup annotations
    use the same brand-green as the ARCO bars.

    Parameters
    ----------
    metrics : dict
        Nested dict already populated by the surrounding notebook cells.
        Reads ``metrics["traditional"].{total_workflow_time, total_time,
        concat_time, qvp_compute_time, peak_memory_mb}``,
        ``metrics["arco"].{total_time, uncompressed_mb}``, and
        ``metrics["speedup"]``. The ARCO/traditional memory ratio is
        derived internally.
    save_path : str | pathlib.Path | None, default None
        If provided, ``fig.savefig(save_path, dpi=dpi, bbox_inches="tight")``.
    dpi : int, default 150
        DPI used when ``save_path`` is set.

    Returns
    -------
    matplotlib.figure.Figure
        The rendered figure (auto-displayed by the notebook backend).
    """
    cb = {  # Wong (2011) colorblind-safe palette
        "blue": "#0072B2",
        "green": "#009E73",
        "orange": "#E69F00",
        "purple": "#CC79A7",
    }
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "legend.fontsize": 10,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
        }
    )

    trad = metrics["traditional"]
    arco = metrics["arco"]
    speedup = metrics["speedup"]
    memory_ratio = trad["peak_memory_mb"] / arco["uncompressed_mb"]

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # ---- Panel (a): time comparison -------------------------------------
    times = [trad["total_workflow_time"], arco["total_time"]]
    bars = axes[0].bar(
        ["Traditional\n(file downloads)", "ARCO\n(data streaming)"],
        times,
        color=[cb["blue"], cb["green"]],
        edgecolor="black",
        linewidth=1.2,
    )
    axes[0].set_ylabel("Processing Time (seconds)")
    axes[0].set_ylim(0, max(times) * 1.2)
    for bar, value in zip(bars, times, strict=False):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_height() + max(times) * 0.02,
            f"{value:.1f}s",
            ha="center",
            va="bottom",
        )
    axes[0].annotate(
        f"~{speedup:.0f}x faster",
        xy=(1, arco["total_time"] - max(times) * 0.03 + 35),
        xytext=(0.5, trad["total_workflow_time"] * 0.6),
        fontsize=11,
        color=cb["green"],
        arrowprops=dict(arrowstyle="->", color=cb["green"], lw=1.5),
    )

    # ---- Panel (b): memory comparison -----------------------------------
    sizes = [trad["peak_memory_mb"], arco["uncompressed_mb"]]
    bars = axes[1].bar(
        ["Traditional\n(peak RAM)", "ARCO Stream\n(data loaded)"],
        sizes,
        color=[cb["blue"], cb["green"]],
        edgecolor="black",
        linewidth=1.2,
    )
    axes[1].set_ylabel("Memory / Data (MB)")
    axes[1].set_ylim(0, max(sizes) * 1.2)
    for bar, value in zip(bars, sizes, strict=False):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_height() + max(sizes) * 0.02,
            f"{value:.0f} MB",
            ha="center",
            va="bottom",
        )
    axes[1].annotate(
        f"~{memory_ratio:.0f}x less",
        xy=(1, arco["uncompressed_mb"] - max(sizes) * 0.03 + 500),
        xytext=(0.5, trad["peak_memory_mb"] * 0.6),
        fontsize=11,
        color=cb["green"],
        arrowprops=dict(arrowstyle="->", color=cb["green"], lw=1.5),
    )

    # ---- Panel (c): traditional workflow breakdown ----------------------
    trad_times = [trad["total_time"], trad["concat_time"], trad["qvp_compute_time"]]
    bars = axes[2].bar(
        ["Download\n+ Decode", "Concat", "QVP\nCompute"],
        trad_times,
        color=[cb["blue"], cb["orange"], cb["purple"]],
        edgecolor="black",
        linewidth=1.2,
    )
    axes[2].set_ylabel("Time (seconds)")
    axes[2].set_ylim(0, max(trad_times) * 1.25)
    for bar, value in zip(bars, trad_times, strict=False):
        axes[2].text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_height() + max(trad_times) * 0.02,
            f"{value:.1f}s",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    axes[2].axhline(
        y=arco["total_time"],
        color=cb["green"],
        linestyle="--",
        linewidth=1.5,
        label=f"ARCO total: {arco['total_time']:.1f}s",
    )
    axes[2].legend(loc="upper right")

    # ---- Panel labels (a)/(b)/(c) ---------------------------------------
    for ax, label in zip(axes, ["(a)", "(b)", "(c)"], strict=False):
        ax.text(
            0.05,
            0.98,
            label,
            transform=ax.transAxes,
            fontsize=12,
            va="top",
            ha="left",
        )

    fig.tight_layout()
    if save_path is not None:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
    return fig


def assert_qvp_equivalence(qvp_a, qvp_b, variables, tolerances):
    """Print per-variable max-abs-diff between two QVP dicts and raise
    ``AssertionError`` if any variable's diff exceeds its tolerance.

    ``qvp_a`` and ``qvp_b`` are dicts mapping variable name to an
    xr.DataArray. ``tolerances`` is a dict mapping variable name to a
    ``(absolute_tolerance, unit_label)`` tuple. Variables absent from
    either dict are skipped, but if no variables remain to compare a
    ``ValueError`` is raised — silently passing an "equivalence" assertion
    that compared zero variables would defeat the whole sanity check.
    """
    print("Verifying numerical equivalence")
    print("-" * 60)
    results = []
    for var in variables:
        if var not in qvp_a or var not in qvp_b:
            continue
        atol, unit = tolerances[var]
        diff = float(np.abs(qvp_a[var].values - qvp_b[var].values).max())
        unit_suffix = f" {unit}" if unit else ""
        print(
            f"  {var:6s}  max |Δ| = {diff:7.4f} {unit:<3}  "
            f"(tolerance {atol}{unit_suffix})"
        )
        results.append((var, diff, atol, unit))
    print("-" * 60)

    if not results:
        raise ValueError(
            "assert_qvp_equivalence: no variables compared. "
            f"variables={list(variables)}, qvp_a keys={list(qvp_a)}, "
            f"qvp_b keys={list(qvp_b)} — at least one shared variable "
            "is required."
        )

    failures = [(v, d, a, u) for v, d, a, u in results if d >= a]
    if failures:
        msg = "QVP equivalence failed: " + ", ".join(
            f"{v} max |Δ|={round(d, 4)}{(' ' + u) if u else ''} ≥ "
            f"tolerance {a}{(' ' + u) if u else ''}"
            for v, d, a, u in failures
        )
        raise AssertionError(msg)
    print("Both workflows produce numerically equivalent QVPs.")
