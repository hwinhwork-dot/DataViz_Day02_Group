# Session 2 · Activity A · Which dataset type? (slide 14)
#   Six situations. For each: which dataset type (table, network, tree, field, geometry),
#   and is it static or a stream? One card per situation: a small drawing of the type and
#   the two answers. Cards that can be argued another way say so in one line.
# Standalone: no data file needed. Run from VS Code, or: python activities/activity_a_dataset_types.py

import sys
from pathlib import Path
from textwrap import wrap

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # so `src` can be imported
from src.style import (BLUE, GREY, INK, MUTED, PAPER, WASH, canvas, footer, headline, save,
                       use_style)

# situation, dataset type, static or stream, the other defensible answer (or None)
ITEMS = [
    ("Daily sales of each branch in 2024–2025", "table", "Table", "Static", None),
    ("Which customers follow each other on the cafe's social media page", "network",
     "Network", "Static", "Also right: stream, if new follows arrive live"),
    ("The chain's reporting lines: CEO → area managers → branch managers", "tree",
     "Tree", "Static", "Also right: network (a tree is a network without loops)"),
    ("Air temperature every hour on a 1 km grid over the city", "field",
     "Field", "Static", "Also right: stream, if the sensors send data live"),
    ("The boundaries of the districts of Ho Chi Minh City", "geometry",
     "Geometry", "Static", None),
    ("Orders arriving right now from a delivery app", "stream", "Table", "Stream", None),
]
VN = {"Table": "bảng", "Network": "mạng", "Tree": "cây", "Field": "trường",
      "Geometry": "hình học", "Static": "tĩnh", "Stream": "luồng"}


# ---------------------------------------------------------------------------
# 1. Small drawings of each type, centred on (cx, cy); s = size in inches
# ---------------------------------------------------------------------------
def glyph_table(ax, cx, cy, s, new_row=False):
    cols, rows = 4, 5
    w, h = s / cols, s * 0.7 / rows
    x0, y0 = cx - s / 2, cy - s * 0.35
    for r in range(rows):
        for c in range(cols):
            face = WASH if r == rows - 1 else PAPER
            if new_row and r == 0:
                face = BLUE                                    # the row arriving now
            ax.add_patch(Rectangle((x0 + c * w, y0 + r * h), w, h, facecolor=face,
                                   edgecolor=INK, lw=0.8))
    if new_row:
        ax.annotate("", xy=(x0 + s + 0.03, y0 + h / 2), xytext=(x0 + s + 0.32, y0 + h / 2),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6, mutation_scale=12))


def nodes(ax, pts, links, cx, cy, s):
    pts = np.array(pts) * s
    for a, b in links:
        ax.plot(*zip(pts[a] + (cx, cy), pts[b] + (cx, cy)), color=GREY, lw=1.2, zorder=1)
    for x, y in pts:
        ax.add_patch(Circle((cx + x, cy + y), 0.065, facecolor=INK, edgecolor=PAPER, lw=1.2,
                            zorder=2))


def glyph_network(ax, cx, cy, s):
    nodes(ax, [(-0.45, 0.25), (0.02, 0.38), (0.45, 0.12), (0.28, -0.32), (-0.25, -0.3),
               (-0.02, 0.0)],
          [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (5, 3), (1, 5)], cx, cy, s)


def glyph_tree(ax, cx, cy, s):
    nodes(ax, [(0, 0.35), (-0.3, 0.0), (0.3, 0.0), (-0.45, -0.35), (-0.15, -0.35),
               (0.15, -0.35), (0.45, -0.35)],
          [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)], cx, cy, s)


def glyph_field(ax, cx, cy, s):
    n, m = 8, 6
    step = s / n
    xx, yy = np.meshgrid(np.linspace(-1, 1, n), np.linspace(-1, 1, m))
    heat = np.exp(-((xx - 0.2) ** 2 + (yy + 0.1) ** 2) * 1.3)
    for i in range(m):
        for j in range(n):
            ax.add_patch(Rectangle((cx - s / 2 + j * step, cy - m * step / 2 + i * step), step,
                                   step, facecolor=plt.get_cmap("Greys")(0.08 + 0.8 * heat[i, j]),
                                   edgecolor=PAPER, lw=0.7))


def glyph_geometry(ax, cx, cy, s):
    shared = [(0.03, 0.38), (-0.06, -0.03), (0.06, -0.38)]
    left = [(-0.5, 0.28), *shared, (-0.46, -0.32), (-0.55, 0.0)]
    right = [*shared[::-1], (0.3, 0.4), (0.46, 0.18), (0.52, -0.25)]
    for shape in (left, right):
        ax.add_patch(Polygon([(cx + x * s, cy + y * s) for x, y in shape], closed=True,
                             facecolor=PAPER, edgecolor=INK, lw=1.3))


GLYPHS = {"table": glyph_table, "network": glyph_network, "tree": glyph_tree,
          "field": glyph_field, "geometry": glyph_geometry,
          "stream": lambda ax, cx, cy, s: glyph_table(ax, cx, cy, s, new_row=True)}


# ---------------------------------------------------------------------------
# 2. One card per situation
# ---------------------------------------------------------------------------
def card(ax, x, y_top, w, h, n, text, glyph, kind, time, other):
    ax.add_patch(Rectangle((x, y_top - h), w, h, facecolor=WASH, edgecolor="none"))
    ax.add_patch(Circle((x + 0.32, y_top - 0.36), 0.19, facecolor=INK, edgecolor="none"))
    ax.text(x + 0.32, y_top - 0.37, str(n), color=PAPER, fontsize=11, fontweight="bold",
            ha="center", va="center")
    ax.text(x + 0.65, y_top - 0.2, "\n".join(wrap(text, 36)), fontsize=11.5, va="top",
            linespacing=1.3)

    GLYPHS[glyph](ax, x + 1.0, y_top - 1.75, 1.05)

    for k, (label, value) in enumerate([("Type", kind), ("File", time)]):
        y = y_top - 1.45 - k * 0.6
        ax.text(x + 2.15, y, label, fontsize=10, color=MUTED, va="center")
        ax.text(x + 2.75, y, value, fontsize=17, fontweight="bold", va="center")
        ax.text(x + 2.75, y - 0.25, VN[value], fontsize=9.5, style="italic", color=MUTED,
                va="center")
    if other:
        ax.text(x + 0.3, y_top - h + 0.22, other, fontsize=9.5, style="italic", color=MUTED,
                va="bottom")


def main():
    use_style()
    W, H = 14.2, 9.0
    fig = plt.figure(figsize=(W, H))
    ax = canvas(fig)

    cw, ch, gap = 4.2, 2.95, 0.3
    top = H - 1.65
    for i, (text, glyph, kind, time, other) in enumerate(ITEMS):
        r, c = divmod(i, 3)
        card(ax, 0.5 + c * (cw + gap), top - r * (ch + gap), cw, ch, i + 1, text, glyph,
             kind, time, other)

    headline(fig, "Activity A · Which dataset type?",
             "For each situation: is it a table, network, tree, field or geometry? "
             "And is the file static (complete) or a stream (still growing)?")
    footer(fig, "Only situation 6 is a stream: new rows keep arriving while you look. "
                "Situation 1 has dates in it, but the file is complete, so it is static.",
           "Dataset types after Munzner (2014), ch. 2 · Session 2, slide 14")
    return save(fig, "activity_a_dataset_types")


if __name__ == "__main__":
    main()
    plt.show()
