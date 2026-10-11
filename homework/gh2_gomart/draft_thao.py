# %% [markdown]
# # Group Homework 2 · GoMart deliveries · Individual Draft (Thao)
# Question 2: Is the move to e-wallet payments real, or just noise?
#
# Sections:
#   1. Load clean data (5,913 orders from Task 4)
#   2. Summary statistics:
#      - Monthly payment shares (%)
#      - Payment shares by member tier (%)
#      - Total revenue and average basket value by payment method
#   3. Primary Chart (Q2): Monthly trend of payment method shares (Line chart)
#   4. Supporting Chart 1: Total revenue by payment method (Horizontal bar chart)
#   5. Supporting Chart 2: Payment shares across member tiers (Grouped bar chart)

# %%
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# %% [markdown]
# ## 1. Load clean data
# %%
csv_path = next(p for p in [Path("homework/gh2_gomart/gomart_orders_clean.csv"),
                            Path("gomart_orders_clean.csv"),
                            Path(__file__).parent / "gomart_orders_clean.csv"] if p.exists())

df = pd.read_csv(csv_path)
df["order_time"] = pd.to_datetime(df["order_time"])
df["member_tier"] = pd.Categorical(df["member_tier"], ["Silver", "Gold", "Platinum"], ordered=True)

print(f"Dataset ready: {len(df):,} orders, {df.shape[1]} columns.")

# %% [markdown]
# ## 2. Summary statistics
# %%
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
# ## 3. Primary Chart (Q2): Monthly transition of payment method shares
# * **(a) Task:** Summarize the trend of monthly payment method shares across 12 months in 2025.
# * **(b) Chart and why:** Line chart.
#   * Conveys temporal continuity and slope, revealing a persistent month-over-month rise in e-wallets.
#   * Visual encodings: E-wallet highlighted in bold blue (#1d56ba, lw=3.2, marker 'o'); other methods in greys with distinct line styles and markers.
#   * Collision-free labeling: Staggered callouts at Month 12 eliminate overlap between Card (11.9%) and Bank transfer (11.7%).
# %%
p = pct_monthly
months = list(range(1, 13))
m_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

fig, ax = plt.subplots(figsize=(10, 5.8), dpi=150)
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

styles = {
    "Cash":          {"color": "#5c5b57", "ls": "--", "marker": "s", "lw": 1.8, "ms": 5,   "zorder": 3},
    "Card":          {"color": "#807f7a", "ls": "-.", "marker": "^", "lw": 1.8, "ms": 5.5, "zorder": 3},
    "Bank transfer": {"color": "#a6a5a0", "ls": ":",  "marker": "d", "lw": 2.0, "ms": 5.5, "zorder": 3},
    "E-wallet":      {"color": "#1d56ba", "ls": "-",  "marker": "o", "lw": 3.2, "ms": 7,   "zorder": 6},
}

for method, s in styles.items():
    ax.plot(months, p[method], label=method, **s)

# Start annotations (Month 1)
ax.text(1, p["Cash"].iloc[0] + 2.2, f"{p['Cash'].iloc[0]:.1f}%", ha="center", va="bottom", fontsize=9, color="#5c5b57", fontweight="bold")
ax.text(1, p["E-wallet"].iloc[0] - 3.2, f"{p['E-wallet'].iloc[0]:.1f}%", ha="center", va="top", fontsize=9.5, color="#1d56ba", fontweight="bold")

# End annotations (Month 12) with staggered arrows
ax.text(12.3, p["E-wallet"].iloc[-1], f"● E-wallet: {p['E-wallet'].iloc[-1]:.1f}%", va="center", fontsize=10.5, fontweight="bold", color="#1d56ba")
ax.text(12.3, p["Cash"].iloc[-1], f"■ Cash: {p['Cash'].iloc[-1]:.1f}%", va="center", fontsize=9.5, fontweight="bold", color="#5c5b57")
ax.annotate(f"▲ Card: {p['Card'].iloc[-1]:.1f}%", xy=(12.05, p["Card"].iloc[-1]), xytext=(12.35, 13.8),
            va="center", fontsize=9.5, color="#52514e",
            arrowprops=dict(arrowstyle="->", color="#807f7a", lw=1.0, shrinkA=3, shrinkB=3))
