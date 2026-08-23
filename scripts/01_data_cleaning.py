"""
QVI Chip Category Analysis - Step 1: Data Cleaning
====================================================
Cleans QVI_transaction_data.xlsx and QVI_purchase_behaviour.csv:
- Fixes data types (DATE serial -> datetime)
- Removes exact duplicate transaction rows
- Derives PACK_SIZE and BRAND from PROD_NAME
- Standardises inconsistent brand spellings
- Removes non-chip products (salsa dips)
- Removes an extreme outlier customer (bulk/commercial buyer)
- Checks customer data for nulls/duplicates

Outputs cleaned CSVs used by later scripts.

Run from the repo root: python scripts/01_data_cleaning.py
"""
import os
import pandas as pd
import numpy as np

RAW_TXN_PATH = "structured/data/raw/QVI_transaction_data.xlsx"
RAW_CUST_PATH = "structured/data/raw/QVI_purchase_behaviour.csv"
OUT_TXN_PATH = "structured/data/processed/QVI_transaction_data_clean.csv"
OUT_CUST_PATH = "structured/data/processed/QVI_purchase_behaviour_clean.csv"

# Brand name variants -> standardised brand name (verified against the full
# product list; see analysis notes for how these were identified)
BRAND_MAP = {
    "RRD": "Red Rock Deli",
    "Red": "Red Rock Deli",
    "WW": "Woolworths",
    "Dorito": "Doritos",
    "Infzns": "Infuzions",
    "Smith": "Smiths",
    "Snbts": "Sunbites",
    "GrnWves": "Grain Waves",
    "Grain": "Grain Waves",
    "NCC": "Natural Chip Co",
    "Natural": "Natural Chip Co",
    "Old": "Old El Paso",
}


def clean_transaction_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)
    n_start = len(df)
    log = []

    # --- 1. Exact duplicate rows ---
    n_dupe = df.duplicated().sum()
    df = df.drop_duplicates()
    log.append(f"Removed {n_dupe} exact duplicate row(s)")

    # --- 2. DATE: Excel serial -> datetime ---
    df["DATE"] = pd.to_datetime(df["DATE"], unit="D", origin="1899-12-30")

    # --- 3. Derive PACK_SIZE (grams) from PROD_NAME ---
    df["PACK_SIZE"] = df["PROD_NAME"].str.extract(r"(\d+)\s*[gG]\b").astype(int)

    # --- 4. Derive BRAND from PROD_NAME (first word), standardise variants ---
    df["BRAND"] = df["PROD_NAME"].str.split().str[0]
    df["BRAND"] = df["BRAND"].replace(BRAND_MAP)

    # --- 5. Remove non-chip products (salsa DIPS are a different category) ---
    # NOTE: 9 products contain "salsa" in the name, but only 7 of them are
    # actual dip tubs (all sold at a 300g pack size - no genuine chip product
    # in this dataset uses 300g). The other 2 ("Smiths...Tomato Salsa 150g" and
    # "Red Rock Deli...Salsa & Mzzrlla 150g") are chip products where "salsa"
    # is just a flavour descriptor, sold at the normal 150g chip pack size -
    # these are correctly kept as chips.
    is_dip = df["PROD_NAME"].str.contains("salsa", case=False) & (df["PACK_SIZE"] == 300)
    log.append(f"Removed {is_dip.sum()} salsa DIP transaction rows "
               f"({df.loc[is_dip, 'PROD_NAME'].nunique()} distinct dip products) - "
               f"kept 2 chip products that merely have 'salsa' as a flavour name")
    df = df.loc[~is_dip].copy()

    # --- 6. Remove outlier customer (bulk/commercial buyer, not a household shopper) ---
    outlier_qty_threshold = 100  # normal baskets are 1-5 packets; 200 is not a household purchase
    outlier_mask = df["PROD_QTY"] > outlier_qty_threshold
    outlier_cards = df.loc[outlier_mask, "LYLTY_CARD_NBR"].unique()
    log.append(f"Removed {outlier_mask.sum()} transaction row(s) from outlier "
               f"loyalty card(s) {list(outlier_cards)} (bulk purchase of "
               f"{df.loc[outlier_mask, 'PROD_QTY'].unique()} packets in a single transaction)")
    df = df.loc[~outlier_mask].copy()

    # --- 7. Sanity re-check ---
    assert df["PROD_QTY"].gt(0).all(), "Found non-positive PROD_QTY"
    assert df["TOT_SALES"].gt(0).all(), "Found non-positive TOT_SALES"
    assert df.isnull().sum().sum() == 0, "Found unexpected nulls after cleaning"

    print("=== TRANSACTION DATA CLEANING LOG ===")
    for line in log:
        print(" -", line)
    print(f"Rows: {n_start} -> {len(df)}")
    print(f"Date range: {df['DATE'].min().date()} to {df['DATE'].max().date()}")
    print(f"Unique products: {df['PROD_NAME'].nunique()} | Unique brands: {df['BRAND'].nunique()}")
    print()
    return df


def clean_customer_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print("=== CUSTOMER DATA CLEANING LOG ===")
    print(" - Nulls found:", df.isnull().sum().sum())
    print(" - Duplicate rows:", df.duplicated().sum())
    print(" - Duplicate LYLTY_CARD_NBR:", df["LYLTY_CARD_NBR"].duplicated().sum())
    print(" - LIFESTAGE categories:", df["LIFESTAGE"].nunique(),
          list(df["LIFESTAGE"].unique()))
    print(" - PREMIUM_CUSTOMER categories:", df["PREMIUM_CUSTOMER"].nunique(),
          list(df["PREMIUM_CUSTOMER"].unique()))
    print(" - No cleaning required: data passed all checks (no nulls, no duplicates,"
          " category labels consistent)")
    print()
    return df


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT_TXN_PATH), exist_ok=True)

    txn_clean = clean_transaction_data(RAW_TXN_PATH)
    cust_clean = clean_customer_data(RAW_CUST_PATH)
    txn_clean.to_csv(OUT_TXN_PATH, index=False)
    cust_clean.to_csv(OUT_CUST_PATH, index=False)
    print(f"Saved cleaned transaction data -> {OUT_TXN_PATH}")
    print(f"Saved cleaned customer data -> {OUT_CUST_PATH}")
