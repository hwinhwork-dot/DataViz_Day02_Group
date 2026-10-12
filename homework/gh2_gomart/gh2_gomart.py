# This file is generated from GH2_TeamName.ipynb (the submitted notebook), cell by cell.
# VS Code runs each `# %%` block like a notebook cell. Edit the notebook, then regenerate this file.

# %% [markdown]
# # Group Homework 2 · GoMart deliveries
# **Data Visualization · UEH · Session 2** · team notebook
#
# | | |
# |---|---|
# | **Team** | *team name* |
# | **Status** | Formative: written feedback with the rubric in the brief (first step of the group project) |
# | **Submit** | File ▸ Download ▸ .ipynb as `GH2_TeamName.ipynb`, within 7 days on the LMS |
#
# Read the brief *Group Homework 2 · GoMart* first. All data is simulated.

# %% [markdown]
# ## Memo to the operations manager
#
# **Big Idea 1 · Riders at peak hours:** In my group's opinion, GoMart should move riders into 11–12h and 18–20h, because these five hours bring 46% of orders, deliveries then take 8 minutes longer, and only 40% of customers give 4–5 stars, against 65% at other hours.
#
# **Big Idea 2 · E-wallet:** The group also believes that GoMart should put its marketing behind e-wallets, because e-wallet overtook cash in March 2025, reached 60% of orders by December, and took almost two thirds of its gain from cash.
#
# The group proposes extra rider shifts at these peaks, starting with the Outer zone, and three months of 10% off the first three e-wallet orders plus double loyalty points for members.

# %%
# Task 6 · explanatory chart for the memo: one panel per Big Idea
# Reads the clean table saved in Task 4 (on a fresh run, run the whole notebook once first).
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

clean_csv = next((p for p in [Path("gomart_orders_clean.csv"),
                              Path("homework/gh2_gomart/gomart_orders_clean.csv")] if p.exists()), None)
if clean_csv is None:
    print("Run the whole notebook once (Task 4 saves gomart_orders_clean.csv), then re-run this cell.")
else:
    memo = pd.read_csv(clean_csv)
    PEAK = [11, 12, 18, 19, 20]                                    # lunch and dinner peaks (Q4)
    BLUE, GREY, LIGHT, INK, MUTED = "#1d56ba", "#5c5b57", "#c9c8c3", "#1d1d1b", "#52514e"
    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Big Idea 1 numbers: orders per hour, delivery time and good ratings at peak vs other hours
    by_hour = memo.groupby("hour").size()
    peak_share = memo["hour"].isin(PEAK).mean()
    done = memo.dropna(subset=["delivery_min"])
    at_peak = done["hour"].isin(PEAK)
    extra_min = done.loc[at_peak, "delivery_min"].median() - done.loc[~at_peak, "delivery_min"].median()
    rated = done.dropna(subset=["rating"])
    good_peak = (rated.loc[rated["hour"].isin(PEAK), "rating"] >= 4).mean()
    good_off = (rated.loc[~rated["hour"].isin(PEAK), "rating"] >= 4).mean()

    # Big Idea 2 numbers: monthly payment shares
    share = pd.crosstab(memo["month"], memo["payment"], normalize="index") * 100
    from_cash = (share.loc[1, "Cash"] - share.loc[12, "Cash"]) / (share.loc[12, "E-wallet"] - share.loc[1, "E-wallet"])
    first_ahead = int((share["E-wallet"] > share["Cash"]).idxmax())   # first month e-wallet leads cash

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.6), dpi=150,
                                   gridspec_kw={"width_ratios": [1.2, 1]})

    # ---- Panel 1 · orders per hour, the five peak hours in blue
    ax1.bar(by_hour.index, by_hour.values, width=0.75,
            color=[BLUE if h in PEAK else LIGHT for h in by_hour.index])
    ax1.set_xticks(by_hour.index, [f"{h}h" for h in by_hour.index], fontsize=8.5)
    ax1.set_ylabel("Orders in 2025")
    ax1.text(11.5, by_hour[[11, 12]].max() + 25, "lunch", ha="center", fontsize=9.5, style="italic", color=BLUE)
    ax1.text(19, by_hour[[18, 19, 20]].max() + 25, "dinner", ha="center", fontsize=9.5, style="italic", color=BLUE)
    ax1.set_ylim(0, by_hour.max() * 1.15)
    ax1.set_title(f"Big Idea 1 · {peak_share:.0%} of orders arrive in 5 peak hours",
                  loc="left", fontsize=12.5, fontweight="bold", color=INK, pad=40)
    ax1.text(0, 1.02, f"Orders per hour of day, 2025. At 11–12h and 18–20h deliveries take {extra_min:.0f} min longer\n"
             f"and only {good_peak:.0%} of ratings are 4–5 stars ({good_off:.0%} at other hours)",
             transform=ax1.transAxes, fontsize=9.5, style="italic", color=MUTED, va="bottom")

    # ---- Panel 2 · monthly e-wallet share, cash for contrast
    for method in ["Card", "Bank transfer"]:                       # context, no labels needed
        ax2.plot(share.index, share[method], color=LIGHT, lw=1.6)
    ax2.plot(share.index, share["Cash"], color=GREY, lw=1.8, ls="--")
    ax2.plot(share.index, share["E-wallet"], color=BLUE, lw=3.2, marker="o", ms=5.5, zorder=3)
    ax2.text(first_ahead, share.loc[first_ahead, "E-wallet"] + 9, f"E-wallet passes cash in {MONTHS[first_ahead - 1]}",
             color=BLUE, ha="center", va="bottom", fontsize=9.5, style="italic")
    ax2.text(1, share.loc[1, "E-wallet"] - 3, f"{share.loc[1, 'E-wallet']:.0f}%", color=BLUE,
             ha="center", va="top", fontsize=10, fontweight="bold")
    ax2.text(12.3, share.loc[12, "E-wallet"], f"E-wallet {share.loc[12, 'E-wallet']:.0f}%",
             color=BLUE, va="center", fontsize=10.5, fontweight="bold")
    ax2.text(12.3, share.loc[12, "Cash"], f"Cash {share.loc[12, 'Cash']:.1f}%", color=GREY, va="center", fontsize=9.5)
    ax2.text(12.3, (share.loc[12, "Card"] + share.loc[12, "Bank transfer"]) / 2, "Card, bank\ntransfer",
             color=MUTED, va="center", fontsize=9, linespacing=1.3)
    ax2.set_xticks(range(1, 13), MONTHS, fontsize=8.5)
    ax2.set_xlim(0.6, 14.4)
    ax2.set_ylim(0, 70)
    ax2.set_ylabel("Share of orders (%)")
    ax2.set_title("Big Idea 2 · E-wallet use doubled in 2025", loc="left",
                  fontsize=12.5, fontweight="bold", color=INK, pad=40)
    ax2.text(0, 1.02, f"Share of orders by payment method, 2025. {from_cash:.0%} of the e-wallet gain\n"
             f"came from cash; {100 - share.loc[12, 'E-wallet']:.0f}% of December orders still use another method",
             transform=ax2.transAxes, fontsize=9.5, style="italic", color=MUTED, va="bottom")

    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color("#a3a29d")
        ax.tick_params(colors=MUTED)
    fig.tight_layout(w_pad=3)
    plt.show()

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
# ## Setup
# In the repo the data is read from `data/raw`. In Colab, upload `gomart_orders_2025.csv` and `gomart_districts.csv` first (folder icon on the left, or `files.upload()`).

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
# ## Task 1 · Look
# Run the first-look checklist. Then fill the table of problems below.

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
# | order_id | categorical (a name made of letters and digits) | none | **key** | none |
# | order_time | quantitative (time) | sequential; its hour and weekday are cyclic | value | none |
# | district | categorical | none | value (key to the district table) | none |
# | customer_type | categorical (new / returning / member) | – (could be read as ordinal by loyalty) | value | none |
# | member_tier | ordinal | sequential: Silver < Gold < Platinum | value | empty = **not applicable**: non-members |
# | payment | categorical | none | value | none |
# | items | quantitative (a count) | sequential | value | none |
# | basket_value_vnd | quantitative (VND) | sequential | value | 25 **not recorded** (after removing duplicates) |
# | status | categorical (delivered / cancelled) | none | value | none |
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
# 3. **Ordered categories:** `member_tier` (Silver < Gold < Platinum) and `rating` (1 < 2 < 3 < 4 < 5),
#    converted by `make_ordered()`; plus `zone` (Central < Inner < Outer) and `weekday` (Mon to Sun),
#    created in Task 4.

