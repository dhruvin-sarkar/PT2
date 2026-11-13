"""Figures for Chapter 4, Practice Set A.  Run: python make_figs_pa.py (from this folder)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
INK, FILL, ACC = "#1f2937", "#93c5fd", "#ef4444"
plt.rcParams.update({"font.size": 11, "svg.fonttype": "none", "text.color": INK,
                     "axes.edgecolor": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})


def q20():
    P, Q, R, S = (1, 2), (4, 3), (7, 4), (3, 7)
    fig, ax = plt.subplots(figsize=(4.8, 4.0))
    ax.fill([P[0], R[0], S[0]], [P[1], R[1], S[1]], color=FILL, alpha=0.45, lw=0)
    ax.plot([P[0], S[0], R[0]], [P[1], S[1], R[1]], color=INK, lw=1.2, ls="--")
    xs = [-0.5, 8.5]
    ax.plot(xs, [(x + 5) / 3 for x in xs], color=ACC, lw=1.6)
    for name, (px, py), off in [("P(1, 2)", P, (-0.2, 0.45)), ("Q(4, 3)", Q, (-0.4, 0.45)),
                                ("R(7, 4)", R, (-0.4, 0.45)), ("S(3, 7)", S, (0.2, 0.1))]:
        ax.plot(px, py, "o", color=INK, ms=5)
        ax.text(px + off[0], py + off[1], name, fontsize=11)
    ax.text(6.0, 2.55, "metro line", color=ACC, fontsize=11)
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-0.5, 8.0)
    ax.set_xticks(range(0, 9))
    ax.set_yticks(range(0, 9))
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
    fig.savefig(os.path.join(HERE, "pa-q20.svg"), transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    q20()
    print("ok")
