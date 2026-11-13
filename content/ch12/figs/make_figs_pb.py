"""Figures for Chapter 12 (Linear Programming), Practice Set B.

Regenerate from the repo root:  python content/ch12/figs/make_figs_pb.py
Each figure is drawn from the real constraint lines, to scale.
Pass a folder as the first argument to also write PNG previews there.
"""
import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.edgecolor": "#1f2937",
    "axes.labelcolor": "#1f2937",
    "xtick.color": "#1f2937",
    "ytick.color": "#1f2937",
    "text.color": "#1f2937",
})

INK = "#1f2937"
SHADE = "#93c5fd"
ACCENT = "#ef4444"
OUT = os.path.dirname(os.path.abspath(__file__))
PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None
BOX = dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), format="svg", transparent=True)
    if PREVIEW:
        fig.savefig(os.path.join(PREVIEW, name.replace(".svg", ".png")), dpi=110, facecolor="white")
    plt.close(fig)


def clip(poly, a, b, c, sense):
    """Keep the part of polygon `poly` with a*x + b*y (sense) c, sense '<=' or '>='."""
    s = 1 if sense == "<=" else -1
    f = lambda p: s * (a * p[0] + b * p[1] - c)  # inside when <= 0
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp, fq = f(p), f(q)
        if fp <= 1e-12:
            out.append(p)
        if (fp < -1e-12 and fq > 1e-12) or (fp > 1e-12 and fq < -1e-12):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def line_pts(a, b, c, xlo, xhi, ylo, yhi):
    """End points of a*x + b*y = c across the window."""
    if b != 0:
        return [(xlo, (c - a * xlo) / b), (xhi, (c - a * xhi) / b)]
    return [(c / a, ylo), (c / a, yhi)]


def angle(ax, a, b):
    """On-screen angle (degrees) of the line a*x + b*y = c."""
    if b == 0:
        return 90
    p0 = ax.transData.transform((0, 0))
    p1 = ax.transData.transform((1, -a / b))
    ang = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    return ang


def setup(size, xlo, xhi, ylo, yhi, xticks=None, yticks=None):
    fig, ax = plt.subplots(figsize=size)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    ax.set_xlim(xlo, xhi)
    ax.set_ylim(ylo, yhi)
    ax.axhline(0, color=INK, lw=1.0)
    ax.axvline(0, color=INK, lw=1.0)
    if xticks is not None:
        ax.set_xticks(list(xticks))
    if yticks is not None:
        ax.set_yticks(list(yticks))
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$", rotation=0, labelpad=8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(labelsize=8.5)
    fig.tight_layout(pad=0.4)
    return fig, ax


def draw_line(ax, a, b, c, label, pos, color=INK, ls="-"):
    xlo, xhi = ax.get_xlim()
    ylo, yhi = ax.get_ylim()
    (x1, y1), (x2, y2) = line_pts(a, b, c, xlo, xhi, ylo, yhi)
    ax.plot([x1, x2], [y1, y2], color=color, lw=1.3, ls=ls, zorder=2)
    if label:
        ax.text(pos[0], pos[1], label, rotation=angle(ax, a, b), ha="center",
                va="center", fontsize=9, color=color, bbox=BOX, zorder=4)


def shade(ax, cons, color=SHADE, alpha=0.45):
    xlo, xhi = ax.get_xlim()
    ylo, yhi = ax.get_ylim()
    poly = [(max(xlo, 0), max(ylo, 0)), (xhi, max(ylo, 0)), (xhi, yhi), (max(xlo, 0), yhi)]
    for a, b, c, s in cons:
        poly = clip(poly, a, b, c, s)
    if poly:
        ax.fill([p[0] for p in poly], [p[1] for p in poly], color=color, alpha=alpha, lw=0, zorder=1)


def points(ax, pts, color=INK):
    for (px, py), (txt, dx, dy, ha) in pts:
        ax.plot(px, py, "o", color=color, ms=4.5, zorder=5)
        ax.annotate(txt, (px, py), xytext=(dx, dy), textcoords="offset points", ha=ha, va="center",
                    fontsize=9, color=color, zorder=6,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))


# ---------------------------------------------------------------- Q1 (question figure)
# Exemplar Fig 12.12: corners (0,0), (5,0), (6,5), (6,8), (4,10), (0,8)
fig, ax = setup((4.4, 4.0), -0.4, 8, -0.6, 11.5, range(0, 9, 2), range(0, 12, 2))
poly = [(0, 0), (5, 0), (6, 5), (6, 8), (4, 10), (0, 8)]
ax.fill([p[0] for p in poly], [p[1] for p in poly], color=SHADE, alpha=0.45, lw=0, zorder=1)
ax.plot([p[0] for p in poly + poly[:1]], [p[1] for p in poly + poly[:1]], color=INK, lw=1.3, zorder=2)
points(ax, [((0, 0), ("(0, 0)", 6, 9, "left")), ((5, 0), ("(5, 0)", 6, 8, "left")),
            ((6, 5), ("(6, 5)", 7, 0, "left")), ((6, 8), ("(6, 8)", 7, 3, "left")),
            ((4, 10), ("(4, 10)", 0, 10, "center")), ((0, 8), ("(0, 8)", 7, 9, "left"))])
