"""Figures for Chapter 12 (Linear Programming), school worksheet.

Regenerate from the repo root:  python content/ch12/figs/make_figs.py
Each figure is drawn from the real constraint lines, to scale.
"""
import math
import os

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


def line_pts(a, b, c, X, Y):
    """End points of a*x + b*y = c inside the window [0, X] x [0, Y] (extended slightly)."""
    pts = []
    if b != 0:
        for xx in (-0.03 * X, X):
            pts.append((xx, (c - a * xx) / b))
    else:
        pts = [(c / a, -0.03 * Y), (c / a, Y)]
    return pts


def lpp_figure(name, X, Y, cons, corners, labels, line_labels, dashed=None, unbounded=False,
               xticks=None, yticks=None, size=(4.8, 4.0), region_label=None):
    fig, ax = plt.subplots(figsize=size)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    poly = [(0, 0), (X, 0), (X, Y), (0, Y)]
    for a, b, c, s in cons:
        poly = clip(poly, a, b, c, s)
    if poly:
        ax.fill([p[0] for p in poly], [p[1] for p in poly], color=SHADE, alpha=0.45, lw=0, zorder=1)

    lines = [(a, b, c, txt, at, side, INK) for (a, b, c, _s), (txt, at, side) in zip(cons, line_labels) if txt]
    for a, b, c, _s in cons:
        if (a, b, c) in ((1, 0, 0), (0, 1, 0)):
            continue
        (x1, y1), (x2, y2) = line_pts(a, b, c, X, Y)
        ax.plot([x1, x2], [y1, y2], color=INK, lw=1.3, zorder=2)

    if dashed:
        a, b, c, txt, at, side = dashed
        (x1, y1), (x2, y2) = line_pts(a, b, c, X, Y)
        ax.plot([x1, x2], [y1, y2], color=ACCENT, lw=1.3, ls="--", zorder=2)
        lines.append((a, b, c, txt, at, side, ACCENT))

    for (px, py), (txt, dx, dy, ha) in zip(corners, labels):
        ax.plot(px, py, "o", color=INK, ms=4.5, zorder=5)
        ax.annotate(txt, (px, py), xytext=(dx, dy), textcoords="offset points", ha=ha, va="center",
                    fontsize=9, zorder=6,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))

    if region_label:
        txt, pos = region_label
        ax.text(pos[0], pos[1], txt, ha="center", va="center", fontsize=9, style="italic", zorder=4)

    ax.set_xlim(-0.03 * X, X)
    ax.set_ylim(-0.03 * Y, Y)
    ax.axhline(0, color=INK, lw=1.0)
    ax.axvline(0, color=INK, lw=1.0)
    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$", rotation=0, labelpad=8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(labelsize=8.5)
    fig.tight_layout(pad=0.4)
    for a, b, c, txt, at, side, col in lines:
        px, py = (at, (c - a * at) / b) if b != 0 else (c / a, at)
        d0 = ax.transData.transform((px, py))
        d1 = ax.transData.transform((px + b, py - a)) if b != 0 else ax.transData.transform((px, py + 1))
        vx, vy = d1 - d0
        if vx < 0:
            vx, vy = -vx, -vy
        ang = math.degrees(math.atan2(vy, vx))
        nrm = math.hypot(vx, vy)
        nx, ny = -vy / nrm, vx / nrm
        ax.annotate(txt, (px, py), xytext=(side * 8 * nx, side * 8 * ny), textcoords="offset points",
                    rotation=ang, rotation_mode="anchor", ha="center", va="center", fontsize=9, color=col,
                    zorder=4)
    fig.savefig(os.path.join(OUT, name), format="svg", transparent=True)
    plt.close(fig)


