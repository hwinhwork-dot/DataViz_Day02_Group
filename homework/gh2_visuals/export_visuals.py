# GH2 GoMart: export one image for each question (Q1 to Q4) into this folder.
#   The script runs the submitted notebook (../gh2_gomart/GH2_TeamName.ipynb) from top to bottom,
#   exactly as written. It collects every chart that a question shows and joins them into one image:
#     Q1: the two simple bar charts (the box plots and the scatter plot of Quang Minh stay in the notebook)
#     Q2: monthly payment shares, then the two supporting bar charts          (Thảo)
#     Q3: average rating by delivery time                                     (Minh Nguyệt)
#     Q4: orders by hour, orders by weekday, then the peak-window heatmap     (Tuấn Anh)
#   A question stops collecting charts when the notebook reaches a note that starts with "More detail".
#   The charts are placed one under the other and are never changed. The notebook runs in a
#   temporary folder, so nothing in the repository is overwritten and no extra image files are left behind.
# Needs: pandas, matplotlib, seaborn and pillow (matplotlib installs pillow).
# Run it from the repository root: python homework/gh2_visuals/export_visuals.py

import contextlib
import io
import json
import os
import shutil
import tempfile
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                      # draw off-screen, so no window opens
import matplotlib.pyplot as plt
from PIL import Image

HERE = Path(__file__).resolve().parent
NOTEBOOK = HERE.parent / "gh2_gomart" / "GH2_TeamName.ipynb"
RAW = HERE.parent.parent / "data" / "raw"
NAMES = {"Q1": "q1_delivery_time.png", "Q2": "q2_ewallet.png",
         "Q3": "q3_ratings.png", "Q4": "q4_order_peaks.png"}
PAD, GAP = 60, 50                          # white space around and between the charts, in pixels


def join_vertically(png_list, path):
    """Put the charts one under the other, centred on a white page."""
    pictures = [Image.open(io.BytesIO(data)).convert("RGB") for data in png_list]
    width = max(p.width for p in pictures) + 2 * PAD
    height = sum(p.height for p in pictures) + GAP * (len(pictures) - 1) + 2 * PAD
    page = Image.new("RGB", (width, height), "white")
    top = PAD
    for p in pictures:
        page.paste(p, ((width - p.width) // 2, top))
        top += p.height + GAP
    page.save(path, optimize=True)


def main():
    cells = json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]
    section, charts = None, {q: [] for q in NAMES}

    def show(*args, **kwargs):              # replaces plt.show while the notebook runs
        for num in plt.get_fignums():
            if section in charts:
                buffer = io.BytesIO()
                plt.figure(num).savefig(buffer, format="png", dpi=200, bbox_inches="tight", facecolor="white")
                charts[section].append(buffer.getvalue())
        plt.close("all")

    with tempfile.TemporaryDirectory() as tmp:
        for name in ("gomart_orders_2025.csv", "gomart_districts.csv"):
            shutil.copy(RAW / name, tmp)    # the notebook finds its data next to itself
        cwd = os.getcwd()
        os.chdir(tmp)
        plt.show = show
        try:
            ns = {}
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                for cell in cells:
                    text = "".join(cell["source"])
                    if cell["cell_type"] == "markdown":
                        for q in NAMES:
                            if f"### {q} " in text:
                                section = q
                        if text.startswith(("## Task 7", "**More detail")):
                            section = None                  # the charts below this note stay in the notebook only
                    elif cell["cell_type"] == "code":
                        with contextlib.redirect_stdout(io.StringIO()):
                            exec(text, ns)
        finally:
            os.chdir(cwd)

    for q, name in NAMES.items():
        if charts[q]:
            join_vertically(charts[q], HERE / name)
            print(f"{q}: {len(charts[q])} chart(s) in {(HERE / name).relative_to(HERE.parent.parent)}")
        else:
            print(f"{q}: no chart found")


if __name__ == "__main__":
    main()
