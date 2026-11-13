"""Figures for Chapter 8 (Application of Integrals), Practice Set A.

Run from anywhere:  python make_figs_pa.py
Writes pa-qNN.svg next to this script. Style follows tools/CONTRACT.md:
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


def axes(xlim, ylim, h=3.2):
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
    ax.tick_params(labelsize=9, length=3)
    return fig, ax


def save(fig, name):
    fig.tight_layout(pad=0.4)
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def shade(ax, xs, y1, y2=0):
    ax.fill_between(xs, y1, y2, color=FILL, alpha=0.45, lw=0)


def dash(ax, xs, ys):
    ax.plot(xs, ys, color=INK, lw=0.9, ls="--")


def pt(ax, x0, y0, label, dx=0.1, dy=0.1, color=ACC, ha="left"):
    ax.plot([x0], [y0], "o", color=color, ms=4)
    ax.text(x0 + dx, y0 + dy, label, fontsize=10, color=color, ha=ha)


# Q7: x^2 = y, y-axis, y = 4 (first quadrant), as in SQP 2025-26 Q23B
def q07():
    fig, ax = axes((-3, 3.2), (-0.6, 5.2))
    t = np.linspace(-2.25, 2.25, 300)
    ax.plot(t, t ** 2, color=INK, lw=1.6)
    ax.plot([-2.8, 3.0], [4, 4], color=INK, lw=1.2)
    ys = np.linspace(0, 4, 200)
    ax.fill_betweenx(ys, 0, np.sqrt(ys), color=FILL, alpha=0.45, lw=0)
    ax.text(-2.75, 4.5, "$x^2=y$", fontsize=11)
    ax.text(2.25, 4.15, "$y=4$", fontsize=11)
    pt(ax, 2, 4, "B(2,4)", 0.08, -0.55, INK)
    pt(ax, 0, 4, "N", -0.3, 0.15, INK)
    ax.text(-0.3, -0.45, "O", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    save(fig, "pa-q07.svg")


# Q8: y = x^2 from x = -1 to x = 2
def q08():
    fig, ax = axes((-1.8, 2.8), (-0.6, 5.2))
    t = np.linspace(-1.6, 2.25, 300)
    ax.plot(t, t ** 2, color=INK, lw=1.6)
    xs = np.linspace(-1, 2, 300)
    shade(ax, xs, xs ** 2)
    dash(ax, [-1, -1], [0, 1])
    dash(ax, [2, 2], [0, 4])
    ax.text(-1, -0.5, "$x=-1$", ha="center", fontsize=10)
    ax.text(2, 4.15, "$x=2$", ha="center", fontsize=10)
    ax.text(2.1, 4.8, "$y=x^2$", fontsize=11)
    ax.text(-0.75, 0.15, "$A_1$", fontsize=10)
    ax.text(1.25, 0.6, "$A_2$", fontsize=10)
    ax.set_xticks([1, 2]); ax.set_yticks([1, 4])
    save(fig, "pa-q08.svg")


# Q9: 2x + y = 8, y = 2, y = 4, y-axis
def q09():
    fig, ax = axes((-0.6, 5.2), (-0.6, 9.0))
    t = np.linspace(0, 4.4, 50)
    ax.plot(t, 8 - 2 * t, color=INK, lw=1.6)
    ys = np.linspace(2, 4, 100)
    ax.fill_betweenx(ys, 0, (8 - ys) / 2, color=FILL, alpha=0.45, lw=0)
    dash(ax, [0, 4.8], [2, 2])
    dash(ax, [0, 4.8], [4, 4])
    ax.text(4.6, 2.2, "$y=2$", fontsize=10)
    ax.text(4.6, 4.2, "$y=4$", fontsize=10)
    pt(ax, 3, 2, "(3,2)", 0.12, -0.75)
    pt(ax, 2, 4, "(2,4)", 0.12, 0.2)
    ax.text(0.6, 7.4, "$2x+y=8$", fontsize=11)
    ax.text(1.0, 2.8, "Area", ha="center", fontsize=10)
    ax.set_xticks([2, 3, 4]); ax.set_yticks([2, 4, 8])
    save(fig, "pa-q09.svg")


# Q10: y = 4 - 2x from x = -1 to x = 3
def q10():
    fig, ax = axes((-1.8, 3.8), (-3.2, 7.4))
    t = np.linspace(-1.4, 3.4, 50)
    ax.plot(t, 4 - 2 * t, color=INK, lw=1.6)
    xs = np.linspace(-1, 3, 300)
    shade(ax, xs, 4 - 2 * xs)
    dash(ax, [-1, -1], [0, 6])
    dash(ax, [3, 3], [-2, 0])
    ax.text(-1, 6.2, "$x=-1$", ha="center", fontsize=10)
    ax.text(3, 0.3, "$x=3$", ha="center", fontsize=10)
    pt(ax, 2, 0, "(2,0)", 0.1, 0.3)
    ax.text(0.2, 6.2, "$y=4-2x$", fontsize=11)
    ax.text(0.4, 1.4, "$A_1$", fontsize=10)
    ax.text(2.45, -0.8, "$A_2$", fontsize=10)
    ax.set_xticks([-1, 1, 3]); ax.set_yticks([-2, 2, 4, 6])
    save(fig, "pa-q10.svg")


# Q11: upper half of x^2/4 + y^2/9 = 1
def q11():
    fig, ax = axes((-3.2, 3.6), (-3.6, 4.0))
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(2 * np.cos(th), 3 * np.sin(th), color=INK, lw=1.0, ls=":")
    xs = np.linspace(-2, 2, 300)
    ax.plot(xs, 1.5 * np.sqrt(4 - xs ** 2), color=INK, lw=1.6)
    shade(ax, xs, 1.5 * np.sqrt(4 - xs ** 2))
    ax.text(2.05, 0.15, "(2,0)", fontsize=10)
    ax.text(-2.9, 0.15, "(-2,0)", fontsize=10)
    ax.text(0.1, 3.1, "(0,3)", fontsize=10)
    ax.text(1.2, 2.9, r"$y=\frac{3}{2}\sqrt{4-x^2}$", fontsize=11)
    ax.text(-0.6, 1.0, "Area", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    save(fig, "pa-q11.svg")


# Q12: minor segment of x^2 + y^2 = 16 cut off by x = 2
def q12():
    fig, ax = axes((-5, 5.8), (-4.8, 5.0), h=3.6)
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(4 * np.cos(th), 4 * np.sin(th), color=INK, lw=1.6)
    r3 = 2 * np.sqrt(3)
    ax.plot([2, 2], [-4.6, 4.6], color=ACC, lw=1.3)
    xs = np.linspace(2, 4, 300)
    yy = np.sqrt(np.clip(16 - xs ** 2, 0, None))
    ax.fill_between(xs, -yy, yy, color=FILL, alpha=0.45, lw=0)
    pt(ax, 2, r3, r"$(2,2\sqrt{3})$", 0.12, 0.1)
    pt(ax, 2, -r3, r"$(2,-2\sqrt{3})$", 0.12, -0.55)
    ax.text(4.1, 0.15, "(4,0)", fontsize=10)
    ax.text(2.1, -4.7, "$x=2$", fontsize=10, color=ACC)
    ax.text(-4.9, 4.3, "$x^2+y^2=16$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    save(fig, "pa-q12.svg")


# Q13: y = 20 cos 2x from pi/6 to pi/3
def q13():
    fig, ax = axes((-0.15, 1.75), (-23, 25), h=3.4)
    t = np.linspace(0, 1.65, 400)
    ax.plot(t, 20 * np.cos(2 * t), color=INK, lw=1.6)
    xs = np.linspace(np.pi / 6, np.pi / 3, 300)
    shade(ax, xs, 20 * np.cos(2 * xs))
    dash(ax, [np.pi / 6] * 2, [0, 10])
    dash(ax, [np.pi / 3] * 2, [-10, 0])
    ax.text(0.62, 2.5, "$A_1$", fontsize=10)
    ax.text(0.92, -5.5, "$A_2$", fontsize=10)
    ax.set_xticks([np.pi / 6, np.pi / 4, np.pi / 3])
    ax.set_xticklabels([r"$\frac{\pi}{6}$", r"$\frac{\pi}{4}$", r"$\frac{\pi}{3}$"], fontsize=11)
    ax.set_yticks([-20, -10, 10, 20])
    ax.text(0.08, 21.5, r"$y=20\cos 2x$", fontsize=11)
    save(fig, "pa-q13.svg")


# Q14: y = x|x| from -1 to 1
def q14():
    fig, ax = axes((-1.7, 1.8), (-1.8, 1.9))
    t = np.linspace(-1.3, 1.3, 300)
    ax.plot(t, t * np.abs(t), color=INK, lw=1.6)
    xs = np.linspace(-1, 1, 300)
    shade(ax, xs, xs * np.abs(xs))
    dash(ax, [-1, -1], [-1, 0])
    dash(ax, [1, 1], [0, 1])
    ax.text(-1, 0.15, "$x=-1$", ha="center", fontsize=10)
    ax.text(1.06, 0.45, "$x=1$", ha="left", fontsize=10)
    ax.text(-0.75, -0.35, "$A_1$", fontsize=10)
    ax.text(0.6, 0.12, "$A_2$", fontsize=10)
    ax.text(0.95, 1.6, r"$y=x|x|$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([-1, 1])
    save(fig, "pa-q14.svg")


# Q15: 0 <= y <= sqrt(4 - x^2), x + y >= 2
def q15():
    fig, ax = axes((-2.7, 3.2), (-0.6, 2.9))
    th = np.linspace(0, np.pi, 300)
    ax.plot(2 * np.cos(th), 2 * np.sin(th), color=INK, lw=1.6)
    t = np.linspace(-0.3, 2.5, 50)
    ax.plot(t, 2 - t, color=INK, lw=1.3)
    xs = np.linspace(0, 2, 300)
    ax.fill_between(xs, 2 - xs, np.sqrt(np.clip(4 - xs ** 2, 0, None)), color=FILL, alpha=0.45, lw=0)
    pt(ax, 0, 2, "B(0,2)", 0.1, 0.12)
    pt(ax, 2, 0, "A(2,0)", 0.08, -0.4)
    ax.text(-2.6, 2.2, r"$y=\sqrt{4-x^2}$", fontsize=11)
    ax.text(1.9, 0.75, "$x+y=2$", fontsize=11)
    ax.text(-0.3, -0.45, "O", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    save(fig, "pa-q15.svg")


# Q16: triangle A(-1,0), B(1,3), C(3,2)
def q16():
    fig, ax = axes((-1.8, 4.0), (-0.6, 3.8))
    P = np.array([[-1, 0], [1, 3], [3, 2], [-1, 0]])
    ax.fill(P[:, 0], P[:, 1], color=FILL, alpha=0.45, lw=0)
    ax.plot(P[:, 0], P[:, 1], color=INK, lw=1.5)
    dash(ax, [1, 1], [0, 3])
    dash(ax, [3, 3], [0, 2])
    pt(ax, -1, 0, "A(-1,0)", -0.6, 0.2)
    pt(ax, 1, 3, "B(1,3)", -0.4, 0.15)
    pt(ax, 3, 2, "C(3,2)", 0.1, 0.1)
    ax.text(-1.45, 1.6, r"$y=\frac{3}{2}(x+1)$", fontsize=10)
    ax.text(2.1, 2.85, r"$y=\frac{7-x}{2}$", fontsize=10)
    ax.text(1.5, 0.75, r"$y=\frac{x+1}{2}$", fontsize=10)
    ax.set_xticks([-1, 1, 2, 3]); ax.set_yticks([1, 2, 3])
    save(fig, "pa-q16.svg")


# Q17: y^2 = 2x and x = 2y
def q17():
    fig, ax = axes((-1, 10.5), (-2.4, 5.4))
    t = np.linspace(-2.2, 4.8, 300)
    ax.plot(t ** 2 / 2, t, color=INK, lw=1.6)
    s = np.linspace(-1, 10, 50)
    ax.plot(s, s / 2, color=INK, lw=1.3)
    xs = np.linspace(0, 8, 300)
    ax.fill_between(xs, xs / 2, np.sqrt(2 * xs), color=FILL, alpha=0.45, lw=0)
    pt(ax, 8, 4, "P(8,4)", -1.6, 0.35)
    ax.text(-0.6, -0.6, "O", fontsize=10)
    ax.text(8.6, 3.5, "$x=2y$", fontsize=11)
    ax.text(9.2, 4.6, "$y^2=2x$", fontsize=11)
    ax.set_xticks([2, 4, 6, 8]); ax.set_yticks([2, 4])
    save(fig, "pa-q17.svg")


# Q18: 25x^2 + 16y^2 = 400, i.e. x^2/16 + y^2/25 = 1
def q18():
    fig, ax = axes((-6, 6.6), (-6.2, 6.4), h=3.8)
    th = np.linspace(0, 2 * np.pi, 400)
    ax.fill(4 * np.cos(th), 5 * np.sin(th), color=FILL, alpha=0.45, lw=0)
    ax.plot(4 * np.cos(th), 5 * np.sin(th), color=INK, lw=1.6)
    ax.text(4.1, 0.25, "(4,0)", fontsize=10)
    ax.text(-5.9, 0.25, "(-4,0)", fontsize=10)
    ax.text(0.15, 5.15, "(0,5)", fontsize=10)
    ax.text(0.15, -5.9, "(0,-5)", fontsize=10)
    ax.text(3.0, 4.2, "$25x^2+16y^2=400$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    save(fig, "pa-q18.svg")


# Q19: x^2 <= 4y and y <= x
def q19():
    fig, ax = axes((-1.6, 5.4), (-0.6, 5.8))
    t = np.linspace(-1.4, 4.7, 300)
    ax.plot(t, t ** 2 / 4, color=INK, lw=1.6)
    s = np.linspace(-0.5, 5.2, 50)
    ax.plot(s, s, color=INK, lw=1.3)
    xs = np.linspace(0, 4, 300)
    ax.fill_between(xs, xs ** 2 / 4, xs, color=FILL, alpha=0.45, lw=0)
    pt(ax, 4, 4, "P(4,4)", 0.15, -0.35)
    ax.text(-0.45, -0.5, "O", fontsize=10)
    ax.text(2.6, 0.7, "$x^2=4y$", fontsize=11)
    ax.text(4.75, 4.7, "$y=x$", fontsize=11)
    ax.set_xticks([2, 4]); ax.set_yticks([2, 4])
    save(fig, "pa-q19.svg")


# Q20: x^2 + y^2 = 100 with the band -5 <= x <= 5
def q20():
    fig, ax = axes((-12.5, 13.5), (-11.5, 12.2), h=3.8)
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(10 * np.cos(th), 10 * np.sin(th), color=INK, lw=1.6)
    xs = np.linspace(-5, 5, 300)
    yy = np.sqrt(100 - xs ** 2)
    ax.fill_between(xs, -yy, yy, color=FILL, alpha=0.45, lw=0)
    r = 5 * np.sqrt(3)
    ax.plot([-5, -5], [-r, r], color=ACC, lw=1.3)
    ax.plot([5, 5], [-r, r], color=ACC, lw=1.3)
    ax.text(5.3, r + 0.4, r"$(5,5\sqrt{3})$", fontsize=10)
    ax.text(5.2, -1.6, "$x=5$", fontsize=10, color=ACC)
    ax.text(-8.6, -1.6, "$x=-5$", fontsize=10, color=ACC)
    ax.text(10.2, 0.4, "(10,0)", fontsize=10)
    ax.text(-12.4, 10.6, "$x^2+y^2=100$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    save(fig, "pa-q20.svg")


if __name__ == "__main__":
    for f in (q07, q08, q09, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20):
        f()
    print("figures written to", HERE)