# %% [markdown]
# ## Task 3 · Clean
# Write `clean_orders(df)` returning `(clean_df, log)`. Then justify every step in the Markdown cell below.

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
# plus `hour`, `weekday` (ordered Mon to Sun) and `month`. No order lost its zone in the merge.
# It is also saved as `gomart_orders_clean.csv` next to this notebook. A CSV forgets types: after
# `pd.read_csv` parse `order_time` again and re-create the ordered categories.
# For averages of `rating`, use `orders["rating"].astype(float)`.

# %% [markdown]
# ## Task 5 · From question to chart
# ### Q1 · Where are deliveries slow?
# *Task (action + target):* My group wants to **compare** the **distribution** of delivery time across zones and districts, and to **discover** how delivery time **depends** on the distance to the hub.
#
# *Chart and why:* My group used box plots by zone and by district. A box plot shows both the typical time and the spread of the times, so the places where customers wait longest stand out, and sorting the districts by median and highlighting the slowest one makes the ranking easy to read. A scatter plot of distance against delivery time, with a trend line, then shows whether customers who live far from the hub wait longer. The charts use the 5,601 delivered orders that have a valid delivery time.

# %%
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Exclude cancelled orders. Keep rows with missing distance for the category comparisons.
delivery_data = orders.dropna(subset=["delivery_min"]).copy()

# Set the required ordinal zone order.
zone_order = ["Central", "Inner", "Outer"]
delivery_data["zone"] = pd.Categorical(
    delivery_data["zone"],
    categories=zone_order,
    ordered=True,
)

# Find median delivery times to identify the slowest zone and district.
zone_medians = (
    delivery_data.dropna(subset=["zone"])
    .groupby("zone", observed=True)["delivery_min"]
    .median()
    .reindex(zone_order)
    .dropna()
)
district_medians = (
    delivery_data.dropna(subset=["district"])
    .groupby("district", observed=True)["delivery_min"]
    .median()
    .sort_values()
)

if zone_medians.empty or district_medians.empty:
    raise ValueError("Completed orders must include zone and district values for these comparisons.")

slowest_zone = zone_medians.idxmax()
slowest_district = district_medians.idxmax()

# Highlight the slowest zone and district; use neutral colors for the others.
zone_palette = {
    zone: ("#e68613" if zone == slowest_zone else "#aebbc4")
    for zone in zone_order
}
district_palette = {
    district: ("#e68613" if district == slowest_district else "#4c78a8")
    for district in district_medians.index
}
district_order = district_medians.index.tolist()

# Compare delivery-time distributions across zones and districts.
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.boxplot(
    data=delivery_data.dropna(subset=["zone"]),
    x="zone",
    y="delivery_min",
    order=zone_order,
    palette=zone_palette,
    ax=axes[0],
)
axes[0].set_title(f"Typical delivery times are longest in {slowest_zone}")
axes[0].set_xlabel("Delivery Zone")
axes[0].set_ylabel("Delivery Time (minutes)")

