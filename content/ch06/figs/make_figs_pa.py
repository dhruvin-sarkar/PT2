"""Figures for Chapter 6 (Application of Derivatives), Practice Set A.
Run from anywhere: python content/ch06/figs/make_figs_pa.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, Arc

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


# Q12: kite at height 3 m, horizontal distance x = 4 m, string s = 5 m
def q12():
    fig, ax = new(6.4, 3.8)
    ax.plot([-0.3, 5.0], [0, 0], color=INK, lw=2.5)
    ax.add_patch(Polygon([(0, 0), (4, 0), (4, 3)], closed=True, fc=FILL, alpha=0.45, ec="none"))
    ax.plot([0, 4], [0, 3], color=ACC, lw=2.2)
    ax.plot([4, 4], [0, 3], color=INK, lw=1.2, ls="--")
    ax.plot([3.75, 3.75, 4], [0, 0.25, 0.25], color=INK, lw=1)
    ax.add_patch(Polygon([(4, 3.3), (4.22, 3.0), (4, 2.7), (3.78, 3.0)], closed=True, fc=ACC, ec=INK, lw=1))
    ax.text(1.75, 1.75, "string $s$ (= 5 m)", rotation=36.87, ha="center", va="bottom", color=ACC)
    ax.text(4.12, 1.5, "3 m", ha="left", va="center")
    ax.annotate("", xy=(4, -0.35), xytext=(0, -0.35), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(2, -0.62, "$x$ (= 4 m at the instant)", ha="center", va="center")
    ax.annotate("", xy=(5.0, 3.0), xytext=(4.35, 3.0), arrowprops=dict(arrowstyle="->", color=ACC, lw=1.5))
    ax.text(4.7, 3.2, "200 cm/s", ha="center", va="bottom", color=ACC)
    ax.text(-0.1, -0.12, "O (boy)", ha="right", va="top")
    ax.text(4.0, 3.42, "kite", ha="center", va="bottom")
    ax.set_xlim(-1.3, 5.4)
    ax.set_ylim(-0.9, 3.9)
    save(fig, "pa-q12-kite.svg")


# Q15: open tank with a square base of side x and depth h (no lid), drawn in oblique view
def q15():
    fig, ax = new(5.4, 4.2)
    x = 3.0                      # side of the square base
    h = x / 2                    # depth at the optimum (h = x/2)
    d = np.array([1.1, 0.75])    # oblique offset for the receding edge (length x drawn shorter)
    F = [np.array(p, float) for p in [(0, 0), (x, 0), (x, h), (0, h)]]   # front face
    B = [p + d for p in F]                                               # back face
    # side and front faces shaded (the sheet metal); top left open
    for face in ([F[0], F[1], F[2], F[3]], [F[1], B[1], B[2], F[2]]):
        ax.add_patch(Polygon(face, closed=True, fc=FILL, alpha=0.45, ec="none"))
    # visible edges
    for p, q in [(F[0], F[1]), (F[1], F[2]), (F[2], F[3]), (F[3], F[0]),
                 (F[1], B[1]), (B[1], B[2]), (F[2], B[2]), (F[3], B[3]), (B[3], B[2])]:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=2)
    # hidden edges
    for p, q in [(F[0], B[0]), (B[0], B[1]), (B[0], B[3])]:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=1, ls="--")
    ax.text(x / 2 + d[0] / 2, h + d[1] / 2, "open top", ha="center", va="center", color=ACC)
    ax.annotate("", xy=(x, -0.3), xytext=(0, -0.3), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(x / 2, -0.55, "$x$", ha="center", va="center", fontsize=13)
    ax.text(x + d[0] / 2 + 0.15, d[1] / 2 - 0.1, "$x$", ha="left", va="center", fontsize=13)
    ax.annotate("", xy=(-0.3, h), xytext=(-0.3, 0), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(-0.45, h / 2, "$h$", ha="right", va="center", fontsize=13)
    ax.text(x / 2 + 0.2, 0.32, "volume $V = x^2h$ (fixed)", ha="center", va="center", fontsize=11)
    ax.set_xlim(-1.0, x + d[0] + 0.6)
    ax.set_ylim(-0.85, h + d[1] + 0.3)
    save(fig, "pa-q15-open-tank.svg")


# Q16: cone inscribed in a sphere of radius r (cross-section), h = 4r/3
def q16():
    fig, ax = new(5.4, 4.9)
    r = 2.0
    h = 4 * r / 3
    rho = np.sqrt(2 * r * h - h ** 2)
    V = (0, r)                 # vertex at top of sphere
    yb = r - h                 # base level
    ax.add_patch(Circle((0, 0), r, fill=False, ec=INK, lw=2))
    ax.add_patch(Polygon([V, (-rho, yb), (rho, yb)], closed=True, fc=FILL, alpha=0.45, ec="none"))
    ax.add_patch(Polygon([V, (-rho, yb), (rho, yb)], closed=True, fill=False, ec=INK, lw=1.8))
    ax.plot([0, 0], [r, yb], color=INK, lw=1, ls="--")
    ax.plot([0, rho], [0, yb], color=ACC, lw=2)
    ax.plot(0, 0, "o", color=INK, ms=4)
    ax.text(-0.1, 0.05, "O", ha="right", va="bottom")
    ax.text(rho / 2 + 0.1, yb / 2 + 0.05, "$r$", color=ACC, fontsize=13, ha="left")
    ax.text(rho / 2, yb - 0.08, "$R$", ha="center", va="top", fontsize=13)
    ax.annotate("", xy=(-rho - 0.3, r), xytext=(-rho - 0.3, yb), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(-rho - 0.42, (r + yb) / 2, "$h$", ha="right", va="center", fontsize=13)
    ax.plot([-rho - 0.4, 0], [r, r], color=INK, lw=0.6, ls=":")
    ax.text(0.08, -0.33, "$h - r$", ha="left", va="center")
    ax.text(0.05, r + 0.08, "vertex", ha="left", va="bottom")
    ax.text(0, -r - 0.12, "sphere of radius $r$ (cross-section)", ha="center", va="top")
    ax.set_xlim(-2.6, 2.3)
    ax.set_ylim(-2.6, 2.5)
    save(fig, "pa-q16-cone-in-sphere.svg")


# Q17: window = rectangle surmounted by an equilateral triangle
def q17():
    fig, ax = new(4.8, 4.8)
    x = 2.0
    y = 1.3
    top = (x / 2, y + np.sqrt(3) / 2 * x)
    ax.add_patch(Polygon([(0, 0), (x, 0), (x, y), top, (0, y)], closed=True, fc=FILL, alpha=0.45, ec="none"))
    ax.plot([0, 0, x, x], [y, 0, 0, y], color=INK, lw=2)
    ax.plot([0, top[0], x], [y, top[1], y], color=INK, lw=2)
    ax.plot([0, x], [y, y], color=INK, lw=1, ls="--")
    ax.annotate("", xy=(x, -0.25), xytext=(0, -0.25), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(x / 2, -0.45, "$x$", ha="center", va="center", fontsize=13)
    ax.annotate("", xy=(x + 0.3, y), xytext=(x + 0.3, 0), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(x + 0.42, y / 2, "$y$", ha="left", va="center", fontsize=13)
    ax.text(x * 0.18, y + 0.95, "$x$", ha="right", va="center", fontsize=13, color=ACC)
    ax.text(x * 0.82, y + 0.95, "$x$", ha="left", va="center", fontsize=13, color=ACC)
    ax.text(x / 2, y / 2, "rectangle", ha="center", va="center")
    ax.text(x / 2, y + 0.45, "equilateral\ntriangle", ha="center", va="center", fontsize=11)
    ax.set_xlim(-0.4, x + 0.8)
    ax.set_ylim(-0.7, top[1] + 0.2)
    save(fig, "pa-q17-window.svg")


# Q19: inverted cone tank, semi-vertical angle tan^-1(0.5)
def q19():
    fig, ax = new(4.8, 4.8)
    H = 6.0
    Rtop = H * 0.5
    h = 4.0
    rw = h * 0.5
    ax.add_patch(Polygon([(0, 0), (-rw, h), (rw, h)], closed=True, fc=FILL, alpha=0.45, ec="none"))
    ax.plot([-Rtop, 0, Rtop], [H, 0, H], color=INK, lw=2)
    ax.plot([-Rtop, Rtop], [H, H], color=INK, lw=1, ls="--")
    ax.plot([-rw, rw], [h, h], color=INK, lw=1.4)
    ax.plot([0, 0], [0, H], color=INK, lw=0.8, ls=":")
    ax.plot([0, rw], [h, h], color=ACC, lw=2)
    ax.text(rw / 2, h + 0.08, "$r$", ha="center", va="bottom", color=ACC, fontsize=13)
    ax.annotate("", xy=(-rw - 0.6, h), xytext=(-rw - 0.6, 0), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(-rw - 0.75, h / 2, "$h$", ha="right", va="center", fontsize=13)
    ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=np.degrees(np.arctan2(1, 0.5)), theta2=90, color=ACC, lw=1.5))
    ax.text(0.22, 0.95, r"$\alpha$", color=ACC, fontsize=13)
    ax.text(0, h / 2, "water", ha="center", va="center")
    ax.text(0, -0.15, "vertex", ha="center", va="top")
    ax.text(2.2, 0.8, r"$\tan\alpha = 0.5$", ha="left", va="center")
    ax.set_xlim(-3.6, 3.9)
    ax.set_ylim(-0.6, H + 0.2)
    save(fig, "pa-q19-cone-tank.svg")


if __name__ == "__main__":
    q12(); q15(); q16(); q17(); q19()
    print("done")
