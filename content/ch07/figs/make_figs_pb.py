"""Figures for Chapter 7 (Integrals), Practice Set B.
Run from anywhere: python content/ch07/figs/make_figs_pb.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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


# Q13: y = x^3 - 3x^2 + 2x = x(x-1)(x-2) on [-1, 2]; sign of each piece and the three areas
def q13():
    f = lambda x: x**3 - 3 * x**2 + 2 * x
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    fig.patch.set_alpha(0)
    ax.axis("off")
    # axes
    ax.annotate("", xy=(2.75, 0), xytext=(-1.55, 0), arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
    ax.annotate("", xy=(0, 1.6), xytext=(0, -6.6), arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
    ax.text(2.8, 0, "$x$", ha="left", va="center")
    ax.text(0.06, 1.6, "$y$", ha="left", va="center")
    # shaded pieces
    for lo, hi in [(-1, 0), (0, 1), (1, 2)]:
        xs = np.linspace(lo, hi, 200)
        ax.fill_between(xs, f(xs), 0, color=FILL, alpha=0.45, lw=0)
    # curve
    xs = np.linspace(-1.12, 2.45, 400)
    ax.plot(xs, f(xs), color=INK, lw=2.2)
    ax.plot([-1, -1], [0, f(-1)], color=ACC, lw=1.4, ls="--")
    # labels
    ax.text(-1, 0.18, "$-1$", ha="center", va="bottom")
    ax.text(-0.08, 0.15, "O", ha="right", va="bottom")
    ax.text(1, -0.2, "$1$", ha="center", va="top")
    ax.text(2, 0.18, "$2$", ha="center", va="bottom")
    ax.text(-1.05, -6, "$(-1,\\,-6)$", ha="right", va="center")
    ax.text(-0.76, -1.2, "$-$", ha="center", va="center", fontsize=16, color=ACC)
    ax.text(-0.76, -2.2, "$\\frac{9}{4}$", ha="center", va="center", fontsize=14)
    ax.text(0.5, 0.75, "$+\\ \\ \\frac{1}{4}$", ha="center", va="bottom", fontsize=13, color=INK)
    ax.text(1.5, -0.62, "$-\\ \\ \\frac{1}{4}$", ha="center", va="top", fontsize=13, color=INK)
    ax.text(2.45, f(2.45) + 0.1, "$y=x^3-3x^2+2x$", ha="right", va="bottom")
    ax.set_xlim(-2.1, 3.0)
    ax.set_ylim(-6.8, 1.9)
    save(fig, "pb-q13-cubic.svg")


if __name__ == "__main__":
    q13()
    print("done")