save(fig, "pb-q01.svg")

# ---------------------------------------------------------------- Q2 (question figure)
# CBSE SQP 2023-24 Q11: region x + y >= 2, x + 2y <= 10, x - y <= 1, x >= 0
fig, ax = setup((4.8, 3.7), -0.6, 11, -1.3, 6.4, range(0, 11, 2), range(0, 7, 1))
shade(ax, [(1, 1, 2, ">="), (1, 2, 10, "<="), (1, -1, 1, "<="), (1, 0, 0, ">=")])
draw_line(ax, 1, 1, 2, "$x+y=2$", (3.0, -1.0))
draw_line(ax, 1, 2, 10, "$x+2y=10$", (7.5, 1.25))
draw_line(ax, 1, -1, 1, "$x-y=1$", (5.8, 4.8))
points(ax, [((0, 5), ("(0, 5)", 7, 6, "left")), ((0, 2), ("(0, 2)", -6, 0, "right")),
            ((1, 0), ("(1, 0)", 2, -10, "left")), ((2, 0), ("(2, 0)", 6, 8, "left")),
            ((10, 0), ("(10, 0)", -2, 9, "right"))])
save(fig, "pb-q02.svg")

# ---------------------------------------------------------------- Q4 (solution figure)
# x - y <= -1 (y >= x + 1) and -x + y <= 0 (y <= x): no common region
fig, ax = setup((4.4, 3.6), -0.3, 5, -0.3, 5, range(0, 6), range(0, 6))
shade(ax, [(1, -1, -1, "<=")], color=SHADE)
shade(ax, [(-1, 1, 0, "<=")], color=ACCENT, alpha=0.18)
draw_line(ax, 1, -1, -1, "$x-y=-1$", (1.6, 2.6))
draw_line(ax, -1, 1, 0, "$y=x$", (4.2, 4.2))
ax.text(1.0, 4.0, "$y \\geq x+1$", ha="center", fontsize=9, style="italic", zorder=4, bbox=BOX)
ax.text(3.9, 1.4, "$y \\leq x$", ha="center", fontsize=9, style="italic", zorder=4, bbox=BOX)
ax.text(2.75, 3.25, "no common region", rotation=angle(ax, -1, 1), ha="center", va="center", fontsize=8.5, color=ACCENT, zorder=4)
save(fig, "pb-q04-sol.svg")

# ---------------------------------------------------------------- Q5
# min 13x - 15y ; x + y <= 7, 2x - 3y + 6 >= 0
fig, ax = setup((4.8, 3.9), -0.3, 8.5, -0.3, 7.5, range(0, 9), range(0, 8))
shade(ax, [(1, 1, 7, "<="), (2, -3, -6, ">=")])
draw_line(ax, 1, 1, 7, "$x+y=7$", (5.5, 1.5))
draw_line(ax, 2, -3, -6, "$2x-3y+6=0$", (6.3, 6.2))
points(ax, [((0, 0), ("O(0, 0)", 6, 9, "left")), ((7, 0), ("A(7, 0)", 5, 9, "left")),
            ((3, 4), ("B(3, 4)", 8, 2, "left")), ((0, 2), ("C(0, 2)", 7, -8, "left"))])
save(fig, "pb-q05-sol.svg")

# ---------------------------------------------------------------- Q6
# max -x + 2y ; x >= 3, x + y >= 5, x + 2y >= 6 (unbounded) ; dashed -x + 2y = 1
fig, ax = setup((4.8, 3.7), -0.3, 9, -0.3, 6, range(0, 10), range(0, 7))
shade(ax, [(1, 0, 3, ">="), (1, 1, 5, ">="), (1, 2, 6, ">=")])
draw_line(ax, 1, 0, 3, "$x=3$", (3.0, 5.3))
draw_line(ax, 1, 1, 5, "$x+y=5$", (1.2, 3.8))
draw_line(ax, 1, 2, 6, "$x+2y=6$", (1.0, 2.5))
draw_line(ax, -1, 2, 1, "$-x+2y=1$", (7.6, 4.3), color=ACCENT, ls="--")
points(ax, [((3, 2), ("A(3, 2)", -7, 0, "right")), ((4, 1), ("B(4, 1)", -7, -6, "right")),
            ((6, 0), ("C(6, 0)", 4, 9, "left"))])
points(ax, [((3, 3), ("(3, 3): Z = 3", 7, 6, "left"))], color=ACCENT)
ax.text(5.9, 2.9, "unbounded region", ha="center", fontsize=9, style="italic", zorder=4)
save(fig, "pb-q06-sol.svg")

