"""Figures for Chapter 11, Practice Set A (names start with pa-).

Run:  python content/ch11/figs/make_figs_pa.py   (from the repo root)
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#1f2937"
ACC = "#ef4444"
plt.rcParams.update({"font.size": 12, "svg.fonttype": "none", "font.family": "DejaVu Sans"})


def q16_image():
    """Schematic: point P, foot L on the line, image Q (L is the midpoint of PQ)."""
    fig, ax = plt.subplots(figsize=(4.8, 3.4))
    # the given line, drawn as a slanted segment
    ax.plot([-3.2, 3.2], [-1.2, 1.2], color=INK, lw=2)
    ax.text(3.25, 1.25, "given line\n$(x-3)/1=(y+1)/2=(z-1)/3$", fontsize=10, color=INK, ha="right", va="bottom")
    # foot L at origin, perpendicular direction is (-1.2, 3.2) normalised
    import math
    n = (-1.2, 3.2)
    m = math.hypot(*n)
    ux, uy = n[0] / m, n[1] / m
    d = 2.0
    P = (ux * d, uy * d)
    Q = (-ux * d, -uy * d)
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=ACC, lw=1.6, ls="--")
    for (x, y), lab, off in [(P, "$P(1,2,1)$", (0.15, 0.05)), ((0, 0), "$L$ (foot)", (0.2, -0.35)),
                             (Q, "$Q$ (image)", (0.15, -0.2))]:
        ax.plot(x, y, "o", color=INK, ms=5)
        ax.text(x + off[0], y + off[1], lab, color=INK, fontsize=11)
    # right-angle mark at L
    tx, ty = 3.2 / math.hypot(3.2, 1.2), 1.2 / math.hypot(3.2, 1.2)
    s = 0.28
    ax.plot([tx * s, tx * s + ux * s, ux * s], [ty * s, ty * s + uy * s, uy * s], color=INK, lw=1)
    ax.text(-2.9, 1.7, "$PL = LQ$ and $PQ \\perp$ line", fontsize=10, color=INK)
    ax.set_aspect("equal")
    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-2.3, 2.3)
    ax.axis("off")
    fig.savefig(os.path.join(HERE, "pa-q16-image.svg"), transparent=True, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    q16_image()
    print("done")