ax.annotate(f"◆ Bank transfer: {p['Bank transfer'].iloc[-1]:.1f}%", xy=(12.05, p["Bank transfer"].iloc[-1]), xytext=(12.35, 9.6),
            va="center", fontsize=9.5, color="#52514e",
            arrowprops=dict(arrowstyle="->", color="#9e9d98", lw=1.0, shrinkA=3, shrinkB=3))

# Axis styling
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
# * **(d) Interpretation (Phase-by-phase trend analysis):**
#   * **Early year (Jan–Apr):** Cash remained the most common payment method (29.0%–35.4%). E-wallet started at 30.9% in January and rose gradually to 35.0% by April.
#   * **Mid-year (May–Aug):** A steady structural shift emerged: E-wallet accelerated past 40% (41.4% in May to 47.0% in August), while Cash dropped steadily from 27.6% down to 20.0%.
#   * **Late year (Sep–Dec):** E-wallet crossed the 50% majority threshold in September (51.0%) and climbed to a peak of 60.0% in December, while Cash reached an annual low of 16.5%.
#   * **Other methods (Card & Bank transfer):** Remained consistently stable within a narrow 10%–22% band throughout the year, finishing December at virtually identical levels (~11.7%–11.9%).
#   * **Conclusion:** The transition toward e-wallets unfolded through persistent monthly increases across 2025, evidencing a genuine structural shift rather than temporary noise.

# %% [markdown]
# ## 4. Supporting Chart 1: Total revenue by payment method
# * **Objective:** Show that e-wallets command the highest total revenue (44.1%, >663M VND), refuting concerns that e-wallets are limited to small baskets.
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
plt.savefig("outputs/figures/q2_revenue_by_payment.png", dpi=200, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## 5. Supporting Chart 2: Payment shares across member tiers
# * **Objective:** Confirm that e-wallet adoption spans all tiers and peaks among Platinum members (49.6%), disproving one-off discount hunting.
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
plt.savefig("outputs/figures/q2_payment_by_tier.png", dpi=200, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## 6. Comprehensive Synthesis & Strategic Interpretation
#
# **Key Finding: The shift toward E-wallet is real, substantial, and sustainable, rather than temporary noise.**
#
# 1. **A genuine, structural transition over time (Chart 1):**
#    The upward trajectory of e-wallets reflects a permanent behavioral shift rather than random fluctuation. In January, Cash was the dominant payment method at 35.4%, while E-wallet accounted for 30.9%. Throughout 2025, E-wallet expanded progressively across every quarter, culminating in an overwhelming **60.0%** share by December, while Cash fell by more than half to an annual low of **16.5%**.
#
# 2. **Sustained financial contribution, not discount-driven noise (Chart 2):**
#    This transition is not an artificial spike driven merely by temporary discount vouchers or promotional campaigns. E-wallet constitutes the largest revenue stream for GoMart, generating **663.4 million VND** (**44.1%** of total system revenue). Crucially, its average basket value of **257,428 VND** is on par with Cash (257,917 VND), demonstrating that customers routinely make full-value purchases through e-wallets rather than reserving them solely for small-basket subsidized orders.
#
# 3. **Consistent penetration across all customer tiers (Chart 3):**
#    E-wallet adoption is widespread across all customer segments rather than isolated to a specific demographic. E-wallet commands the dominant share in every tier: Silver (45.5%), Gold (42.8%), and peaks at **49.6% among top-tier Platinum members**. Because GoMart's most loyal and highest-value customers demonstrate the highest adoption rate, e-wallet usage has clearly become an entrenched payment habit rather than transient deal-seeking behavior.

