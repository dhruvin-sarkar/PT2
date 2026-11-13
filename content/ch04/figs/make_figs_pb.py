"""Figures for Chapter 4, Practice Set B.  Run: python make_figs_pb.py (from this folder)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
INK, FILL, ACC = "#1f2937", "#93c5fd", "#ef4444"
plt.rcParams.update({"font.size": 11, "svg.fonttype": "none", "text.color": INK,
                     "axes.edgecolor": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})


def q20():
    A, B, C, T = (-2, 1), (4, 5), (6, -3), (1, 3)
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    ax.fill([A[0], B[0], C[0]], [A[1], B[1], C[1]], color=FILL, alpha=0.45, lw=0)
    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], color=INK, lw=1.4)
    ax.plot([C[0], T[0]], [C[1], T[1]], color=ACC, lw=1.6, ls="--")
    for name, (px, py), off in [("A(-2, 1)", A, (-1.4, -0.75)), ("B(4, 5)", B, (0.2, 0.2)),
                                ("C(6, -3)", C, (0.2, -0.5))]:
        ax.plot(px, py, "o", color=INK, ms=5)
        ax.text(px + off[0], py + off[1], name, fontsize=11)
    ax.plot(T[0], T[1], "o", color=INK, ms=5)
    ax.annotate("T(k, 3)", xy=T, xytext=(-2.4, 4.3), fontsize=11, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.text(3.9, 0.3, "path", color=ACC, fontsize=11)
    ax.text(1.3, 1.2, "park", fontsize=11)
    ax.set_xlim(-3.5, 8.5)
    ax.set_ylim(-4.5, 6.5)
    ax.set_xticks(range(-3, 9))
    ax.set_yticks(range(-4, 7))
    ax.grid(True, color="#d1d5db", lw=0.6)
    ax.axhline(0, color=INK, lw=0.9)
    ax.axvline(0, color=INK, lw=0.9)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")
    for s in ax.spines.values():
        s.set_visible(False)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "pb-q20.svg"), transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    q20()
    print("ok")
