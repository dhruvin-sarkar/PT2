"""Figures for Chapter 5 school worksheet. Run: python content/ch05/figs/make_figs.py"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
INK, RED = "#1f2937", "#ef4444"
plt.rcParams.update({"font.size": 11, "svg.fonttype": "none", "text.color": INK,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})


def q18():
    """Graph of f(x) = |x-1| + |x-2| with corners at x = 1 and x = 2."""
    fig, ax = plt.subplots(figsize=(4.8, 3.4), dpi=96)
    x = np.linspace(-0.6, 3.6, 400)
    ax.plot(x, np.abs(x - 1) + np.abs(x - 2), color=INK, lw=2)
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    ax.plot([1, 2], [1, 1], "o", color=RED, ms=7, zorder=5)
    ax.annotate("corner (1, 1)", (1, 1), (0.1, 0.3), color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.annotate("corner (2, 1)", (2, 1), (2.15, 0.3), color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.text(0.15, 3.9, "y = 3 - 2x", color=INK)
    ax.text(2.7, 1.6, "y = 2x - 3", color=INK)
    ax.text(1.3, 1.15, "y = 1", color=INK)
    ax.set_xlim(-0.6, 3.6)
    ax.set_ylim(-0.3, 4.4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("f(x) = |x - 1| + |x - 2|", color=INK)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "q18-graph.svg"), transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    q18()
    print("figures written")
