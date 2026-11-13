"""Figures for Chapter 10 (Vector Algebra), Practice Set B.
Run from anywhere: python content/ch10/figs/make_figs_pb.py
"""
import os
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


def arrow(ax, x, y, color=INK, lw=2.0, ls="-"):
    ax.annotate("", xy=(x, y), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, mutation_scale=16))


# Q20: tug of war - three forces on a ring at the origin (to scale, 1 unit = 1 kN)
def q20():
    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    fig.patch.set_alpha(0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.plot([-5.2, 7.2], [0, 0], color=INK, lw=0.8, ls="--", alpha=0.6)
    ax.plot([0, 0], [-4.0, 5.0], color=INK, lw=0.8, ls="--", alpha=0.6)
    ax.text(7.25, 0, "$x$", va="center", ha="left")
    ax.text(0, 5.05, "$y$", va="bottom", ha="center")
    arrow(ax, 6, 0)
    arrow(ax, -4, 4)
    arrow(ax, -3, -3)
    ax.plot(0, 0, "o", ms=9, mfc="white", mec=INK, mew=2)
    ax.text(6.0, 0.25, "Team A", ha="center", va="bottom")
    ax.text(3.0, -0.3, r"$\vec{F_1}=6\hat{i}+0\hat{j}$", ha="center", va="top", fontsize=11)
    ax.text(-4.1, 4.15, "Team B", ha="right", va="bottom")
    ax.text(-2.5, 1.9, r"$\vec{F_2}=-4\hat{i}+4\hat{j}$", ha="right", va="top", fontsize=11)
    ax.text(-3.1, -3.15, "Team C", ha="right", va="top")
    ax.text(-1.2, -1.9, r"$\vec{F_3}=-3\hat{i}-3\hat{j}$", ha="left", va="top", fontsize=11)
    ax.text(0.2, 0.2, "ring", ha="left", va="bottom", fontsize=11)
    ax.set_xlim(-5.6, 7.6)
    ax.set_ylim(-4.2, 5.4)
    save(fig, "pb-q20.svg")


if __name__ == "__main__":
    q20()
    print("done")
