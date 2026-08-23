# Chip Category Review: Initial Findings
**Prepared for:** Zilinka (for onward briefing to Julia, Category Manager – Chips)
**Prepared by:** Retail Analytics Team
**Data period:** 1 July 2018 – 30 June 2019 (transaction data) matched to customer segment data

---

## 1. What this covers

This report analyses one year of chip-category transactions against customer loyalty
profiles to answer three questions for the category strategy:

1. Who is actually driving chip sales today?
2. Which segment(s) should we prioritise in the next six months?
3. Do brand and pack-size preferences differ enough between segments to act on?

All cleaning and analysis was done in Python (pandas/scipy/matplotlib). Code, cleaned
data, and chart files are included alongside this report (see **Section 9**).

---

## 2. Data preparation summary

Both source files were checked for nulls, duplicates, outliers, and formatting issues
before analysis. Customer data (72,637 loyalty profiles) had no issues. Transaction
data (264,836 rows) required the following fixes:

| Issue found | Detail | Action taken |
|---|---|---|
| Exact duplicate row | One transaction was recorded twice, identical in every field | Dropped 1 row |
| Date stored as Excel serial number | `DATE` was an integer (e.g. 43390), not a real date | Converted to datetime |
| Missing day | 25 Dec 2018 has no transactions (store closure) | Left as a gap — expected, not an error |
| Product name bundles brand, size, and flavour | e.g. `"WW Crinkle Cut Chicken 175g"` | Parsed out **BRAND** and **PACK_SIZE (g)** columns |
| Inconsistent brand spelling | Same brand written differently, e.g. `RRD` vs `Red Rock Deli`, `WW` vs `Woolworths`, `Dorito` vs `Doritos`, `Smith` vs `Smiths`, `Infzns` vs `Infuzions`, `Snbts` vs `Sunbites`, `NCC`/`Natural` vs `Natural Chip Co`, `GrnWves`/`Grain` vs `Grain Waves` | Standardised to one brand name each (20 distinct brands after cleaning) |
| Non-chip products mixed in | 9 products contain "salsa" in the name, but only **7 are dip tubs** (all sold at a 300g size that no genuine chip uses); the other 2 (`Smiths...Tomato Salsa 150g`, `Red Rock Deli...Salsa & Mzzrlla 150g`) are salsa-*flavoured chips* at the standard 150g chip size | Removed the 7 true dip products only; kept the 2 flavoured chips |
| Extreme outlier customer | Loyalty card 226000 bought **200 packets in a single transaction, twice** (vs. a typical basket of 1–5 packets) — a bulk/commercial purchase, not household shopping | Removed both transactions (2 rows) |

**Net result:** 249,667 clean transaction rows across 107 products / 20 brands, merged
1:1 with all 71,517 customers who purchased chips in the period (no unmatched records
either direction).

---

## 3. Overall category performance

- **Total sales:** $1,819,778 across 475,909 packets and 248,156 transactions
- Sales are **remarkably stable month to month** (between $141,600 and $157,820), i.e.
  chips are a steady, non-seasonal-growth category rather than one trending up or down
- The one clear spike is the week before Christmas (19–24 Dec 2018), consistent with
  holiday entertaining — a natural window for promotional activity

*(See `charts/sales_trend.png`)*

---

## 4. Who is actually buying chips? Two different "high sales" stories

Segmenting sales by **LIFESTAGE × PREMIUM_CUSTOMER** (21 segments) shows total sales
concentrate in the segments below, but for two different reasons:

| Rank | Segment | Total sales | Why they're high |
|---|---|---|---|
| 1 | Older Families – Budget | $158,380 (8.7%) | Large households buying **more packets per trip** (9.2 packets/customer — the highest of any segment) |
| 2 | Young Singles/Couples – Mainstream | $148,337 (8.2%) | **By far the largest customer base** (7,930 customers — ~1.6x the next largest segment), *plus* the highest price paid per packet of any segment |
| 3 | Retirees – Mainstream | $146,329 (8.0%) | Also a very large customer base (6,382 customers, 3rd largest) |
| 4 | Young Families – Budget | $130,919 (7.2%) | Same "large basket" pattern as Older Families |
| 5 | Older Singles/Couples – Budget | $128,684 (7.1%) | Fairly even spend across Budget/Mainstream/Premium for this lifestage |

**The pattern in short:** Families drive sales through *basket size* — every family
segment buys 8.7–9.4 packets per customer regardless of Budget/Mainstream/Premium
tier. Young Singles/Couples and Retirees buy far fewer packets per customer
(4.3–6.8), so their high total sales come from **having the most customers**, not
from buying more per trip.

*(Full 21-segment breakdown by sales, customer count, packets/customer, and price/unit
is visualised in `charts/segment_dashboard.png` and saved in full in
`segment_summary.csv`)*

---

## 5. The one segment that also pays more: Mainstream Young/Midage Singles & Couples

