"""Figures for Chapter 7 (Integrals), Practice Set A.
Run from anywhere: python content/ch07/figs/make_figs_pa.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#1f2937"
FILL = "#93c5fd"
ACC = "#ef4444"
plt.rcParams.update({
    "svg.fonttype": "none",
    "font.size": 12,
    "font.family": "DejaVu Sans",
    "mathtext.fontset": "dejavuserif",
    "text.color": INK,
    "axes.edgecolor": INK,
})


def save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", transparent=True, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


# Q13: y = |x + 1| on [-4, 2]; two shaded triangles of area 9/2 each
def q13():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    fig.patch.set_alpha(0)
    ax.set_aspect("equal")
    ax.axis("off")
    # axes
    ax.annotate("", xy=(3.0, 0), xytext=(-5.0, 0), arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
    ax.annotate("", xy=(0, 4.2), xytext=(0, -0.6), arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
    ax.text(3.05, -0.05, "$x$", ha="left", va="center")
    ax.text(0.08, 4.2, "$y$", ha="left", va="center")
    ax.text(-0.1, -0.12, "O", ha="right", va="top")
    # shaded regions
    ax.add_patch(Polygon([(-4, 0), (-1, 0), (-4, 3)], closed=True, fc=FILL, alpha=0.45, ec="none"))
    ax.add_patch(Polygon([(-1, 0), (2, 0), (2, 3)], closed=True, fc=FILL, alpha=0.45, ec="none"))
    # curve
    xs = np.linspace(-4.6, 2.6, 400)
    ax.plot(xs, np.abs(xs + 1), color=INK, lw=2.2)
    # ordinates
    ax.plot([-4, -4], [0, 3], color=ACC, lw=1.4, ls="--")
    ax.plot([2, 2], [0, 3], color=ACC, lw=1.4, ls="--")
    # labels
    ax.text(-4, -0.15, "$-4$", ha="center", va="top")
    ax.text(-1, -0.15, "$-1$", ha="center", va="top")
    ax.text(2, -0.15, "$2$", ha="center", va="top")
    ax.text(-4.1, 3.0, "$(-4,\\ 3)$", ha="right", va="center")
    ax.text(2.1, 3.0, "$(2,\\ 3)$", ha="left", va="center")
    ax.text(-3.0, 0.75, "$\\frac{9}{2}$", ha="center", va="center", fontsize=14)
    ax.text(1.0, 0.75, "$\\frac{9}{2}$", ha="center", va="center", fontsize=14)
    ax.text(-2.4, 2.6, "$y=-(x+1)$", ha="center", va="bottom", rotation=-45)
    ax.text(2.15, 1.5, "$y=x+1$", ha="left", va="center")
    ax.set_xlim(-5.6, 3.4)
    ax.set_ylim(-0.8, 4.4)
    save(fig, "pa-q13-modgraph.svg")


if __name__ == "__main__":
    q13()
    print("done")
