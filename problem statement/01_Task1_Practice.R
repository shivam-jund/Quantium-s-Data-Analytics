# =============================================================
# Quantium Retail Strategy & Analytics - Task 1 (PRACTICE COPY)
# Data Preparation and Customer Analytics
# =============================================================
# Fill in each section yourself. Don't peek at your old solution
# until you've given every section a real attempt.

# ---- 0. Libraries ----
# install.packages("data.table")
# install.packages("ggplot2")
# install.packages("ggmosaic")
# install.packages("readr")

library(data.table)
library(ggplot2)
library(ggmosaic)
library(readr)

# ---- 1. Load data ----
filePath <- ""  # <- set your working directory here
transactionData <- fread(paste0(filePath, "QVI_transaction_data.csv"))
customerData <- fread(paste0(filePath, "QVI_purchase_behaviour.csv"))


# ---- 2. Examine transaction data ----
# TODO: inspect structure (types, sample rows)


# TODO: convert DATE from integer to a proper Date type
# (hint: what date do Excel/CSV serial numbers start counting from?)


# TODO: inspect PROD_NAME - list unique product names + counts


# ---- 3. Clean product names ----
# TODO: split all unique PROD_NAME values into individual words


# TODO: remove words containing digits


# TODO: remove words that are only special characters


# TODO: count word frequency, sorted descending - do all words look chip-related?


# TODO: identify and remove any non-chip products (e.g. a dip/salsa line)
# that snuck into the "chips" dataset


# ---- 4. Outlier / null checks ----
# TODO: run summary() on transactionData - check for NAs and skewed ranges


# TODO: find the transaction(s) with an implausibly large quantity


# TODO: check if that loyalty card number has other transactions


# TODO: decide whether to exclude that customer, then do it


# TODO: re-run summary() to confirm the outlier is gone


# ---- 5. Missing dates ----
# TODO: count transactions per date - how many unique dates?


# TODO: build the full expected date sequence for the observation window
# and left-join the transaction counts onto it


# TODO: plot transactions over time


# TODO: zoom into the anomalous period (e.g. a specific month) and explain what you see


# ---- 6. Feature engineering ----
# TODO: extract PACK_SIZE (numeric) from PROD_NAME


# TODO: plot a histogram of PACK_SIZE - does the range look sensible?


# TODO: extract BRAND (first word) from PROD_NAME


# TODO: check brand list for near-duplicates / inconsistent naming


# TODO: consolidate duplicate brand names into single canonical labels


# ---- 7. Examine + merge customer data ----
# TODO: inspect customerData structure


# TODO: check distribution of LIFESTAGE


# TODO: check distribution of PREMIUM_CUSTOMER


# TODO: merge transaction data with customer data (left join)
data <- merge(transactionData, customerData, all.x = TRUE)

# TODO: confirm no row-count drift and no unmatched (null) customers


# Optional: save merged dataset for use in Task 2
# fwrite(data, paste0(filePath, "QVI_data.csv"))


# ---- 8. Segment analysis ----
# TODO: total sales by LIFESTAGE x PREMIUM_CUSTOMER - visualize


# TODO: number of customers by LIFESTAGE x PREMIUM_CUSTOMER - visualize


# TODO: average units per customer by LIFESTAGE x PREMIUM_CUSTOMER - visualize


# TODO: average price per unit by LIFESTAGE x PREMIUM_CUSTOMER - visualize


# TODO: statistically test whether one segment pays significantly more
# per unit than another (e.g. t-test)


# ---- 9. Deep dive into target segment ----
# TODO: pick your target segment (highest value: size x spend)


# TODO: compute brand affinity - does the target segment buy certain
# brands disproportionately more than everyone else?


# TODO: compute pack-size affinity - similarly, for pack sizes


# ---- 10. Write-up ----
# TODO: summarize insights in 3-5 sentences + one actionable recommendation
# for the Category Manager
