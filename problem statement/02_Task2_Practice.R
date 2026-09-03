# =============================================================
# Quantium Retail Strategy & Analytics - Task 2 (PRACTICE COPY)
# Experimentation and Uplift Testing
# =============================================================
# Fill in each section yourself. Don't peek at your old solution
# until you've given every section a real attempt.

library(data.table)
library(ggplot2)

# ---- 0. Load data from Task 1 ----
filePath <- ""  # <- set your working directory here
data <- fread(paste0(filePath, "QVI_data.csv"))

theme_set(theme_bw())
theme_update(plot.title = element_text(hjust = 0.5))


# ---- 1. Build monthly store-level metrics ----
# TODO: create a YEARMONTH key, e.g. year*100 + month


# TODO: for each STORE_NBR x YEARMONTH, calculate:
#   - total sales
#   - number of unique customers
#   - transactions per customer
#   - units (chips) per transaction
#   - average price per unit
# measureOverTime <- data[, .(
#     totSales = ,
#     nCustomers = ,
#     nTxnPerCust = ,
#     nChipsPerTxn = ,
#     avgPricePerUnit =
#   ), by = c("STORE_NBR", "YEARMONTH")][order(STORE_NBR, YEARMONTH)]


# TODO: filter to stores with a full observation period (e.g. 12 months present)


# TODO: filter further to the pre-trial period only


# ---- 2. Control store selection functions ----
# TODO: write calculateCorrelation(inputTable, metricCol, storeComparison)
# It should loop through every store number and compute the correlation
# between that store's metric-over-time and the trial store's metric-over-time.


# TODO: write calculateMagnitudeDistance(inputTable, metricCol, storeComparison)
# It should compute the absolute difference between the trial store and every
# other store for each month, then standardize this to a 0-1 scale where 1 = most similar.


# ---- 3. Find control store for trial store #1 ----
trial_store <- NA  # <- set trial store number

# TODO: use calculateCorrelation() for total sales and number of customers


# TODO: use calculateMagnitudeDistance() for total sales and number of customers


# TODO: combine correlation + magnitude into one score per metric
# (choose a weighting, e.g. simple average)


# TODO: combine scores across metrics into one final composite score


# TODO: select the top-scoring non-trial store as the control store


# ---- 4. Validate control store visually (pre-trial period) ----
# TODO: plot total sales over time: trial vs control vs other stores (pre-trial only)


# TODO: plot number of customers over time: trial vs control vs other stores (pre-trial only)


# ---- 5. Assess the trial ----
# TODO: calculate a scaling factor so the control store's pre-trial sales
# match the trial store's pre-trial sales level


# TODO: apply the scaling factor to the control store's sales across the full period


# TODO: calculate percentage difference between scaled control sales and trial sales, by month


# TODO: calculate the standard deviation of that percentage difference
# during the pre-trial period only


# TODO: determine degrees of freedom (pre-trial months - 1)


# TODO: calculate t-values for each trial-period month


# TODO: find the critical t-value (e.g. 95th percentile) for comparison


# TODO: state your conclusion - is the difference statistically significant?


# TODO: visualize trial store sales vs. control's 5th-95th percentile band,
# with the trial period highlighted


# TODO: repeat the scaling + significance testing + visualization for
# number of customers


# ---- 6. Repeat for remaining trial stores ----
# TODO: repeat steps 3-5 for every other trial store you were given


# ---- 7. Conclusion ----
# TODO: summarize which trial stores showed significant uplift, and on
# which metric(s) (sales, customers, or both)
