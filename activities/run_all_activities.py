# Session 2 · Activities A–D in one run
#   Runs the four activity scripts in order and saves one figure each to outputs/figures/.
#   Each activity is also a standalone file, so a single one can be run (and fixed) alone:
#     A · activity_a_dataset_types.py     which dataset type? static or stream?
#     B · activity_b_attribute_types.py   attribute type, direction, key or value
#     C · activity_c_reshape.py           wide -> long with melt, then add a date
#     D · activity_d_vague_to_precise.py  vague request -> action + target + data -> chart
# Run from VS Code, or from the repo root: python activities/run_all_activities.py

import importlib
import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                                  # the four activity files

ACTIVITIES = [("A · Which dataset type?", "activity_a_dataset_types"),
              ("B · Classify the attributes", "activity_b_attribute_types"),
              ("C · Reshape on paper", "activity_c_reshape"),
              ("D · From vague to precise", "activity_d_vague_to_precise")]


def main():
    saved = []
    for title, name in ACTIVITIES:
        print(f"\n=== Activity {title} " + "=" * (50 - len(title)))
        module = importlib.import_module(name)                 # imported here, so its printout
        saved.append(module.main())                            # lands under its own header
    print("\nAll four figures:")
    for path in saved:
        print("  ", path)
    return saved


if __name__ == "__main__":
    main()
    plt.show()                                                 # one window per figure
