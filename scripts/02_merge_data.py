"""
QVI Chip Category Analysis - Step 2: Merge Data
=================================================
Merges cleaned transaction data with cleaned customer (purchase behaviour)
data on LYLTY_CARD_NBR, validates the merge, and saves the analysis-ready file.

Run from the repo root: python scripts/02_merge_data.py
"""
import os
import pandas as pd

TXN_PATH = "structured/data/processed/QVI_transaction_data_clean.csv"
CUST_PATH = "structured/data/processed/QVI_purchase_behaviour_clean.csv"
OUT_PATH = "structured/data/processed/QVI_merged_data.csv"

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    txn = pd.read_csv(TXN_PATH, parse_dates=["DATE"])
    cust = pd.read_csv(CUST_PATH)

    merged = txn.merge(cust, on="LYLTY_CARD_NBR", how="left", validate="many_to_one")

    n_unmatched = merged["LIFESTAGE"].isnull().sum()
    print(f"Transaction rows: {len(txn)}")
    print(f"Merged rows: {len(merged)}")
    print(f"Rows with no matching customer record: {n_unmatched}")

    assert len(merged) == len(txn), "Merge changed row count - check for duplicate keys"
    assert n_unmatched == 0, "Some transactions have no matching customer record"

    merged.to_csv(OUT_PATH, index=False)
    print(f"Saved merged analysis-ready dataset -> {OUT_PATH}")
    print(f"Columns: {list(merged.columns)}")
