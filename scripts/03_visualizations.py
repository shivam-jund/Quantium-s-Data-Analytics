"""
QVI Chip Category Analysis - Step 3: Visualizations
======================================================
Builds the chart set used in the findings report:
1. segment_dashboard.png - total sales / customers / units per customer /
   price per unit, by LIFESTAGE x PREMIUM_CUSTOMER
2. sales_trend.png - daily sales trend across the year (7-day rolling
   average), with the pre-Christmas peak highlighted
3. target_segment_deep_dive.png - brand & pack-size affinity for the target
   segment (Mainstream Young Singles/Couples + Mainstream Retirees) vs the
   rest of customers

Run from the repo root: python scripts/03_visualizations.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

DATA_PATH = "structured/data/processed/QVI_merged_data.csv"
OUT_DIR = "structured/outputs/charts"

# ---- shared style ----
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

NAVY = "#1f3b57"
TEAL = "#2a9d8f"
CORAL = "#e76f51"
GOLD = "#e9c46a"

LIFESTAGE_ORDER = ["NEW FAMILIES", "YOUNG FAMILIES", "OLDER FAMILIES",
                   "YOUNG SINGLES/COUPLES", "MIDAGE SINGLES/COUPLES",
                   "OLDER SINGLES/COUPLES", "RETIREES"]
PREMIUM_ORDER = ["Budget", "Mainstream", "Premium"]


def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["DATE"])
    df["unit_price"] = df["TOT_SALES"] / df["PROD_QTY"]
    return df


def make_pivot(df, values, agg):
    if callable(agg):
        p = df.groupby(["LIFESTAGE", "PREMIUM_CUSTOMER"]).apply(agg, include_groups=False).unstack()
    else:
        p = df.pivot_table(index="LIFESTAGE", columns="PREMIUM_CUSTOMER", values=values, aggfunc=agg)
    return p.reindex(index=LIFESTAGE_ORDER, columns=PREMIUM_ORDER)


def draw_heatmap(ax, data, title, fmt, cmap):
    im = ax.imshow(data.values, cmap=cmap, aspect="auto")
    ax.set_xticks(range(len(PREMIUM_ORDER)))
    ax.set_xticklabels(PREMIUM_ORDER)
    ax.set_yticks(range(len(LIFESTAGE_ORDER)))
    ax.set_yticklabels([l.title() for l in LIFESTAGE_ORDER])
    ax.set_title(title, pad=10)

    vmin, vmax = np.nanmin(data.values), np.nanmax(data.values)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data.values[i, j]
            rel = (val - vmin) / (vmax - vmin) if vmax > vmin else 0.5
            color = "white" if rel > 0.6 else "#222222"
            ax.text(j, i, fmt.format(val), ha="center", va="center", fontsize=9.5, color=color)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(False)


def chart_segment_dashboard(df):
    sales = make_pivot(df, "TOT_SALES", "sum")
    custs = make_pivot(df, None, lambda g: g["LYLTY_CARD_NBR"].nunique())
    units_pc = make_pivot(df, None, lambda g: g["PROD_QTY"].sum() / g["LYLTY_CARD_NBR"].nunique())
    price_pu = make_pivot(df, None, lambda g: g["TOT_SALES"].sum() / g["PROD_QTY"].sum())

    fig, axes = plt.subplots(2, 2, figsize=(13, 11))
    draw_heatmap(axes[0, 0], sales / 1000, "Total Sales ($'000)", "{:,.0f}", "Blues")
    draw_heatmap(axes[0, 1], custs, "Number of Customers", "{:,.0f}", "Purples")
    draw_heatmap(axes[1, 0], units_pc, "Avg. Packets Bought per Customer", "{:.1f}", "Greens")
    draw_heatmap(axes[1, 1], price_pu, "Avg. Price per Packet ($)", "${:.2f}", "Oranges")

    fig.suptitle("Chip Category: Customer Segment Overview (Jul 2018 - Jun 2019)",
                 fontsize=15, fontweight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(f"{OUT_DIR}/segment_dashboard.png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("Saved segment_dashboard.png")


def chart_sales_trend(df):
    daily = df.set_index("DATE").resample("D")["TOT_SALES"].sum()
    full_idx = pd.date_range(daily.index.min(), daily.index.max())
    daily = daily.reindex(full_idx, fill_value=0)  # keep Dec 25 gap visible as zero
    rolling = daily.rolling(7, center=True).mean()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(daily.index, daily.values, color=TEAL, alpha=0.25, linewidth=1, label="Daily sales")
    ax.plot(rolling.index, rolling.values, color=NAVY, linewidth=2.2, label="7-day rolling average")

    peak_start, peak_end = pd.Timestamp("2018-12-17"), pd.Timestamp("2018-12-24")
    ax.axvspan(peak_start, peak_end, color=CORAL, alpha=0.12)
    ax.annotate("Pre-Christmas peak", xy=(pd.Timestamp("2018-12-21"), daily.max() * 0.97),
                ha="center", fontsize=10, color=CORAL, fontweight="bold")

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.set_ylabel("Total daily sales")
    ax.set_title("Daily Chip Sales Across the Year")
    ax.legend(loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.22))
    plt.xticks(rotation=0)

    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/sales_trend.png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("Saved sales_trend.png")


def chart_target_deep_dive(df):
    df = df.copy()
    df["is_target"] = ((df["PREMIUM_CUSTOMER"] == "Mainstream") &
                        (df["LIFESTAGE"].isin(["YOUNG SINGLES/COUPLES", "RETIREES"])))

    def affinity(group_col):
        t = df[df["is_target"]].groupby(group_col)["PROD_QTY"].sum()
        r = df[~df["is_target"]].groupby(group_col)["PROD_QTY"].sum()
        t_pct, r_pct = t / t.sum() * 100, r / r.sum() * 100
        out = pd.DataFrame({"target_pct": t_pct, "rest_pct": r_pct})
        out["affinity"] = out["target_pct"] / out["rest_pct"]
        return out.sort_values("affinity")

    brand_aff = affinity("BRAND")

    # Pack size: most brands only come in ONE size, so individual pack sizes
    # are almost a re-labelling of brand. Band into Small/Standard/Large to
    # show the genuinely independent size signal (which turns out to be weak).
    def size_band(s):
        if s < 150:
            return "Small\n(<150g)"
        if s <= 180:
            return "Standard\n(150-180g)"
        return "Large\n(200g+)"

    df["SIZE_BAND"] = df["PACK_SIZE"].apply(size_band)
    band_aff = affinity("SIZE_BAND")
    band_order = ["Small\n(<150g)", "Standard\n(150-180g)", "Large\n(200g+)"]
    band_aff = band_aff.reindex(band_order)

    fig, axes = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={"width_ratios": [2, 1]})

    # --- Brand affinity (left, full detail - the strong signal) ---
    ax = axes[0]
    colors = [CORAL if v < 1 else TEAL for v in brand_aff["affinity"]]
    ax.barh(brand_aff.index, brand_aff["affinity"] - 1, left=1, color=colors, height=0.65)
    ax.axvline(1, color="#444444", linewidth=1)
    ax.set_xlabel("Affinity index (1.0 = same share as rest of customers)")
    ax.set_title("Brand Affinity (strong differentiator)")
    for i, v in enumerate(brand_aff["affinity"]):
        offset = 0.015 if v >= 1 else -0.015
        ha = "left" if v >= 1 else "right"
        ax.text(v + offset, i, f"{v:.2f}x", va="center", ha=ha, fontsize=8.5)
    ax.set_xlim(0.6, 1.25)

    # --- Pack size band affinity (right, coarse - the weak signal) ---
    ax = axes[1]
    colors = [CORAL if v < 1 else TEAL for v in band_aff["affinity"]]
    ax.barh(band_aff.index, band_aff["affinity"] - 1, left=1, color=colors, height=0.55)
    ax.axvline(1, color="#444444", linewidth=1)
    ax.set_xlabel("Affinity index")
    ax.set_title("Pack-Size Affinity (weak - close to 1.0x)")
    for i, v in enumerate(band_aff["affinity"]):
        offset = 0.008 if v >= 1 else -0.008
        ha = "left" if v >= 1 else "right"
        ax.text(v + offset, i, f"{v:.2f}x", va="center", ha=ha, fontsize=9.5)
    ax.set_xlim(0.85, 1.15)

    fig.suptitle("Target Segment (Mainstream Young Singles/Couples + Mainstream Retirees):\n"
                 "Brand Choice Differentiates Them Far More Than Pack Size Does",
                 fontsize=14, fontweight="bold", y=1.03)
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/target_segment_deep_dive.png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("Saved target_segment_deep_dive.png")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    df = load_data()
    chart_segment_dashboard(df)
    chart_sales_trend(df)
    chart_target_deep_dive(df)
