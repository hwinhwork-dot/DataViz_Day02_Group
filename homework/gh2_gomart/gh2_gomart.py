# %% [markdown]
# # Group Homework 2 · GoMart deliveries · team file (Tasks 0–4 done, Tasks 5–7 TODO)
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

# In the repo the files are in data/raw; in Colab, upload both files next to the notebook
DATA_DIR = next((p for p in [Path("../../data/raw"), Path("data/raw"), Path(".")]
                 if (p / "gomart_orders_2025.csv").exists()), None)
assert DATA_DIR is not None, "Upload gomart_orders_2025.csv and gomart_districts.csv first"
# The clean CSV (Task 4) is saved next to this file, or in the working folder in Colab
HERE = Path(__file__).parent if "__file__" in globals() else Path(".")
raw = pd.read_csv(DATA_DIR / "gomart_orders_2025.csv")
districts = pd.read_csv(DATA_DIR / "gomart_districts.csv")
print("orders:", raw.shape, "| districts:", districts.shape)

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
# **Team name:** *(to agree)*
#
# | Student ID | Name | Role |
# |---|---|---|
# | 31221020403 | Phạm Tuấn Anh | |
# | 31241027205 | Trần Nhã Đoan | |
# | 31221021575 | Nguyễn Hoàng Minh | Leader |
# | 31221021576 | Phạm Quang Minh | |
# | 31241021154 | Nguyễn Minh Nguyệt | |
# | 31241026554 | Trần Nguyễn Thanh Thảo | |
#
# **Candidate project datasets**
#
# | # | Dataset and source | Data abstraction | Two questions as tasks (action + target) |
# |---|---|---|---|
# | 1 | **World Development Indicators**, World Bank Open Data ([data.worldbank.org](https://data.worldbank.org/indicator/IT.NET.USER.ZS)) | Multidimensional table, static: keys *country* + *year*; values are quantitative indicators such as internet users (% of population) and GDP per capita. | *Summarize* the *trend* of internet use in Viet Nam and its ASEAN neighbours, 2000–2024. · *Discover* the *correlation* between GDP per capita and internet use across ASEAN countries. |
# | 2 | **Brazilian E-Commerce Public Dataset by Olist**, Kaggle ([kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)) | Several flat tables linked by keys (*order_id*, *customer_id*), static, about 99,000 orders 2016–2018: delivery timestamps (quantitative), review score 1–5 (ordinal), customer state (categorical). | *Discover* the *dependency* of the review score on late delivery. · *Compare* the *distribution* of delivery time across customer states. |
# | 3 | **Provincial statistics of Viet Nam**, National Statistics Office, formerly GSO ([nso.gov.vn](https://www.nso.gov.vn)) | Multidimensional table, static: keys *province* + *year*; values such as population and monthly income per capita (quantitative); region (categorical). Can be joined to province boundaries (geometry) for a map. | *Compare* the *extremes* of income per capita across provinces. · *Summarize* the *trend* of income by region. Check first: provinces were merged in 2025, so tables may use different province lists. |

# %% [markdown]
# ## Task 1 · Look
# First-look checklist (Tutorial 2, ch. 2): shape, head, info, describe,
# value_counts on EVERY text column, isna, duplicated, nunique.
# Then list at least SIX different problems in the table below.

# %%
# 1 · How big is the file, what does a row look like, is each column the type we expect?
print(raw.shape)
print(raw.head().to_string())
raw.info()
print(raw.nunique().to_string())   # 20 districts for a 10-district table: a first warning

# %%
# 2 · Text columns: every distinct value (repr shows hidden spaces) · number columns: min and max
for col in ["district", "payment", "customer_type", "member_tier", "status"]:
    print(raw[col].map(repr).value_counts(dropna=False).to_string(), "\n")
print(raw.describe().round(1).to_string())             # look at min and max first
print(raw["basket_value_vnd"].head(3).tolist())         # a number column stored as text

