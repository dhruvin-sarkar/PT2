"""Figures for Chapter 11, Practice Set B (names start with pb-).

Run:  python content/ch11/figs/make_figs_pb.py   (from the repo root)
"""
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#1f2937"
ACC = "#ef4444"
plt.rcParams.update({"font.size": 12, "svg.fonttype": "none", "font.family": "DejaVu Sans"})


def q16_image():
    """Schematic for Q16: P(2,-1,5), foot L(1,2,3) on the line, image P'(0,5,1); L is the mid-point of PP'."""
    fig, ax = plt.subplots(figsize=(4.8, 3.4))
    ax.plot([-3.2, 3.2], [-1.2, 1.2], color=INK, lw=2)
    ax.text(3.3, 0.75, "given line\nDRs 10, −4, −11", fontsize=10, color=INK, ha="right", va="top")
    n = (-1.2, 3.2)
    m = math.hypot(*n)
    ux, uy = n[0] / m, n[1] / m
    d = 2.0
    P = (ux * d, uy * d)
    Q = (-ux * d, -uy * d)
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=ACC, lw=1.6, ls="--")
    for (x, y), lab, off in [(P, "P(2, −1, 5)", (0.15, 0.05)), ((0, 0), "L(1, 2, 3)  foot", (0.2, -0.4)),
                             (Q, "P′(0, 5, 1)  image", (0.15, -0.2))]:
        ax.plot(x, y, "o", color=INK, ms=5)
        ax.text(x + off[0], y + off[1], lab, color=INK, fontsize=11)
    tx, ty = 3.2 / math.hypot(3.2, 1.2), 1.2 / math.hypot(3.2, 1.2)
    s = 0.28
    ax.plot([tx * s, tx * s + ux * s, ux * s], [ty * s, ty * s + uy * s, uy * s], color=INK, lw=1)
    ax.text(-3.3, -2.15, "PL = LP′  and  PP′ ⊥ line", fontsize=10, color=INK)
    ax.set_aspect("equal")
    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-2.3, 2.3)
    ax.axis("off")
    fig.savefig(os.path.join(HERE, "pb-q16-image.svg"), transparent=True, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    q16_image()
    print("done")
