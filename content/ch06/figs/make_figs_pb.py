"""Figures for Chapter 6 (Application of Derivatives), Practice Set B.
Run from anywhere: python content/ch06/figs/make_figs_pb.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, Ellipse

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


def new(w=6.4, h=4.4):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_alpha(0)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", transparent=True, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


# Q15: isosceles triangle ABC inscribed in a circle of radius r, centre O;
# base BC at distance x below O, so height AD = r + x and BD = sqrt(r^2 - x^2)
def q15():
    fig, ax = new(5.0, 5.0)
    r = 2.0
    x = 0.85                       # a general position (not the optimum)
    hb = np.sqrt(r ** 2 - x ** 2)
    A, B, C, D = (0, r), (-hb, -x), (hb, -x), (0, -x)
    ax.add_patch(Circle((0, 0), r, fill=False, ec=INK, lw=2))
    ax.add_patch(Polygon([A, B, C], closed=True, fc=FILL, alpha=0.45, ec="none"))
    ax.add_patch(Polygon([A, B, C], closed=True, fill=False, ec=INK, lw=1.8))
    ax.plot([0, 0], [r, -x], color=INK, lw=1, ls="--")
    ax.plot([0, hb], [0, -x], color=ACC, lw=2)
    ax.plot(0, 0, "o", color=INK, ms=4)
    ax.plot([0.18, 0.18, 0], [-x, -x + 0.18, -x + 0.18], color=INK, lw=1)
    ax.text(-0.1, 0.05, "O", ha="right", va="bottom")
    ax.text(0, r + 0.1, "A", ha="center", va="bottom")
    ax.text(-hb - 0.1, -x - 0.05, "B", ha="right", va="top")
    ax.text(hb + 0.1, -x - 0.05, "C", ha="left", va="top")
    ax.text(0, -x - 0.12, "D", ha="center", va="top")
    ax.text(hb / 2 + 0.12, -x / 2 + 0.05, "$r$", color=ACC, fontsize=13, ha="left")
    ax.text(-0.08, -x / 2, "$x$", ha="right", va="center", fontsize=13)
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.5)
    save(fig, "pb-q15-triangle-in-circle.svg")


# Q16: cylinder of radius x inscribed in a cone of height h, semi-vertical angle alpha (cross-section)
def q16():
    fig, ax = new(5.0, 5.0)
    h = 4.0
    al = np.radians(33)
    R = h * np.tan(al)
    x = 2 * h * np.tan(al) / 3
    H = h - x / np.tan(al)
    ax.plot([-R, 0, R], [0, h, 0], color=INK, lw=2)
    ax.plot([-R - 0.3, R + 0.3], [0, 0], color=INK, lw=2)
    ax.add_patch(Rectangle((-x, 0), 2 * x, H, fc=FILL, alpha=0.45, ec="none"))
    ax.add_patch(Rectangle((-x, 0), 2 * x, H, fill=False, ec=INK, lw=1.8))
    ax.plot([0, 0], [0, h], color=INK, lw=1, ls="--")
    ax.plot([0, x], [H, H], color=ACC, lw=2)
    ax.text(x / 2, H + 0.08, "$x$", color=ACC, fontsize=13, ha="center", va="bottom")
    ax.annotate("", xy=(R + 0.5, h), xytext=(R + 0.5, 0), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(R + 0.62, h / 2, "$h$", ha="left", va="center", fontsize=13)
    ax.plot([0, R + 0.6], [h, h], color=INK, lw=0.6, ls=":")
    ax.annotate("", xy=(-x - 0.3, H), xytext=(-x - 0.3, 0), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(-x - 0.5, H / 2, "$H$", ha="right", va="center", fontsize=13)
    t = np.linspace(np.pi / 2 - al, np.pi / 2, 30)
    ax.plot(0.9 * np.cos(t), h - 0.9 * np.sin(t), color=ACC, lw=1.4)
    ax.text(0.2, h - 1.25, r"$\alpha$", color=ACC, fontsize=13, ha="center")
    ax.text(R / 2 + 0.35, -0.1, "$h\\tan\\alpha$", ha="center", va="top")
    ax.text(0, h + 0.1, "vertex", ha="center", va="bottom")
    ax.set_xlim(-R - 0.9, R + 1.1)
    ax.set_ylim(-0.6, h + 0.5)
    save(fig, "pb-q16-cylinder-in-cone.svg")


# Q17: wire of 28 m cut into two pieces: square of side a and circle of radius r
def q17():
    fig, ax = new(6.4, 3.2)
    ax.plot([0, 7], [2.9, 2.9], color=INK, lw=3)
    ax.plot([4.2, 4.2], [2.7, 3.1], color=ACC, lw=2)
    ax.text(2.1, 3.05, "$28 - 2\\pi r$", ha="center", va="bottom")
    ax.text(5.6, 3.05, "$2\\pi r$", ha="center", va="bottom")
    ax.text(4.2, 2.6, "cut", color=ACC, ha="center", va="top", fontsize=11)
    ax.add_patch(Rectangle((0.8, 0), 2.2, 2.2, fc=FILL, alpha=0.45, ec=INK, lw=2))
    ax.text(1.9, -0.12, "$a$", ha="center", va="top", fontsize=13)
    ax.text(1.9, 1.1, "square", ha="center", va="center")
    ax.add_patch(Circle((5.6, 1.1), 1.1, fc=FILL, alpha=0.45, ec=INK, lw=2))
    ax.plot([5.6, 6.7], [1.1, 1.1], color=ACC, lw=2)
    ax.plot(5.6, 1.1, "o", color=INK, ms=3)
    ax.text(6.15, 1.18, "$r$", color=ACC, ha="center", va="bottom", fontsize=13)
    ax.text(5.6, 0.55, "circle", ha="center", va="center")
    ax.set_xlim(-0.2, 7.2)
    ax.set_ylim(-0.6, 3.6)
    save(fig, "pb-q17-wire.svg")


# Q19: spotlight L on the ground, man MN (2 m) at distance x from L, wall 12 m away; shadow height y on wall
def q19():
    fig, ax = new(6.6, 3.6)
    x, W = 8.0, 12.0
    y = 24 / x
    ax.plot([-0.5, W + 0.3], [0, 0], color=INK, lw=2.5)
    ax.plot([W, W], [0, 3.8], color=INK, lw=3)
    ax.add_patch(Polygon([(0, 0), (W, y), (W, 0)], closed=True, fc=FILL, alpha=0.45, ec="none"))
    ax.plot([0, W], [0, y], color=ACC, lw=1.6, ls="--")
    ax.plot([x, x], [0, 2], color=INK, lw=3)
    ax.plot(x, 2.12, "o", color=INK, ms=6)
    ax.plot([W, W], [0, y], color=ACC, lw=3.5)
    ax.add_patch(Polygon([(-0.3, 0), (0.3, 0), (0, 0.35)], closed=True, fc=INK))
    ax.text(0, -0.15, "L (spotlight)", ha="center", va="top")
    ax.text(x - 0.15, 1.0, "2 m", ha="right", va="center")
    ax.text(W + 0.15, y / 2, "$y$", color=ACC, ha="left", va="center", fontsize=13)
    ax.text(W + 0.15, 3.4, "wall", ha="left", va="center")
    ax.annotate("", xy=(x, -0.75), xytext=(0, -0.75), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(x / 2, -0.95, "$x$", ha="center", va="top", fontsize=13)
    ax.annotate("", xy=(W, -1.55), xytext=(0, -1.55), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(W / 2, -1.75, "12 m", ha="center", va="top")
    ax.annotate("", xy=(x + 1.6, 3.3), xytext=(x + 0.2, 3.3), arrowprops=dict(arrowstyle="->", color=ACC, lw=1.5))
    ax.text(x + 0.9, 3.4, "1.6 m/s", color=ACC, ha="center", va="bottom", fontsize=11)
    ax.set_xlim(-1.2, W + 1.2)
    ax.set_ylim(-2.3, 4.0)
    save(fig, "pb-q19-spotlight.svg")


# Q20: rectangle of length 2x and breadth 2y inscribed in the ellipse x^2/a^2 + y^2/b^2 = 1
def q20():
    fig, ax = new(6.4, 4.4)
    a, b = 3.0, 2.0
    x = 2.1
    y = b / a * np.sqrt(a ** 2 - x ** 2)
    ax.annotate("", xy=(3.6, 0), xytext=(-3.6, 0), arrowprops=dict(arrowstyle="->", color=INK, lw=1))
    ax.annotate("", xy=(0, 2.6), xytext=(0, -2.6), arrowprops=dict(arrowstyle="->", color=INK, lw=1))
    ax.text(3.65, -0.05, "$X$", ha="left", va="top")
    ax.text(0.08, 2.6, "$Y$", ha="left", va="top")
    ax.add_patch(Ellipse((0, 0), 2 * a, 2 * b, fill=False, ec=INK, lw=2))
    ax.add_patch(Rectangle((-x, -y), 2 * x, 2 * y, fc=FILL, alpha=0.45, ec=INK, lw=1.8))
    ax.plot(x, y, "o", color=ACC, ms=5)
    ax.text(x + 0.1, y + 0.08, "$P(x, y)$", color=ACC, ha="left", va="bottom")
    ax.text(a + 0.05, 0.08, "$a$", ha="left", va="bottom")
    ax.text(0.08, b + 0.05, "$b$", ha="left", va="bottom")
    ax.text(-x / 2 - 0.4, y / 2 + 0.25, "soccer field", ha="center", va="center", fontsize=11)
    ax.text(-2.35, -2.25, r"$\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$", ha="left", va="center")
    ax.set_xlim(-3.8, 3.9)
    ax.set_ylim(-2.7, 2.7)
    save(fig, "pb-q20-ellipse-field.svg")


if __name__ == "__main__":
    q15(); q16(); q17(); q19(); q20()
    print("done")
