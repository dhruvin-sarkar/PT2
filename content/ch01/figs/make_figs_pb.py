"""Figures for content/ch01/practice-b.json. Run: python content/ch01/figs/make_figs_pb.py"""
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


# Q12: graph of f(x) = x^2 / (1 + x^2): range [0, 1); f(1) = f(-1) = 1/2; y = 1 never reached
fig, ax = plt.subplots(figsize=(4.8, 3.0), dpi=96)
x = np.linspace(-8, 8, 1200)
ax.axhspan(0, 1, color=FILL, alpha=0.45, lw=0)
ax.plot(x, x ** 2 / (1 + x ** 2), color=INK, lw=2)
ax.axhline(1, color=INK, ls=":", lw=1.2)
ax.text(-7.9, 1.04, "$y = 1$ (never reached)", fontsize=10, va="bottom")
ax.axhline(0.5, color=ACC, ls="--", lw=1.2)
ax.plot([-1, 1], [0.5, 0.5], "o", color=ACC, ms=5)
ax.text(2.4, 0.56, r"$y=\frac{1}{2}$ meets the graph twice", color=ACC, fontsize=10, va="bottom")
ax.plot([0], [0], "o", color=INK, ms=4)
ax.text(-7.9, 0.62, "range $[0, 1)$", color=INK, fontsize=10)
ax.text(3.2, 0.12, r"$f(x)=\dfrac{x^2}{1+x^2}$", color=INK)
ax.set_xlim(-8.3, 8.3)
ax.set_ylim(-0.35, 1.35)
axes_cross(ax)
ax.set_xticks([-6, -4, -2, 2, 4, 6])
ax.set_yticks([])
ax.text(-1.25, 0.44, r"$(-1, \frac{1}{2})$", color=ACC, fontsize=10, ha="right", va="top")
ax.text(1.25, 0.44, r"$(1, \frac{1}{2})$", color=ACC, fontsize=10, ha="left", va="top")
ax.text(8.3, -0.04, "$x$", ha="right", va="top")
ax.text(0.25, 1.34, "$y$", ha="left", va="top")
save(fig, "pb-q12-graph.svg")

# Q15: points related to P lie on the circle with centre O and radius OP
fig, ax = plt.subplots(figsize=(4.8, 3.4), dpi=96)
t = np.linspace(0, 2 * np.pi, 400)
r = 2.0
ax.plot(r * np.cos(t), r * np.sin(t), color=INK, lw=2)
P = (r * np.cos(0.6), r * np.sin(0.6))
Q = (r * np.cos(2.4), r * np.sin(2.4))
ax.plot([0, P[0]], [0, P[1]], color=ACC, lw=1.6)
ax.plot([0, Q[0]], [0, Q[1]], color=ACC, lw=1.6, ls="--")
for pt, lab, dx, dy in [(P, "$P$", 0.12, 0.05), (Q, "$Q$", -0.3, 0.05), ((0, 0), "$O$", -0.25, -0.3)]:
    ax.plot(*pt, "o", color=INK, ms=4)
    ax.text(pt[0] + dx, pt[1] + dy, lab)
ax.text(0.95, 0.35, "$OP$", color=ACC)
ax.text(-1.15, 0.35, "$OQ = OP$", color=ACC, ha="right")
ax.text(1.5, -2.1, "circle: centre $O$, radius $OP$", fontsize=10, ha="center", va="top")
ax.set_xlim(-2.8, 2.8)
ax.set_ylim(-2.6, 2.4)
ax.set_aspect("equal")
ax.axis("off")
save(fig, "pb-q15-sol.svg")
print("figures written to", HERE)
