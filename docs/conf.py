# Sphinx configuration for Radar DataTree documentation

# NOTE: no sys.path manipulation here. `../notebooks` used to be prepended so
# the build could import notebooks/demo_functions.py; that module is gone and
# every notebook is self-contained, so nothing needs to be importable.

project = "Radar DataTree"
author = "Alfonso Ladino-Rincón"
copyright = "2026, AtmoScale"

extensions = [
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx_sitemap",
]

# Canonical site URL — required by sphinx-sitemap and used for OG/Twitter URLs.
html_baseurl = "https://atmoscale.github.io/radar-datatree/"
sitemap_url_scheme = "{link}"

# MyST-NB settings
nb_execution_mode = (
    "cache"  # Execute and cache results; re-execute only when code changes
)
# Per-cell timeout (seconds). The file-based 1-day download cell in
# notebook 3 (the file-based QVP download loop) takes ~7–8 minutes on a CI runner.
nb_execution_timeout = 600
# Fail the build if any notebook cell raises during execution. Without
# this, myst-nb degrades a CellExecutionError into a non-blocking
# warning — and a broken notebook still deploys, with the traceback
# rendered on the live page (PR #19's notebook 2 import failure shipped
# this way).
nb_execution_raise_on_error = True
# Auto-register cross-ref targets for headings up to H2 so links like
# [Foo](other.md#some-heading) validate without manual (foo)= markers.
myst_heading_anchors = 2
myst_enable_extensions = [
    "attrs_block",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# Theme
html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": "https://github.com/AtmoScale/radar-datatree",
    "repository_branch": "main",
    # The .ipynb pages under docs/ are symlinks to the real notebooks/ files;
    # GitHub serves committed symlinks as their target-path text blob, not the
    # resolved content, so the launch URL must point at notebooks/ to give
    # Colab a real .ipynb to fetch.
    "path_to_docs": "notebooks",
    "launch_buttons": {
        "colab_url": "https://colab.research.google.com",
        "notebook_interface": "jupyterlab",
    },
    "use_repository_button": True,
    "use_download_button": True,
    "show_toc_level": 2,
    "logo": {
        "image_light": "_static/logo.png",
        "image_dark": "_static/logo-dark.png",
        "alt_text": "radar-datatree",
    },
    "pygments_light_style": "tango",
    "pygments_dark_style": "monokai",
    "extra_footer": (
        'An open-source project by <a href="https://atmoscale.ai">AtmoScale</a>. '
        "Apache 2.0 licensed."
    ),
}

# Static assets (logos, favicon, custom CSS)
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_favicon = "_static/favicon.png"

# Custom templates inject OG/Twitter meta + JSON-LD into <head>.
templates_path = ["_templates"]

# Values consumed by _templates/layout.html. Edit copy here, not in the template.
# Keys are prefixed `og_` to avoid colliding with theme-provided context vars
# (e.g. sphinx_book_theme already defines `github_url`, which would silently
# shadow ours and render as the bare repo host).
html_context = {
    "og_site_name": "AtmoScale",
    "og_title": "Radar DataTree",
    "og_description": (
        "Stream petabyte-scale NEXRAD radar archives from the cloud — the "
        "open-source on-ramp to the AtmoScale platform."
    ),
    "og_image": "https://atmoscale.github.io/radar-datatree/_static/social-card.png",
    "og_url_base": "https://atmoscale.github.io/radar-datatree/",
    "og_atmoscale_url": "https://atmoscale.ai",
    "og_github_url": "https://github.com/AtmoScale/radar-datatree",
    "og_doi_url": "https://doi.org/10.48550/arXiv.2510.24943",
}

# Source settings
source_suffix = {
    ".rst": "restructuredtext",
    ".ipynb": "myst-nb",
    ".md": "myst-nb",
}

# Exclude patterns
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    # Claude Code's per-project agent memory lives at docs/.claude/agent-memory/.
    # Without this guard sphinx renders MEMORY.md into the published site.
    ".claude",
    # Hidden until refactored against rustytree + xarray 2026.4. Each
    # comes back in its own PR as the rewrite lands.
    "4.Basin-Precipitation-Monitoring.ipynb",
    "5.Rainfall-QPE-Marshall-Palmer.ipynb",
    # notebooks/3.QPE-Snow-Storm.ipynb is parked deliberately: it lives in the
    # repo but has no docs/ symlink and is in no toctree, so sphinx never sees
    # it and it does not render in the book. It is self-contained (its helpers
    # are inlined like every other notebook), so it will run if resurrected.
    #
    # Its data IS available (verified 2026-07-20: KLOT VCP-34, 318 scans over
    # 2025-12-13/14) — the earlier "dataset unavailable" note was wrong. The
    # real blocker is scientific: VCP-34 tops out at 4.48°, too low for a QVP
    # (reaching 3 km needs ~38 km range, so each profile point averages a
    # ~76 km swath and the dendritic growth zone smears out). A winter QVP
    # needs a precipitation VCP — e.g. KLOT VCP-215 on 2022-02-02/03,
    # sweep_16 at 16.70°, 563 scans, all four polarimetric variables.
]

# Suppress warnings for notebooks with no outputs
suppress_warnings = ["myst.header"]
