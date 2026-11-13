"""Figures for Chapter 8 (Application of Integrals), Practice Set B.

Run from anywhere:  python make_figs_pb.py
Writes pb-qNN.svg next to this script. Style follows tools/CONTRACT.md:
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


def shade(ax, xs, y1, y2=0, color=FILL):
    ax.fill_between(xs, y1, y2, color=color, alpha=0.45, lw=0)


def dash(ax, xs, ys, color=INK):
    ax.plot(xs, ys, color=color, lw=0.9, ls="--")


def pt(ax, x0, y0, label, dx=0.1, dy=0.1, color=ACC, ha="left"):
    ax.plot([x0], [y0], "o", color=color, ms=4)
    ax.text(x0 + dx, y0 + dy, label, fontsize=10, color=color, ha=ha)


# Q7: x = y^2 and x = 4, cut into two equal parts by x = k
def q07():
    fig, ax = axes((-0.6, 5.4), (-2.8, 2.9))
    t = np.linspace(-2.4, 2.4, 300)
    ax.plot(t ** 2, t, color=INK, lw=1.6)
    ax.plot([4, 4], [-2.6, 2.6], color=INK, lw=1.2)
    k = 4 ** (2 / 3)
    xs = np.linspace(0, 4, 400)
    yy = np.sqrt(xs)
    ax.fill_between(xs, -yy, yy, color=FILL, alpha=0.45, lw=0)
    ax.plot([k, k], [-np.sqrt(k), np.sqrt(k)], color=ACC, lw=1.4)
    ax.text(k, -2.45, "$x=k$", color=ACC, ha="center", fontsize=10)
    ax.text(4.1, 2.3, "$x=4$", fontsize=10)
    ax.text(0.15, 2.3, "$x=y^2$", fontsize=11)
    ax.text(1.05, 0.25, "$A_1$", fontsize=10)
    ax.text(3.05, 0.25, "$A_2$", fontsize=10)
    pt(ax, 4, 2, "(4,2)", 0.1, -0.45, INK)
    pt(ax, 4, -2, "(4,-2)", 0.1, -0.3, INK)
    ax.set_xticks([]); ax.set_yticks([])
    save(fig, "pb-q07.svg")


# Q8: y^2 = 4ax (drawn with a = 1) between x = a and x = 4a
def q08():
    fig, ax = axes((-0.6, 5.6), (-4.9, 5.2))
    t = np.linspace(-4.6, 4.6, 300)
    ax.plot(t ** 2 / 4, t, color=INK, lw=1.6)
    xs = np.linspace(1, 4, 300)
    yy = 2 * np.sqrt(xs)
    ax.fill_between(xs, -yy, yy, color=FILL, alpha=0.45, lw=0)
    ax.plot([1, 1], [-2, 2], color=INK, lw=1.2)
    ax.plot([4, 4], [-4, 4], color=INK, lw=1.2)
    pt(ax, 1, 2, "(a, 2a)", -0.15, 0.3, ACC, "right")
    pt(ax, 4, 4, "(4a, 4a)", 0.12, 0.05)
    pt(ax, 1, -2, "(a, -2a)", -0.15, -0.55, ACC, "right")
    pt(ax, 4, -4, "(4a, -4a)", 0.12, -0.3)
    ax.text(1.05, -0.45, "$x=a$", fontsize=10)
    ax.text(4.05, 0.25, "$x=4a$", fontsize=10)
    ax.text(4.2, 2.6, "$y^2=4ax$", fontsize=11)
    ax.text(2.2, 0.9, "Area", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    save(fig, "pb-q08.svg")


# Q9: y^2 = 4x, y-axis, y = -2 and y = 4
def q09():
    fig, ax = axes((-0.8, 5.6), (-3.0, 5.0))
    t = np.linspace(-2.8, 4.6, 300)
    ax.plot(t ** 2 / 4, t, color=INK, lw=1.6)
    ys = np.linspace(-2, 4, 300)
    ax.fill_betweenx(ys, 0, ys ** 2 / 4, color=FILL, alpha=0.45, lw=0)
    dash(ax, [0, 5.0], [4, 4])
    dash(ax, [0, 3.0], [-2, -2])
    pt(ax, 4, 4, "(4,4)", -0.1, -0.55, INK, "right")
    pt(ax, 1, -2, "(1,-2)", 0.15, -0.15, INK)
    ax.text(0.15, 4.15, "$y=4$", fontsize=10)
    ax.text(3.05, -2.15, "$y=-2$", fontsize=10)
    ax.text(4.2, 3.0, "$y^2=4x$", fontsize=11)
    ax.set_xticks([1, 4]); ax.set_yticks([-2, 2, 4])
    save(fig, "pb-q09.svg")


# Q10: y = |x + 1| from x = -4 to x = 2
def q10():
    fig, ax = axes((-5.0, 3.0), (-0.8, 4.0))
    t = np.linspace(-4.6, 2.6, 300)
    ax.plot(t, np.abs(t + 1), color=INK, lw=1.6)
    xs = np.linspace(-4, 2, 300)
    shade(ax, xs, np.abs(xs + 1))
    dash(ax, [-4, -4], [0, 3])
    dash(ax, [2, 2], [0, 3])
    pt(ax, -1, 0, "(-1,0)", 0.0, -0.55, ACC, "center")
    pt(ax, -4, 3, "(-4,3)", 0.1, 0.1, INK)
    pt(ax, 2, 3, "(2,3)", 0.1, 0.1, INK)
    ax.text(-2.9, 0.55, "$A_1$", fontsize=10)
    ax.text(0.7, 0.55, "$A_2$", fontsize=10)
    ax.text(-4.9, 3.6, "$y=|x+1|$", fontsize=11)
    ax.set_xticks([-4, -1, 2]); ax.set_yticks([1, 2, 3])
    save(fig, "pb-q10.svg")


# Q11: x^2/4 + y^2/16 = 1, y-axis, y = 0 to y = 2 in the first quadrant
def q11():
    fig, ax = axes((-2.8, 3.6), (-4.6, 4.8), h=3.6)
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(2 * np.cos(th), 4 * np.sin(th), color=INK, lw=1.6)
    ys = np.linspace(0, 2, 200)
    ax.fill_betweenx(ys, 0, 0.5 * np.sqrt(16 - ys ** 2), color=FILL, alpha=0.45, lw=0)
    dash(ax, [0, 2.6], [2, 2])
    pt(ax, np.sqrt(3), 2, r"$(\sqrt{3},2)$", 0.1, 0.15)
    ax.text(2.05, -0.5, "(2,0)", fontsize=10)
    ax.text(0.12, 4.05, "(0,4)", fontsize=10)
    ax.text(2.65, 1.8, "$y=2$", fontsize=10)
    ax.text(-2.75, 4.2, r"$\frac{x^2}{4}+\frac{y^2}{16}=1$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    save(fig, "pb-q11.svg")


# Q12: y = sqrt(36 - x^2) from x = -3 to x = 3*sqrt(3)
def q12():
    fig, ax = axes((-7.4, 8.4), (-0.9, 7.4))
    th = np.linspace(0, np.pi, 400)
    ax.plot(6 * np.cos(th), 6 * np.sin(th), color=INK, lw=1.6)
    r3 = 3 * np.sqrt(3)
    xs = np.linspace(-3, r3, 400)
    shade(ax, xs, np.sqrt(36 - xs ** 2))
    dash(ax, [-3, -3], [0, r3])
    dash(ax, [r3, r3], [0, 3])
    pt(ax, -3, r3, r"$(-3,3\sqrt{3})$", -0.2, 0.3, ACC, "right")
    pt(ax, r3, 3, r"$(3\sqrt{3},3)$", 0.15, 0.2)
    ax.text(-3, -0.75, "$x=-3$", ha="center", fontsize=10)
    ax.text(r3, -0.75, r"$x=3\sqrt{3}$", ha="center", fontsize=10)
    ax.text(6.1, 0.2, "(6,0)", fontsize=10)
    ax.text(-7.3, 6.4, r"$y=\sqrt{36-x^2}$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    save(fig, "pb-q12.svg")


# Q13: y = sin 2x from pi/4 to 3pi/4
def q13():
    fig, ax = axes((-0.15, 3.4), (-1.35, 1.45))
    t = np.linspace(0, 3.2, 400)
    ax.plot(t, np.sin(2 * t), color=INK, lw=1.6)
    xs = np.linspace(np.pi / 4, 3 * np.pi / 4, 300)
    shade(ax, xs, np.sin(2 * xs))
    dash(ax, [np.pi / 4] * 2, [0, 1])
    dash(ax, [3 * np.pi / 4] * 2, [-1, 0])
    ax.text(1.05, 0.35, "$A_1$", fontsize=10)
    ax.text(1.85, -0.5, "$A_2$", fontsize=10)
    ax.set_xticks([np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])
    ax.set_xticklabels([r"$\frac{\pi}{4}$", r"$\frac{\pi}{2}$", r"$\frac{3\pi}{4}$", r"$\pi$"], fontsize=11)
    ax.set_yticks([-1, 1])
    ax.text(2.45, 0.75, r"$y=\sin 2x$", fontsize=11)
    save(fig, "pb-q13.svg")


# Q14: y = x^3, y = x + 6 and x = 0
def q14():
    fig, ax = axes((-1.6, 3.2), (-2.0, 10.5))
    t = np.linspace(-1.2, 2.2, 300)
    ax.plot(t, t ** 3, color=INK, lw=1.6)
    s = np.linspace(-1.4, 2.9, 50)
    ax.plot(s, s + 6, color=INK, lw=1.3)
    xs = np.linspace(0, 2, 300)
    ax.fill_between(xs, xs ** 3, xs + 6, color=FILL, alpha=0.45, lw=0)
    pt(ax, 2, 8, "(2,8)", 0.12, -0.6)
    pt(ax, 0, 6, "(0,6)", -0.12, 0.3, INK, "right")
    ax.text(2.25, 9.4, "$y=x+6$", fontsize=11)
    ax.text(2.25, 5.0, "$y=x^3$", fontsize=11)
    ax.text(-0.35, -0.9, "O", fontsize=10)
    ax.set_xticks([1, 2]); ax.set_yticks([2, 4, 6, 8])
    save(fig, "pb-q14.svg")


# Q15: |x| <= y <= sqrt(8 - x^2)
def q15():
    fig, ax = axes((-3.6, 3.9), (-0.7, 3.4))
    th = np.linspace(0, np.pi, 400)
    R = 2 * np.sqrt(2)
    ax.plot(R * np.cos(th), R * np.sin(th), color=INK, lw=1.6)
    s = np.linspace(-3.0, 3.0, 50)
    ax.plot(s, np.abs(s), color=INK, lw=1.3)
    xs = np.linspace(-2, 2, 400)
    ax.fill_between(xs, np.abs(xs), np.sqrt(8 - xs ** 2), color=FILL, alpha=0.45, lw=0)
    pt(ax, 2, 2, "B(2,2)", 0.12, 0.05)
    pt(ax, -2, 2, "A(-2,2)", -0.12, 0.05, ACC, "right")
    ax.text(0.08, R + 0.12, r"$(0,2\sqrt{2})$", fontsize=10)
    ax.text(2.7, 2.95, "$y=x$", fontsize=11)
    ax.text(-3.55, 2.95, "$y=-x$", fontsize=11)
    ax.text(1.75, 0.6, "$x^2+y^2=8$", fontsize=10)
    ax.text(-0.35, -0.5, "O", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    save(fig, "pb-q15.svg")


# Q16: triangle formed by x + 2y = 2, y - x = 1, 2x + y = 7
def q16():
    fig, ax = axes((-1.2, 5.6), (-1.9, 4.2))
    P = np.array([[0, 1], [2, 3], [4, -1], [0, 1]])
    ax.fill(P[:, 0], P[:, 1], color=FILL, alpha=0.45, lw=0)
    ax.plot(P[:, 0], P[:, 1], color=INK, lw=1.5)
    dash(ax, [2, 2], [0, 3])
    pt(ax, 0, 1, "A(0,1)", -0.12, 0.15, ACC, "right")
    pt(ax, 2, 3, "B(2,3)", 0.1, 0.12)
    pt(ax, 4, -1, "C(4,-1)", 0.12, -0.2)
    ax.text(0.15, 2.4, "$y-x=1$", fontsize=10)
    ax.text(3.15, 1.55, "$2x+y=7$", fontsize=10)
    ax.text(2.6, -1.0, "$x+2y=2$", fontsize=10)
    ax.set_xticks([1, 2, 3, 4]); ax.set_yticks([-1, 1, 2, 3])
    save(fig, "pb-q16.svg")


# Q17: y^2 = 2x and x - y = 4
def q17():
    fig, ax = axes((-1.0, 10.6), (-3.2, 5.4))
    t = np.linspace(-2.9, 4.6, 300)
    ax.plot(t ** 2 / 2, t, color=INK, lw=1.6)
    s = np.linspace(0.8, 9.6, 50)
    ax.plot(s, s - 4, color=INK, lw=1.3)
    ys = np.linspace(-2, 4, 300)
    ax.fill_betweenx(ys, ys ** 2 / 2, ys + 4, color=FILL, alpha=0.45, lw=0)
    pt(ax, 8, 4, "B(8,4)", -0.2, 0.3, ACC, "right")
    pt(ax, 2, -2, "A(2,-2)", -0.2, -0.75, ACC, "right")
    ax.text(9.0, 4.75, "$y^2=2x$", fontsize=11)
    ax.text(8.0, 2.2, "$x-y=4$", fontsize=11)
    ax.text(-0.6, -0.6, "O", fontsize=10)
    ax.set_xticks([2, 4, 6, 8]); ax.set_yticks([-2, 2, 4])
    save(fig, "pb-q17.svg")


# Q18: x^2/a^2 + y^2/b^2 = 1 (drawn with a = 3, b = 2)
def q18():
    fig, ax = axes((-4.2, 4.6), (-2.8, 3.0))
    th = np.linspace(0, 2 * np.pi, 400)
    ax.fill(3 * np.cos(th), 2 * np.sin(th), color=FILL, alpha=0.25, lw=0)
    xs = np.linspace(0, 3, 300)
    shade(ax, xs, (2 / 3) * np.sqrt(9 - xs ** 2))
    ax.plot(3 * np.cos(th), 2 * np.sin(th), color=INK, lw=1.6)
    ax.text(3.05, 0.15, "A(a,0)", fontsize=10)
    ax.text(-4.15, 0.15, "(-a,0)", fontsize=10)
    ax.text(0.1, 2.12, "B(0,b)", fontsize=10)
    ax.text(0.1, -2.45, "(0,-b)", fontsize=10)
    ax.text(0.9, 0.6, "OAB", fontsize=10)
    ax.text(2.2, 2.0, r"$\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    save(fig, "pb-q18.svg")


# Q19: x^2 = 4y and x = 4y - 2
def q19():
    fig, ax = axes((-2.4, 3.2), (-0.4, 2.2))
    t = np.linspace(-2.2, 2.8, 300)
    ax.plot(t, t ** 2 / 4, color=INK, lw=1.6)
    s = np.linspace(-2.2, 3.0, 50)
    ax.plot(s, (s + 2) / 4, color=INK, lw=1.3)
    xs = np.linspace(-1, 2, 300)
    ax.fill_between(xs, xs ** 2 / 4, (xs + 2) / 4, color=FILL, alpha=0.45, lw=0)
    pt(ax, -1, 0.25, r"$A(-1,\frac{1}{4})$", -0.15, 0.3, ACC, "right")
    pt(ax, 2, 1, "B(2,1)", 0.1, -0.2)
    ax.text(2.2, 1.85, "$x^2=4y$", fontsize=11)
    ax.text(2.25, 1.15, "$x=4y-2$", fontsize=11)
    ax.text(-0.2, -0.3, "O", fontsize=10)
    ax.set_xticks([-1, 1, 2]); ax.set_yticks([1])
    ax.set_aspect("equal")
    save(fig, "pb-q19.svg")


# Q20: lawn x^2/100 + y^2/64 = 1, pool x^2 + y^2 = 16, path x/10 + y/8 = 1
def q20():
    fig, ax = axes((-12.5, 14.0), (-9.6, 10.4), h=3.8)
    th = np.linspace(0, 2 * np.pi, 400)
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch
    outer = np.column_stack([10 * np.cos(th), 8 * np.sin(th)])
    inner = np.column_stack([4 * np.cos(th[::-1]), 4 * np.sin(th[::-1])])
    verts = np.vstack([outer, inner])
    codes = ([Path.MOVETO] + [Path.LINETO] * (len(outer) - 1)
             + [Path.MOVETO] + [Path.LINETO] * (len(inner) - 1))
    ax.add_patch(PathPatch(Path(verts, codes), color=FILL, alpha=0.45, lw=0))
    ax.plot(10 * np.cos(th), 8 * np.sin(th), color=INK, lw=1.6)
    ax.plot(4 * np.cos(th), 4 * np.sin(th), color=INK, lw=1.3)
    xs = np.linspace(0, 10, 300)
    ax.fill_between(xs, 8 - 0.8 * xs, 0.8 * np.sqrt(100 - xs ** 2), color=ACC, alpha=0.30, lw=0)
    ax.plot([10, 0], [0, 8], color=ACC, lw=1.4)
    ax.text(10.2, 0.4, "(10,0)", fontsize=10)
    ax.text(0.3, 8.4, "(0,8)", fontsize=10)
    ax.text(4.1, -1.3, "(4,0)", fontsize=10)
    ax.text(-1.6, 1.0, "pool", fontsize=10)
    ax.text(-8.6, -2.8, "lawn", fontsize=10)
    ax.text(5.2, 4.9, "path", fontsize=10, color=ACC)
    ax.text(-12.4, 8.8, r"$\frac{x^2}{100}+\frac{y^2}{64}=1$", fontsize=11)
    ax.text(-12.4, -9.2, "$x^2+y^2=16$", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    save(fig, "pb-q20.svg")


if __name__ == "__main__":
    for f in (q07, q08, q09, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20):
        f()
    print("figures written to", HERE)
