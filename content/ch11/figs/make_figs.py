"""Figures for content/ch11/school.json.

Each figure is drawn true to scale in the plane that contains the point and the line
(distances in that plane equal the real 3-D distances).
Run from anywhere:  python content/ch11/figs/make_figs.py
"""
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#1f2937"
ACC = "#ef4444"
HERE = os.path.dirname(os.path.abspath(__file__))
plt.rcParams.update({"font.size": 11, "svg.fonttype": "none", "font.family": "DejaVu Sans"})


def base(w=4.8, h=3.4):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def right_angle(ax, s=0.45, up=1):
    ax.plot([s, s, 0], [0, s * up, s * up], color=INK, lw=1)


def save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", transparent=True, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


# Q15: P(1,2,3), foot M(3,5,9), PM = 7; L0 = (6,7,7) on the line, ML0 = sqrt(17)
def q15():
    fig, ax = base()
    d = math.sqrt(17)
    ax.plot([-2.0, d + 2.2], [0, 0], color=INK, lw=1.8)
    ax.annotate("", xy=(d + 2.3, 0), xytext=(d + 1.9, 0), arrowprops=dict(arrowstyle="->", color=INK, lw=1.8))
    ax.text(0.7, 0.4, r"line $\frac{x-6}{3}=\frac{y-7}{2}=\frac{z-7}{-2}$", color=INK, fontsize=11)
    ax.plot([0, 0], [0, 7], color=ACC, lw=1.6, ls="--")
    right_angle(ax)
    for (x, y, lab, dx, dy) in [(0, 7, "P(1, 2, 3)", 0.3, 0.0), (0, 0, "M(3, 5, 9)", 0.25, -0.75),
                                (d, 0, "(6, 7, 7)", -0.4, -0.75)]:
        ax.plot(x, y, "o", color=INK, ms=5)
        ax.text(x + dx, y + dy, lab, color=INK, fontsize=11)
    ax.text(0.3, 3.4, "PM = 7", color=ACC, fontsize=11)
    ax.text(0.7, 5.0, "M = foot of perpendicular", color=INK, fontsize=11)
    ax.set_xlim(-2.2, d + 2.6)
    ax.set_ylim(-1.2, 7.8)
    save(fig, "q15-sol.svg")


# Q16: A(1,6,3), foot M(1,3,5), AM = sqrt(13); image A'(1,0,7); L0 = (0,1,2), ML0 = sqrt(14)
def q16():
    fig, ax = base(4.8, 4.2)
    a = math.sqrt(13)
    d = math.sqrt(14)
    ax.plot([-d - 1.0, 3.6], [0, 0], color=INK, lw=1.8)
    ax.annotate("", xy=(3.7, 0), xytext=(3.3, 0), arrowprops=dict(arrowstyle="->", color=INK, lw=1.8))
    ax.text(0.9, 0.3, r"line $\frac{x}{1}=\frac{y-1}{2}=\frac{z-2}{3}$", color=INK, fontsize=11)
    ax.plot([0, 0], [a, -a], color=ACC, lw=1.6, ls="--")
    right_angle(ax)
    for (x, y, lab, dx, dy) in [(0, a, "A(1, 6, 3)", 0.3, -0.1), (0, 0, "M(1, 3, 5)", 0.25, -0.7),
                                (0, -a, "A'(1, 0, 7)", 0.3, -0.1), (-d, 0, "(0, 1, 2)", -0.6, -0.7)]:
        ax.plot(x, y, "o", color=INK, ms=5)
        ax.text(x + dx, y + dy, lab, color=INK, fontsize=11)
    ax.text(-2.9, a * 0.5, "AM = MA'", color=ACC, fontsize=11)
    ax.set_xlim(-d - 1.2, 4.0)
    ax.set_ylim(-a - 0.8, a + 0.8)
    save(fig, "q16-sol.svg")


if __name__ == "__main__":
    q15()
    q16()
    print("ok")
