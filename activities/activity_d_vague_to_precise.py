# Session 2 · Activity D · From vague to precise (slide 44)
#   Four vague requests from the manager. Each row: what the manager says -> the precise
#   task (action + target + data) -> a small chart, drawn from the sales file, that answers it.
#   Request 2 hides two tasks, so it gets two charts. Request 3 asks about "last month's
#   numbers", so it uses the raw export as the manager received it (December 2025).
# Needs: data/raw/phocaphe_sales_clean.csv and phocaphe_sales_messy.csv.
# Run from VS Code, or: python activities/activity_d_vague_to_precise.py

import sys
from pathlib import Path
from textwrap import wrap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # so `src` can be imported
from src.style import (BLUE, DATA_DIR, GREY, HAIR, INK, MUTED, NAMES, ORANGE, PAPER, WASH,
                       canvas, footer, headline, save, use_style)

FOCUS = "Thao Dien"
TET = [pd.Timestamp("2024-02-10"), pd.Timestamp("2025-01-29")]   # Lunar New Year days
LIGHT = "#cfcec9"                                               # context lines and bars

clean = pd.read_csv(DATA_DIR / "phocaphe_sales_clean.csv", parse_dates=["date"])
raw = pd.read_csv(DATA_DIR / "phocaphe_sales_messy.csv", parse_dates=["date"])
day = (clean.groupby(["date", "branch"], as_index=False)
            .agg(units=("units", "sum"), revenue=("revenue_mvnd", "sum"), promo=("promo", "first")))
day["weekend"] = day["date"].dt.dayofweek >= 5

# 1 · "Show me the sales data" -> the chain's monthly revenue
monthly = clean.set_index("date")["revenue_mvnd"].resample("MS").sum()

# 2 · "How is the new branch doing?" -> (a) revenue per day open, (b) its monthly trend
per_branch = day.groupby("branch").agg(revenue=("revenue", "sum"), days_open=("date", "nunique"))
per_day = (per_branch["revenue"] / per_branch["days_open"]).sort_values()
rank_day = int((per_day > per_day[FOCUS]).sum()) + 1
branch_month = (clean.groupby([pd.Grouper(key="date", freq="MS"), "branch"])["revenue_mvnd"]
                     .sum().unstack())
td = branch_month[FOCUS].dropna()
smallest = branch_month.drop(columns=FOCUS).mean().idxmin()
months_to_pass = int(np.argmax(td.values > branch_month.loc[td.index, smallest].values)) + 1
print(f"2 · {FOCUS}: {per_day[FOCUS]:.1f} million VND per day open, rank {rank_day} of 6; "
      f"above {smallest} from month {months_to_pass}")

# 3 · "Anything strange last month?" -> each December day vs that branch's usual day
dec = raw[raw["date"] >= "2025-12-01"].copy()
dec["branch"] = dec["branch"].str.strip().str.title()          # same names as the clean file
dec_day = dec.groupby(["date", "branch"], as_index=False)["revenue_mvnd"].sum()
weekend = dec_day["date"].dt.dayofweek >= 5
usual = dec_day.groupby(["branch", weekend])["revenue_mvnd"].transform("median")
dec_day["gap"] = dec_day["revenue_mvnd"] / usual - 1            # weekdays vs weekdays, weekends vs weekends
spread = 1.4826 * (dec_day["gap"] - dec_day["gap"].median()).abs().median()   # robust SD
band = 4 * spread                                               # beyond this = strange
strange = dec_day[dec_day["gap"].abs() > band]
twice = dec[dec.duplicated(keep=False)].drop_duplicates()
cause = {}
for row in strange.itertuples():
    hit = twice[(twice["date"] == row.date) & (twice["branch"] == row.branch)]
    cause[row.Index] = (f"{hit['category'].iloc[0]} row entered twice" if len(hit)
                        else "no duplicate: ask the branch")
print(f"3 · usual range ±{band:.0%}; strange days:")
for row in strange.itertuples():
    print(f"    {row.date:%d %b} {row.branch} {row.gap:+.0%}: {cause[row.Index]}")
dedup = dec.drop_duplicates().groupby(["date", "branch"], as_index=False)["revenue_mvnd"].sum()
dedup_usual = dedup.groupby(["branch", dedup["date"].dt.dayofweek >= 5])["revenue_mvnd"].transform("median")
print(f"    after removing duplicate rows: "
      f"{int(((dedup['revenue_mvnd'] / dedup_usual - 1).abs() > band).sum())} strange days left")

# 4 · "Do promotions work?" -> promo days vs similar days (same branch, month, weekday/weekend)
near_tet = day["date"].apply(lambda d: min(abs((d - t).days) for t in TET)) <= 9
fair = day[~near_tet].assign(month=lambda d: d["date"].dt.to_period("M"))
cells = (fair.groupby(["branch", "month", "weekend", "promo"])[["units", "revenue"]].mean()
             .unstack("promo").dropna())
