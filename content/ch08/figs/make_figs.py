"""Figures for Chapter 8 (Application of Integrals), school worksheet.

Run from anywhere:  python make_figs.py
Writes qNN.svg next to this script. Style follows tools/CONTRACT.md:
ink #1f2937, shaded region #93c5fd at 45% opacity, accent #ef4444,
transparent background, about 460 px wide, text at least 11 px.
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
    "svg.fonttype": "path",
    "font.size": 10,
    "mathtext.fontset": "dejavusans",
    "text.color": INK,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "savefig.transparent": True,
})


def axes(xlim, ylim, h=3.2, xlabel=True, ticks=True):
    fig, ax = plt.subplots(figsize=(4.8, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["left"].set_linewidth(0.9)
    ax.spines["bottom"].set_linewidth(0.9)
    ax.plot(1, 0, ">", color=INK, transform=ax.get_yaxis_transform(), clip_on=False, ms=4)
    ax.plot(0, 1, "^", color=INK, transform=ax.get_xaxis_transform(), clip_on=False, ms=4)
    ax.text(1.0, 0.0, "  X", transform=ax.get_yaxis_transform(), va="center", ha="left", fontsize=10)
    ax.text(0.0, 1.0, "Y", transform=ax.get_xaxis_transform(), va="bottom", ha="center", fontsize=10)
    if not ticks:
        ax.set_xticks([])
        ax.set_yticks([])
    ax.tick_params(labelsize=9, length=3)
    return fig, ax


def save(fig, name):
    fig.tight_layout(pad=0.4)
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def shade(ax, xs, y1, y2=0):
    ax.fill_between(xs, y1, y2, color=FILL, alpha=0.45, lw=0)


def vline(ax, x0, y0, y1, label=None, ly=None):
    ax.plot([x0, x0], [y0, y1], color=INK, lw=0.9, ls="--")
    if label:
        ax.text(x0, ly if ly is not None else y1, label, ha="center", va="bottom", fontsize=10)


# Q7: y^2 = x, x = 1 to 4
def q07():
    fig, ax = axes((-0.5, 5), (-0.6, 2.7))
    t = np.linspace(0, 4.8, 300)
    ax.plot(t, np.sqrt(t), color=INK, lw=1.6)
    xs = np.linspace(1, 4, 200)
    shade(ax, xs, np.sqrt(xs))
    vline(ax, 1, 0, 1.0)
    ax.text(0.95, 1.08, "$x=1$", ha="right", fontsize=10)
    vline(ax, 4, 0, 2.0, "$x=4$", 2.05)
    ax.text(4.5, 2.2, r"$y=\sqrt{x}$", fontsize=11)
    ax.text(2.5, 0.55, "Area", ha="center", fontsize=10)
    ax.set_xticks([1, 2, 3, 4]); ax.set_yticks([1, 2])
    save(fig, "q07.svg")


# Q8: y^2 = 9x, x = 2 to 4
def q08():
    fig, ax = axes((-0.5, 5), (-1, 7.5))
    t = np.linspace(0, 4.8, 300)
    ax.plot(t, 3 * np.sqrt(t), color=INK, lw=1.6)
    xs = np.linspace(2, 4, 200)
    shade(ax, xs, 3 * np.sqrt(xs))
    vline(ax, 2, 0, 3 * np.sqrt(2))
    ax.text(1.95, 4.5, "$x=2$", ha="right", fontsize=10)
    vline(ax, 4, 0, 6, "$x=4$", 6.15)
    ax.text(3.6, 6.9, r"$y=3\sqrt{x}$", fontsize=11)
    ax.text(3, 2, "Area", ha="center", fontsize=10)
    ax.set_xticks([1, 2, 3, 4]); ax.set_yticks([2, 4, 6])
    save(fig, "q08.svg")


# Q9: x^2 = 4y, y = 2 to 4, bounded by y-axis
def q09():
    fig, ax = axes((-4.8, 5.2), (-0.6, 5.5))
    t = np.linspace(-4.6, 4.6, 300)
    ax.plot(t, t ** 2 / 4, color=INK, lw=1.6)
    ys = np.linspace(2, 4, 200)
    ax.fill_betweenx(ys, 0, 2 * np.sqrt(ys), color=FILL, alpha=0.45, lw=0)
    ax.plot([-4.6, 4.6], [2, 2], color=INK, lw=0.9, ls="--")
    ax.plot([-4.6, 4.6], [4, 4], color=INK, lw=0.9, ls="--")
    ax.text(4.7, 2.0, "$y=2$", va="center", fontsize=10)
    ax.text(4.7, 4.0, "$y=4$", va="center", fontsize=10)
    ax.text(3.0, 4.9, "$x^2=4y$", fontsize=11)
    ax.text(1.0, 3.0, "Area", ha="center", fontsize=10)
    ax.set_xticks([-4, -2, 2, 4]); ax.set_yticks([2, 4])
    save(fig, "q09.svg")


# Q10: y = 3x + 2, x = -1 to 1
def q10():
    fig, ax = axes((-1.6, 1.8), (-1.8, 5.8))
    t = np.linspace(-1.3, 1.3, 100)
    ax.plot(t, 3 * t + 2, color=INK, lw=1.6)
    xs = np.linspace(-1, 1, 200)
    shade(ax, xs, 3 * xs + 2)
    vline(ax, -1, -1, 0)
    vline(ax, 1, 0, 5)
    ax.text(-1, 0.2, "$x=-1$", ha="center", fontsize=10)
    ax.text(1.08, 4.3, "$x=1$", ha="left", fontsize=10)
    ax.plot([-2 / 3], [0], "o", color=ACC, ms=4)
    ax.text(-0.5, -0.75, r"$(-\frac{2}{3},0)$", ha="left", fontsize=10, color=ACC)
    ax.text(1.3, 5.3, "$y=3x+2$", fontsize=11)
    ax.annotate("$A_1$", xy=(-0.88, -0.3), xytext=(-1.5, -1.0), fontsize=10,
                arrowprops=dict(arrowstyle="->", color=INK, lw=0.8))
    ax.text(0.4, 1.2, "$A_2$", fontsize=10)
    ax.set_xticks([1]); ax.set_yticks([-1, 2, 5])
    save(fig, "q10.svg")


def ellipse(ax, A, B, lw=1.6):
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(A * np.cos(th), B * np.sin(th), color=INK, lw=lw)


# Q11: x^2/16 + y^2/9 = 1, first quadrant
def q11():
    fig, ax = axes((-5, 5.6), (-3.6, 4.2))
    ellipse(ax, 4, 3)
    xs = np.linspace(0, 4, 300)
    shade(ax, xs, 0.75 * np.sqrt(16 - xs ** 2))
    ax.text(4.1, 0.15, "A(4,0)", fontsize=10)
    ax.text(0.15, 3.15, "B(0,3)", fontsize=10)
    ax.text(1.5, 1.0, "Area", fontsize=10)
    ax.text(-4.9, 3.4, r"$\frac{x^2}{16}+\frac{y^2}{9}=1$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    save(fig, "q11.svg")


# Q12: x^2 + y^2 = 16, x = 0 to 2
def q12():
    fig, ax = axes((-5, 5.6), (-4.6, 5.0), h=4.3)
    ax.set_aspect("equal")
    ellipse(ax, 4, 4)
    xs = np.linspace(0, 2, 200)
    shade(ax, xs, np.sqrt(16 - xs ** 2))
    vline(ax, 2, 0, np.sqrt(12))
    ax.text(2.1, np.sqrt(12) + 0.1, r"$(2,2\sqrt{3})$", fontsize=10)
    ax.text(2.05, -0.55, "$x=2$", fontsize=10)
    ax.text(4.1, 0.15, "(4,0)", fontsize=10)
    ax.text(0.9, 1.5, "Area", ha="center", fontsize=10)
    ax.text(-4.9, 4.3, "$x^2+y^2=16$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    save(fig, "q12.svg")


# Q13: y = sin x, 0 to 3pi/2
def q13():
    fig, ax = axes((-0.3, 5.6), (-1.4, 1.5))
    t = np.linspace(0, 5.3, 400)
    ax.plot(t, np.sin(t), color=INK, lw=1.6)
    xs = np.linspace(0, 3 * np.pi / 2, 400)
    shade(ax, xs, np.sin(xs))
    ax.text(np.pi / 2, 0.4, "$A_1$", ha="center", fontsize=10)
    ax.text(4.3, -0.5, "$A_2$", ha="center", fontsize=10)
    vline(ax, 3 * np.pi / 2, -1, 0)
    ax.set_xticks([np.pi / 2, np.pi, 3 * np.pi / 2])
    ax.set_xticklabels([r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$"], fontsize=11)
    ax.set_yticks([-1, 1])
    ax.text(1.6, 1.12, r"$y=\sin x$", fontsize=11)
    save(fig, "q13.svg")


# Q14: y = x^3, x = -2 to 1
def q14():
    fig, ax = axes((-2.6, 1.8), (-9, 3))
    t = np.linspace(-2.15, 1.4, 300)
    ax.plot(t, t ** 3, color=INK, lw=1.6)
    xs = np.linspace(-2, 1, 300)
    shade(ax, xs, xs ** 3)
    vline(ax, -2, -8, 0)
    vline(ax, 1, 0, 1)
    ax.text(-2, 0.4, "$x=-2$", ha="center", fontsize=10)
    ax.text(1.12, 0.3, "$x=1$", ha="left", fontsize=10)
    ax.text(-1.75, -3.0, "$A_1$", fontsize=10)
    ax.annotate("$A_2$", xy=(0.85, 0.2), xytext=(1.2, -2.2), fontsize=10,
                arrowprops=dict(arrowstyle="->", color=INK, lw=0.8))
    ax.text(0.5, 2.3, "$y=x^3$", fontsize=11)
    ax.set_xticks([-1]); ax.set_yticks([-8, -4])
    save(fig, "q14.svg")


# Q15: x-axis, y = x, x^2 + y^2 = 32 (first quadrant)
def q15():
    R = 4 * np.sqrt(2)
    fig, ax = axes((-1, 7.2), (-0.9, 6.6), h=4.3)
    ax.set_aspect("equal")
    th = np.linspace(0, np.pi / 2, 200)
    ax.plot(R * np.cos(th), R * np.sin(th), color=INK, lw=1.6)
    t = np.linspace(0, 6, 50)
    ax.plot(t, t, color=INK, lw=1.4)
    x1 = np.linspace(0, 4, 100)
    shade(ax, x1, x1)
    x2 = np.linspace(4, R, 200)
    shade(ax, x2, np.sqrt(np.clip(32 - x2 ** 2, 0, None)))
    vline(ax, 4, 0, 4)
    ax.plot([4], [4], "o", color=ACC, ms=4)
    ax.text(2.4, 4.3, "B(4,4)", fontsize=10, color=ACC)
    ax.text(3.75, -0.6, "M(4,0)", fontsize=10)
    ax.text(R - 0.2, -0.6, r"A$(4\sqrt{2},0)$", fontsize=10)
    ax.text(-0.5, -0.6, "O", fontsize=10)
    ax.text(5.6, 5.95, "$y=x$", fontsize=11)
    ax.text(0.4, 6.0, "$x^2+y^2=32$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    save(fig, "q15.svg")


# Q16: triangle A(1,0), B(2,2), C(3,1)
def q16():
    fig, ax = axes((-0.4, 3.9), (-0.5, 2.7))
    P = np.array([[1, 0], [2, 2], [3, 1], [1, 0]])
    ax.fill(P[:, 0], P[:, 1], color=FILL, alpha=0.45, lw=0)
    ax.plot(P[:, 0], P[:, 1], color=INK, lw=1.5)
    vline(ax, 2, 0, 2)
    vline(ax, 3, 0, 1)
    for (px, py, s, dx, dy) in [(1, 0, "A(1,0)", -0.15, -0.38), (2, 2, "B(2,2)", -0.25, 0.12), (3, 1, "C(3,1)", 0.08, 0.05)]:
        ax.plot([px], [py], "o", color=ACC, ms=4)
        ax.text(px + dx, py + dy, s, fontsize=10)
    ax.text(0.85, 1.2, "$y=2x-2$", fontsize=10)
    ax.text(2.6, 1.75, "$y=4-x$", fontsize=10)
    ax.text(2.05, 0.15, r"$y=\frac{x-1}{2}$", fontsize=10)
    ax.set_xticks([1, 2, 3]); ax.set_yticks([1, 2])
    save(fig, "q16.svg")


# Q17: y = 4x^2 and y = 8x + 12
def q17():
    fig, ax = axes((-2, 4), (-3, 42), h=3.6)
    t = np.linspace(-1.9, 3.3, 300)
    ax.plot(t, 4 * t ** 2, color=INK, lw=1.6)
    t2 = np.linspace(-1.9, 3.6, 50)
    ax.plot(t2, 8 * t2 + 12, color=INK, lw=1.4)
    xs = np.linspace(-1, 3, 300)
    ax.fill_between(xs, 4 * xs ** 2, 8 * xs + 12, color=FILL, alpha=0.45, lw=0)
    for (px, py, s, dx, dy) in [(-1, 4, "P(-1,4)", -0.95, 1.0), (3, 36, "Q(3,36)", -1.35, 1.0)]:
        ax.plot([px], [py], "o", color=ACC, ms=4)
        ax.text(px + dx, py + dy, s, fontsize=10, color=ACC)
    ax.text(3.15, 33, "$y=4x^2$", fontsize=11)
    ax.text(0.3, 28, "$y=8x+12$", fontsize=11)
    ax.text(1.0, 12, "Area", ha="center", fontsize=10)
    ax.set_xticks([-1, 1, 2, 3]); ax.set_yticks([12, 36])
    save(fig, "q17.svg")


# Q18: 4x^2 + y^2 = 36, i.e. x^2/9 + y^2/36 = 1
def q18():
    fig, ax = axes((-5, 5.5), (-7.2, 7.4), h=3.8)
    th = np.linspace(0, 2 * np.pi, 400)
    ax.fill(3 * np.cos(th), 6 * np.sin(th), color=FILL, alpha=0.45, lw=0)
    ellipse(ax, 3, 6)
    ax.text(3.1, 0.25, "(3,0)", fontsize=10)
    ax.text(-4.6, 0.25, "(-3,0)", fontsize=10)
    ax.text(0.15, 6.15, "(0,6)", fontsize=10)
    ax.text(0.15, -6.9, "(0,-6)", fontsize=10)
    ax.text(3.0, 4.5, "$4x^2+y^2=36$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    save(fig, "q18.svg")


# Q19: y^2 = 4ax and latus rectum x = a (drawn with a = 1)
def q19():
    fig, ax = axes((-0.5, 2.4), (-3.2, 3.4))
    t = np.linspace(-3, 3, 300)
    ax.plot(t ** 2 / 4, t, color=INK, lw=1.6)
    ys = np.linspace(-2, 2, 200)
    ax.fill_betweenx(ys, ys ** 2 / 4, 1, color=FILL, alpha=0.45, lw=0)
    ax.plot([1, 1], [-2, 2], color=ACC, lw=1.5)
    ax.plot([1, 1, 1], [2, 0, -2], "o", color=ACC, ms=4)
    ax.text(0.95, 2.15, "L(a, 2a)", ha="right", fontsize=10)
    ax.text(0.95, -2.45, "L'(a, -2a)", ha="right", fontsize=10)
    ax.text(1.06, 0.12, "S(a, 0)", fontsize=10)
    ax.text(-0.35, -0.35, "O", fontsize=10)
    ax.text(1.65, 2.9, "$y^2=4ax$", fontsize=11)
    ax.text(0.45, 0.9, "Area", ha="center", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    save(fig, "q19.svg")


# Q20: x^2/36 + y^2/16 = 1, first quadrant and the strip x = 0 to 3
def q20():
    fig, ax = axes((-7.5, 8.2), (-5, 5.6), h=3.6)
    ellipse(ax, 6, 4)
    xs = np.linspace(0, 6, 300)
    shade(ax, xs, (2 / 3) * np.sqrt(36 - xs ** 2))
    xs3 = np.linspace(0, 3, 200)
    ax.fill_between(xs3, (2 / 3) * np.sqrt(36 - xs3 ** 2), 0, color=ACC, alpha=0.25, lw=0)
    ax.plot([3, 3], [0, 2 * np.sqrt(3)], color=ACC, lw=1.2)
    ax.text(1.5, 1.6, "(iii)", ha="center", fontsize=10)
    ax.text(4.4, 0.8, "(ii)", ha="center", fontsize=10)
    ax.text(3.1, 2 * np.sqrt(3) + 0.15, r"$(3,2\sqrt{3})$", fontsize=10)
    ax.text(3.0, -0.75, "$x=3$", ha="center", fontsize=10)
    ax.text(6.1, 0.2, "(6,0)", fontsize=10)
    ax.text(0.15, 4.15, "(0,4)", fontsize=10)
    ax.text(-7.4, 4.6, r"$\frac{x^2}{36}+\frac{y^2}{16}=1$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    save(fig, "q20.svg")


if __name__ == "__main__":
    for f in (q07, q08, q09, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20):
        f()
    print("figures written to", HERE)