# line_labels: (text, x-position along the line, side) ; side +1 = above the line, -1 = below
# Q2: 3x + y >= 3, 2x - y >= -5, x, y >= 0  -> unbounded, first quadrant
lpp_figure(
    "q02-sol.svg", 6, 12,
    [(3, 1, 3, ">="), (2, -1, -5, ">="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(1, 0), (0, 3), (0, 5)],
    labels=[("(1, 0)", 6, 9, "left"), ("(0, 3)", 7, 0, "left"), ("(0, 5)", 7, 0, "left")],
    line_labels=[("$3x+y=3$", 0.45, -1), ("$2x-y=-5$", 2.6, 1), ("", 0, 0), ("", 0, 0)],
    region_label=("unbounded region", (4.0, 5.0)),
    xticks=range(0, 7), yticks=range(0, 13, 2), size=(4.8, 3.8),
)

# Q5: min 600x + 400y ; x + y >= 8, x + 2y <= 16, 4x + y <= 29
lpp_figure(
    "q05-sol.svg", 10, 12,
    [(1, 1, 8, ">="), (1, 2, 16, "<="), (4, 1, 29, "<="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(0, 8), (6, 5), (7, 1)],
    labels=[("A(0, 8)", 7, 7, "left"), ("B(6, 5)", 7, 7, "left"), ("C(7, 1)", -8, -7, "right")],
    line_labels=[("$x+y=8$", 2.5, -1), ("$x+2y=16$", 8.8, 1), ("$4x+y=29$", 5.4, 1),
                 ("", 0, 0), ("", 0, 0)],
    xticks=range(0, 11, 2), yticks=range(0, 13, 2),
)

# Q6: min 3x + 5y ; x + 3y >= 3, x + y >= 2  (unbounded) ; dashed 3x + 5y = 7
lpp_figure(
    "q06-sol.svg", 5, 3.5,
    [(1, 3, 3, ">="), (1, 1, 2, ">="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(0, 2), (1.5, 0.5), (3, 0)],
    labels=[("A(0, 2)", 7, 4, "left"), ("B(3/2, 1/2)", 9, 8, "left"), ("C(3, 0)", 4, 10, "left")],
    line_labels=[("$x+3y=3$", 2.45, 1), ("$x+y=2$", 0.95, 1), ("", 0, 0), ("", 0, 0)],
    dashed=(3, 5, 7, "$3x+5y=7$", 0.6, -1),
    region_label=("unbounded region", (3.4, 2.4)),
    xticks=range(0, 6), yticks=[0, 1, 2, 3], size=(4.8, 3.6),
)

# Q7: max 5x + 3y ; 3x + 5y <= 15, 5x + 2y <= 10
lpp_figure(
    "q07-sol.svg", 5.5, 5.5,
    [(3, 5, 15, "<="), (5, 2, 10, "<="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(0, 0), (2, 0), (20 / 19, 45 / 19), (0, 3)],
    labels=[("O(0, 0)", 6, 9, "left"), ("A(2, 0)", 5, 9, "left"),
            ("B(20/19, 45/19)", 8, 8, "left"), ("C(0, 3)", 7, 7, "left")],
    line_labels=[("$3x+5y=15$", 4.2, 1), ("$5x+2y=10$", 0.4, 1), ("", 0, 0), ("", 0, 0)],
    xticks=range(0, 6), yticks=range(0, 6),
)

# Q8: Z = x + 2y ; x + 2y >= 100, 2x - y <= 0, 2x + y <= 200
lpp_figure(
    "q08-sol.svg", 110, 215,
    [(1, 2, 100, ">="), (2, -1, 0, "<="), (2, 1, 200, "<="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(0, 50), (20, 40), (50, 100), (0, 200)],
    labels=[("A(0, 50)", 7, 7, "left"), ("B(20, 40)", 0, -15, "left"),
            ("C(50, 100)", 9, 0, "left"), ("D(0, 200)", 7, 2, "left")],
    line_labels=[("$x+2y=100$", 75, 1), ("$2x-y=0$", 80, 1), ("$2x+y=200$", 85, 1),
                 ("", 0, 0), ("", 0, 0)],
    xticks=range(0, 111, 20), yticks=range(0, 201, 50),
)

# Q9: max 250x + 75y ; 5x + y <= 100, x + y <= 60
lpp_figure(
    "q09-sol.svg", 66, 106,
    [(5, 1, 100, "<="), (1, 1, 60, "<="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(0, 0), (20, 0), (10, 50), (0, 60)],
    labels=[("O(0, 0)", 6, 9, "left"), ("A(20, 0)", 5, 9, "left"),
            ("B(10, 50)", 8, 6, "left"), ("C(0, 60)", 7, 7, "left")],
    line_labels=[("$5x+y=100$", 14, 1), ("$x+y=60$", 40, 1), ("", 0, 0), ("", 0, 0)],
    xticks=range(0, 61, 10), yticks=range(0, 101, 20),
)

# Q10: min 50x + 70y ; 2x + y >= 8, x + 2y >= 10 (unbounded) ; dashed 50x + 70y = 380
lpp_figure(
    "q10-sol.svg", 12, 10,
    [(2, 1, 8, ">="), (1, 2, 10, ">="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(0, 8), (2, 4), (10, 0)],
    labels=[("A(0, 8)", 7, 4, "left"), ("B(2, 4)", 8, 6, "left"), ("C(10, 0)", 4, 10, "left")],
    line_labels=[("$2x+y=8$", 0.8, -1), ("$x+2y=10$", 7.0, -1), ("", 0, 0), ("", 0, 0)],
    dashed=(50, 70, 380, "$50x+70y=380$", 4.5, -1),
    region_label=("unbounded region", (8.0, 6.5)),
    xticks=range(0, 13, 2), yticks=range(0, 11, 2),
)

print("figures written to", OUT)
