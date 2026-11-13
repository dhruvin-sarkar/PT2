"""Figures for Chapter 2 (Inverse Trigonometric Functions), Practice Set B.

Run from anywhere:  python content/ch02/figs/make_figs_pb.py
Writes pb-q15-graph.svg and pb-q20-tower.svg next to this script.
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
GREY = "#6b7280"

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


def bare_axes(ax):
    for s in ["top", "right", "left", "bottom"]:
        ax.spines[s].set_visible(False)
    ax.axhline(0, color=INK, lw=0.9)
    ax.axvline(0, color=INK, lw=0.9)


def q15_graph():
    """y = sin^-1 x and y = cos^-1 x on one axes; they meet at (1/sqrt2, pi/4)."""
    fig, ax = plt.subplots(figsize=(4.8, 4.8), dpi=96)
    xs = np.linspace(-1, 1, 400)
    a = 1 / np.sqrt(2)
    # region where sin^-1 x > cos^-1 x (x in (1/sqrt2, 1])
    xr = np.linspace(a, 1, 100)
    ax.fill_between(xr, np.arccos(xr), np.arcsin(xr), color=FILL, alpha=0.45, lw=0)
    ax.plot(xs, np.arcsin(xs), color=INK, lw=2.2)
    ax.plot(xs, np.arccos(xs), color=ACCENT, lw=2.2)
    bare_axes(ax)
    pts = [(-1, -np.pi / 2), (0, 0), (1, np.pi / 2), (-1, np.pi), (0, np.pi / 2), (1, 0)]
    for px, py in pts:
        ax.plot(px, py, "o", color=GREY, ms=4, zorder=5)
    ax.plot(a, np.pi / 4, "o", color=ACCENT, ms=7, zorder=6)
    ax.annotate(r"$P\left(\frac{1}{\sqrt{2}},\,\frac{\pi}{4}\right)$", (a, np.pi / 4),
                textcoords="offset points", xytext=(-95, 6), fontsize=12)
    ax.plot([a, a], [0, np.pi / 4], ls="--", lw=0.9, color=GREY)
    ax.plot([-1, -1], [-np.pi / 2, np.pi], ls=":", lw=0.8, color=GREY)
    ax.plot([1, 1], [-np.pi / 2, np.pi], ls=":", lw=0.8, color=GREY)
    ax.text(-0.72, 2.95, r"$y=\cos^{-1}x$", fontsize=12, color=ACCENT)
    ax.text(0.15, -1.1, r"$y=\sin^{-1}x$", fontsize=12, color=INK)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.9, 3.5)
    ax.set_xticks([-1, a, 1])
    ax.set_xticklabels(["$-1$", r"$\frac{1}{\sqrt{2}}$", "$1$"])
    ax.set_yticks([-np.pi / 2, np.pi / 4, np.pi / 2, np.pi])
    ax.set_yticklabels([r"$-\frac{\pi}{2}$", r"$\frac{\pi}{4}$", r"$\frac{\pi}{2}$", r"$\pi$"])
    ax.text(1.27, -0.25, "$x$", fontsize=12, ha="right")
    ax.text(0.05, 3.35, "$y$", fontsize=12)
    save(fig, "pb-q15-graph.svg")


def q20_tower():
    """Tower PQ = 30 m; A at 30 sqrt3 m on the left of Q, B at 10 sqrt3 m on the right (to scale)."""
    fig, ax = plt.subplots(figsize=(5.6, 3.4), dpi=96)
    h = 30.0
    qa, qb = 30 * np.sqrt(3), 10 * np.sqrt(3)
    A, B, P = (-qa, 0.0), (qb, 0.0), (0.0, h)
    ax.fill([A[0], B[0], P[0]], [0, 0, P[1]], color=FILL, alpha=0.45, lw=0)
    ax.plot([A[0] - 4, B[0] + 4], [0, 0], color=INK, lw=2)                 # ground
    ax.plot([0, 0], [0, h], color=INK, lw=2.5)                             # tower
    ax.plot([A[0], P[0]], [0, h], color=ACCENT, lw=1.6)
    ax.plot([B[0], P[0]], [0, h], color=ACCENT, lw=1.6)
    s = 2.0
    ax.plot([s, s, 0], [0, s, s], color=INK, lw=1)                         # right angle at Q
    ra = np.linspace(0, np.pi / 6, 30)
    ax.plot(A[0] + 9 * np.cos(ra), 9 * np.sin(ra), color=INK, lw=1.2)
    ax.text(A[0] + 10, 1.2, r"$\alpha$", fontsize=13)
    rb = np.linspace(np.pi - np.pi / 3, np.pi, 30)
    ax.plot(B[0] + 5 * np.cos(rb), 5 * np.sin(rb), color=INK, lw=1.2)
    ax.text(B[0] - 7.6, 1.2, r"$\beta$", fontsize=13)
    ax.text(A[0], -3.6, "A", fontsize=12, ha="center")
    ax.text(0, -3.6, "Q", fontsize=12, ha="center")
    ax.text(B[0], -3.6, "B", fontsize=12, ha="center")
    ax.text(0, h + 1.2, "P", fontsize=12, ha="center")
    ax.text(-1.2, h / 2, "30 m", ha="right", fontsize=11, va="center")
    ax.text(-qa / 2, -3.6, r"$30\sqrt{3}$ m", fontsize=11, ha="center")
    ax.text(qb / 2, -3.6, r"$10\sqrt{3}$ m", fontsize=11, ha="center")
    ax.set_xlim(A[0] - 5, B[0] + 5)
    ax.set_ylim(-5.5, h + 4)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "pb-q20-tower.svg")


if __name__ == "__main__":
    q15_graph()
    q20_tower()
    print("figures written to", HERE)