sns.boxplot(
    data=delivery_data.dropna(subset=["district"]),
    x="district",
    y="delivery_min",
    order=district_order,
    palette=district_palette,
    ax=axes[1],
)
axes[1].set_title(f"{slowest_district} has the longest typical delivery time")
axes[1].set_xlabel("District")
axes[1].set_ylabel("Delivery Time (minutes)")
axes[1].tick_params(axis="x", rotation=45)

fig.tight_layout()
plt.show()

# For the distance plot, only complete distance-time pairs can be shown.
distance_data = delivery_data.dropna(subset=["km_to_hub"]).copy()
if distance_data.empty:
    raise ValueError("No completed orders have a non-missing km_to_hub value.")

# Calculate the linear correlation and estimated change in minutes per kilometer.
pearson_r = distance_data["km_to_hub"].corr(distance_data["delivery_min"])
can_fit_line = (
    len(distance_data) >= 2
    and distance_data["km_to_hub"].nunique() > 1
)

if can_fit_line:
    minutes_per_km = (
        distance_data["delivery_min"].cov(distance_data["km_to_hub"])
        / distance_data["km_to_hub"].var()
    )

# Plot distance against delivery time, colored by zone.
fig, ax = plt.subplots(figsize=(9, 6))
sns.scatterplot(
    data=distance_data,
    x="km_to_hub",
    y="delivery_min",
    hue="zone",
    hue_order=zone_order,
    palette=zone_palette,
    alpha=0.7,
    ax=ax,
)

# Add a linear trendline when distance varies across at least two orders.
if can_fit_line:
    sns.regplot(
        data=distance_data,
        x="km_to_hub",
        y="delivery_min",
        scatter=False,
        color="black",
        line_kws={"linewidth": 2},
        ax=ax,
    )

if pd.notna(pearson_r):
    if pearson_r > 0:
        distance_finding = "delivery time tends to increase with distance"
    elif pearson_r < 0:
        distance_finding = "delivery time tends to decrease with distance"
    else:
        distance_finding = "there is no linear association with distance"
    distance_title = f"Distance relationship: {distance_finding} (r = {pearson_r:.2f})"
else:
    distance_finding = "a linear relationship with distance could not be estimated"
    distance_title = "Distance relationship could not be estimated"

ax.set_title(distance_title)
ax.set_xlabel("Distance from Hub (km)")
ax.set_ylabel("Delivery Time (minutes)")
ax.legend(title="Delivery Zone")
fig.tight_layout()
plt.show()

# Summarize the observed typical waits and the distance relationship.
if pd.notna(pearson_r) and can_fit_line:
    print(
        f"Typical delivery times are longest in {slowest_zone} "
        f"(median {zone_medians[slowest_zone]:.1f} minutes) and "
        f"{slowest_district} (median {district_medians[slowest_district]:.1f} minutes); "
        f"{distance_finding} (about {minutes_per_km:.1f} minutes per km, "
        f"Pearson r = {pearson_r:.2f})."
    )
else:
    print(
        f"Typical delivery times are longest in {slowest_zone} "
        f"(median {zone_medians[slowest_zone]:.1f} minutes) and "
        f"{slowest_district} (median {district_medians[slowest_district]:.1f} minutes); "
        f"{distance_finding}."
    )

# %% [markdown]
# #### Interpretation
#
# **Key finding:** Deliveries take longer in the Outer zone, especially in Thu Duc City, and delivery time rises with distance from the hub.
#
# **Zone and district boxplots:** Each box shows the middle 50% of delivery times, with the median line marking the typical time. Median delivery time increases from 28.2 minutes in Central to 35.2 in Inner and 47.7 in Outer. Thu Duc City is slowest at 51.7 minutes; District 1 is fastest at 26.7 minutes.
#
# **Distance scatter plot:** Each dot is an order; distance from the hub (km) is on the horizontal axis and delivery time (minutes) on the vertical axis. The upward trendline and Pearson correlation (r = 0.82) show a strong positive association; each additional kilometre corresponds to about 2.6 more delivery minutes in this dataset.
#
# This is an association, not proof that distance causes the delay. The zone boxes overlap, so distance does not explain every difference in delivery time.

# %% [markdown]
# ### Q2 · Is the move to e-wallet real?
# *Task (action + target):* Summarize the trend of monthly payment method shares across 12 months in 2025.
#
# *Chart and why:* Line chart. It conveys temporal continuity and slope across sequential months, demonstrating a persistent structural rise in e-wallet adoption while ruling out random fluctuation or temporary noise.

# %% [markdown]
# #### Comprehensive Synthesis & Strategic Interpretation
#
# **Key Finding: The shift toward E-wallet is real, substantial, and sustainable, rather than temporary noise.**
#
# 1. **A genuine, structural transition over time (Primary Chart 1):**
#    The upward trajectory of e-wallets reflects a permanent behavioral shift rather than random fluctuation. In January, Cash was the dominant payment method at 35.4%, while E-wallet accounted for 30.9%. Throughout 2025, E-wallet expanded progressively across every quarter, culminating in an overwhelming **60.0%** share by December, while Cash fell by more than half to an annual low of **16.5%**.
#
# 2. **Sustained financial contribution, not discount-driven noise (Supporting Chart 1):**
#    This transition is not an artificial spike driven merely by temporary discount vouchers or promotional campaigns. E-wallet constitutes the largest revenue stream for GoMart, generating **663.4 million VND** (**44.1%** of total system revenue). Crucially, its average basket value of **257,428 VND** is on par with Cash (257,917 VND), demonstrating that customers routinely make full-value purchases through e-wallets rather than reserving them solely for small-basket subsidized orders.
#
# 3. **Consistent penetration across all customer tiers (Supporting Chart 2):**
#    E-wallet adoption is widespread across all customer segments rather than isolated to a specific demographic. E-wallet commands the dominant share in every tier: Silver (45.5%), Gold (42.8%), and peaks at **49.6% among top-tier Platinum members**. Because GoMart's most loyal and highest-value customers demonstrate the highest adoption rate, e-wallet usage has clearly become an entrenched payment habit rather than transient deal-seeking behavior.

