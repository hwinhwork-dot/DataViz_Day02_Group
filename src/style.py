# House style for the Session 2 activities, carried over from the Session 1 charts
#   Editorial look: serif type, black ink, grey for context, one accent colour.
#   Every figure: a title that states the answer, an italic subtitle, and a footer
#   with the caveat and the data source (as in fig3/fig4 of Session 1).

from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw"
FIG_DIR = ROOT / "outputs" / "figures"

# Ink and paper
INK, MUTED, GREY, HAIR = "#1d1d1b", "#52514e", "#a3a29d", "#d9d8d3"
WASH, PAPER = "#f4f3ef", "#ffffff"

# Accent colours from Session 1 (make_charts.py). Checked with a colour-blind
# validator: BLUE / GOLD / GREEN pass for every pair; ORANGE is close to GREEN
# for deuteranopes, so the two are never used without a direct label.
BLUE, ORANGE, GREEN, GOLD = "#4176cf", "#db7043", "#3fab7d", "#e2a424"

SERIF = ["Georgia", "Times New Roman", "DejaVu Serif", "DejaVu Sans"]   # last one: symbols ✕ ★
MONO = ["Menlo", "Consolas", "DejaVu Sans Mono"]

# Branch names as people write them (Session 1, make_thao_dien.py)
NAMES = {"Ben Thanh": "Bến Thành", "Vo Van Tan": "Võ Văn Tần", "Thao Dien": "Thảo Điền",
         "Phan Xich Long": "Phan Xích Long", "Quang Trung": "Quang Trung",
         "Phu My Hung": "Phú Mỹ Hưng"}


def use_style():
    plt.rcParams.update({
        "font.family": SERIF,                     # a list: missing glyphs (→ ≠ ×) fall back
        "font.serif": SERIF,
        "font.monospace": MONO,
        "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
        "text.color": INK,
        "axes.edgecolor": GREY, "axes.labelcolor": MUTED, "axes.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "xtick.color": GREY, "ytick.color": GREY,
        "xtick.labelcolor": MUTED, "ytick.labelcolor": MUTED,
        "axes.unicode_minus": True,
    })


def canvas(fig):
    """One axes over the whole figure, measured in inches from the bottom-left.

    Used for diagrams (tables, cards, glyphs) where positions matter more than scales."""
    w, h = fig.get_size_inches()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return ax


def headline(fig, title, subtitle, left=0.5):
    """Answer-first title and an italic subtitle, placed in inches from the top."""
    w, h = fig.get_size_inches()
    fig.text(left / w, 1 - 0.3 / h, title, ha="left", va="top", fontsize=21,
             fontweight="bold")
    fig.text(left / w, 1 - 0.85 / h, subtitle, ha="left", va="top", fontsize=12,
             style="italic", color=MUTED, linespacing=1.4)


def footer(fig, note, source, left=0.5):
    w, h = fig.get_size_inches()
    fig.text(left / w, 0.5 / h, note, ha="left", va="bottom", fontsize=10.5,
             linespacing=1.35)
    fig.text(left / w, 0.22 / h, source, ha="left", va="bottom", fontsize=9,
             style="italic", color=MUTED)


def save(fig, name):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = FIG_DIR / f"{name}.png"
    fig.savefig(path, dpi=200)
    print("Saved:", path.relative_to(ROOT))
    return path
