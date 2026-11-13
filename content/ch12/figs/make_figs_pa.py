"""Figures for Chapter 12 (Linear Programming), Practice Set A.

Regenerate from the repo root:  python content/ch12/figs/make_figs_pa.py
Each figure is drawn from the real constraint lines, to scale.
Pass a folder as the first argument to also write PNG previews there.
"""
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


def line_pts(a, b, c, X, Y, x0=None):
    """End points of a*x + b*y = c across the window (extended slightly)."""
    x0 = -0.03 * X if x0 is None else x0
    if b != 0:
        return [(x0, (c - a * x0) / b), (X, (c - a * X) / b)]
    return [(c / a, -0.03 * Y), (c / a, Y)]


def lpp_figure(name, X, Y, cons, corners, labels, line_labels, dashed=None, segment=None,
               xticks=None, yticks=None, size=(4.8, 4.0), region_label=None):
    fig, ax = plt.subplots(figsize=size)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    poly = [(0, 0), (X, 0), (X, Y), (0, Y)]
    for a, b, c, s in cons:
        poly = clip(poly, a, b, c, s)
    if poly:
        ax.fill([p[0] for p in poly], [p[1] for p in poly], color=SHADE, alpha=0.45, lw=0, zorder=1)

    for (a, b, c, _s), (txt, pos, rot) in zip(cons, line_labels):
        if not txt:
            continue
        (x1, y1), (x2, y2) = line_pts(a, b, c, X, Y)
        ax.plot([x1, x2], [y1, y2], color=INK, lw=1.3, zorder=2)
        ax.text(pos[0], pos[1], txt, rotation=rot, ha="center", va="center", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85), zorder=4)

    if dashed:
        a, b, c, txt, pos, rot = dashed
        (x1, y1), (x2, y2) = line_pts(a, b, c, X, Y)
        ax.plot([x1, x2], [y1, y2], color=ACCENT, lw=1.3, ls="--", zorder=2)
        ax.text(pos[0], pos[1], txt, rotation=rot, ha="center", va="center", fontsize=9, color=ACCENT,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85), zorder=4)

    if segment:
        (sx1, sy1), (sx2, sy2) = segment
        ax.plot([sx1, sx2], [sy1, sy2], color=ACCENT, lw=3.0, zorder=3, solid_capstyle="round")

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
    save(fig, name)


