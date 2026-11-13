"""Figures for content/ch04/school.json. Run: python content/ch04/figs/make_figs.py"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#1f2937"
FILL = "#93c5fd"
ACCENT = "#ef4444"

plt.rcParams.update({
    "font.size": 11,
    "svg.fonttype": "none",
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "text.color": INK,
})


def q20():
    """Triangular plot A(2,3), B(-1,0), C(3,-2), line AB: y = x + 1, pole D(0,1)."""
    A, B, C, D = (2, 3), (-1, 0), (3, -2), (0, 1)
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    ax.fill([A[0], B[0], C[0]], [A[1], B[1], C[1]], color=FILL, alpha=0.45, lw=0)
    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], color=INK, lw=1.6)
    # line AB extended
    xs = [-2.5, 3.2]
    ax.plot(xs, [x + 1 for x in xs], color=ACCENT, lw=1.2, ls="--")
    ax.text(-2.9, 3.3, "line AB: x − y + 1 = 0", color=ACCENT, fontsize=11)
    for (px, py), name, dx, dy in [(A, "A(2, 3)", 0.12, 0.1), (B, "B(-1, 0)", -1.1, 0.15),
                                   (C, "C(3, -2)", 0.12, -0.35), (D, "D(0, 1)", -0.95, 0.2)]:
        ax.plot(px, py, "o", color=ACCENT if name.startswith("D") else INK, ms=5)
        ax.text(px + dx, py + dy, name, fontsize=11)
    ax.text(1.45, 0.8, "Area =\n9 sq units", fontsize=11, ha="center", va="center")
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_xlim(-3, 4.2)
    ax.set_ylim(-3, 4)
    ax.set_xticks(range(-3, 5))
    ax.set_yticks(range(-3, 5))
    ax.set_aspect("equal")
    ax.grid(color="#d1d5db", lw=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "q20-plot.svg"), transparent=True)
    if os.environ.get("PREVIEW_DIR"):
        fig.savefig(os.path.join(os.environ["PREVIEW_DIR"], "q20-plot.png"), dpi=90)
    plt.close(fig)


if __name__ == "__main__":
    q20()
    print("ok")