# %% [markdown]
# **Quick summary of raw data:** Prior to data visualization, the descriptive statistics tables below provide a comprehensive overview of the payment method distribution across time (months), member tiers, and total system transaction value.

# %%
# --- Q2: Summary Statistics & Chart ---
df = orders if "orders" in globals() else pd.read_csv(HERE / "gomart_orders_clean.csv")

# 1. Monthly payment shares (%)
pct_monthly = pd.crosstab(df["month"], df["payment"], normalize="index") * 100
print("--- 1. Monthly Payment Shares (%) ---\n", pct_monthly.round(1), "\n")

# 2. Payment shares by member tier (%)
members_df = df[df["customer_type"] == "member"]
tier_pct = pd.crosstab(members_df["member_tier"], members_df["payment"], normalize="index") * 100
print("--- 2. Payment Shares by Member Tier (%) ---\n", tier_pct.round(1), "\n")

# 3. Revenue summary by payment method
rev_summary = df.groupby("payment")["basket_value_vnd"].agg(
    orders="count", total_revenue_vnd="sum", avg_basket_vnd="mean"
).reset_index()
rev_summary["revenue_share_%"] = rev_summary["total_revenue_vnd"] / rev_summary["total_revenue_vnd"].sum() * 100

disp_rev = rev_summary.assign(
    total_rev=rev_summary["total_revenue_vnd"].map("{:,.0f} VND".format),
    avg_basket=rev_summary["avg_basket_vnd"].map("{:,.0f} VND".format),
    share=rev_summary["revenue_share_%"].map("{:.1f}%".format)
)[["payment", "orders", "total_rev", "avg_basket", "share"]]
print("--- 3. Revenue by Payment Method ---\n", disp_rev.to_string(index=False), "\n")

# %% [markdown]
# #### Primary Chart: Monthly share of payment methods
# *Objective:* Show that e-wallets grew steadily from 30.9% in Jan to 60.0% in Dec while cash fell from 35.4% to 16.5%, confirming a genuine structural shift rather than random noise.

# %%
# Monthly share of payment methods at GoMart in 2025 - Line Chart
p = pct_monthly
months = list(range(1, 13))
m_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

fig, ax = plt.subplots(figsize=(10, 5.8), dpi=150)
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

# Card and Bank transfer use hollow circle / square: shapes with no direction, so no marker
# looks like an arrow head pointing back to January.
styles = {
    "Cash":          {"color": "#5c5b57", "ls": "--", "marker": "s", "lw": 1.8, "ms": 5,   "zorder": 3},
    "Card":          {"color": "#807f7a", "ls": "-.", "marker": "o", "mfc": "white", "mew": 1.5, "lw": 1.8, "ms": 5.5, "zorder": 3},
    "Bank transfer": {"color": "#a6a5a0", "ls": ":",  "marker": "s", "mfc": "white", "mew": 1.5, "lw": 2.0, "ms": 5.5, "zorder": 3},
    "E-wallet":      {"color": "#1d56ba", "ls": "-",  "marker": "o", "lw": 3.2, "ms": 7,   "zorder": 6},
}

for method, s in styles.items():
    ax.plot(months, p[method], label=method, **s)

# Start annotations (Month 1)
ax.text(1, p["Cash"].iloc[0] + 2.2, f"{p['Cash'].iloc[0]:.1f}%", ha="center", va="bottom", fontsize=9, color="#5c5b57", fontweight="bold")
ax.text(1, p["E-wallet"].iloc[0] - 3.2, f"{p['E-wallet'].iloc[0]:.1f}%", ha="center", va="top", fontsize=9.5, color="#1d56ba", fontweight="bold")

# End annotations (Month 12): text only, right of each line's last point. No symbols and no
# connectors, so nothing looks like a line turning back. Card and Bank transfer end at almost the
# same value, so they share one two-line label.
ax.text(12.3, p["E-wallet"].iloc[-1], f"E-wallet: {p['E-wallet'].iloc[-1]:.1f}%", va="center", fontsize=10.5, fontweight="bold", color="#1d56ba")
ax.text(12.3, p["Cash"].iloc[-1], f"Cash: {p['Cash'].iloc[-1]:.1f}%", va="center", fontsize=9.5, fontweight="bold", color="#5c5b57")
ax.text(12.3, (p["Card"].iloc[-1] + p["Bank transfer"].iloc[-1]) / 2,
        f"Card: {p['Card'].iloc[-1]:.1f}%\nBank transfer: {p['Bank transfer'].iloc[-1]:.1f}%",
        va="center", fontsize=9.5, color="#52514e", linespacing=1.4)

# Axis and grid styling
ax.set(xticks=months, xticklabels=m_labels, ylabel="Share of orders (%)", ylim=(0, 70), xlim=(0.65, 15.6))
ax.yaxis.grid(True, linestyle=":", alpha=0.5, color="#d9d8d3")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ["left", "bottom"]: ax.spines[s].set_color("#a3a29d")

leg = ax.legend(loc="upper left", frameon=True, framealpha=0.9, edgecolor="#e0dfdb", fontsize=9.5, labelspacing=0.45)
leg.get_texts()[3].set_weight("bold")
leg.get_texts()[3].set_color("#1d56ba")