# Q2: open half-plane 3x + 5y < 10 (contains the origin; boundary dashed, not included)
fig, ax = plt.subplots(figsize=(4.8, 3.6))
fig.patch.set_alpha(0)
ax.set_facecolor("none")
x0, x1, y0, y1 = -2, 5, -2, 4
poly = clip([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 3, 5, 10, "<=")
ax.fill([p[0] for p in poly], [p[1] for p in poly], color=SHADE, alpha=0.45, lw=0, zorder=1)
ax.plot([x0, x1], [(10 - 3 * x0) / 5, (10 - 3 * x1) / 5], color=INK, lw=1.3, ls="--", zorder=2)
ax.text(3.5, 1.5, "$3x+5y=10$\n(not included)", rotation=0, ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85), zorder=4)
for (px, py), txt, dx, dy in [((10 / 3, 0), "(10/3, 0)", 4, -10), ((0, 2), "(0, 2)", 6, 8)]:
    ax.plot(px, py, "o", color=INK, ms=4.5, zorder=5)
    ax.annotate(txt, (px, py), xytext=(dx, dy), textcoords="offset points", fontsize=9, zorder=6,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
ax.plot(0, 0, "o", color=ACCENT, ms=4.5, zorder=5)
ax.annotate("O(0, 0): 0 < 10 true", (0, 0), xytext=(-6, -12), textcoords="offset points", ha="right",
            fontsize=9, color=ACCENT, zorder=6,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
ax.text(1.4, -1.2, "$3x+5y<10$", ha="center", fontsize=9, style="italic", zorder=4)
ax.axhline(0, color=INK, lw=1.0)
ax.axvline(0, color=INK, lw=1.0)
ax.set_xlim(x0, x1)
ax.set_ylim(y0, y1)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$", rotation=0, labelpad=8)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.tick_params(labelsize=8.5)
fig.tight_layout(pad=0.4)
save(fig, "pa-q02-sol.svg")

# Q5: min 6x + 3y ; 4x + y >= 80, x + 5y >= 115, 3x + 2y <= 150
lpp_figure(
    "pa-q05-sol.svg", 55, 85,
    [(4, 1, 80, ">="), (1, 5, 115, ">="), (3, 2, 150, "<="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(15, 20), (40, 15), (2, 72)],
    labels=[("A(15, 20)", -8, -8, "right"), ("B(40, 15)", 8, 6, "left"), ("C(2, 72)", 8, 4, "left")],
    line_labels=[("$4x+y=80$", (7.5, 45), -76), ("$x+5y=115$", (48, 4.5), -12),
                 ("$3x+2y=150$", (34, 32), -60), ("", (0, 0), 0), ("", (0, 0), 0)],
    xticks=range(0, 56, 10), yticks=range(0, 81, 20),
)

# Q6: min x + 2y ; 2x + y >= 3, x + 2y >= 6 (unbounded) ; minimum on segment AB
lpp_figure(
    "pa-q06-sol.svg", 8, 5,
    [(2, 1, 3, ">="), (1, 2, 6, ">="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(0, 3), (6, 0)],
    labels=[("A(0, 3)", 7, 4, "left"), ("B(6, 0)", 4, 10, "left")],
    line_labels=[("$2x+y=3$", (1.25, 1.2), -55), ("$x+2y=6$", (3.3, 0.95), -24),
                 ("", (0, 0), 0), ("", (0, 0), 0)],
    segment=((0, 3), (6, 0)),
    region_label=("unbounded region", (5.6, 3.6)),
    xticks=range(0, 9), yticks=range(0, 6), size=(4.8, 3.6),
)

# Q7: max 2x + y ; x + y <= 1200, x + y >= 600, y <= x/2
lpp_figure(
    "pa-q07-sol.svg", 1300, 800,
    [(1, 1, 1200, "<="), (1, 1, 600, ">="), (-1, 2, 0, "<="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(600, 0), (1200, 0), (800, 400), (400, 200)],
    labels=[("A(600, 0)", -6, 10, "right"), ("B(1200, 0)", -4, 10, "right"),
            ("C(800, 400)", 8, 6, "left"), ("D(400, 200)", -8, 6, "right")],
    line_labels=[("$x+y=1200$", (560, 660), -32), ("$x+y=600$", (190, 430), -32),
                 ("$y=\\dfrac{x}{2}$", (1150, 610), 0), ("", (0, 0), 0), ("", (0, 0), 0)],
    xticks=range(0, 1301, 200), yticks=range(0, 801, 200),
)

# Q8: Z = 3x + 9y ; x + 3y <= 60, x + y >= 10, x <= y ; maximum on segment CD
lpp_figure(
    "pa-q08-sol.svg", 26, 26,
    [(1, 3, 60, "<="), (1, 1, 10, ">="), (1, -1, 0, "<="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(0, 10), (5, 5), (15, 15), (0, 20)],
    labels=[("A(0, 10)", 7, -4, "left"), ("B(5, 5)", 8, -4, "left"),
            ("C(15, 15)", 8, -4, "left"), ("D(0, 20)", 7, 7, "left")],
    line_labels=[("$x+3y=60$", (21, 12.2), -18), ("$x+y=10$", (8.5, 1.4), -45),
                 ("$x=y$", (22, 23.5), 45), ("", (0, 0), 0), ("", (0, 0), 0)],
    segment=((15, 15), (0, 20)),
    xticks=range(0, 26, 5), yticks=range(0, 26, 5),
)

# Q9: max 80x + 120y ; 3x + 4y <= 60, x + 3y <= 30
lpp_figure(
    "pa-q09-sol.svg", 32, 18,
    [(3, 4, 60, "<="), (1, 3, 30, "<="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(0, 0), (20, 0), (12, 6), (0, 10)],
    labels=[("O(0, 0)", 6, 9, "left"), ("A(20, 0)", 5, 9, "left"),
            ("B(12, 6)", 8, 6, "left"), ("C(0, 10)", 7, 7, "left")],
    line_labels=[("$3x+4y=60$", (6.5, 13.6), -37), ("$x+3y=30$", (26.5, 1.8), -18),
                 ("", (0, 0), 0), ("", (0, 0), 0)],
    xticks=range(0, 31, 5), yticks=range(0, 17, 4), size=(4.8, 3.6),
)

# Q10: min 250x + 200y ; 2x + y >= 12, 2x + 9y >= 36, 2x + 3y >= 24 (unbounded) ; dashed 5x + 4y = 39
lpp_figure(
    "pa-q10-sol.svg", 21, 14,
    [(2, 1, 12, ">="), (2, 9, 36, ">="), (2, 3, 24, ">="), (1, 0, 0, ">="), (0, 1, 0, ">=")],
    corners=[(0, 12), (3, 6), (9, 2), (18, 0)],
    labels=[("A(0, 12)", 7, 4, "left"), ("B(3, 6)", 8, 5, "left"),
            ("C(9, 2)", 8, 6, "left"), ("D(18, 0)", 4, 10, "left")],
    line_labels=[("$2x+y=12$", (1.2, 9.0), -63), ("$2x+9y=36$", (15.5, 0.95), -12),
                 ("$2x+3y=24$", (6.0, 4.6), -34), ("", (0, 0), 0), ("", (0, 0), 0)],
    dashed=(5, 4, 39, "$250x+200y=1950$", (5.6, 0.9), -55),
    region_label=("unbounded region", (14.5, 8.5)),
    xticks=range(0, 21, 3), yticks=range(0, 15, 2),
)

print("figures written to", OUT)