Breaking price-per-packet down by Budget/Mainstream/Premium *within* each lifestage
(which controls for household-size effects) surfaces a genuine anomaly: for most
lifestages, the three tiers pay a similar price per packet. But for **Young
Singles/Couples** and **Midage Singles/Couples**, the **Mainstream** tier pays
noticeably more than both Budget *and* Premium in the same lifestage:

| Lifestage | Budget | Mainstream | Premium |
|---|---|---|---|
| Young Singles/Couples | $3.67 | **$4.06** | $3.68 |
| Midage Singles/Couples | $3.74 | **$3.98** | $3.76 |

Pooling these two lifestages, Mainstream customers pay **9.1% more per packet**
than Budget/Premium customers in the same lifestages ($4.03 vs $3.69). This is not
noise — a Welch's t-test on 58,009 transactions gives **t = 38.1, p < 0.0001**. Full
test output is in `price_premium_significance_test.csv`.

Notably, this pattern does **not** hold for Mainstream Retirees, who pay about the
same per packet as Budget/Premium retirees — their high total sales are explained
by customer count alone, not a price premium. Worth flagging so the recommendation
below isn't over-generalised.

---

## 6. Deep dive: what does the target segment actually buy?

Based on Sections 4–5, we defined the **target segment** as **Mainstream Young
Singles/Couples + Mainstream Retirees** — together the two largest Mainstream
customer bases (20% of all customers, 16.2% of sales) and the clearest combination
of reach and (for one of the two) price premium.

**Brand affinity** (target segment's share of packets bought, vs. everyone else's
share, for each brand) shows a real, actionable skew:

- **Over-indexed:** Twisties (1.15x), Doritos (1.14x), Pringles (1.13x), Kettle
  (1.12x), Tyrrells (1.12x) — the target segment consistently over-buys these
  relative to other customers
- **Under-indexed:** Woolworths (0.69x), Burger Rings (0.68x), Sunbites (0.74x),
  CCs (0.77x), Red Rock Deli (0.78x) — these under-perform with this segment

**Pack size affinity**, by contrast, is weak once you control for brand. Individual
sizes looked like they varied a lot (e.g. 270g at 1.15x), but that's almost
entirely a brand effect — 11 of the 20 brands only come in one pack size each
(all 134g packets are Pringles; all 270g/250g are Twisties). Banding sizes into
Small (<150g) / Standard (150–180g) / Large (200g+) makes this clear: affinity is
1.08x, 0.96x, and 1.04x respectively — essentially flat. **Pack size is not an
independent lever for this segment; brand is.**

*(See `charts/target_segment_deep_dive.png` and `target_segment_brand_affinity.csv`)*

---

## 7. Recommendations for the category review

1. **Prioritise Mainstream Young Singles/Couples and Mainstream Retirees** as the
   headline target segments — together they're already ~16% of sales from just
   20% of customers, and Young Singles/Couples Mainstream specifically shows both
   the largest customer base *and* a statistically robust ~9% price premium.
2. **Lead category/promotional space with Kettle, Doritos, Pringles, Twisties, and
   Tyrrells** for these segments — don't spread promotional spend evenly across all
   20 brands; these five are where the target segment already over-indexes.
3. **Don't lead with pack-size promotions** (e.g. "buy the big bag") for this
   segment specifically — the data doesn't support a size-driven strategy once
   brand is accounted for. Size decisions should follow brand assortment, not
   drive it.
4. **Treat Older/Young Families as a separate, volume-driven segment** — they
   already buy the most per trip; the lever there is likely trip frequency or
   multi-buy deals, not price or brand-switching, and merits its own workstream
   rather than being folded into the Mainstream Singles/Couples strategy above.

---

## 8. Limitations & suggested next steps

- This is chip-category data only — we can't see whether Mainstream Young
  Singles/Couples spend more broadly across the store, which would strengthen
  the "worth targeting" case further.
- One year of data shows *seasonality* (Christmas peak) but not enough history to
  confirm a *growth trend* in any segment — worth re-checking after another
  6–12 months.
- Brand affinity here is based on packet **volume** share; a margin-weighted
  version (if product cost data is available) would sharpen the promotional ROI
  case in point 2 above.

---

## 9. Files accompanying this report

| File | Contents |
|---|---|
| `QVI_transaction_data_clean.csv` | Cleaned transaction data with derived BRAND / PACK_SIZE |
| `QVI_purchase_behaviour_clean.csv` | Customer segment data (passed all checks, no changes needed) |
| `QVI_merged_data.csv` | Final analysis-ready merged dataset |
| `segment_summary.csv` | Full 21-segment metrics table (sales, customers, units/customer, price/unit) |
| `target_segment_brand_affinity.csv` | Brand-level affinity index for the target segment |
| `price_premium_significance_test.csv` | Statistical test backing the price-premium finding |
| `charts/segment_dashboard.png` | 4-panel segment overview (sales, customers, units/customer, price/unit) |
| `charts/sales_trend.png` | Daily sales trend across the year |
| `charts/target_segment_deep_dive.png` | Brand and pack-size affinity for the target segment |
| `code/01_data_cleaning.py` – `04_summary_tables.py` | Full analysis code, in order |
