"""Figures for Chapter 2 (Inverse Trigonometric Functions), Practice Set A.

Run from anywhere:  python content/ch02/figs/make_figs_pa.py
Writes pa-q04-graph.svg, pa-q15-graph.svg and pa-q20-drone.svg next to this script.
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


def q20_drone():
    """Drone D at height 60 m above P; observer O at horizontal distance x m; angle of elevation theta."""
    fig, ax = plt.subplots(figsize=(4.8, 3.0), dpi=96)
    ox, px, top = 0.0, 4.0, 2.4
    ax.fill([ox, px, px], [0, 0, top], color=FILL, alpha=0.45, lw=0)
    ax.plot([ox - 0.2, px + 0.5], [0, 0], color=INK, lw=2)
    ax.plot([px, px], [0, top], color=INK, lw=1.2, ls="--")
    ax.plot([ox, px], [0, top], color=INK, lw=1.4)
    s = 0.18
    ax.plot([px - s, px - s, px], [0, s, s], color=INK, lw=1)
    th = np.arctan2(top, px)
    a = np.linspace(0, th, 40)
    ax.plot(0.75 * np.cos(a), 0.75 * np.sin(a), color=ACCENT, lw=1.6)
    ax.text(0.85, 0.13, r"$\theta$", fontsize=13, color=ACCENT)
    # drone: body + two rotors
    ax.plot([px - 0.3, px + 0.3], [top, top], color=INK, lw=3)
    for dx in (-0.3, 0.3):
        ax.plot([px + dx - 0.15, px + dx + 0.15], [top + 0.12, top + 0.12], color=INK, lw=1.5)
        ax.plot([px + dx, px + dx], [top, top + 0.12], color=INK, lw=1)
    ax.text(px + 0.4, top - 0.05, "Drone (D)", fontsize=11)
    ax.text(ox - 0.15, -0.35, "Observer (O)", fontsize=11, ha="left")
    ax.text(px, -0.35, "P", fontsize=11, ha="center")
    ax.text(px + 0.12, top / 2, "60 m", fontsize=12)
    ax.text((ox + px) / 2, -0.35, "$x$ m", fontsize=12, ha="center")
    ax.set_xlim(-0.4, 5.4)
    ax.set_ylim(-0.6, 2.85)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "pa-q20-drone.svg")


if __name__ == "__main__":
    q04_graph()
    q15_graph()
    q20_drone()
    print("figures written to", HERE)
