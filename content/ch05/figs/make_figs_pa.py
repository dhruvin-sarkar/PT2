"""Figures for Chapter 5 Practice Set A. Run: python content/ch05/figs/make_figs_pa.py"""
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
    """f(x) = |x|^3 is smooth at 0; f'(x) = 3x|x| and f''(x) = 6|x| (corner at 0)."""
    fig, ax = plt.subplots(figsize=(4.8, 3.4), dpi=96)
    x = np.linspace(-1.6, 1.6, 400)
    ax.plot(x, np.abs(x) ** 3, color=INK, lw=2, label="f(x) = |x|³")
    ax.plot(x, 6 * np.abs(x), color=RED, lw=1.6, ls="--", label="f''(x) = 6|x|")
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    ax.plot([0], [0], "o", color=RED, ms=6, zorder=5)
    ax.annotate("f''(0) = 0", (0, 0), (0.62, 1.7), color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-0.4, 6.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper center", frameon=False, fontsize=11)
    tidy(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "pa-q18.svg"), transparent=True)
    plt.close(fig)


def q20():
    """Case study: both pieces meet at (1, 2) with the same slope -1."""
    fig, ax = plt.subplots(figsize=(4.8, 3.4), dpi=96)
    xl = np.linspace(-1.5, 1, 200)
    xr = np.linspace(1, 5, 200)
    ax.plot(xl, xl ** 2 / 4 - 3 * xl / 2 + 13 / 4, color=INK, lw=2)
    ax.plot(xr, np.abs(xr - 3), color=INK, lw=2)
    xt = np.linspace(0.2, 1.8, 50)
    ax.plot(xt, 2 - (xt - 1), color=RED, lw=1.4, ls="--")
    ax.plot([1], [2], "o", color=RED, ms=6, zorder=5)
    ax.annotate("(1, 2): slope -1 on both sides", (1, 2), (1.35, 3.6), color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.text(0.15, 5.6, "x²/4 - 3x/2 + 13/4", color=INK)
    ax.text(3.3, 1.35, "|x - 3|", color=INK)
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_xlim(-1.6, 5.1)
    ax.set_ylim(-0.3, 6.2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    tidy(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "pa-q20.svg"), transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    q18()
    q20()
    print("figures written")
