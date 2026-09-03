# Quantium Retail Strategy & Analytics — Practice Checklist

Use this as a self-test. Don't look at your old solution — try to complete each
step from scratch, then compare.

Datasets needed:
- `QVI_transaction_data.csv` (or .xlsx)
- `QVI_purchase_behaviour.csv`

---

## Task 1 — Data Preparation & Customer Analytics

### A. Load & inspect
- [ ] Load both datasets (`data.table::fread` or `pandas.read_csv`)
- [ ] Inspect structure/dtypes of `transactionData` (`str()` / `.info()`)
- [ ] Confirm `DATE` column is not already a proper date — convert it
  - Hint: Excel/CSV serial dates start from 30 Dec 1899
- [ ] Inspect `PROD_NAME` — list unique product names and counts

### B. Clean product names
- [ ] Split all unique `PROD_NAME` values into individual words
- [ ] Strip out words containing digits
- [ ] Strip out words containing only special characters
- [ ] Count frequency of remaining words — sanity check they're all chip-related
- [ ] Identify and remove any non-chip products hiding in the data (e.g. a dip/salsa product line)

### C. Outlier / null checks
- [ ] Run summary statistics on the full transaction table — check for NAs
- [ ] Look for outliers in `PROD_QTY` (or quantity-equivalent column)
- [ ] Investigate any transaction with an implausibly large quantity
- [ ] Check whether that same loyalty card had other transactions
- [ ] Decide whether to exclude that customer — and do it
- [ ] Re-run summary stats to confirm outlier is gone

### D. Missing dates
- [ ] Count transactions per date — how many unique dates appear?
- [ ] Compare against expected number of days in the observation window
- [ ] Generate the full expected date sequence and left-join transaction counts onto it
- [ ] Plot transactions over time — identify anomalies (e.g. holiday spike, missing day)
- [ ] Zoom into the anomalous month/period to confirm the cause

### E. Feature engineering
- [ ] Extract `PACK_SIZE` from the product name (numeric digits)
- [ ] Sanity-check the distribution of pack sizes (histogram)
- [ ] Extract `BRAND` from the product name (first word)
- [ ] Check brand list for near-duplicates (e.g. abbreviations, inconsistent casing)
- [ ] Consolidate duplicate brand names into single canonical brand labels

### F. Customer data
- [ ] Inspect `customerData` structure
- [ ] Check distribution of lifestage categories
- [ ] Check distribution of premium/mainstream/budget segment
- [ ] Merge transaction data with customer data (left join on loyalty card)
- [ ] Confirm no row-count drift and no unmatched/null customers after merge

### G. Segment analysis
- [ ] Total sales by lifestage × customer segment — visualize (e.g. mosaic/heatmap)
- [ ] Number of customers by lifestage × segment — visualize
- [ ] Average units purchased per customer by lifestage × segment
- [ ] Average price per unit by lifestage × segment
- [ ] Statistically test whether a specific segment pays a significantly different price per unit than others (e.g. t-test)

### H. Deep dive
- [ ] Pick your top target segment (highest value combination of size + spend)
- [ ] Compute brand affinity: does the target segment buy certain brands disproportionately more than everyone else?
- [ ] Compute pack-size affinity: does the target segment prefer certain pack sizes?
- [ ] Write 3–5 sentence summary of insights + one actionable recommendation

---

## Task 2 — Experimentation & Uplift Testing

### A. Metric construction
- [ ] Create a `YEARMONTH` key (year × 100 + month, or similar)
- [ ] For each store × month, calculate:
  - [ ] Total sales
  - [ ] Number of unique customers
  - [ ] Transactions per customer
  - [ ] Units per transaction
  - [ ] Average price per unit
- [ ] Filter to stores with a complete observation period (e.g. full 12 months)
- [ ] Filter to the pre-trial period only

### B. Control store selection
- [ ] Write a function to compute correlation between a trial store and every other store on a given metric, across months
- [ ] Write a function to compute a standardized magnitude-distance score (0 to 1) between a trial store and every other store on a given metric
- [ ] For each metric of interest, combine correlation + magnitude into one score (choose and justify a weighting)
- [ ] Combine scores across multiple metrics (e.g. sales + customers) into one final composite score
- [ ] Select the top-scoring store (excluding the trial store itself) as the control store
- [ ] Repeat for each trial store you've been given

### C. Pre-trial validation
- [ ] Plot trial vs. control vs. other-stores average sales over the pre-trial period — do trends look similar?
- [ ] Plot trial vs. control number of customers over the pre-trial period — similar?

### D. Trial assessment
- [ ] Calculate a scaling factor to align the control store's pre-trial sales level with the trial store's
- [ ] Apply the scaling factor to the control store's sales across the whole period
- [ ] Calculate percentage difference between scaled control sales and trial store sales, month by month
- [ ] Calculate the standard deviation of that percentage difference during the pre-trial period (this represents "normal" variation)
- [ ] Determine degrees of freedom (based on number of pre-trial months)
- [ ] Compute t-values for each month in the trial period
- [ ] Compare against the critical t-value at your chosen confidence level (e.g. 95th percentile)
- [ ] State a conclusion: is the sales difference statistically significant?
- [ ] Repeat the entire scaling/testing process for number of customers
- [ ] Visualize: trial store sales vs. control store's 5th–95th percentile confidence band, trial period highlighted
- [ ] Do the same visualization for number of customers

### E. Repeat for all trial stores
- [ ] Repeat B–D for every trial store you were given
- [ ] Summarize: which trial stores showed a significant uplift, and on which metric(s)?

---

## Task 3 — Analytics & Commercial Application

- [ ] Consolidate Task 1 findings (target segment, brand/pack affinities, seasonality)
- [ ] Consolidate Task 2 findings (which trial stores succeeded, on what metric)
- [ ] Build a short slide deck for a non-technical business stakeholder:
  - [ ] Executive summary slide (headline takeaways only)
  - [ ] Category/customer insights section
  - [ ] Trial store performance section
  - [ ] Clear, prioritized recommendations
- [ ] Keep charts simple — one clear takeaway per chart, labeled directly
- [ ] Proofread for a non-technical audience — no leftover code/jargon

---

## Self-Grading Tips
- If you got stuck on the control-store scoring function, that's the most
  algorithmically tricky part — it's worth re-deriving from scratch a second time.
- If your t-test/confidence-interval logic feels shaky, revisit *why* we scale the
  control store's pre-trial sales before comparing (it's about matching baseline
  levels, not just trends).
- For Task 3, the skill being tested is business communication, not more analysis —
  resist the urge to add new charts; distill what you already found.
