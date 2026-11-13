"""Figures for Chapter 2 (Inverse Trigonometric Functions), Practice Set A.

Run from anywhere:  python content/ch02/figs/make_figs_pa.py
Writes pa-q04-graph.svg, pa-q15-graph.svg and pa-q20-ladder.svg next to this script.
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


def q04_graph():
    """SQP 2024-25 Q15: an unlabelled curve, which is y = cos^-1 x (domain [-1, 1], range [0, pi])."""
    fig, ax = plt.subplots(figsize=(4.8, 4.0), dpi=96)
    xs = np.linspace(-1, 1, 400)
    for yv in [np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi]:
        ax.plot([-1.3, 1.3], [yv, yv], color="#e5e7eb", lw=0.8, zorder=0)
    for xv in [-1, -0.5, 0.5, 1]:
        ax.plot([xv, xv], [-0.1, 3.4], color="#e5e7eb", lw=0.8, zorder=0)
    ax.plot(xs, np.arccos(xs), color=ACCENT, lw=2.2)
    bare_axes(ax)
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-0.35, 3.5)
    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels(["$-1$", "$0$", "$1$"])
    ax.set_yticks([np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])
    ax.set_yticklabels([r"$\frac{\pi}{4}$", r"$\frac{\pi}{2}$", r"$\frac{3\pi}{4}$", r"$\pi$"])
    ax.text(1.3, -0.28, "$x$", fontsize=12, ha="right")
    ax.text(0.06, 3.35, "$y$", fontsize=12)
    save(fig, "pa-q04-graph.svg")


def q15_graph():
    """CBSE 2023: y = sin^-1 x for x in [-1/sqrt2, 1/sqrt2]; range [-pi/4, pi/4]."""
    fig, ax = plt.subplots(figsize=(4.8, 4.4), dpi=96)
    a = 1 / np.sqrt(2)
    full = np.linspace(-1, 1, 400)
    part = np.linspace(-a, a, 300)
    ax.plot(full, np.arcsin(full), color=GREY, lw=1.0, ls=":", label="rest of the principal branch")
    ax.plot(part, np.arcsin(part), color=INK, lw=2.4)
    bare_axes(ax)
    for px, py, lab, off in [(-a, -np.pi / 4, r"$\left(-\frac{1}{\sqrt{2}},\,-\frac{\pi}{4}\right)$", (-30, -26)),
                             (0, 0, r"$O(0,0)$", (8, -14)),
                             (a, np.pi / 4, r"$\left(\frac{1}{\sqrt{2}},\,\frac{\pi}{4}\right)$", (-70, 12))]:
        ax.plot(px, py, "o", color=ACCENT, ms=6, zorder=5)
        ax.annotate(lab, (px, py), textcoords="offset points", xytext=off, fontsize=12)
    for px in (-0.5, 0.5):  # table points (+-1/2, +-pi/6)
        ax.plot(px, np.arcsin(px), "o", color=ACCENT, ms=5, zorder=5)
    ax.plot([a, a], [0, np.pi / 4], ls="--", lw=0.9, color=GREY)
    ax.plot([0, a], [np.pi / 4, np.pi / 4], ls="--", lw=0.9, color=GREY)
    ax.plot([-a, -a], [0, -np.pi / 4], ls="--", lw=0.9, color=GREY)
    ax.plot([-a, 0], [-np.pi / 4, -np.pi / 4], ls="--", lw=0.9, color=GREY)
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.85, 1.85)
    ax.set_xticks([-1, -a, a, 1])
    ax.set_xticklabels(["$-1$", r"$-\frac{1}{\sqrt{2}}$", r"$\frac{1}{\sqrt{2}}$", "$1$"])
    ax.set_yticks([-np.pi / 2, -np.pi / 4, np.pi / 4, np.pi / 2])
    ax.set_yticklabels([r"$-\frac{\pi}{2}$", r"$-\frac{\pi}{4}$", r"$\frac{\pi}{4}$", r"$\frac{\pi}{2}$"])
    ax.text(1.22, -0.2, "$x$", fontsize=12, ha="right")
    ax.text(0.05, 1.72, "$y$", fontsize=12)
    ax.text(0.2, -0.75, r"$y=\sin^{-1}x$", fontsize=12)
    ax.text(-1.2, 1.45, "dotted: rest of the\nprincipal branch", fontsize=11, color=GREY)
    save(fig, "pa-q15-graph.svg")


def q20_ladder():
    """Ladder FT of length 10 m against a vertical wall; foot F is x m from the wall foot W; theta at F.

    Drawn to scale for x = 5 (theta = pi/3); labels stay general.
    """
    fig, ax = plt.subplots(figsize=(4.8, 4.2), dpi=96)
    L = 10.0
    th = np.pi / 3
    fx, wx = 0.0, L * np.cos(th)          # foot of ladder, foot of wall
    top = L * np.sin(th)
    ax.fill([fx, wx, wx], [0, 0, top], color=FILL, alpha=0.45, lw=0)
    ax.plot([fx - 1.2, wx + 0.2], [0, 0], color=INK, lw=2)                 # ground
    ax.fill([wx, wx + 0.6, wx + 0.6, wx], [0, 0, top + 1.0, top + 1.0], color="#e5e7eb", lw=0)
    ax.plot([wx, wx], [0, top + 1.0], color=INK, lw=2)                     # wall face
    ax.plot([fx, wx], [0, top], color=ACCENT, lw=3)                        # ladder
    s = 0.45
    ax.plot([wx - s, wx - s, wx], [0, s, s], color=INK, lw=1)              # right angle at W
    a = np.linspace(0, th, 40)
    ax.plot(1.3 * np.cos(a), 1.3 * np.sin(a), color=INK, lw=1.4)
    ax.text(1.45, 0.35, r"$\theta$", fontsize=13)
    ax.text(1.0, top / 2 + 0.5, "ladder 10 m", fontsize=12, rotation=np.degrees(th) - 2,
            ha="center", va="center", color=ACCENT)
    ax.text(wx + 0.75, top / 2, "Wall", fontsize=11, rotation=90, va="center")
    ax.text((fx + wx) / 2, -0.75, "$x$ m", fontsize=12, ha="center")
    ax.text(fx, -0.75, "F", fontsize=11, ha="center")
    ax.text(wx, -0.75, "W", fontsize=11, ha="center")
    ax.text(wx - 0.25, top, "T", fontsize=11, ha="right", va="bottom")
    ax.text(-1.2, 0.2, "Ground", fontsize=11)
    ax.set_xlim(-1.4, wx + 1.6)
    ax.set_ylim(-1.2, top + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "pa-q20-ladder.svg")


if __name__ == "__main__":
    q04_graph()
    q15_graph()
    q20_ladder()
    print("figures written to", HERE)