# %%
# 3 · Missing values, duplicates, and the two date formats
print(raw.isna().sum().to_string())
print("duplicate rows:", raw.duplicated().sum(), "| repeated order_id:", raw["order_id"].duplicated().sum())

slash = raw["order_time"].str.contains("/")
print("order_time written xx/xx/yyyy:", slash.sum(), "of", len(raw))
first = raw.loc[slash, "order_time"].str[:2].astype(int)
second = raw.loc[slash, "order_time"].str[3:5].astype(int)
print("first number > 12:", (first > 12).sum(), "| second number > 12:", (second > 12).sum(),
      "-> day first: dd/mm/yyyy")

odd = raw.loc[(raw["delivery_min"] <= 0) | (raw["delivery_min"] > 180), "delivery_min"]
print("impossible delivery times:", sorted(odd.tolist()))

# %% [markdown]
# **Problems found** (counts on the raw file, 5,973 rows)
#
# | # | Problem | Column | How we found it |
# |---|---|---|---|
# | 1 | 60 exact duplicate rows: 60 `order_id` appear twice | all, `order_id` | `raw.duplicated().sum()` |
# | 2 | 10 districts written 20 ways: extra space (`"Go Vap "`), capitals (`BINH THANH`), `Q1` / `Quận 1`, `Q7` / `Quận 7`, `Thu Duc` / `TP Thu Duc` (200 rows) | `district` | `nunique()`, `value_counts()` with `repr` |
# | 3 | E-wallet written 4 ways: `E-wallet`, `e-wallet`, `ewallet`, `Momo/ZaloPay` (81 rows) | `payment` | `value_counts()` |
# | 4 | Two date formats in one column: 45 rows `dd/mm/yyyy`, the rest `yyyy-mm-dd`; so the rows are not in time order either | `order_time` | `head()`, `str.contains("/")` |
# | 5 | A number stored as text with commas (`"140,000"`) | `basket_value_vnd` | `info()` shows text, `head()` |
# | 6 | Impossible delivery times: −12, −4, 0, 720, 999 and 1440 minutes | `delivery_min` | `describe()`: min and max |
# | 7 | 26 basket values missing | `basket_value_vnd` | `isna().sum()` |
# | 8 | Empty cells that are **not** errors: `member_tier` (4,164), `delivery_min` (312), `rating` (2,262). Task 2 explains why. | `member_tier`, `delivery_min`, `rating` | `isna().sum()`, then `pd.crosstab` in Task 2 |

# %% [markdown]
# ## Task 2 · Name
# **Dataset type:** a flat, static table (one row = one order), plus a lookup table of districts
# (one row = one district), joined on `district` (many orders to one district).
#
# | Column | Attribute type | Direction | Key / value | Notes on missing values |
# |---|---|---|---|---|
# | order_id | categorical (a name made of letters and digits) | – | **key** | none |
# | order_time | quantitative (time) | sequential; its hour and weekday are cyclic | value | none |
# | district | categorical | – | value (key to the district table) | none |
# | customer_type | categorical (new / returning / member) | – (could be read as ordinal by loyalty) | value | none |
# | member_tier | ordinal | sequential: Silver < Gold < Platinum | value | empty = **not applicable**: non-members |
# | payment | categorical | – | value | none |
# | items | quantitative (a count) | sequential | value | none |
# | basket_value_vnd | quantitative (VND) | sequential | value | 25 **not recorded** (after removing duplicates) |
# | status | categorical (delivered / cancelled) | – | value | none |
# | delivery_min | quantitative (minutes) | sequential | value | empty = **not applicable**: cancelled orders; 6 impossible values set to missing |
# | rating | ordinal (1–5) | sequential (or diverging around 3) | value | empty = **not given**: rating is optional |
# | zone *(joined)* | ordinal | sequential by distance: Central < Inner < Outer | value | none |
# | km_to_hub *(joined)* | quantitative (km) | sequential | value | none |

# %%
# Key: one order_id per order?
print("order_id repeats in the raw file:", raw["order_id"].duplicated().sum(),
      "(the duplicate rows; unique after cleaning, checked in Task 3)")

