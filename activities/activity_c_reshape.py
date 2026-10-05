# Session 2 · Activity C · Reshape on paper (slide 27)
#   The wide table from the slide (units sold on 1 March 2025) turned into a long table with
#   melt, answering the slide's three questions in order:
#     Q1 how many rows, which keys · Q2 the one line of pandas · Q3 why a date is easy in
#     long form but awkward in wide form.
#   Colour = product category, so each number can be followed from wide to long.
# Needs: data/raw/phocaphe_sales_clean.csv. Run from VS Code, or: python activities/activity_c_reshape.py

import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # so `src` can be imported
from src.style import (BLUE, DATA_DIR, GOLD, GREEN, HAIR, INK, MUTED, PAPER, WASH, canvas,
                       footer, headline, save, use_style)

CATS = ["Coffee", "Tea", "Bakery"]
CAT_COLOUR = {"Coffee": BLUE, "Tea": GOLD, "Bakery": GREEN}
BRANCHES = ["Ben Thanh", "Quang Trung"]
DAY1, DAY2 = pd.Timestamp("2025-03-01"), pd.Timestamp("2025-03-02")


def tint(colour, k=0.25):
    """A light wash of a colour (mixed with white), so ink text stays readable on it."""
    r, g, b = to_rgb(colour)
    return (1 - k * (1 - r), 1 - k * (1 - g), 1 - k * (1 - b))


# ---------------------------------------------------------------------------
# 1. Data · the slide's numbers come straight from the clean sales file
# ---------------------------------------------------------------------------
sales = pd.read_csv(DATA_DIR / "phocaphe_sales_clean.csv", parse_dates=["date"])
pick = sales[sales["branch"].isin(BRANCHES) & sales["category"].isin(CATS)]


def wide_for(day):
    one = pick[pick["date"] == day]
    return (one.pivot(index="branch", columns="category", values="units")[CATS]
               .rename_axis(columns=None).reset_index())


wide = wide_for(DAY1)
long = wide.melt(id_vars="branch", var_name="category", value_name="units")   # Q2
by_hand = pd.DataFrame({"branch": BRANCHES * 3,
                        "category": ["Coffee", "Coffee", "Tea", "Tea", "Bakery", "Bakery"],
                        "units": [466, 282, 268, 173, 190, 116]})
pd.testing.assert_frame_equal(long, by_hand, check_dtype=False)                # Q1 by hand
wide2 = wide_for(DAY2)
print(wide.to_string(index=False), "\n")
print(long.to_string(), "\n")
print(f"Q1: {len(long)} rows; keys = branch, category; value = units")


# ---------------------------------------------------------------------------
# 2. Drawing helpers
# ---------------------------------------------------------------------------
def draw_table(ax, x, y_top, widths, header, rows, fills, head_h=0.42, row_h=0.36, size=11,
               head_fills=None, right=()):
    xs = [x + sum(widths[:k]) for k in range(len(widths))]
    for k, (text, w) in enumerate(zip(header, widths)):
        ax.add_patch(Rectangle((xs[k], y_top - head_h), w, head_h,
                               facecolor=(head_fills or {}).get(k, WASH), edgecolor=PAPER, lw=2))
        ax.text(xs[k] + 0.1, y_top - head_h / 2, text, va="center", fontsize=size - 0.5,
                fontweight="bold", linespacing=1.1)
    for i, row in enumerate(rows):
        y = y_top - head_h - (i + 1) * row_h
        for k, (text, w) in enumerate(zip(row, widths)):
            ax.add_patch(Rectangle((xs[k], y), w, row_h, facecolor=fills[i][k],
                                   edgecolor=PAPER, lw=2))
            ax.text(xs[k] + w - 0.1 if k in right else xs[k] + 0.1, y + row_h / 2, text,
                    ha="right" if k in right else "left", va="center", fontsize=size)
    return y_top - head_h - len(rows) * row_h                     # bottom edge


def q_tag(ax, x, y, label):
    ax.add_patch(FancyBboxPatch((x, y - 0.14), 0.42, 0.28, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=INK, edgecolor=INK))
    ax.text(x + 0.21, y, label, ha="center", va="center", fontsize=10, fontweight="bold",
            color=PAPER)


