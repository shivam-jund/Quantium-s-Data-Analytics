"""
QVI Chip Category Analysis - Step 4: Analysis Summary Tables
==============================================================
Saves the key derived analysis tables (not just cleaned raw data) as CSVs,
ready to drop into the report to Julia.

Run from the repo root: python scripts/04_summary_tables.py
"""
import os
import pandas as pd
from scipy import stats

DATA_PATH = "structured/data/processed/QVI_merged_data.csv"
OUT_DIR = "structured/outputs/tables"

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH, parse_dates=["DATE"])
    df["unit_price"] = df["TOT_SALES"] / df["PROD_QTY"]

    # --- 1. Segment summary table ---
    seg = df.groupby(["LIFESTAGE", "PREMIUM_CUSTOMER"]).agg(
        total_sales=("TOT_SALES", "sum"),
        total_units=("PROD_QTY", "sum"),
        num_customers=("LYLTY_CARD_NBR", "nunique"),
        num_transactions=("TXN_ID", "count"),
    ).reset_index()
    seg["avg_units_per_customer"] = (seg["total_units"] / seg["num_customers"]).round(2)
    seg["avg_price_per_unit"] = (seg["total_sales"] / seg["total_units"]).round(2)
    seg["sales_per_customer"] = (seg["total_sales"] / seg["num_customers"]).round(2)
    seg["pct_of_total_sales"] = (seg["total_sales"] / seg["total_sales"].sum() * 100).round(2)
    seg = seg.sort_values("total_sales", ascending=False)
    seg.to_csv(f"{OUT_DIR}/segment_summary.csv", index=False)
    print(f"Saved segment_summary.csv ({len(seg)} segments)")

    # --- 2. Target segment brand & pack-size affinity ---
    df["is_target"] = ((df["PREMIUM_CUSTOMER"] == "Mainstream") &
                        (df["LIFESTAGE"].isin(["YOUNG SINGLES/COUPLES", "RETIREES"])))

    def affinity(group_col):
        t = df[df["is_target"]].groupby(group_col)["PROD_QTY"].sum()
        r = df[~df["is_target"]].groupby(group_col)["PROD_QTY"].sum()
        out = pd.DataFrame({
            "target_segment_pct_of_units": (t / t.sum() * 100).round(2),
            "rest_of_customers_pct_of_units": (r / r.sum() * 100).round(2),
        })
        out["affinity_index"] = (out["target_segment_pct_of_units"] /
                                  out["rest_of_customers_pct_of_units"]).round(3)
        return out.sort_values("affinity_index", ascending=False)

    brand_aff = affinity("BRAND").reset_index().rename(columns={"BRAND": "brand"})
    brand_aff.to_csv(f"{OUT_DIR}/target_segment_brand_affinity.csv", index=False)
    print(f"Saved target_segment_brand_affinity.csv ({len(brand_aff)} brands)")

    # --- 3. Statistical test backing the price-premium finding ---
    sub = df[df["LIFESTAGE"].isin(["YOUNG SINGLES/COUPLES", "MIDAGE SINGLES/COUPLES"])]
    mainstream = sub.loc[sub["PREMIUM_CUSTOMER"] == "Mainstream", "unit_price"]
    other = sub.loc[sub["PREMIUM_CUSTOMER"] != "Mainstream", "unit_price"]
    t_stat, p_val = stats.ttest_ind(mainstream, other, equal_var=False)

    stats_summary = pd.DataFrame([{
        "comparison": "Mainstream vs Budget+Premium, unit price ($/packet)",
        "scope": "Young + Midage Singles/Couples lifestages only",
        "mainstream_mean_price": round(mainstream.mean(), 4),
        "other_mean_price": round(other.mean(), 4),
        "pct_difference": round((mainstream.mean() / other.mean() - 1) * 100, 2),
        "t_statistic": round(t_stat, 3),
        "p_value": p_val,
        "n_mainstream": len(mainstream),
        "n_other": len(other),
    }])
    stats_summary.to_csv(f"{OUT_DIR}/price_premium_significance_test.csv", index=False)
    print("Saved price_premium_significance_test.csv")

    print("\nTop of segment_summary.csv:")
    print(seg.head(5).to_string(index=False))