# Missing values: the same reason for member_tier and rating?
print(pd.crosstab(raw["customer_type"], raw["member_tier"].isna().map({True: "tier empty", False: "tier set"})))
print(pd.crosstab(raw["status"], raw["rating"].isna().map({True: "no rating", False: "rating"})))
print(pd.crosstab(raw["status"], raw["delivery_min"].isna().map({True: "no time", False: "time"})))

# Ordered categories (zone and weekday follow in Task 4, once those columns exist)
TIERS = ["Silver", "Gold", "Platinum"]
RATINGS = [1, 2, 3, 4, 5]


def make_ordered(df):
    """member_tier and rating as ordered categories. Used again on the clean table in Task 4."""
    df = df.copy()
    df["member_tier"] = pd.Categorical(df["member_tier"], TIERS, ordered=True)
    df["rating"] = pd.Categorical(df["rating"], RATINGS, ordered=True)
    return df


named = make_ordered(raw)
print(named["member_tier"].cat.categories.tolist(), "| ordered:", named["member_tier"].cat.ordered)
print(named["rating"].cat.categories.tolist(), "| ordered:", named["rating"].cat.ordered)

# %% [markdown]
# **Answers to the three questions**
#
# 1. **Key:** `order_id`. In the raw file it repeats 60 times, exactly the 60 duplicate rows; after
#    cleaning it is unique (the `assert` in Task 3 checks it).
# 2. **`member_tier` and `rating` are empty for different reasons.** `member_tier` is empty for exactly
#    the non-members: *not applicable*, so we keep it empty and never invent a tier. `rating` is empty
#    for every cancelled order and for about a third of delivered ones: *not given*, because rating is
#    optional. We keep it empty and do not fill it; in Q3 we remember that customers who rate may not
#    be typical.
# 3. **Ordered categories:** `member_tier` (Silver < Gold < Platinum) and `rating` (1 < … < 5),
#    converted by `make_ordered()`; plus `zone` (Central < Inner < Outer) and `weekday` (Mon → Sun),
#    created in Task 4.

# %% [markdown]
# ## Task 3 · Clean
# clean_orders(df) -> (clean_df, log), like clean_sales in Tutorial 2, Section 4.6.
# For every step: WHAT you did, HOW MANY rows it touched, WHY (remove / correct /
# set to missing / keep).

# %%
DISTRICT_FIX = {"Q1": "District 1", "Quận 1": "District 1",      # after strip + title case
                "Q7": "District 7", "Quận 7": "District 7",
                "Thu Duc": "Thu Duc City", "Tp Thu Duc": "Thu Duc City"}
E_WALLET = {"e-wallet", "ewallet", "momo/zalopay"}               # Momo and ZaloPay are e-wallets
MAX_DELIVERY_MIN = 180      # 3 hours: generous; real deliveries take at most about 70 minutes
TEXT_COLS = ["order_id", "district", "customer_type", "member_tier", "payment", "status"]


