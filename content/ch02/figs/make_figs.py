"""Figures for Chapter 2 (Inverse Trigonometric Functions), school worksheet.

Run from anywhere:  python content/ch02/figs/make_figs.py
Writes q15-graph.svg and q20-triangle.svg next to this script.
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#1f2937"
FILL = "#93c5fd"
ACCENT = "#ef4444"

plt.rcParams.update({
    "font.size": 11,
    "svg.fonttype": "path",
    "text.color": INK,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "mathtext.fontset": "dejavusans",
})


def save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", transparent=True, bbox_inches="tight")
    plt.close(fig)


def q15_graph():
    """y = cos^-1 x on its principal branch: domain [-1, 1], range [0, pi]."""
    fig, ax = plt.subplots(figsize=(4.8, 4.2), dpi=96)
    xs = np.linspace(-1, 1, 400)
    ax.plot(xs, np.arccos(xs), color=INK, lw=2.2, label=r"$y=\cos^{-1}x$")
    # axes through origin
    ax.axhline(0, color=INK, lw=0.9)
    ax.axvline(0, color=INK, lw=0.9)
    # guide lines
    ax.plot([-1, -1], [0, np.pi], ls="--", lw=0.9, color="#6b7280")
    ax.plot([-1, 0], [np.pi, np.pi], ls="--", lw=0.9, color="#6b7280")
    ax.plot([-1, 1], [np.pi, np.pi], ls=":", lw=0.8, color="#9ca3af")
    # key points
    pts = [(-1, np.pi, r"$(-1,\ \pi)$", (8, 6)),
           (0, np.pi / 2, r"$(0,\ \frac{\pi}{2})$", (8, 2)),
           (1, 0, r"$(1,\ 0)$", (-44, 8))]
    for px, py, lab, off in pts:
        ax.plot(px, py, "o", color=ACCENT, ms=6, zorder=5)
        ax.annotate(lab, (px, py), textcoords="offset points", xytext=off, fontsize=12, color=INK)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.4, 3.6)
    ax.set_xticks([-1, 1])
    ax.set_xticklabels(["$-1$", "$1$"])
    ax.set_yticks([np.pi / 2, np.pi])
    ax.set_yticklabels([r"$\frac{\pi}{2}$", r"$\pi$"])
    for s in ["top", "right", "left", "bottom"]:
        ax.spines[s].set_visible(False)
    ax.text(1.45, -0.28, "$x$", fontsize=12, ha="right")
    ax.text(0.06, 3.45, "$y$", fontsize=12)
    ax.text(0.3, 2.3, r"$y=\cos^{-1}x$", fontsize=12, color=INK)
    ax.text(0.45, 3.35, r"range $[0,\pi]$", fontsize=11, color="#374151")
    ax.text(-0.95, 0.12, r"domain $[-1,1]$", fontsize=11, color="#374151")
    save(fig, "q15-graph.svg")


def q20_triangle():
    """Lighthouse of height 20 m, boat at distance x m, angle of elevation theta."""
    fig, ax = plt.subplots(figsize=(4.8, 3.0), dpi=96)
    bx, by = 0.0, 0.0      # boat
    fx, fy = 4.0, 0.0      # foot of lighthouse
    tx, ty = 4.0, 2.3      # top of lighthouse
    ax.fill([bx, fx, tx], [by, fy, ty], color=FILL, alpha=0.45, lw=0)
    ax.plot([bx, fx], [by, fy], color=INK, lw=2)
    ax.plot([fx, tx], [fy, ty], color=INK, lw=3)
    ax.plot([bx, tx], [by, ty], color=INK, lw=1.4, ls="--")
    # right-angle mark
    s = 0.18
    ax.plot([fx - s, fx - s, fx], [0, s, s], color=INK, lw=1)
    # angle arc at boat
    th = np.arctan2(ty, tx)
    a = np.linspace(0, th, 40)
    ax.plot(0.7 * np.cos(a), 0.7 * np.sin(a), color=ACCENT, lw=1.6)
    ax.text(0.8, 0.12, r"$\theta$", fontsize=13, color=ACCENT)
    ax.text(bx - 0.1, by - 0.32, "Boat (B)", fontsize=11, ha="left")
    ax.text(fx, fy - 0.32, "Foot (F)", fontsize=11, ha="center")
    ax.text(tx + 0.08, ty - 0.05, "Top (T)", fontsize=11)
    ax.text(fx + 0.1, ty / 2, "20 m", fontsize=12)
    ax.text((bx + fx) / 2, -0.32, "$x$ m", fontsize=12, ha="center")
    ax.text(2.0, 0.45, r"$\tan\theta=\dfrac{20}{x}$", fontsize=12)
    ax.set_xlim(-0.4, 5.0)
    ax.set_ylim(-0.55, 2.6)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "q20-triangle.svg")


if __name__ == "__main__":
    q15_graph()
    q20_triangle()
    print("figures written to", HERE)