ax.set_title("Monthly share of payment methods at GoMart in 2025", fontsize=12.5, fontweight="bold", pad=22, loc="left", color="#1d1d1b")
ax.text(0, 1.02, "Summary of 5,913 delivered orders across 12 months (January to December 2025)",
        transform=ax.transAxes, fontsize=9.5, style="italic", color="#52514e", va="bottom")

plt.tight_layout()
Path("outputs/figures").mkdir(parents=True, exist_ok=True)
plt.savefig("outputs/figures/q2_ewallet_trend.png", dpi=200, bbox_inches="tight")
plt.show()

# %% [markdown]
# #### Supporting Chart 1: Total revenue by payment method
# *Objective:* Show that e-wallets command the highest total revenue (44.1%, >663M VND), refuting concerns that e-wallets are limited to small baskets.

# %%
rev = df.groupby("payment")["basket_value_vnd"].sum().reset_index(name="total_rev")
rev["pct"] = rev["total_rev"] / rev["total_rev"].sum() * 100
rev["million_vnd"] = rev["total_rev"] / 1e6
rev = rev.sort_values("total_rev", ascending=True)

fig, ax = plt.subplots(figsize=(9, 4.2), dpi=150)
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

bars = ax.barh(rev["payment"], rev["million_vnd"], color=["#8c8b86", "#8c8b86", "#5c5b57", "#1d56ba"], height=0.55)
for bar, (_, row) in zip(bars, rev.iterrows()):
    is_ew = (row["payment"] == "E-wallet")
    ax.text(bar.get_width() + 12, bar.get_y() + bar.get_height() / 2,
            f"{row['million_vnd']:,.1f}M VND ({row['pct']:.1f}%)",
            va="center", fontsize=9.5, fontweight="bold" if is_ew else "normal",
            color="#1d56ba" if is_ew else "#333333")

ax.set(xlim=(0, 820), xlabel="Total revenue (Million VND)")
ax.xaxis.grid(True, linestyle=":", alpha=0.5, color="#d9d8d3")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ["left", "bottom"]: ax.spines[s].set_color("#a3a29d")

ax.set_title("Total revenue by payment method at GoMart in 2025", fontsize=12.5, fontweight="bold", pad=22, loc="left", color="#1d1d1b")
ax.text(0, 1.02, "Aggregated over 5,913 orders (Total system revenue: ~1.5B VND)",
        transform=ax.transAxes, fontsize=9.5, style="italic", color="#52514e", va="bottom")

plt.tight_layout()
Path("outputs/figures").mkdir(parents=True, exist_ok=True)
plt.savefig("outputs/figures/q2_revenue_by_payment.png", dpi=200, bbox_inches="tight")
plt.show()

# %% [markdown]
# #### Supporting Evidence 2 · Payment shares across member tiers
# *Objective:* Confirm that e-wallet adoption spans all tiers and peaks among Platinum members (49.6%), disproving one-off discount hunting.

# %%
tiers = ["Silver", "Gold", "Platinum"]
x, width = np.arange(len(tiers)), 0.18
offsets = [-1.5, -0.5, 0.5, 1.5]
colors = {"Cash": "#5c5b57", "Card": "#807f7a", "Bank transfer": "#a6a5a0", "E-wallet": "#1d56ba"}

fig, ax = plt.subplots(figsize=(9.5, 4.8), dpi=150)
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

for off, (m, c) in zip(offsets, colors.items()):
    bars = ax.bar(x + off * width, tier_pct.loc[tiers, m], width, label=m, color=c)
    if m == "E-wallet":
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.2, f"{b.get_height():.1f}%",
                    ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=c)

ax.set(xticks=x, xticklabels=tiers, ylabel="Share of orders (%)", ylim=(0, 70))
ax.yaxis.grid(True, linestyle=":", alpha=0.5, color="#d9d8d3")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ["left", "bottom"]: ax.spines[s].set_color("#a3a29d")

leg = ax.legend(loc="upper left", frameon=True, framealpha=0.9, edgecolor="#e0dfdb", fontsize=9)
leg.get_texts()[3].set_weight("bold")
leg.get_texts()[3].set_color("#1d56ba")

ax.set_title("Payment method shares across member tiers at GoMart in 2025", fontsize=12.5, fontweight="bold", pad=22, loc="left", color="#1d1d1b")
ax.text(0, 1.02, "Platinum members use e-wallets the most (49.6%), followed by Silver (45.5%) and Gold (42.8%)",
        transform=ax.transAxes, fontsize=9.5, style="italic", color="#52514e", va="bottom")

plt.tight_layout()
Path("outputs/figures").mkdir(parents=True, exist_ok=True)
plt.savefig("outputs/figures/q2_payment_by_tier.png", dpi=200, bbox_inches="tight")
plt.show()

# %% [markdown]
# ### Q3 · Do slow deliveries cost good ratings?
# *Task (action + target):* My group wants to **discover** how customer rating **depends** on delivery time, and to **locate** the delivery time at which ratings start to fall.
#
# *Chart and why:* My group chose a line chart. The delivery times are grouped into ordered 10-minute bands, so a connected line shows the direction and the steepness of the change from one band to the next. The line also makes the point where ratings start to fall easy to see. The chart uses only the 3,669 delivered orders that have both a valid delivery time and a rating.

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
# #### Interpretation
#
# **Key finding:** In my group's opinion, slow deliveries do cost good ratings. Ratings stay high up to about 30 minutes, and then they fall quickly.
#
# Orders that arrive in under 30 minutes receive an average of 4.5 to 4.7 stars. The drop starts at about 30 minutes: the average falls from 4.53 stars for deliveries of 20 to 29 minutes to 3.87 stars for 30 to 39 minutes, and to 2.81 stars for 40 to 49 minutes. Customers therefore take away more than one and a half stars within 20 minutes. Beyond 50 minutes, the average stays at about 2.2 to 2.3 stars.
#
# My group reads this result with three cautions. First, the chart shows an association, so it does not prove that slow delivery causes low ratings. Second, a 1–5 rating is ordinal, so the average only summarises the answers, and the trend matters more than the exact decimals. Third, only about two thirds of delivered orders were rated, so the customers who rate may not be typical.

