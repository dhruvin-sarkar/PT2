"""Figures for content/ch09/practice-b.json (Practice Set B). Run: python make_figs_pb.py"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#1f2937"
FILL = "#93c5fd"
ACCENT = "#ef4444"

plt.rcParams.update({
    "font.size": 11,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "text.color": INK,
    "svg.fonttype": "none",
})


def q20():
    """Q20: amount of medicine A = 400 (3/4)^(t/3)."""
    t = np.linspace(0, 12, 400)
    A = 400 * (0.75) ** (t / 3)
    fig, ax = plt.subplots(figsize=(4.8, 3.2), dpi=100)
    ax.plot(t, A, color=INK, linewidth=1.8, label=r"$A=400\left(\dfrac{3}{4}\right)^{t/3}$")
    pts = [(0, 400), (3, 300), (6, 225), (9, 168.75)]
    for tx, ay in pts:
        ax.plot([tx], [ay], "o", color=ACCENT, markersize=5)
        ax.annotate(f"({tx}, {ay:g})", (tx, ay), textcoords="offset points", xytext=(6, 6), fontsize=11)
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 460)
    ax.set_xlabel("t (hours)")
    ax.set_ylabel("A (mg)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="upper right", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "pb-q20.svg"), transparent=True)
    plt.close(fig)


def q17():
    """Q17: the curve 2(x^2 - y^2) = 3x (both branches) through (2, 1) and its tangent there."""
    # y^2 = x^2 - 3x/2 >= 0 for x <= 0 or x >= 3/2
    xr = 1.5 + (4 - 1.5) * np.linspace(0, 1, 400) ** 2
    xl = -2.5 * np.linspace(0, 1, 400) ** 2
    fig, ax = plt.subplots(figsize=(4.8, 3.6), dpi=100)
    first = True
    for xs in (xr, xl):
        yy = np.sqrt(np.clip(xs * xs - 1.5 * xs, 0, None))
        ax.plot(np.r_[xs[::-1], xs], np.r_[-yy[::-1], yy], color=INK, linewidth=1.8,
                label=r"$2(x^2-y^2)=3x$" if first else None)
        first = False
    m = (4 + 1) / (2 * 2 * 1)  # slope (x^2+y^2)/(2xy) at (2,1)
    xt = np.linspace(0.6, 3.4, 50)
    ax.plot(xt, 1 + m * (xt - 2), color=ACCENT, linewidth=1.3, linestyle="--", label=r"tangent at $(2,1)$, slope $\dfrac{5}{4}$")
    ax.plot([2], [1], "o", color=ACCENT, markersize=5)
    ax.annotate("(2, 1)", (2, 1), textcoords="offset points", xytext=(8, -14), fontsize=11)
    ax.axhline(0, color=INK, linewidth=0.8)
    ax.axvline(0, color=INK, linewidth=0.8)
    ax.set_xlim(-2.6, 4.1)
    ax.set_ylim(-3.4, 3.4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "pb-q17.svg"), transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    q20()
    q17()
    print("done")
