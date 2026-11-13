"""Figures for Chapter 5 Practice Set B. Run: python content/ch05/figs/make_figs_pb.py"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
INK, RED = "#1f2937", "#ef4444"
plt.rcParams.update({"font.size": 11, "svg.fonttype": "none", "text.color": INK,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})


def tidy(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def q18():
    """f(x) = x[x] on [0, 2), (x - 1)x on [2, 3): jump at x = 1, corner at x = 2."""
    fig, ax = plt.subplots(figsize=(4.8, 3.4), dpi=96)
    x0 = np.linspace(0, 1, 50, endpoint=False)
    x1 = np.linspace(1, 2, 100)
    x2 = np.linspace(2, 2.999, 100)
    ax.plot(x0, 0 * x0, color=INK, lw=2)
    ax.plot(x1, x1, color=INK, lw=2)
    ax.plot(x2, (x2 - 1) * x2, color=INK, lw=2)
    ax.plot([1], [0], "o", mfc="white", mec=INK, ms=6, zorder=5)
    ax.plot([1], [1], "o", color=INK, ms=6, zorder=5)
    ax.plot([2], [2], "o", color=RED, ms=6, zorder=5)
    ax.plot([3], [6], "o", mfc="white", mec=INK, ms=6, zorder=5)
    ax.annotate("jump at x = 1", (1, 0.5), (0.05, 2.2), color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.annotate("corner at (2, 2):\nslope 1 | slope 3", (2, 2), (2.05, 0.4), color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.text(1.0, 1.9, "y = x", color=INK)
    ax.text(1.2, 4.6, "y = (x - 1)x", color=INK)
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_xlim(-0.2, 3.2)
    ax.set_ylim(-0.4, 6.4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    tidy(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "pb-q18.svg"), transparent=True)
    plt.close(fig)


def q20():
    """Slide profile: -x^2 + 3x on [0, 1] meets 2 + log x on (1, e] at (1, 2) with slope 1."""
    fig, ax = plt.subplots(figsize=(4.8, 3.4), dpi=96)
    xl = np.linspace(0, 1, 200)
    xr = np.linspace(1, np.e, 200)
    ax.plot(xl, -xl ** 2 + 3 * xl, color=INK, lw=2)
    ax.plot(xr, 2 + np.log(xr), color=INK, lw=2)
    xt = np.linspace(0.45, 1.6, 50)
    ax.plot(xt, 2 + (xt - 1), color=RED, lw=1.4, ls="--")
    ax.plot([1], [2], "o", color=RED, ms=6, zorder=5)
    ax.annotate("(1, 2): slope 1 on both sides", (1, 2), (0.9, 0.7), color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.text(0.05, 2.3, "y = -x² + 3x", color=INK)
    ax.text(1.75, 2.95, "y = 2 + log x", color=INK)
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_xlim(-0.1, 2.9)
    ax.set_ylim(-0.2, 3.4)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("height (m)")
    tidy(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "pb-q20.svg"), transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    q18()
    q20()
    print("figures written")