lift = pd.Series({m: (cells[(m, True)] / cells[(m, False)] - 1).mean() for m in ("units", "revenue")})
price = clean.assign(p=clean["revenue_mvnd"] / clean["units"]).groupby("promo")["p"].mean()
cheaper = 1 - price[True] / price[False]
print(f"4 · promo vs similar days: items {lift['units']:+.1%}, revenue {lift['revenue']:+.1%}; "
      f"price per item {cheaper:.0%} lower\n")


# ---------------------------------------------------------------------------
# Layout: three columns, one row per request (inches from the top of the figure)
# ---------------------------------------------------------------------------
W, H = 16.0, 15.1
X_ASK, X_TASK, X_CHART = 0.5, 4.15, 8.5


def add_axes(fig, x, top, w, h):
    return fig.add_axes([x / W, (H - top - h) / H, w / W, h / H])


def chart_title(cv, x, top, title, note):
    cv.text(x, H - top, title, fontsize=12.5, fontweight="bold", va="top")
    cv.text(x, H - top - 0.27, note, fontsize=9.5, style="italic", color=MUTED, va="top")


def plain(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(GREY)
    ax.tick_params(labelsize=9.5, length=3, color=GREY)


def ask(cv, top, n, quote, hint):
    cv.text(X_ASK, H - top, str(n), fontsize=22, fontweight="bold", color=GREY, va="top")
    lines = wrap(f"“{quote}”", 24)
    for k, line in enumerate(lines):
        cv.text(X_ASK + 0.45, H - top - 0.02 - k * 0.32, line, fontsize=15, style="italic", va="top")
    cv.text(X_ASK + 0.45, H - top - 0.15 - len(lines) * 0.32, hint, fontsize=9.5, color=MUTED,
            va="top")


def task(cv, top, sentence, action, target, idiom, label=None):
    y = H - top
    if label:
        cv.text(X_TASK, y, label, fontsize=10.5, fontweight="bold", color=MUTED, va="top")
        y -= 0.27
    lines = wrap(sentence, 44)
    cv.text(X_TASK, y, "\n".join(lines), fontsize=11.5, va="top", linespacing=1.3)
    y -= 0.23 * len(lines) + 0.12
    cv.text(X_TASK, y, f"action: {action}   ·   target: {target}", fontsize=10, color=MUTED,
            va="top")
    cv.text(X_TASK, y - 0.3, f"→ {idiom}", fontsize=11.5, fontweight="bold", va="top")


def main():
    use_style()
    fig = plt.figure(figsize=(W, H))
    cv = canvas(fig)

    head = H - 1.5
    for x, text in [(X_ASK, "The manager says"), (X_TASK, "Precise task  (action + target + data)"),
                    (X_CHART, "The chart that answers it")]:
        cv.text(x, head, text, fontsize=11, fontweight="bold", color=MUTED, va="bottom")
    cv.plot([X_ASK, W - 0.5], [head - 0.08] * 2, color=INK, lw=1)

    rows = [1.85, 5.05, 8.45, 11.85]                          # top of each row
    for top in rows[1:]:
        cv.plot([X_ASK, W - 0.5], [H - top + 0.3] * 2, color=HAIR, lw=0.8)

    # ---- 1 · trend ----------------------------------------------------------
    top = rows[0]
    ask(cv, top, 1, "Show me the sales data.", "No task yet: ask what they want to decide.")
    task(cv, top, "Summarize the trend of the chain's monthly revenue, 2024–2025.",
         "summarize", "trend", "line chart")
    chart_title(cv, X_CHART, top, "Revenue grows, with a dip at every Tết",
                "Chain revenue per month, million VND")
    ax = add_axes(fig, X_CHART + 0.55, top + 0.7, 6.4, 1.85)
    ax.plot(monthly.index, monthly.values, color=BLUE, lw=2.2)
    for t in TET:
        m = pd.Timestamp(t.year, t.month, 1)
        ax.text(m, monthly[m] - 350, "Tết", ha="center", va="top", fontsize=10, style="italic",
                color=MUTED)
    ax.set_ylim(0, monthly.max() * 1.12)
    ax.set_yticks([0, 2000, 4000])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.xaxis.set_major_locator(mdates.MonthLocator([1, 7]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plain(ax)

    # ---- 2 · the new branch: two tasks --------------------------------------
    top = rows[1]
    ask(cv, top, 2, "How is the new branch doing?", "Hides two tasks: is it good? is it improving?")
    task(cv, top, f"Compare {NAMES[FOCUS]}'s revenue per day open with the other branches.",
         "compare", "extremes", "sorted bar chart", label="(a)")
    task(cv, top + 1.45, f"Summarize {NAMES[FOCUS]}'s monthly trend since it opened.",
         "summarize", "trend", "line chart, others in grey", label="(b)")

    chart_title(cv, X_CHART, top, f"(a) Per day open: {rank_day}th of 6",
                "Revenue per day open, million VND")
    ax = add_axes(fig, X_CHART + 1.3, top + 0.7, 1.95, 1.95)
    bars = ax.barh([NAMES[b] for b in per_day.index], per_day.values, height=0.62,
                   color=[BLUE if b == FOCUS else LIGHT for b in per_day.index])
    ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=9.5)
    ax.set_xlim(0, per_day.max() * 1.2)
    ax.set_xticks([])
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.spines["left"].set_color(GREY)
    ax.tick_params(axis="y", length=0, labelsize=9.5)
    for label, b in zip(ax.get_yticklabels(), per_day.index):
        label.set_fontweight("bold" if b == FOCUS else "normal")

    x2 = X_CHART + 3.75
    chart_title(cv, x2, top, f"(b) Caught up within {months_to_pass} months",
                f"Monthly revenue, million VND · {NAMES[FOCUS]} in blue")
    ax = add_axes(fig, x2 + 0.5, top + 0.7, 2.45, 1.95)
    for b in branch_month.columns.drop(FOCUS):
        ax.plot(branch_month.index, branch_month[b], color=LIGHT, lw=1.1)
    ax.plot(td.index, td.values, color=BLUE, lw=2.4)
    ax.set_ylim(0, branch_month.max().max() * 1.1)
    ax.set_yticks([0, 500, 1000])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.xaxis.set_major_locator(mdates.MonthLocator([1]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plain(ax)

    # ---- 3 · strange days ---------------------------------------------------
    top = rows[2]
    ask(cv, top, 3, "Is there anything strange in last month's numbers?",
        "Last month = December 2025, raw export.")
    task(cv, top, "Locate the days in December 2025 that differ from each branch's usual day.",
         "locate", "outliers", "dot plot, one dot per day")
    chart_title(cv, X_CHART, top, f"{len(strange)} strange days, both a row entered twice",
                "Each dot = one day, compared with that branch's usual December day")
    ax = add_axes(fig, X_CHART + 1.3, top + 0.7, 5.6, 2.1)
    order = list(NAMES)[::-1]
    ax.axvspan(-band, band, color=WASH, zorder=0)
    ax.axvline(0, color=GREY, lw=0.8)
    ax.text(-band + 0.005, len(order) - 0.45, "normal range", fontsize=9, style="italic",
            color=MUTED, va="bottom")
    rng = np.random.default_rng(3)                              # small vertical jitter
    for i, b in enumerate(order):
        g = dec_day[dec_day["branch"] == b]
        normal = g[g["gap"].abs() <= band]
        ax.scatter(normal["gap"], i + rng.uniform(-0.15, 0.15, len(normal)), s=16, color=GREY,
                   alpha=0.7, linewidths=0)
        for row in g[g["gap"].abs() > band].itertuples():
            ax.scatter(row.gap, i, s=70, color=ORANGE, edgecolor=PAPER, lw=1.5, zorder=3)
            ax.text(row.gap + 0.015, i, f"{row.date:%d Dec}: {cause[row.Index]}", fontsize=9.5,
                    va="center")
    ax.set_yticks(range(len(order)), [NAMES[b] for b in order])
    ax.set_ylim(-0.6, len(order) - 0.1)
    ax.set_xlim(-0.2, 0.62)
    ax.set_xticks([-0.1, 0, 0.1, 0.2])
    ax.xaxis.set_major_formatter(FuncFormatter(
        lambda v, _: f"{v:+.0%}".replace("-", "−") if v else "usual"))
    plain(ax)
    ax.tick_params(axis="y", length=0)

    # ---- 4 · promotions -----------------------------------------------------
    top = rows[3]
    ask(cv, top, 4, "Do promotions work?", "“Work” = more items, or more money?")
    task(cv, top, "Compare items sold and revenue on promo days with similar days without "
                  "a promo.", "compare", "dependency", "bar chart of the % change")
    chart_title(cv, X_CHART, top, f"{lift['units']:+.0%} items sold, but no extra revenue",
                f"Promo days vs similar normal days · promo prices are {cheaper:.0%} lower")
    ax = add_axes(fig, X_CHART + 1.3, top + 0.75, 5.0, 1.2)
    labels = ["Items sold", "Revenue"]
    values = [lift["units"], lift["revenue"]]
    ax.barh(labels[::-1], values[::-1], height=0.55, color=[LIGHT, BLUE])
    for k, v in enumerate(values[::-1]):
        ax.text(max(v, 0) + 0.004, k, f"{v:+.0%}" if abs(v) >= 0.005 else "+0%  (no change)",
                va="center", fontsize=11, fontweight="bold")
    ax.axvline(0, color=INK, lw=0.9)
    ax.set_xlim(-0.01, 0.25)
    ax.set_xticks([])
    ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=10.5)

    headline(fig, "Activity D · From vague to precise",
             "Rewrite each vague request as action + target + data, then pick the chart that "
             "answers it. Charts drawn from the Pho Ca Phe sales file (simulated).")
    footer(fig, "Same data, four requests, five charts: the task decides the chart.",
           "Data: phocaphe_sales_clean.csv; request 3 from phocaphe_sales_messy.csv · "
           "tasks after Munzner (2014), ch. 3 · Session 2, slide 44")
    return save(fig, "activity_d_vague_to_precise")


if __name__ == "__main__":
    main()
    plt.show()
