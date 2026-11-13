"""Figures for the renderer fixture (tools/fixture/ch00). Run: python make_figs.py"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#1f2937"
FILL = "#93c5fd"
ACCENT = "#ef4444"

plt.rcParams.update(
    {
        "font.size": 11,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "svg.fonttype": "path",
    }
)


def axes(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.set_aspect("auto")
    ax.text(xlim[1], 0, "  X", va="center", ha="left")
    ax.text(0, ylim[1], "Y", va="bottom", ha="center")


def save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", transparent=True, bbox_inches="tight")
    plt.close(fig)


# Question figure: parabola y = x^2 and line y = 4
fig, ax = plt.subplots(figsize=(4.8, 3.4))
x = np.linspace(-2.6, 2.6, 300)
ax.plot(x, x**2, color=INK, lw=1.6)
ax.axhline(4, color=ACCENT, lw=1.4)
axes(ax, (-3, 3), (-0.6, 6.4))
ax.text(1.55, 5.9, r"$y = x^2$", ha="right")
ax.text(2.95, 3.55, r"$y = 4$", color=ACCENT, ha="right")
ax.plot([-2, 2], [4, 4], "o", color=INK, ms=4)
ax.text(-2.1, 4.3, "A(-2, 4)", ha="right")
ax.text(2.1, 4.3, "B(2, 4)", ha="left")
ax.set_xticks([-2, -1, 1, 2])
ax.set_yticks([1, 2, 3, 4, 5])
save(fig, "q-parabola.svg")

# Solution figure: shaded region between y = x^2 and y = 4
fig, ax = plt.subplots(figsize=(4.8, 3.4))
ax.fill_between(x, x**2, 4, where=(np.abs(x) <= 2), color=FILL, alpha=0.45, lw=0)
ax.plot(x, x**2, color=INK, lw=1.6)
ax.axhline(4, color=ACCENT, lw=1.4)
axes(ax, (-3, 3), (-0.6, 6.4))
ax.text(0, 2.6, "required\nregion", ha="center")
ax.text(2.25, 5.6, r"$y = x^2$")
ax.text(-2.9, 4.2, r"$y = 4$", color=ACCENT)
ax.set_xticks([-2, -1, 1, 2])
ax.set_yticks([1, 2, 3, 4, 5])
save(fig, "sol-area.svg")

# Step figure: y = |x - 1|
fig, ax = plt.subplots(figsize=(4.2, 2.8))
x2 = np.linspace(-1.5, 3.5, 200)
ax.plot(x2, np.abs(x2 - 1), color=INK, lw=1.6)
axes(ax, (-1.6, 3.6), (-0.4, 2.8))
ax.plot([1], [0], "o", color=ACCENT, ms=5)
ax.text(1.15, -0.3, "corner at x = 1", color=ACCENT)
ax.text(2.2, 2.0, r"$y = |x-1|$", ha="right")
ax.set_xticks([-1, 1, 2, 3])
ax.set_yticks([1, 2])
save(fig, "step-abs.svg")
print("ok")