def clean_orders(df):
    """Return (clean DataFrame, log dict). Each step is one decision."""
    log = {"rows_in": len(df)}
    df = df.copy()

    # 1 · dates: two formats in one column -> parse each format separately
    slash = df["order_time"].str.contains("/")                  # dd/mm/yyyy HH:MM
    time = pd.to_datetime(df["order_time"].where(~slash), format="%Y-%m-%d %H:%M")
    time[slash] = pd.to_datetime(df.loc[slash, "order_time"], format="%d/%m/%Y %H:%M")
    df["order_time"] = time
    log["dates_in_dd/mm/yyyy"] = int(slash.sum())

    # 2 · text: spaces, capitals and spelling variants
    district_before, payment_before = df["district"], df["payment"]
    for col in TEXT_COLS:
        df[col] = df[col].str.strip()
    df["district"] = df["district"].str.title().replace(DISTRICT_FIX)
    log["district_variants_fixed"] = int((df["district"] != district_before).sum())
    df.loc[df["payment"].str.lower().isin(E_WALLET), "payment"] = "E-wallet"
    log["payment_variants_fixed"] = int((df["payment"] != payment_before).sum())

    # 3 · a number stored as text: "140,000" -> 140000
    df["basket_value_vnd"] = pd.to_numeric(df["basket_value_vnd"].str.replace(",", ""))

    # 4 · duplicates (only after the text is fixed)
    log["duplicates_removed"] = int(df.duplicated().sum())
    df = df.drop_duplicates()

    # 5 · impossible delivery times: the order happened, the time is wrong -> missing
    bad = (df["delivery_min"] <= 0) | (df["delivery_min"] > MAX_DELIVERY_MIN)
    log["impossible_delivery_set_missing"] = int(bad.sum())
    df.loc[bad, "delivery_min"] = np.nan

    # 6 · missing values kept on purpose (nothing is changed, only counted)
    log["missing_basket_kept"] = int(df["basket_value_vnd"].isna().sum())
    log["no_tier_non_member"] = int(df["member_tier"].isna().sum())
    log["no_delivery_time_cancelled"] = int((df["status"] == "cancelled").sum())
    log["no_rating_kept"] = int(df["rating"].isna().sum())

    log["rows_out"] = len(df)
    return df.sort_values("order_time").reset_index(drop=True), log


clean, log = clean_orders(raw)
print(pd.Series(log).to_string())

# %%
# Checks: what must be true after cleaning (an error here means a step went wrong)
assert clean["order_id"].is_unique                                # one row = one order
assert set(clean["district"]) == set(districts["district"])       # the 10 names of the table
assert clean["delivery_min"].dropna().between(0, MAX_DELIVERY_MIN).all()
assert (clean["member_tier"].isna() == (clean["customer_type"] != "member")).all()
assert clean.loc[clean["status"] == "cancelled", "delivery_min"].isna().all()
print(clean["district"].value_counts().to_string(), "\n")
print(clean["payment"].value_counts().to_string(), "\n")
print(clean.dtypes.to_string())

# %% [markdown]
# **Step-by-step justification** (rows counted on the raw file of 5,973 rows)
#
# | # | What we did | Rows | Why |
# |---|---|---|---|
# | 1 | Parsed `order_time`, which mixes two formats: `yyyy-mm-dd` and `dd/mm/yyyy` | 45 in `dd/mm/yyyy` | 24 of the 45 start with a number above 12 and none has a month above 12, so they are day-first. Parsing each format separately loses no row. |
# | 2 | Fixed `district` spellings (extra space, capitals, Q1 / Quận 1, Q7 / Quận 7, Thu Duc / TP Thu Duc) to the 10 names of the district table | 200 | Otherwise one district splits into several bars, and the merge in Task 4 cannot find their zone. |
# | 3 | Merged `payment` variants (e-wallet, ewallet, Momo/ZaloPay) into `E-wallet` | 81 | Same method, different spelling. Judgement call: Momo and ZaloPay are e-wallet brands (24 rows). Without this, Q2 understates the e-wallet share. |
# | 4 | Turned `basket_value_vnd` from text (`"140,000"`) into numbers | all rows | Text cannot be summed or averaged. |
# | 5 | Removed exact duplicate rows, **after** fixing the text | 60 | Each was a second copy of the same `order_id`; they would count orders twice. Fixing text first means no copy survives under another spelling. |
# | 6 | Set impossible `delivery_min` to missing: −12, −4, 0, 720, 999, 1440 | 6 | A delivery cannot take 0 minutes or a whole day; real ones take at most about 70 minutes. The orders did happen, so we keep the rows (district, payment, basket are still valid) and remove only the wrong time. |
# | 7 | Kept missing `basket_value_vnd` | 25 | Not recorded. Deleting the orders would hide real orders; filling 0 would be false. Basket statistics skip them. |
# | 8 | Kept empty `member_tier` | 4,123 | Not applicable: exactly the non-members. |
# | 9 | Kept empty `delivery_min` of cancelled orders | 306 | Not applicable: these orders were never delivered. |
# | 10 | Kept missing `rating` | 2,241 | Not given: rating is optional (and impossible for cancelled orders). Careful in Q3: customers who rate may not be typical. |
#
# Result: 5,973 rows in, **5,913 orders** out.

