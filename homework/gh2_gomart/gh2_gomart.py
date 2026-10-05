# %% [markdown]
# # Group Homework 2 · GoMart deliveries · team skeleton (NOT done yet)
# Same sections as the official notebook GH2_TeamName.ipynb, as a .py file with `# %%` cells:
# VS Code runs each cell like a notebook, and git can merge it when several members edit
# on their own branches. Copy the finished cells into GH2_TeamName.ipynb before submitting.
#
# Brief: Session 2 · Group Homework 2 (LMS). All data is simulated.
# Data: data/raw/gomart_orders_2025.csv, data/raw/gomart_districts.csv
#
# The operations manager asks:
#   1. Where are deliveries slow? Do customers far from the hub wait much longer?
#   2. Is the move to e-wallet payments real, or just noise?
#   3. Do slow deliveries cost us good ratings? From how many minutes on?
#   4. When are the peaks, so we can plan riders' shifts?

# %%
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "outputs" / "figures"

# %% [markdown]
# ## Memo to the operations manager (Task 6 · write this LAST, put it at the top)
# **Big Idea:** *one complete sentence: your point and what is at stake.*
#
# *At most 120 words + one explanatory chart (grey for context, one highlight colour,
# an action title).*

# %%
# TODO Task 6: the explanatory chart

# %% [markdown]
# ## Task 0 · Team card
# | Student ID | Name | Role |
# |---|---|---|
# | | | |
#
# Candidate project datasets: see homework/project_kickoff_team_card.md

# %% [markdown]
# ## Task 1 · Look
# First-look checklist (Tutorial 2, ch. 2): shape, head, info, describe,
# value_counts on EVERY text column, isna, duplicated, nunique.
# Then list at least SIX different problems in the table below.

# %%
# TODO Task 1: raw = pd.read_csv(DATA_DIR / "gomart_orders_2025.csv")

# %% [markdown]
# | # | Problem | Column | How we found it (command) |
# |---|---|---|---|
# | 1 | | | |
# | 2 | | | |
# | 3 | | | |
# | 4 | | | |
# | 5 | | | |
# | 6 | | | |

# %% [markdown]
# ## Task 2 · Name
# | Column | Attribute type | Direction | Key / value | Notes on missing values |
# |---|---|---|---|---|
# | order_id | | | | |
# | order_time | | | | |
# | district | | | | |
# | customer_type | | | | |
# | member_tier | | | | |
# | payment | | | | |
# | items | | | | |
# | basket_value_vnd | | | | |
# | status | | | | |
# | delivery_min | | | | |
# | rating | | | | |
#
# Also answer: which column(s) form the key (check it in code)? Are member_tier and rating
# missing for the same reason? Which columns become ordered categories (convert them)?

# %%
# TODO Task 2: check the key, convert ordered categories

# %% [markdown]
# ## Task 3 · Clean
# clean_orders(df) -> (clean_df, log), like clean_sales in Tutorial 2, Section 4.6.
# For every step: WHAT you did, HOW MANY rows it touched, WHY (remove / correct /
# set to missing / keep).

# %%
def clean_orders(df):
    """Return (clean DataFrame, log dict). Each step is one decision."""
    log = {"rows_in": len(df)}
    df = df.copy()
    # TODO
    log["rows_out"] = len(df)
    return df, log

# %% [markdown]
# *Step-by-step justification:*

# %% [markdown]
# ## Task 4 · Reshape and combine
# Merge gomart_districts.csv (use validate=...), derive hour, weekday (ordered), month.
# Confirm that no order lost its zone in the merge.

# %%
# TODO Task 4

# %% [markdown]
# ## Task 5 · From question to chart
# For each question: (a) task = action + target, (b) chart and why it fits,
# (c) the chart (title states the finding, axes with units, honest scales),
# (d) one sentence of interpretation.
#
# ### Q1 · Where are deliveries slow?
# *Task: ...  Chart and why: ...*

# %%
# TODO Q1

# %% [markdown]
# *Interpretation:*
#
# ### Q2 · Is the move to e-wallet real?
# *Task: ...  Chart and why: ...*

# %%
# TODO Q2

# %% [markdown]
# *Interpretation:*
#
# ### Q3 · Do slow deliveries cost good ratings?
# *Task: ...  Chart and why: ...*

# %%
# TODO Q3

# %% [markdown]
# *Interpretation:*
#
# ### Q4 · When are the peaks?
# *Task: ...  Chart and why: ...*

# %%
# TODO Q4

# %% [markdown]
# *Interpretation:*

# %% [markdown]
# ## Task 7 · Team and AI
# | Member | What they did | Share of work |
# |---|---|---|
# | | | |

# %%
AI_USE = """
Tool(s) used:
What we asked:
What we checked or changed ourselves:
"""
print(AI_USE)
