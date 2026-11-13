"""Figures for Practice Set A, Chapter 1 (run: python make_figs_pa.py)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle

INK = "#1f2937"
ACCENT = "#ef4444"
HERE = os.path.dirname(os.path.abspath(__file__))
plt.rcParams.update({"font.size": 12, "svg.fonttype": "none", "font.family": "DejaVu Sans"})


def q20():
    pos = {"A": (0.0, 0.0), "B": (1.6, 1.1), "C": (1.6, 0.0), "D": (1.6, -1.1), "E": (3.2, 0.0)}
    flows = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("B", "E"),
             ("C", "E"), ("D", "E"), ("D", "C")]
    fig, ax = plt.subplots(figsize=(4.8, 3.0), dpi=96)
    r = 0.22
    for name, (px, py) in pos.items():
        ax.add_patch(Circle((px, py), r, fill=False, lw=1.8, ec=INK))
        ax.text(px, py, name, ha="center", va="center", fontsize=14, fontweight="bold", color=INK)
    for s, t in flows:
        (x1, y1), (x2, y2) = pos[s], pos[t]
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14,
                                     lw=1.4, color=INK, shrinkA=r * 72 + 2, shrinkB=r * 72 + 4))
    ax.text(1.6, -1.62, "arrow $X \\rightarrow Y$: one-way traffic from $X$ to $Y$",
            ha="center", va="center", fontsize=11, color=INK)
    ax.set_xlim(-0.4, 3.6)
    ax.set_ylim(-1.85, 1.45)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(os.path.join(HERE, "pa-q20.svg"), transparent=True, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    q20()
    print("written pa-q20.svg")