# ---------------------------------------------------------------- Q7
# max x + y ; x + 4y <= 8, 2x + 3y <= 12, 3x + y <= 9
fig, ax = setup((4.8, 3.6), -0.2, 7, -0.2, 4.6, range(0, 8), range(0, 5))
shade(ax, [(1, 4, 8, "<="), (2, 3, 12, "<="), (3, 1, 9, "<=")])
draw_line(ax, 1, 4, 8, "$x+4y=8$", (6.0, 0.5))
draw_line(ax, 2, 3, 12, "$2x+3y=12$", (4.2, 1.2))
draw_line(ax, 3, 1, 9, "$3x+y=9$", (1.75, 3.75))
points(ax, [((0, 0), ("O(0, 0)", 6, 9, "left")), ((3, 0), ("A(3, 0)", 6, 9, "left")),
            ((28 / 11, 15 / 11), ("B$\\left(\\frac{28}{11}, \\frac{15}{11}\\right)$", 8, 6, "left")),
            ((0, 2), ("C(0, 2)", 6, 9, "left"))])
save(fig, "pb-q07-sol.svg")

# ---------------------------------------------------------------- Q8
# Z = 3x - 4y ; x - 2y <= 0, -3x + y <= 4, x - y <= 6 (unbounded) ; dashed 3x - 4y = 12
fig, ax = setup((4.8, 4.2), -0.6, 22, -0.6, 19, range(0, 23, 4), range(0, 20, 4))
c8 = [(1, -2, 0, "<="), (-3, 1, 4, "<="), (1, -1, 6, "<=")]
shade(ax, c8)
draw_line(ax, 1, -2, 0, "$x-2y=0$", (19.0, 9.5))
draw_line(ax, -3, 1, 4, "$-3x+y=4$", (4.0, 16.0))
draw_line(ax, 1, -1, 6, "$x-y=6$", (19.0, 13.0))
draw_line(ax, 3, -4, 12, "$3x-4y=12$", (6.0, 1.5), color=ACCENT, ls="--")
points(ax, [((0, 0), ("O(0, 0)", 6, 9, "left")), ((12, 6), ("B(12, 6)", -8, 6, "right")),
            ((0, 4), ("A(0, 4)", 7, 0, "left"))])
points(ax, [((2, 10), ("(2, 10): Z = -34", 8, 0, "left"))], color=ACCENT)
ax.text(10.5, 14.5, "unbounded region", ha="center", fontsize=9, style="italic", zorder=4)
save(fig, "pb-q08-sol.svg")

# ---------------------------------------------------------------- Q9
# max 200x + 120y ; 3x + y <= 600, x + y <= 300, -x + y <= 100
fig, ax = setup((4.8, 4.0), -8, 320, -8, 330, range(0, 321, 50), range(0, 331, 50))
shade(ax, [(3, 1, 600, "<="), (1, 1, 300, "<="), (-1, 1, 100, "<=")])
draw_line(ax, 3, 1, 600, "$3x+y=600$", (185, 45))
draw_line(ax, 1, 1, 300, "$x+y=300$", (255, 45))
draw_line(ax, -1, 1, 100, "$y-x=100$", (180, 280))
points(ax, [((0, 0), ("O(0, 0)", 6, 9, "left")), ((200, 0), ("A(200, 0)", -6, 9, "right")),
            ((150, 150), ("B(150, 150)", 8, 4, "left")), ((100, 200), ("C(100, 200)", 8, 4, "left")),
            ((0, 100), ("D(0, 100)", 7, -8, "left"))])
save(fig, "pb-q09-sol.svg")

# ---------------------------------------------------------------- Q10
# min 12000x + 15000y ; 5x + 4y >= 640, 5x + 2y >= 400, 3x + 4y >= 480 (unbounded)
fig, ax = setup((4.8, 4.2), -4, 192, -4, 220, range(0, 181, 40), range(0, 221, 40))
shade(ax, [(5, 4, 640, ">="), (5, 2, 400, ">="), (3, 4, 480, ">=")])
draw_line(ax, 5, 4, 640, "$5x+4y=640$", (16, 140))
draw_line(ax, 5, 2, 400, "$5x+2y=400$", (55, 62.5))
draw_line(ax, 3, 4, 480, "$3x+4y=480$", (128, 24))
draw_line(ax, 4, 5, 620, "", (0, 0), color=ACCENT, ls="--")
ax.annotate("$12000x+15000y=1860000$", (40, 92), xytext=(2, 28), textcoords="data", ha="left", va="center",
            fontsize=8.5, color=ACCENT, bbox=BOX, zorder=6, arrowprops=dict(arrowstyle="->", color=ACCENT, lw=0.9))
points(ax, [((0, 200), ("A(0, 200)", 7, 4, "left")), ((32, 120), ("B(32, 120)", 8, 4, "left")),
            ((80, 60), ("C(80, 60)", 8, 6, "left")), ((160, 0), ("D(160, 0)", 4, 9, "left"))])
ax.text(140, 175, "unbounded region", ha="center", fontsize=9, style="italic", zorder=4)
save(fig, "pb-q10-sol.svg")

print("figures written to", OUT)