# ---------------------------------------------------------------------------
# 3. The figure
# ---------------------------------------------------------------------------
def main():
    use_style()
    W, H = 14.2, 9.4
    fig = plt.figure(figsize=(W, H))
    ax = canvas(fig)
    top = H - 1.75

    # ---- wide -> long -------------------------------------------------------
    ax.text(0.5, top, "Wide, as on the slide", fontsize=13, fontweight="bold", va="bottom")
    w_rows = [[b] + [f"{v}" for v in wide.loc[wide.branch == b, CATS].iloc[0]] for b in BRANCHES]
    w_fills = [[PAPER] + [tint(CAT_COLOUR[c]) for c in CATS] for _ in BRANCHES]
    draw_table(ax, 0.5, top - 0.15, [1.5, 0.95, 0.95, 0.95], ["branch"] + CATS, w_rows, w_fills,
               row_h=0.46, right=(1, 2, 3),
               head_fills={k + 1: tint(CAT_COLOUR[c], 0.5) for k, c in enumerate(CATS)})
    ax.text(0.5, top - 1.65, "2 rows: the categories hide in the column names",
            fontsize=10, style="italic", color=MUTED, va="top")

    ax.add_patch(FancyArrowPatch((5.1, top - 0.75), (7.75, top - 0.75), arrowstyle="-|>",
                                 mutation_scale=20, color=INK, lw=1.8))
    ax.text(6.42, top - 0.62, "melt", family="monospace", fontsize=15, fontweight="bold",
            ha="center", va="bottom")
    q_tag(ax, 5.1, top - 1.2, "Q2")
    ax.text(5.65, top - 1.06, 'wide.melt(\n  id_vars="branch",\n  var_name="category",\n'
            '  value_name="units")', family="monospace", fontsize=10, va="top",
            linespacing=1.45)

    lx = 8.2
    ax.text(lx, top, "Long (tidy)", fontsize=13, fontweight="bold", va="bottom")
    l_rows = [[r.branch, r.category, f"{r.units}"] for r in long.itertuples()]
    l_fills = [[tint(CAT_COLOUR[r.category])] * 3 for r in long.itertuples()]
    draw_table(ax, lx, top - 0.15, [1.5, 1.1, 0.85], ["branch", "category", "units"], l_rows,
               l_fills, right=(2,))

    ax_x = 12.0                                                  # the Q1 answer, beside the table
    q_tag(ax, ax_x, top - 0.35, "Q1")
    ax.text(ax_x, top - 0.65, f"{len(long)} rows", fontsize=24, fontweight="bold", va="top")
    ax.text(ax_x, top - 1.2, f"{len(BRANCHES)} branches × {len(CATS)} categories",
            fontsize=10.5, va="top")
    ax.text(ax_x, top - 1.65, "Keys", fontsize=10.5, fontweight="bold", va="top")
    ax.text(ax_x, top - 1.9, "branch, category", fontsize=10.5, va="top")
    ax.text(ax_x, top - 2.25, "Value", fontsize=10.5, fontweight="bold", va="top")
    ax.text(ax_x, top - 2.5, "units", fontsize=10.5, va="top")

    # ---- Q3 · add a date ----------------------------------------------------
    y3 = top - 3.25
    ax.plot([0.5, W - 0.5], [y3 + 0.3] * 2, color=HAIR, lw=1)
    q_tag(ax, 0.5, y3, "Q3")
    ax.text(1.05, y3, "Add a date: why is it easy in long form but awkward in wide form?",
            fontsize=13, fontweight="bold", va="center")

    t3 = y3 - 0.55
    ax.text(0.5, t3, "Long: one more column ✓", fontsize=12, fontweight="bold", va="bottom")
    d_rows = [["1 Mar"] + row for row in l_rows]
    d_fills = [[tint(INK, 0.12)] + f for f in l_fills]
    bottom = draw_table(ax, 0.5, t3 - 0.12, [0.85, 1.5, 1.1, 0.85],
                        ["date", "branch", "category", "units"], d_rows, d_fills, head_h=0.36,
                        row_h=0.3, size=10, right=(3,), head_fills={0: tint(INK, 0.25)})
    ax.text(0.5, bottom - 0.12, "A second day just adds 6 more rows below.\nThe columns "
            "never change.", fontsize=10.5, va="top", linespacing=1.35)

    vx = 6.0
    ax.text(vx, t3, "Wide: the date must go into the column names ✗", fontsize=12,
            fontweight="bold", va="bottom")
    v_head = ["branch"] + [f"{c}\n{d.day} Mar" for d in (DAY1, DAY2) for c in CATS]
    v_rows = [[b] + [f"{t.loc[t.branch == b, c].iloc[0]}" for t in (wide, wide2) for c in CATS]
              for b in BRANCHES]
    v_fills = [[PAPER] + [tint(CAT_COLOUR[c]) for _ in (1, 2) for c in CATS] for _ in BRANCHES]
    bottom = draw_table(ax, vx, t3 - 0.12, [1.25] + [1.05] * 6, v_head, v_rows, v_fills,
                        head_h=0.55, row_h=0.4, size=10, right=tuple(range(1, 7)),
                        head_fills={k: tint(CAT_COLOUR[c], 0.5)
                                    for k, c in enumerate(CATS * 2, start=1)})
    ax.text(vx, bottom - 0.12, "Every new day adds 3 more columns, and the table soon becomes "
            "too wide to read or to filter.", fontsize=10.5, va="top")

    headline(fig, "Activity C · Reshape on paper",
             "Units sold on 1 March 2025 (simulated). Turn the wide table into a long (tidy) "
             "table. Colour = product category.")
    footer(fig, "Rule of thumb: store and clean data long; turn it wide only when a person "
                "needs to read it.",
           "Data: phocaphe_sales_clean.csv (simulated) · Session 2, slides 23–27")
    return save(fig, "activity_c_reshape")


if __name__ == "__main__":
    main()
    plt.show()
