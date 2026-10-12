# GH2 GoMart · export the main chart of each question (Q1–Q4) as a PNG into this folder
#   Runs the submitted notebook (../gh2_gomart/GH2_TeamName.ipynb) from top to bottom, exactly as
#   written, and saves the FIRST figure shown in each question's section:
#     Q1 · box plots of delivery time by zone and district   (Quang Minh)
#     Q2 · monthly share of payment methods, trend line       (Thảo)
#     Q3 · average rating by delivery time                    (Minh Nguyệt)
#     Q4 · orders by hour of day, bar chart                   (Tuấn Anh)
#   The notebook runs in a temporary folder, so nothing in the repo is overwritten
#   (the clean CSV stays as it is, and no extra image files are left behind).
# Needs: pandas, matplotlib, seaborn (requirements.txt). Run: python homework/gh2_visuals/export_visuals.py

import contextlib
import io
import json
import os
import shutil
import tempfile
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                      # draw off-screen: no windows pop up
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
NOTEBOOK = HERE.parent / "gh2_gomart" / "GH2_TeamName.ipynb"
RAW = HERE.parent.parent / "data" / "raw"
NAMES = {"Q1": "q1_delivery_time_by_zone.png", "Q2": "q2_ewallet_trend.png",
         "Q3": "q3_rating_vs_delivery_time.png", "Q4": "q4_order_peaks.png"}


def main():
    cells = json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]
    section, saved = None, {}

    def show(*args, **kwargs):              # replaces plt.show while the notebook runs
        for num in plt.get_fignums():
            if section in NAMES and section not in saved:
                path = HERE / NAMES[section]
                plt.figure(num).savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
                saved[section] = path
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
                        if text.startswith("## Task 7"):
                            section = None
                    elif cell["cell_type"] == "code":
                        with contextlib.redirect_stdout(io.StringIO()):
                            exec(text, ns)
        finally:
            os.chdir(cwd)

    for q in NAMES:
        print(f"{q}: {saved[q].relative_to(HERE.parent.parent)}" if q in saved else f"{q}: no figure found")
    return saved


if __name__ == "__main__":
    main()
