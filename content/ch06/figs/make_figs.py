"""Figures for Chapter 6 (Application of Derivatives), school worksheet.
Run from anywhere: python content/ch06/figs/make_figs.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Polygon

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


# Q12: ladder against a wall (x = 4, y = 3, ladder = 5)
def q12():
    fig, ax = new(6.4, 4.2)
    ax.plot([0, 0], [0, 3.6], color=INK, lw=2.5)
    ax.plot([-0.3, 5.0], [0, 0], color=INK, lw=2.5)
    for k in np.arange(0.2, 3.6, 0.35):
        ax.plot([0, -0.18], [k, k - 0.18], color=INK, lw=0.8)
    ax.plot([0, 4], [3, 0], color=ACC, lw=3)
    ax.plot([0, 0.25, 0.25], [0.25, 0.25, 0], color=INK, lw=1)
    ax.text(2.15, 1.75, "ladder = 5 m", rotation=-36.9, ha="center", va="bottom", fontsize=12)
    ax.annotate("", xy=(4, -0.35), xytext=(0, -0.35), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(2, -0.62, "$x$ (= 4 m at the instant)", ha="center", va="center")
    ax.annotate("", xy=(-0.55, 3), xytext=(-0.55, 0), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(-0.75, 1.5, "$y$", ha="right", va="center", fontsize=13)
    ax.annotate("", xy=(4.9, 0.25), xytext=(4.1, 0.25), arrowprops=dict(arrowstyle="->", color=ACC, lw=1.5))
    ax.text(4.5, 0.45, "2 cm/s", ha="center", color=ACC)
    ax.text(0.15, 3.25, "wall", ha="left")
    ax.text(4.0, 0.08, "B", ha="center", va="bottom")
    ax.text(0.08, 3.0, "A", ha="left", va="center")
    ax.text(-0.1, -0.15, "O", ha="right", va="top")
    ax.set_xlim(-1.2, 5.2)
    ax.set_ylim(-0.9, 3.8)
    save(fig, "q12-ladder.svg")


# Q15: rectangle inscribed in a circle of radius a
def q15():
    fig, ax = new(5.2, 4.6)
    a = 2.0
    xx, yy = 2.6, np.sqrt(16 - 2.6 ** 2)  # sides x, y with x^2 + y^2 = (2a)^2
    ax.add_patch(Circle((0, 0), a, fill=False, ec=INK, lw=2))
    ax.add_patch(Rectangle((-xx / 2, -yy / 2), xx, yy, fc=FILL, alpha=0.45, ec="none"))
    ax.add_patch(Rectangle((-xx / 2, -yy / 2), xx, yy, fill=False, ec=INK, lw=1.8))
    ax.plot([-xx / 2, xx / 2], [-yy / 2, yy / 2], color=ACC, lw=2)
    ax.plot(0, 0, "o", color=INK, ms=4)
    ax.text(0.12, -0.18, "O", ha="left", va="top")
    ax.text(0.35, 0.55, "$2a$", color=ACC, fontsize=13)
    ax.text(0, -yy / 2 - 0.12, "$x$", ha="center", va="top", fontsize=13)
    ax.text(xx / 2 + 0.1, 0, "$y$", ha="left", va="center", fontsize=13)
    ax.text(-1.55, 1.7, "radius $a$", ha="center")
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-2.3, 2.3)
    save(fig, "q15-rectangle-in-circle.svg")


# Q16: cylinder inscribed in a sphere (cross-section)
def q16():
    fig, ax = new(5.4, 4.8)
    R = 2.0
    h = 2 * R / np.sqrt(3)
    r = np.sqrt(R ** 2 - h ** 2 / 4)
    ax.add_patch(Circle((0, 0), R, fill=False, ec=INK, lw=2))
    ax.add_patch(Rectangle((-r, -h / 2), 2 * r, h, fc=FILL, alpha=0.45, ec="none"))
    ax.add_patch(Rectangle((-r, -h / 2), 2 * r, h, fill=False, ec=INK, lw=1.8))
    ax.plot([0, r], [0, h / 2], color=ACC, lw=2)
    ax.plot([0, 0], [0, h / 2], color=INK, lw=1, ls="--")
    ax.plot([0, r], [h / 2, h / 2], color=INK, lw=1, ls="--")
    ax.plot(0, 0, "o", color=INK, ms=4)
    ax.text(-0.1, -0.05, "O", ha="right", va="top")
    ax.text(1.0, 0.38, "$R$", color=ACC, fontsize=13)
    ax.text(-0.08, h / 4, "$h/2$", ha="right", va="center")
    ax.text(r / 2, h / 2 + 0.06, "$r$", ha="center", va="bottom", fontsize=13)
    ax.annotate("", xy=(r + 0.35, h / 2), xytext=(r + 0.35, -h / 2), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(r + 0.48, 0, "$h$", ha="left", va="center", fontsize=13)
    ax.text(0, -R - 0.12, "sphere of radius $R$ (cross-section)", ha="center", va="top")
    ax.set_xlim(-2.3, 2.4)
    ax.set_ylim(-2.6, 2.3)
    save(fig, "q16-cylinder-in-sphere.svg")


# Q17: Norman window
def q17():
    fig, ax = new(5.0, 4.8)
    r = 1.0
    hh = 1.4
    th = np.linspace(0, np.pi, 100)
    pts = [(-r, 0), (r, 0), (r, hh)] + [(r * np.cos(t), hh + r * np.sin(t)) for t in th] + [(-r, hh)]
    ax.add_patch(Polygon(pts, closed=True, fc=FILL, alpha=0.45, ec="none"))
    ax.plot([-r, r, r], [hh, hh, hh], color=INK, lw=1, ls="--")
    ax.plot([-r, -r, r, r], [hh, 0, 0, hh], color=INK, lw=2)
    ax.plot(r * np.cos(th), hh + r * np.sin(th), color=INK, lw=2)
    ax.plot([0, r * np.cos(np.pi / 4)], [hh, hh + r * np.sin(np.pi / 4)], color=ACC, lw=1.8)
    ax.text(0.5, hh + 0.08, "$r$", color=ACC, fontsize=13)
    ax.annotate("", xy=(r, -0.25), xytext=(-r, -0.25), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(0, -0.45, "$2r$", ha="center", va="center", fontsize=13)
    ax.annotate("", xy=(r + 0.3, hh), xytext=(r + 0.3, 0), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(r + 0.42, hh / 2, "$h$", ha="left", va="center", fontsize=13)
    ax.text(0, hh / 2, "rectangle", ha="center", va="center")
    ax.text(0, hh + 0.55 * r, "semicircle", ha="center", va="center")
    ax.set_xlim(-1.6, 1.9)
    ax.set_ylim(-0.7, hh + r + 0.2)
    save(fig, "q17-window.svg")


# Q19: lamp post and shadow (similar triangles)
def q19():
    fig, ax = new(6.6, 3.8)
    x, s = 4.0, 2.0
    ax.plot([-0.4, x + s + 0.6], [0, 0], color=INK, lw=2)
    ax.plot([0, 0], [0, 6], color=INK, lw=3)
    ax.plot([x, x], [0, 2], color=INK, lw=3)
    ax.plot([0, x + s], [6, 0], color=ACC, lw=1.4, ls="--")
    ax.add_patch(Polygon([(x, 0), (x + s, 0), (x, 2)], closed=True, fc=FILL, alpha=0.45, ec="none"))
    ax.plot(0, 6, "o", color="#f59e0b", ms=9)
    ax.text(-0.15, 3, "6 m", ha="right", va="center")
    ax.text(x - 0.12, 1, "2 m", ha="right", va="center")
    ax.text(0, -0.25, "A", ha="center", va="top")
    ax.text(x, -0.25, "B", ha="center", va="top")
    ax.text(x + s, -0.25, "C", ha="center", va="top")
    ax.text(0.15, 6.05, "L (lamp)", ha="left", va="bottom")
    ax.text(x + 0.12, 2.1, "M", ha="left", va="bottom")
    ax.annotate("", xy=(x, -0.9), xytext=(0, -0.9), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(x / 2, -1.2, "$x$", ha="center", va="center", fontsize=13)
    ax.annotate("", xy=(x + s, -0.9), xytext=(x, -0.9), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(x + s / 2, -1.2, "$s$ (shadow)", ha="center", va="center")
    ax.set_xlim(-1.0, x + s + 0.8)
    ax.set_ylim(-1.5, 6.6)
    save(fig, "q19-lamp-post.svg")


# Q20: rectangular solar panel with one partition
def q20():
    fig, ax = new(6.4, 3.8)
    X, Y = 3.0, 2.0
    ax.add_patch(Rectangle((0, 0), X, Y, fc=FILL, alpha=0.45, ec="none"))
    ax.add_patch(Rectangle((0, 0), X, Y, fill=False, ec=INK, lw=2))
    ax.plot([X / 2, X / 2], [0, Y], color=ACC, lw=2.2)
    ax.text(X / 2 + 0.08, Y / 2, "partition ($y$)", color=ACC, ha="left", va="center", rotation=90)
    ax.annotate("", xy=(X, -0.25), xytext=(0, -0.25), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(X / 2, -0.48, "$x$", ha="center", va="center", fontsize=13)
    ax.annotate("", xy=(X + 0.25, Y), xytext=(X + 0.25, 0), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(X + 0.38, Y / 2, "$y$", ha="left", va="center", fontsize=13)
    ax.text(X / 4, Y / 2, "section 1", ha="center", va="center")
    ax.text(3 * X / 4 + 0.1, Y / 2, "section 2", ha="center", va="center")
    ax.set_xlim(-0.3, X + 0.7)
    ax.set_ylim(-0.7, Y + 0.2)
    save(fig, "q20-solar-panel.svg")


if __name__ == "__main__":
    q12(); q15(); q16(); q17(); q19(); q20()
    print("done")
