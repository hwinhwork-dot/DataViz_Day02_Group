# Session 2 · Activity B · Classify the attributes (slide 21)
#   An online-shop order table with 11 columns. Each column is sorted into one of the three
#   attribute types, like the tree on slide 15: categorical, ordinal, quantitative.
#   Each chip shows the column, an example of its values and its ordering direction.
#   The bottom row answers "key or value?" and the last question on the slide.
# Standalone: no data file needed. Run from VS Code, or: python activities/activity_b_attribute_types.py

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Wedge

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # so `src` can be imported
from src.style import (GREY, INK, MUTED, PAPER, WASH, canvas, footer, headline, save,
                       use_style)

# type -> [(column, example values, direction, is_key)]
LANES = {
    ("Categorical", "định danh", "only same or different:  = ≠"): [
        ("order_id", "100231, 100232, …", None, True),
        ("province", "TP.HCM, Hà Nội, Đà Nẵng, …", None, False),
        ("payment_method", "COD, card, e-wallet, …", None, False),
        ("returned", "yes / no", None, False),
    ],
    ("Ordinal", "thứ bậc", "also an order:  < >"): [
        ("delivery_speed", "economy < standard < express", ("sequential", 3), False),
        ("rating", "1 star < … < 5 stars", ("sequential", 5), False),
        ("weekday", "Mon < … < Sun, then Mon again", ("cyclic", 7), False),
    ],
    ("Quantitative", "định lượng", "also a distance:  + − mean"): [
        ("order_time", "2025-03-14 09:31", ("sequential", None), False),
        ("basket_value_kvnd", "85, 240, 410, …", ("sequential", None), False),
        ("discount_pct", "0, 5, 10, 20", ("sequential", None), False),
        ("profit_change_pct", "−12, 0, +7, …  (0 = no change)", ("diverging", None), False),
    ],
}


def direction(ax, x, y, kind, steps):
    """A small colour bar (or ring) for the ordering direction, with its name under it."""
    w, h = 0.75, 0.2
    if kind == "cyclic":
        for k in range(steps):
            ax.add_patch(Wedge((x + w / 2, y + 0.02), 0.17, 90 - (k + 1) * 360 / steps,
                               90 - k * 360 / steps, width=0.07,
                               facecolor=plt.get_cmap("twilight")(k / steps),
                               edgecolor=PAPER, lw=0.8))
    else:
        n = steps or 30
        cmap = plt.get_cmap("Blues" if kind == "sequential" else "RdBu")
        for k in range(n):
            ax.add_patch(Rectangle((x + k * w / n, y - h / 2 + 0.02), w / n, h,
                                   facecolor=cmap(0.15 + 0.8 * k / (n - 1)),
                                   edgecolor=PAPER if steps else "none", lw=1.2 if steps else 0))
        if kind == "diverging":
            ax.plot([x + w / 2] * 2, [y - h / 2 - 0.02, y + h / 2 + 0.06], color=INK, lw=1)
    ax.text(x + w / 2, y - 0.25, kind, ha="center", va="top", fontsize=9, color=MUTED)


def main():
    use_style()
    W, H = 14.2, 9.0
    fig = plt.figure(figsize=(W, H))
    ax = canvas(fig)

    lane_w, gap, top = 4.2, 0.3, H - 1.55
    chip_h, chip_gap = 0.82, 0.14
    for i, ((name, vn, ops), chips) in enumerate(LANES.items()):
        x = 0.5 + i * (lane_w + gap)
        # lane header
        ax.text(x, top, name, fontsize=17, fontweight="bold", va="top")
        ax.text(x + 0.08 + len(name) * 0.135, top - 0.06, vn, fontsize=11, style="italic",
                color=MUTED, va="top")
        ax.text(x, top - 0.42, ops, fontsize=11, va="top")
        ax.plot([x, x + lane_w], [top - 0.78] * 2, color=INK, lw=1)
        # one chip per column
        for k, (col, example, dirn, key) in enumerate(chips):
            y_top = top - 0.93 - k * (chip_h + chip_gap)
            ax.add_patch(Rectangle((x, y_top - chip_h), lane_w, chip_h, facecolor=WASH,
                                   edgecolor="none"))
            ax.text(x + 0.2, y_top - 0.27, col, family="monospace", fontsize=12.5,
                    fontweight="bold", va="center")
            if key:
                ax.add_patch(FancyBboxPatch((x + 1.42, y_top - 0.39), 0.52, 0.24,
                                            boxstyle="round,pad=0,rounding_size=0.05",
                                            facecolor=INK, edgecolor=INK))
                ax.text(x + 1.68, y_top - 0.27, "KEY", ha="center", va="center", fontsize=9,
                        fontweight="bold", color=PAPER)
            ax.text(x + 0.2, y_top - 0.6, example, fontsize=10, color=MUTED, va="center")
            if dirn:
                direction(ax, x + lane_w - 0.95, y_top - 0.32, *dirn)
            else:
                ax.text(x + lane_w - 0.57, y_top - 0.36, "no order", ha="center", va="center",
                        fontsize=9, style="italic", color=GREY)

    # The two remaining answers
    y = 1.85
    ax.plot([0.5, W - 0.5], [y + 0.45] * 2, color=INK, lw=1)
    answers = [("Key or value?", "order_id is the only key (one per order). The other 10 "
                                 "columns are values."),
               ("Read as a number, but never average it?",
                "order_id: the digits are only a name. Debatable: rating, because the step "
                "1→2 may not equal 4→5.")]
    for k, (q, a) in enumerate(answers):
        ax.text(0.5, y - k * 0.42, q, fontsize=11.5, fontweight="bold", va="center")
        ax.text(4.95, y - k * 0.42, a, fontsize=11.5, va="center")

    headline(fig, "Activity B · Classify the attributes",
             "Online-shop orders (a made-up table). For each column: which type is it, "
             "which ordering direction, and is it a key or a value?")
    footer(fig, "Colour bar = ordering direction: sequential (low → high), diverging "
                "(two ways from 0), cyclic (wraps around).",
           "Attribute types after Munzner (2014), ch. 2.5 · Session 2, slide 21")
    return save(fig, "activity_b_attribute_types")


if __name__ == "__main__":
    main()
    plt.show()