# %% [markdown]
# ### Q4 · When are the peaks?
#
# **Task (action + target):** Identify the weekday–hour slots with the highest order volume to plan rider shifts.
#
# **What the question asks:** The operations manager needs to know *when* orders concentrate — which hours of the day and which days of the week see the most demand — so rider shifts can be scheduled to match. A mismatch between rider supply and order demand means either long customer wait times (understaffed peaks) or idle riders (overstaffed lulls).
#
# **Our approach — three complementary charts instead of one dense heatmap:**
#
# A raw 7 × 24 heatmap packs 168 cells into one view. While complete, it overwhelms the reader — every cell competes for attention and the actionable patterns drown in detail. We decompose the question into three layers, each answering a progressively more specific sub-question:
#
# | Chart | Sub-question | Form | Why this form |
# |---|---|---|---|
# | **1 — Hourly demand profile** | *What time of day is busiest?* | Vertical bar chart | Magnitude comparison across 24 ordered hours; height encodes volume directly |
# | **2 — Daily demand profile** | *Which weekdays need more riders?* | Horizontal bar chart | Magnitude comparison across 7 days; easy to read day labels |
# | **3 — Peak-window heatmap** | *Within busy hours, which day × hour slots are hottest?* | Annotated heatmap (10:00–21:00 only) | Two-dimensional grid with exact counts; focusing on the active 12-hour window removes noise from empty overnight cells |
#
# The reader first sees the overall patterns (Charts 1 & 2), then drills into the specific day–hour interaction (Chart 3).

# %% [markdown]
# #### Comprehensive Synthesis & Strategic Interpretation
#
# **Key Finding: Order demand follows a clear double-peak pattern — a strong evening surge (17:00–20:00) and a moderate lunch bump (11:00–13:00) — consistent across all weekdays, with Friday and Saturday showing the highest overall volumes.**
#
# 1. **Evening dominance is unmistakable (Chart 1):** The 19:00 hour alone accounts for 674 orders across the week — roughly 2.4× the quietest daytime hour. The evening block (17:00–20:00) contains the four busiest hours, indicating the primary demand window for rider scheduling.
#
# 2. **Lunch provides a secondary, predictable bump (Chart 1):** A clear but smaller spike at 12:00 (551 orders) means the midday window also warrants dedicated shift coverage, though at roughly 80% of the evening peak intensity.
#
# 3. **Weekday variation is small but consistent (Chart 2):** Friday (869) and Saturday (862) carry the highest daily volumes, while Thursday is the quietest (815). The ~6.6% spread between busiest and quietest days suggests a roughly even weekly distribution, though Friday–Saturday staffing can be slightly boosted.
#
# 4. **The interaction reveals specific hotspots (Chart 3):** Tuesday 19:00 is the single busiest slot (112 orders) despite Tuesday not being the busiest day overall — the 19:00 hour concentrates demand regardless of the day. Saturday and Sunday evenings are also consistently heavy. These specific peaks help fine-tune shift scheduling beyond the general "evenings are busy" insight.

# %% [markdown]
# **Quick summary of raw data:** The tables below summarize order counts by hour and by weekday before visualization, giving the exact numbers behind the charts.

# %%
# --- Q4: Data Preparation & Summary Statistics ---
df = orders.copy() if "orders" in globals() else pd.read_csv(HERE / "gomart_orders_clean.csv")

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
df["weekday"] = pd.Categorical(df["weekday"].astype(str).str[:3], DAYS, ordered=True)
df["hour"] = df["hour"].astype(int)

counts = pd.crosstab(df["weekday"], df["hour"]).reindex(index=DAYS, columns=range(24), fill_value=0)
assert counts.shape == (7, 24)
assert int(counts.values.sum()) == len(df)

hourly = counts.sum(axis=0)
daily = counts.sum(axis=1)

print("--- 1. Orders by Hour of Day ---")
print(hourly.to_frame("orders").T.to_string(), "\n")

print("--- 2. Orders by Weekday ---")
print(daily.to_string(), "\n")

peak_val = int(counts.values.max())
peak_slots = [(d, int(h)) for d in DAYS for h in range(24) if counts.loc[d, h] == peak_val]
print(f"Peak slot(s): {', '.join(f'{d} {h:02d}:00' for d,h in peak_slots)} = {peak_val} orders")
print(f"Busiest hour overall: {hourly.idxmax():02d}:00 ({hourly.max()} orders)")
print(f"Busiest day overall:  {daily.idxmax()} ({daily.max()} orders)")
print(f"Total orders plotted: {int(counts.values.sum()):,}")

out_dir = Path("outputs/figures")
out_dir.mkdir(parents=True, exist_ok=True)

# %% [markdown]
# #### Chart 1: Hourly demand profile across the week
# *Objective:* Reveal the daily rhythm — which hours concentrate the most orders — so the manager knows *when* during the day to schedule peak rider shifts.

# %%
# Chart 1: Orders by hour of day (vertical bar chart)
h_labels = [f"{h:02d}" for h in range(24)]
top3_hours = hourly.nlargest(3).index.tolist()
colors_h = ["#1d56ba" if h in top3_hours else "#b0afaa" for h in range(24)]

fig, ax = plt.subplots(figsize=(11, 5), dpi=150)
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

