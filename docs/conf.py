# Sphinx configuration for Radar DataTree documentation
import os
import sys

# Add notebooks directory to path
sys.path.insert(0, os.path.abspath("../notebooks"))

project = "Radar DataTree"
author = "Alfonso Ladino-Rincón"
copyright = "2026, AtmoScale"

extensions = [
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "sphinx_copybutton",
]

# MyST-NB settings
nb_execution_mode = (
    "cache"  # Execute and cache results; re-execute only when code changes
)
# Per-cell timeout (seconds). The file-based 1-day download cell in
# notebook 2 takes ~7–8 minutes on a CI runner.
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
}

# Static assets (logos, favicon, custom CSS)
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_favicon = "_static/favicon.png"

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
    # comes back in its own PR as the rewrite lands. (3.QPE-Snow-Storm
    # was retired here — the December 2025 IL snow-storm dataset is not
    # currently available; the QPE story now lives in
    # 3.QPE-Scaling-Benchmark.ipynb, the paper companion.)
    "4.Basin-Precipitation-Monitoring.ipynb",
    "5.Rainfall-QPE-Marshall-Palmer.ipynb",
]

# Suppress warnings for notebooks with no outputs
suppress_warnings = ["myst.header"]
