"""Figures for content/ch01/school.json. Run: python content/ch01/figs/make_figs.py"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
INK, FILL, ACC = "#1f2937", "#93c5fd", "#ef4444"
plt.rcParams.update({"font.size": 11, "text.color": INK, "axes.edgecolor": INK,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
                     "svg.fonttype": "path"})
PREVIEW = os.environ.get("FIG_PREVIEW")  # optional folder for PNG previews


def save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", transparent=True, bbox_inches="tight")
    if PREVIEW:
        fig.savefig(os.path.join(PREVIEW, name.replace(".svg", ".png")), dpi=110, bbox_inches="tight")
    plt.close(fig)


def axes_cross(ax):
    for s in ("left", "bottom"):
        ax.spines[s].set_position("zero")
    for s in ("right", "top"):
        ax.spines[s].set_visible(False)


# Q17: graph of f(x) = x / (1 + |x|), squeezed between y = -1 and y = 1
fig, ax = plt.subplots(figsize=(4.8, 3.0), dpi=96)
x = np.linspace(-10, 10, 800)
ax.axhspan(-1, 1, color=FILL, alpha=0.45, lw=0)
ax.plot(x, x / (1 + np.abs(x)), color=INK, lw=2)
ax.axhline(1, color=ACC, ls="--", lw=1.2)
ax.axhline(-1, color=ACC, ls="--", lw=1.2)
ax.text(10, 1.08, "$y=1$ (never reached)", ha="right", va="bottom", color=ACC)
ax.text(-10, -1.08, "$y=-1$ (never reached)", ha="left", va="top", color=ACC)
ax.text(3.2, 0.42, r"$f(x)=\dfrac{x}{1+|x|}$", color=INK)
ax.set_xlim(-10.5, 10.5)
ax.set_ylim(-1.6, 1.6)
axes_cross(ax)
ax.set_xticks([-8, -4, 4, 8])
ax.set_yticks([])
ax.text(-0.3, 1.0, "$1$", ha="right", va="bottom")
ax.text(0.3, -1.0, "$-1$", ha="left", va="bottom")
ax.text(10.5, -0.12, "$x$", ha="right", va="top")
ax.text(0.3, 1.55, "$y$", ha="left", va="top")
save(fig, "q17-graph.svg")

# Q15: L1 perpendicular to L2, L2 perpendicular to L3, so L1 parallel to L3
fig, ax = plt.subplots(figsize=(4.8, 2.8), dpi=96)
ax.plot([-3, 3], [1, 1], color=INK, lw=2)
ax.plot([-3, 3], [-1, -1], color=INK, lw=2)
ax.plot([0, 0], [-2, 2], color=ACC, lw=2)
for yy in (1, -1):  # small right-angle marks where L2 meets L1 and L3
    s = -1 if yy > 0 else 1
    ax.plot([0, 0.25, 0.25], [yy + 0.25 * s, yy + 0.25 * s, yy], color=INK, lw=1)
ax.text(3.1, 1, "$L_1$", va="center")
ax.text(3.1, -1, "$L_3$", va="center")
ax.text(0.1, 1.9, "$L_2$", color=ACC, va="top")
ax.text(-3, 1.25, r"$L_1 \perp L_2$", fontsize=11)
ax.text(-3, -1.55, r"$L_2 \perp L_3$", fontsize=11)
ax.text(0.5, 0.15, r"$L_1 \parallel L_3$", va="bottom", fontsize=11)
ax.text(0.5, -0.15, r"so $L_1$ is not $\perp$ to $L_3$", va="top", fontsize=11)
ax.set_xlim(-3.3, 3.6)
ax.set_ylim(-2.1, 2.1)
ax.set_aspect("equal")
ax.axis("off")
save(fig, "q15-sol.svg")
print("figures written to", HERE)