# %% [markdown]
# ## Task 4 · Reshape and combine
# Merge gomart_districts.csv (use validate=...), derive hour, weekday (ordered), month.
# Confirm that no order lost its zone in the merge.

# %%
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# many_to_one: many orders per district, exactly one row per district in the table
orders = clean.merge(districts, on="district", how="left", validate="many_to_one")
print("rows before / after the merge:", len(clean), "/", len(orders))
print("orders without a zone:", orders["zone"].isna().sum())

orders["zone"] = pd.Categorical(orders["zone"], ["Central", "Inner", "Outer"], ordered=True)
orders["hour"] = orders["order_time"].dt.hour
orders["weekday"] = pd.Categorical(orders["order_time"].dt.strftime("%a"), DAYS, ordered=True)
orders["month"] = orders["order_time"].dt.month

print(orders[["order_time", "district", "zone", "km_to_hub", "hour", "weekday", "month"]].head())
print(orders.groupby("zone", observed=True)["km_to_hub"].agg(["min", "max", "size"]))

orders = make_ordered(orders)                                  # member_tier, rating (Task 2)
orders.to_csv(HERE / "gomart_orders_clean.csv", index=False)
print("saved:", HERE / "gomart_orders_clean.csv", orders.shape)

# %% [markdown]
# `orders` is the table for Task 5: one row per order, with its zone and distance to the hub,
# plus `hour`, `weekday` (ordered Mon → Sun) and `month`. No order lost its zone in the merge.
# It is also saved as `gomart_orders_clean.csv` next to this notebook. A CSV forgets types: after
# `pd.read_csv` parse `order_time` again and re-create the ordered categories.
# For averages of `rating`, use `orders["rating"].astype(float)`.

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
# **Task:** Discover the relationship between delivery time
# and customer rating, and identify when ratings start to decline.
#
# **Chart and why:** A line chart shows average customer ratings
# across 10-minute delivery intervals, making it easy to identify
# the downward trend and an approximate threshold.
# Only delivered orders with valid times and ratings are included.

# %%
# Q3 - Delivery Time vs Customer Rating
# Use the cleaned dataset from Task 4

q3_data = pd.read_csv(HERE / "gomart_orders_clean.csv")

q3_data = q3_data[
    (q3_data["status"] == "delivered")
    & q3_data["delivery_min"].notna()
    & q3_data["rating"].notna()
].copy()

q3_data["rating"] = pd.to_numeric(q3_data["rating"])

# Group delivery times into 10-minute intervals
q3_data["time_bin"] = (
    q3_data["delivery_min"] // 10 * 10
).astype(int)

q3_summary = (
    q3_data.groupby("time_bin")
    .agg(
        avg_rating=("rating", "mean"),
        n_orders=("rating", "size")
    )
    .reset_index()
)

print(q3_summary)

# Plot
fig, ax = plt.subplots(figsize=(10, 5))

plot_data = q3_summary[q3_summary["n_orders"] >= 10]

ax.plot(
    plot_data["time_bin"] + 5,
    plot_data["avg_rating"],
    marker="o",
    linewidth=2
)

ax.set_xlabel("Delivery Time (minutes)")
ax.set_ylabel("Average Rating (1–5)")
ax.set_title("Customer Rating vs Delivery Time")
ax.set_ylim(1, 5)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.show()
# %% [markdown]
# **Interpretation:**
# Average customer ratings decline as delivery time increases.
# Ratings fall from 4.53 for deliveries taking 20–29 minutes
# to 3.87 at 30–39 minutes and 2.81 at 40–49 minutes.
# This suggests that ratings begin to decline noticeably
# around 30 minutes, with a sharper drop after 40 minutes.
# However, this is an association, not proof of causation.
# Since ratings are optional, selection bias may exist.
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