bars = ax.bar(range(24), hourly.values, color=colors_h, width=0.7,
              edgecolor="white", linewidth=0.5)

for h in top3_hours:
    ax.text(h, hourly[h] + 12, f"{hourly[h]}", ha="center", va="bottom",
            fontsize=10, fontweight="bold", color="#1d56ba")
for h in range(24):
    if h not in top3_hours and hourly[h] > 300:
        ax.text(h, hourly[h] + 12, f"{hourly[h]}", ha="center", va="bottom",
                fontsize=8.5, color="#5c5b57")

ax.set(xticks=range(24), xticklabels=h_labels, xlabel="Hour of day",
       ylabel="Total orders (all weekdays)", ylim=(0, hourly.max() * 1.18))
ax.yaxis.grid(True, linestyle=":", alpha=0.5, color="#d9d8d3")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ["left", "bottom"]: ax.spines[s].set_color("#a3a29d")

ax.axvspan(17.5, 20.5, alpha=0.07, color="#1d56ba", zorder=0)
ax.text(19, hourly.max() * 1.12, "Evening peak\n(18:00–20:00)", ha="center",
        fontsize=9, color="#1d56ba", fontstyle="italic")
ax.axvspan(10.5, 13.5, alpha=0.05, color="#5c5b57", zorder=0)
ax.text(12, max(hourly[11], hourly[12], hourly[13]) * 1.15, "Lunch bump", ha="center",
        fontsize=8.5, color="#5c5b57", fontstyle="italic")

ax.set_title("Order volume by hour of day at GoMart in 2025",
             fontsize=12.5, fontweight="bold", pad=22, loc="left", color="#1d1d1b")
ax.text(0, 1.02,
        f"Top 3 hours highlighted in blue — all {len(df):,} cleaned orders aggregated across 7 weekdays",
        transform=ax.transAxes, fontsize=9.5, style="italic", color="#52514e", va="bottom")

plt.tight_layout()
plt.savefig(out_dir / "q4_hourly_demand.png", dpi=200, bbox_inches="tight")
print("Saved:", out_dir / "q4_hourly_demand.png")
plt.show()

# %% [markdown]
# #### Chart 2: Daily demand profile across the week
# *Objective:* Show which weekdays carry the heaviest order load, informing day-differentiated staffing decisions.

# %%
# Chart 2: Orders by weekday (horizontal bar chart)
top2_days = daily.nlargest(2).index.tolist()
colors_d = ["#1d56ba" if d in top2_days else "#b0afaa" for d in DAYS]

fig, ax = plt.subplots(figsize=(9, 4.2), dpi=150)
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

bars = ax.barh(DAYS[::-1], daily.values[::-1], color=colors_d[::-1], height=0.55,
               edgecolor="white", linewidth=0.5)

for bar, val, day in zip(bars, daily.values[::-1], DAYS[::-1]):
    is_top = day in top2_days
    ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height() / 2,
            f"{val:,} orders", va="center", fontsize=10,
            fontweight="bold" if is_top else "normal",
            color="#1d56ba" if is_top else "#5c5b57")

ax.set(xlim=(0, daily.max() * 1.25), xlabel="Total orders (all hours)")
ax.xaxis.grid(True, linestyle=":", alpha=0.5, color="#d9d8d3")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ["left", "bottom"]: ax.spines[s].set_color("#a3a29d")

ax.set_title("Order volume by weekday at GoMart in 2025",
             fontsize=12.5, fontweight="bold", pad=22, loc="left", color="#1d1d1b")
ax.text(0, 1.02,
        f"Top 2 days highlighted — all {len(df):,} orders aggregated across 24 hours",
        transform=ax.transAxes, fontsize=9.5, style="italic", color="#52514e", va="bottom")

plt.tight_layout()
plt.savefig(out_dir / "q4_daily_demand.png", dpi=200, bbox_inches="tight")
print("Saved:", out_dir / "q4_daily_demand.png")
plt.show()

# %% [markdown]
# #### Chart 3: Peak-window heatmap (10:00–21:00)
# *Objective:* Zoom into the 12-hour active window where the vast majority of orders occur. Annotated cell values remove guesswork — the reader sees exact counts, not just colour shading.

# %%
# Chart 3: Focused heatmap — only hours 10-21, annotated with counts
from matplotlib.colors import LinearSegmentedColormap

focus_hours = list(range(10, 22))
focus = counts[focus_hours]

cmap = LinearSegmentedColormap.from_list("gomart", ["#f4f3ef", "#a9c0e2", "#1d56ba"])
fig, ax = plt.subplots(figsize=(12, 4.8), dpi=150)
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

im = ax.imshow(focus.values, aspect="auto", cmap=cmap, origin="upper")

vmax = focus.values.max()
for i in range(len(DAYS)):
    for j in range(len(focus_hours)):
        val = focus.values[i, j]
        text_color = "white" if val > vmax * 0.6 else "#1d1d1b"
        weight = "bold" if val == vmax else "normal"
        ax.text(j, i, str(val), ha="center", va="center",
                fontsize=9, color=text_color, fontweight=weight)

for (d, h) in peak_slots:
    if h in focus_hours:
        ax.add_patch(plt.Rectangle((focus_hours.index(h) - 0.5, DAYS.index(d) - 0.5),
                                   1, 1, fill=False, edgecolor="#db7043", linewidth=2.4))

ax.set_xticks(range(len(focus_hours)))
ax.set_xticklabels([f"{h:02d}:00" for h in focus_hours], fontsize=9)
ax.set_yticks(range(7))
ax.set_yticklabels(DAYS, fontsize=10)
ax.set_xticks(np.arange(-0.5, len(focus_hours), 1), minor=True)
ax.set_yticks(np.arange(-0.5, 7, 1), minor=True)
ax.grid(which="minor", color="white", linewidth=1.2)
ax.tick_params(which="minor", length=0)
ax.set_xlabel("Hour of day (10:00–21:00)", fontsize=11)

