"""Render the 1200x630 social-share card used in Open Graph / Twitter meta.

Re-run when copy or brand changes:
    uv run python scripts/generate_social_card.py
"""

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DOCS = REPO_ROOT / "docs" / "_static" / "social-card.png"
OUT_ROOT = REPO_ROOT / "social-card.png"

NAVY = "#0F2F4D"
TEAL = "#13B5EA"
SOFT_WHITE = "#F4F8FB"
SUBTLE = "#8FA8B8"


def _pick_font(candidates: list[str]) -> str:
    """Return the first installed font from candidates.

    The last entry must be a font matplotlib always ships (DejaVu Sans), so
    the lookup is total.
    """
    available = {f.name for f in fm.fontManager.ttflist}
    return next(c for c in candidates if c in available)


def render(out_paths: list[Path]) -> None:
    display = _pick_font(["Quicksand", "Inter Tight", "DejaVu Sans"])
    body = _pick_font(["Inter Tight", "Inter", "DejaVu Sans"])

    fig = plt.figure(figsize=(12, 6.3), dpi=100)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.3)
    ax.set_axis_off()

    ax.add_patch(Rectangle((0, 0), 12, 6.3, facecolor=NAVY, zorder=0))
    ax.add_patch(Rectangle((0, 0), 12, 0.18, facecolor=TEAL, zorder=1))

    ax.add_patch(
        FancyBboxPatch(
            (0.7, 5.15),
            2.6,
            0.7,
            boxstyle="round,pad=0.04,rounding_size=0.18",
            linewidth=1.4,
            edgecolor=TEAL,
            facecolor="none",
            zorder=2,
        )
    )
    ax.text(
        2.0,
        5.51,
        "ATMOSCALE",
        ha="center",
        va="center",
        fontname=display,
        fontsize=22,
        fontweight="bold",
        color=TEAL,
        zorder=3,
    )

    ax.text(
        0.7,
        4.05,
        "Radar DataTree",
        ha="left",
        va="bottom",
        fontname=display,
        fontsize=72,
        fontweight="bold",
        color=SOFT_WHITE,
        zorder=3,
    )

    ax.text(
        0.7,
        3.45,
        "Stream petabyte-scale NEXRAD archives from the cloud.",
        ha="left",
        va="top",
        fontname=body,
        fontsize=26,
        color=SOFT_WHITE,
        zorder=3,
    )

    metrics = [
        ("60×", "faster"),
        ("22×", "less RAM"),
        ("5 lines", "of code"),
    ]
    base_x = 0.7
    spacing = 3.7
    metric_y = 1.55
    for i, (number, label) in enumerate(metrics):
        x = base_x + i * spacing
        ax.text(
            x,
            metric_y + 0.35,
            number,
            ha="left",
            va="center",
            fontname=display,
            fontsize=58,
            fontweight="bold",
            color=TEAL,
            zorder=3,
        )
        ax.text(
            x,
            metric_y - 0.45,
            label,
            ha="left",
            va="center",
            fontname=body,
            fontsize=22,
            color=SUBTLE,
            zorder=3,
        )

    ax.text(
        0.7,
        0.55,
        "atmoscale.ai  ·  github.com/AtmoScale/radar-datatree",
        ha="left",
        va="center",
        fontname=body,
        fontsize=18,
        color=SUBTLE,
        zorder=3,
    )

    for path in out_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=100, facecolor=NAVY)
        print(f"wrote {path.relative_to(REPO_ROOT)}")

    plt.close(fig)


if __name__ == "__main__":
    render([OUT_DOCS, OUT_ROOT])