cbar = fig.colorbar(im, ax=ax, pad=0.015, shrink=0.85)
cbar.set_label("Orders", fontsize=10)
cbar.outline.set_visible(False)

peak_desc = ", ".join(f"{d} {h:02d}:00" for d, h in peak_slots)
ax.set_title(f"Order heatmap — active hours only (peak: {peak_desc}, {peak_val} orders)",
             fontsize=12.5, fontweight="bold", pad=22, loc="left", color="#1d1d1b")
pct_in_window = focus.values.sum() / counts.values.sum() * 100
ax.text(0, 1.02,
        f"This 12-hour window contains {pct_in_window:.0f}% of all orders — "
        f"cell values show exact counts; orange border = busiest slot",
        transform=ax.transAxes, fontsize=9.5, style="italic", color="#52514e", va="bottom")

plt.tight_layout()
plt.savefig(out_dir / "q4_peak_heatmap.png", dpi=200, bbox_inches="tight")
print("Saved:", out_dir / "q4_peak_heatmap.png")
plt.show()

# %% [markdown]
# #### Detailed Interpretation
#
# **Reading the charts together — from general pattern to specific hotspots:**
#
# **Chart 1 (Hourly profile)** reveals a clear double-peak daily rhythm:
# - **Evening surge (17:00–20:00):** The four busiest hours of the day. Hour 19:00 alone has 674 orders across the week — about 11.4% of all orders concentrated in a single hour. This is the primary demand window and should receive the highest rider allocation.
# - **Lunch bump (11:00–13:00):** A moderate but consistent secondary peak. Hour 12:00 records 551 orders — substantial enough to justify dedicated midday coverage, though at roughly 80% of the evening peak intensity.
# - **Quiet periods:** Before 08:00 and after 22:00, demand drops sharply. These hours need minimal rider staffing.
#
# **Chart 2 (Daily profile)** shows a relatively even distribution across weekdays:
# - **Friday** (869) and **Saturday** (862) are the busiest days. **Thursday** is the quietest (815).
# - The spread between busiest and quietest is only ~6.6%, meaning daily volume is fairly stable. However, Friday–Saturday staffing can still be slightly boosted to handle the higher load.
# - Weekend behaviour: Saturday is high, but Sunday drops to mid-range (853) — the "weekend" is not uniformly busy.
#
# **Chart 3 (Peak-window heatmap)** pinpoints the specific day × hour hotspots:
# - **Tuesday 19:00** is the single busiest cell (112 orders), followed by Thursday 19:00 (104) and then Wednesday 18:00 and Saturday 19:00 (both 98).
# - The evening dominance holds every day of the week — there is no weekday where lunch overtakes evening.
# - The 19:00 column is the darkest across the entire grid, confirming it as the universal peak hour regardless of day.
#
# **Operational recommendation:** Weight rider shifts toward 17:00–20:00 every day, with slight extra allocation on Fridays and Saturdays. A secondary shift covering 11:00–13:00 captures the lunch demand. Before 08:00 and after 22:00, a skeleton crew suffices.
#
# *All 5,913 cleaned orders for 2025 are counted (delivered and cancelled alike). Source: gomart_orders_clean.csv (Task 4).*

# %% [markdown]
# ## Task 7 · Team and AI
# | Member | What they did | Share of work |
# |---|---|---|
# | Nguyễn Hoàng Minh (leader) | Hoàng Minh worked on Tasks 1 to 4 with Nhã Đoan. Hoàng Minh also managed the repository, put everyone's parts into one notebook and led the memo. | 20% |
# | Trần Nhã Đoan | Nhã Đoan worked on Tasks 1 to 4 with Hoàng Minh: looking at the raw data, naming the columns, cleaning the file and joining the district table. | 20% |
# | Phạm Quang Minh | Quang Minh answered Q1: where deliveries are slow, by zone, by district and by distance to the hub. | 15% |
# | Trần Nguyễn Thanh Thảo | Thảo answered Q2: whether the move to e-wallet payments is real. | 15% |
# | Nguyễn Minh Nguyệt | Minh Nguyệt answered Q3: whether slow deliveries cost good ratings. | 15% |
# | Phạm Tuấn Anh | Tuấn Anh answered Q4: when the order peaks happen. | 15% |

# %%
AI_USE = """
Tool(s) used:
My group used Claude Code, an AI assistant from Anthropic. It worked inside our project folder, so it could read our files and run our code.

What we asked:
My group asked the assistant to go through the raw GoMart file and tell us what was wrong with it. It found duplicate orders, district and payment names written in different ways, two date formats in one column, basket values saved as text, delivery times that cannot be true, and empty cells. Then my group asked it for ways to clean each problem, and it explained the choices, for example why an order stays in the data when only its delivery time is wrong. We also asked it to write a first draft of the cleaning code, the code that joins the district table, and the tables in Tasks 0, 1 and 2. For the memo, we told it which two ideas the group chose, and it wrote the first wording and the chart. Later we asked it to rewrite the explanation of Q3, to change the markers in the Q2 chart, and to help us put the members' work into one notebook.

What we checked or changed ourselves:
My group chose the two Big Ideas of the memo. The first draft did not convince us, so we asked for another one with more facts from the charts. The assistant checked each number in the memo against the cleaned data file, and my group read every draft and asked for changes until we agreed with it. Members wrote Q1 to Q4 on their own branches and kept their own results. The assistant did not change any number or chart in Q1 to Q4. The only change to a member's chart was the Q2 markers, because the group thought the triangle looked like an arrow.
"""
print(AI_USE)
