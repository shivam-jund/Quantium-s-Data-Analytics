# The Complete Guide: Chip Category Analytics Project
### From zero to "I can defend every decision in an interview"

This covers the *whole* project — data cleaning, analysis, statistics, experimentation, and communication — teaching each concept from first principles, then showing exactly how you applied it. Read it once top to bottom, then use it as a reference.

---

## Table of Contents
1. [The 60-Second Version](#1-the-60-second-version)
2. [Part 1: Data Cleaning](#2-part-1-data-cleaning)
3. [Part 2: Analysis, Segmentation & Statistics](#3-part-2-analysis-segmentation--statistics)
4. [Part 3: Experimentation & Causal Inference](#4-part-3-experimentation--causal-inference)
5. [Part 4: Communicating to a Client](#5-part-4-communicating-to-a-client)
6. [Part 5: The Full Tool/Skill Inventory](#6-part-5-the-full-toolskill-inventory)

---

## 1. The 60-Second Version

**The business problem:** A supermarket's Category Manager for chips wants two things: (1) which customers should we target for the next 6 months, and (2) did a new store layout trial actually work, so should we roll it out everywhere?

**What you did, in order:**
1. Cleaned two messy real-world datasets (~265,000 transactions, ~72,000 customers) — fixed data types, removed junk records, engineered new features from raw text.
2. Segmented customers into 21 groups and found who really drives sales, and why — then proved a pricing insight with a statistical test.
3. Ran a **causal inference experiment**: since you can't A/B test a store layout the way you'd A/B test a website, you built a *matched control group* for 3 trial stores and statistically tested whether the trial caused a real uplift.
4. Packaged it all into a client-ready presentation using a structured communication framework (the Pyramid Principle), not just a data dump.

**Why this is a strong project to talk about:** it's not just "I made some charts." It touches data engineering (cleaning), statistics (hypothesis testing), experimental design (causal inference — the hardest and most valuable skill here), and business communication. That's the full stack of what a data/business analyst actually does.

---

## 2. Part 1: Data Cleaning

### 2.1 Why data cleaning is most of the job (concept)

In the real world, nobody hands you a tidy dataset. Surveys have this backwards: people think "data analyst" means building models or dashboards. In practice, **60-80% of real analytics work is figuring out what's wrong with your data before you can trust anything you calculate from it.** If you skip this step, you get *garbage in, garbage out* — a beautiful chart built on a broken number is still wrong, just confidently wrong.

The categories of things that go wrong, and what they'd do to your analysis if you didn't catch them:

| Problem | Example in general | What happens if you don't fix it |
|---|---|---|
| Wrong data type | A date stored as a number | You can't do date math (find months, sort chronologically) |
| Duplicate records | Same transaction logged twice | You double-count revenue |
| Outliers | One value wildly unlike the rest | It skews averages and can hide real patterns |
| Inconsistent categories | "RRD" and "Red Rock Deli" are the same brand but look different to a computer | You undercount that brand's real popularity, split into two "brands" |
| Out-of-scope records | Non-chip products mixed into a chip dataset | You analyze the wrong thing without knowing it |

### 2.2 What you actually found and fixed

You worked with two files: `QVI_transaction_data.xlsx` (264,836 rows: every chip purchase for a year) and `QVI_purchase_behaviour.csv` (72,637 rows: which customer segment each shopper belongs to).

**Fix #1 — Date format.** The `DATE` column was stored as an integer like `43390`, not a real date. This is a classic Excel quirk: Excel/CSV dates are stored as "days since a fixed starting point" (30 Dec 1899, for historical reasons tracing back to old Lotus 1-2-3 spreadsheet software). You converted it with:
```python
pd.to_datetime(df["DATE"], unit="D", origin="1899-12-30")
```
**Why it matters:** without this, you can't group transactions by month, find "the week before Christmas," or do anything date-based.

**Fix #2 — An exact duplicate row.** One transaction was byte-for-byte identical to another — same customer, product, date, everything. You used `df.duplicated()` to find it (this flags any row that's a perfect copy of an earlier row) and dropped it. If you don't, that transaction's revenue gets counted twice.

**Fix #3 — Feature engineering from messy text (the regex part).** The product name column had everything jammed into one string: `"Smiths Crinkle Cut Chips Chicken 170g"`. You needed the **brand** and **pack size** as their own columns to analyze them. This is where regular expressions (regex) come in — a mini-language for pattern-matching inside text.

You used: `df["PROD_NAME"].str.extract(r"(\d+)\s*[gG]\b").astype(int)`

In plain English, this regex says: *"find one or more digits (`\d+`), optionally followed by a space (`\s*`), followed by a lowercase or uppercase 'g' (`[gG]`), where that 'g' is at a word boundary (`\b`, so it doesn't accidentally match inside another word)."* Applied to `"...Chicken 170g"`, it pulls out `170`.

**A real gotcha you caught:** one product was named `"Kettle 135g Swt Pot Sea Salt"` — the size wasn't at the *end* of the string like every other product. A regex anchored to the end of the string would have silently failed on this one row. You caught it by testing the regex against *every single unique product name* first and checking for failures, rather than assuming it would just work — that's the difference between "the code ran" and "the code is correct."

For brand, you took the first word of the product name (`str.split().str[0]`) — simple, but it created a new problem (next section).

**Fix #4 — Entity resolution (brand name consolidation).** Taking "the first word" as brand created duplicates that are really the same thing: `RRD` and `Red` (both mean "Red Rock Deli"), `WW` and `Woolworths`, `Dorito` and `Doritos`, `Smith` and `Smiths`, `Infzns` and `Infuzions`, and more. This is a real, named problem in data work called **entity resolution** — figuring out when two different-looking records refer to the same real-world thing. You built a mapping dictionary and applied it with `.replace()`, taking 28 raw "brands" down to 20 real ones.

**Why this matters commercially:** if you don't fix this, "Red Rock Deli" looks like a small, unpopular brand (because half its sales are hiding under "RRD"), when it's actually a significant player. Any brand-level recommendation built on the dirty data would be wrong.

**Fix #5 — The subtlest one: distinguishing category-scope errors from legitimate data (the "salsa" problem).** The dataset was supposed to be "chips" only, but 9 products had the word "salsa" in the name. The obvious move — and what most people did — is to remove every row containing "salsa." **You checked first, and found that was wrong.** Two of those nine products (`"Smiths...Tomato Salsa 150g"`, `"Red Rock Deli...Salsa & Mzzrlla 150g"`) are actual bags of chips that just happen to be *salsa-flavoured* — sold in the normal 150g chip size. The other seven are genuine tubs of salsa dip, and — this was the tell — **every single one of them was sold in a 300g size that no real chip product uses.** So you removed only the 7 true dip products (using "contains salsa" AND "pack size = 300g" as the combined rule), correctly keeping the 2 flavoured chips.

**This is one of your best interview stories.** It shows you don't just follow the obvious instruction — you verify it, and you use a secondary signal (pack size) to disambiguate when the primary signal (a keyword) is ambiguous.

**Fix #6 — A genuine outlier.** One loyalty card (226000) had two transactions of **200 packets each** in a single purchase — versus a normal basket of 1–5 packets. You checked whether this customer had any *other* activity all year (`df[df.LYLTY_CARD_NBR==226000]`) and found: no, just these two bulk purchases. That's not a household shopper — almost certainly a business buying in bulk for resale or an event. You removed both rows.

**Why this specific check mattered (not just "remove big numbers"):** a data analyst's job isn't to mechanically strip outliers — it's to understand *why* a value is unusual and decide if it belongs in the analysis. A genuine but unusual regular customer should often stay; a data entry error should be fixed, not deleted; a fundamentally different *type* of customer (commercial buyer vs. household shopper) should be excluded because including them would corrupt any "average household" statistic you calculate afterward.

**Fix #7 — Checking for a missing date.** You counted unique dates in the data and got 364, not the 365 you'd expect for a full year. Building the full expected date range and comparing (`pd.date_range` then set-difference) pinpointed **25 December 2018** as the missing day — the store was closed for Christmas. This isn't an error to fix; it's a legitimate gap, and knowing *why* it's missing (rather than assuming your code is broken) is the point.

### 2.3 How to explain this section in an interview

> "The datasets looked clean at first glance — no obvious missing values — but I found six real issues by actively looking for them rather than assuming: a duplicate transaction, dates stored as raw numbers, an outlier customer buying 200 packets who turned out to be a commercial buyer, brand names that were really the same brand written differently, and a subtle one where a naive 'remove anything containing salsa' filter would have wrongly deleted two legitimate chip products — I caught it by checking pack sizes and found the true dip products all shared a telltale 300g size that no real chip uses."

---

## 3. Part 2: Analysis, Segmentation & Statistics

### 3.1 Why segment customers at all? (concept)

If you just calculate "average sales per customer" across everyone, you get a number that describes *nobody*. A family buying 9 packets a week and a single person buying 2 packets a month get blended into a meaningless average. This is related to a classic statistics trap called **Simpson's Paradox** — a trend that appears in overall data can reverse or vanish when you break the data into the right subgroups. The fix is to segment first, then analyze *within* meaningful groups.

You had two dimensions already provided: **LIFESTAGE** (7 categories: young/older/new families, young/midage/older singles-couples, retirees) and **PREMIUM_CUSTOMER** (Budget/Mainstream/Premium — a proxy for spending tier). Crossing them gives 21 segments — small enough to be readable, granular enough to find real patterns.

### 3.2 The four metrics, and why each one (concept: KPI decomposition)

You calculated, per segment:
- **Total sales** — the headline number, but it hides *why*
- **Number of customers** — are there just more people in this segment?
- **Average packets per customer** — are they buying more each trip?
- **Average price per packet** — are they paying more per unit?

This is a **driver tree** (also called KPI decomposition): `Total Sales = Number of Customers × Packets per Customer × Price per Packet`. Breaking a headline number into its multiplicative drivers is one of the single most useful habits in business analytics, because it turns "sales are up" (not actionable) into "sales are up *because we have more customers*, not because they're buying more" (actionable — now you know whether to invest in acquisition or in basket-size promotions).

**What you found:** Families drive sales through the *packets-per-customer* lever (8.7–9.3 packets every trip, regardless of spend tier — larger households need more groceries). Mainstream Young Singles/Couples and Mainstream Retirees drive sales through the *customer-count* lever instead — they buy fewer packets each, but there are simply far more of these customers (7,930 and 6,382 respectively — the two largest segments in the whole dataset) than any other group.

### 3.3 Hypothesis testing and the t-test (concept, from zero)

You noticed something specific: for Young and Midage Singles/Couples, the *Mainstream* spend-tier paid noticeably more per packet ($4.06 and $3.98) than *Budget* or *Premium* customers in the *same* lifestage (~$3.70). That's surprising — you'd expect "Premium" customers to pay the most, not "Mainstream."

But a difference in two averages could just be noise — random sample-to-sample wobble — rather than a real effect. **Hypothesis testing is the formal way to check whether a difference is "real" or could plausibly be chance.**

- **Null hypothesis (H₀):** there is no real difference — Mainstream and Budget/Premium customers pay the same on average, and any gap you see in your sample is just random noise.
- **Alternative hypothesis (H₁):** there is a real difference.
- **A t-test** compares two group means, accounting for how much natural variation ("noise") exists within each group, and produces a **t-statistic** — essentially a signal-to-noise ratio. A big t-statistic means the difference between groups is large *relative to* the normal spread within each group.
- **The p-value** is the probability of seeing a difference this large (or larger) *if the null hypothesis were actually true* — i.e., if there were really no effect. A small p-value means "this would be a very unlikely coincidence if there were truly no difference," which is evidence the difference is real.
- **The common threshold** is p < 0.05 (less than a 5% chance this is a fluke). You got **p < 0.0001** — dramatically below that bar.

You specifically used a **Welch's t-test** (`equal_var=False` in `scipy.stats.ttest_ind`) rather than the standard/Student's t-test. The standard version assumes both groups have equal variance (equal spread of values); Welch's doesn't require that assumption, so it's the safer default when you haven't specifically checked that the two groups vary by similar amounts — which you hadn't, so Welch's was the more defensible choice.

**Result:** t = 38.1, p < 0.0001, on 58,009 transactions. Mainstream customers in this lifestage pay 9.1% more per packet, and this is not explainable by chance.

### 3.4 The confound you controlled for (an important, subtle point)

Notice you didn't test "Mainstream vs. Budget/Premium across *everyone*" — you specifically restricted the test to Young + Midage Singles/Couples. Why? Because lifestage is a **confounding variable**: families naturally buy more than singles for reasons that have nothing to do with spend tier (household size), so mixing lifestages into one big comparison would let a totally unrelated factor masquerade as a "Mainstream effect." By holding lifestage constant and only varying spend-tier, you isolated the thing you actually wanted to measure. (Bonus finding: the same premium did *not* hold for Mainstream Retirees — worth mentioning, since it shows you didn't over-generalize a pattern that only held in part of the data.)

### 3.5 How to explain this section in an interview

> "I broke total sales into its drivers — customer count, basket size, and price — because 'sales are up' isn't actionable on its own; you need to know *why*. That decomposition showed two completely different growth stories: families drive sales through basket size, while Mainstream Young Singles/Couples and Retirees drive it through sheer customer count. Then I noticed Mainstream shoppers were paying more per packet than Budget or Premium in the same age group, which was counterintuitive, so I ran a two-sample t-test — specifically holding lifestage constant so I wasn't letting household-size differences masquerade as a pricing effect — and got p < 0.0001, so I could tell the client with confidence this wasn't noise."

---

## 4. Part 3: Experimentation & Causal Inference
*(This is the most advanced part of the project — and the best thing to talk about in an interview if you want to sound senior.)*

### 4.1 The core problem: correlation isn't causation (concept, from zero)

The business question was: **did the new store layout cause higher sales, or did sales just happen to go up for some other reason at the same time?**

The naive approach: look at the trial store's sales before the trial vs. during the trial. If it went up, the trial worked — right?

**No — and this is the single most important idea in this whole project.** Sales could rise during the trial period for reasons that have nothing to do with the layout: a seasonal effect (maybe that store always does better in March), a general company-wide trend (maybe all stores are growing), local factors (a competitor closed nearby), etc. If you don't account for these, you can't tell how much of the change — if any — the *layout* actually caused. This is called a **confound**: something else that changed at the same time as your treatment, tangled up with its effect.

**The concept you need: the counterfactual.** The real question is "what would sales have been *if we had not* changed the layout?" You can never observe this directly — a store can't simultaneously get the new layout and not get it. So you need to *estimate* it.

### 4.2 The solution: a matched control group (concept, then application)

This is a real, industry-used technique (related to what's called a "synthetic control method" in economics — famously used to study things like the effect of policy changes, e.g. Abadie & Gunadi's California tobacco tax study). The idea:

1. Find another store that historically moved *almost identically* to the trial store, before the trial started.
2. Since that store didn't get the layout change, its behavior during the trial period is your best available estimate of the counterfactual — "what the trial store probably would have done anyway."
3. Compare the trial store's *actual* performance to that estimate. A gap that's bigger than normal month-to-month noise is evidence of a real effect.

**Why "moved almost identically" needs two different checks, not one:**
- **Correlation** checks *trend similarity* — do the two stores' sales go up and down together over time? (A store that's always busier in December and quieter in February, same as your trial store, correlates highly.)
- **Magnitude distance** checks *level similarity* — are the actual dollar amounts close? (Correlation alone can be fooled: a tiny store and a huge store could both reliably jump 10% every December — perfectly correlated, completely different scale, and a bad match.)

You need *both*. You built one function to compute Pearson correlation (a standard −1 to +1 measure of how two series move together) between the trial store and every candidate store, and a second function to compute magnitude distance:
```
1 - (|difference| - min possible difference) / (max possible difference - min possible difference)
```
This rescales the raw dollar-difference onto a clean 0–1 scale, so it can be combined fairly with the correlation score (which is already roughly 0–1). You averaged the two into one score per store, then averaged the sales-score and customer-score into one final ranking, and picked the highest-scoring store *that wasn't the trial store itself* (the trial store trivially "matches" itself perfectly, so it always ranks #1 and has to be excluded).

**Validation — an important habit:** you didn't just trust your own code. You had access to the official solution's *expected* control stores (233, 155, 237) and ran your algorithm to check it reproduced them exactly before trusting any downstream result. It did, on the first pass — strong evidence the method was implemented correctly.

### 4.3 Scaling, then testing significance (concept, then application)

Even the "best" control store won't be *exactly* the same size as the trial store. Before comparing, you rescale the control's sales by a **scaling factor** = (trial store's pre-trial total) ÷ (control store's pre-trial total), so both are on the same footing. Now the trial-period comparison is about *relative movement*, not raw size.

For each trial month, you calculated a **signed percentage difference**: (trial store's actual sales − scaled control's sales) ÷ scaled control's sales. Positive means the trial store outperformed its counterfactual estimate.

To test if that gap is "real," you needed a sense of normal noise. You calculated the **standard deviation** of this same percentage-difference metric *during the pre-trial period* (when, by definition, there was no trial effect yet — so any variation there is just natural month-to-month noise). Then:

```
t-value = (this month's percentage difference) / (standard deviation of pre-trial noise)
```

This is again a signal-to-noise ratio: how big is this month's gap, measured in units of "how much this pair of stores normally wobbles by chance." You compared each t-value against a **critical value** from the t-distribution at 95% confidence with 7 degrees of freedom (7 = the 7 pre-trial months minus 1 — degrees of freedom roughly means "how many independent pieces of information went into estimating the noise level"). If the t-value's absolute size exceeds that critical threshold, the month is flagged as significant.

**A real debugging story worth telling:** your first version of this formula used the *absolute* percentage difference and had an extra scaling term in the denominator. When you ran it, the significance pattern didn't match the known expected results (e.g., store 86 was supposed to show customers-up-but-sales-not-significant, and your first pass didn't show that). Rather than assume the expected answer was wrong, you treated the mismatch as a signal your formula was off, worked back through the math, realized the test needs the *signed* difference (so direction matters) with a simpler, correctly-scaled denominator, fixed it, and re-ran — and this time every single result matched the expected pattern for all three stores and both metrics. That's a genuinely good interview story about verification and debugging, not just "I wrote a function."

### 4.4 What the results actually meant, and why one nuanced result matters

- **Stores 77 and 88:** both sales and customer counts significantly higher in March and April — a clean, internally consistent positive result.
- **Store 86:** customer counts significantly higher in *all three* trial months, but sales significantly higher in only one. More people walked in, but it didn't reliably turn into more revenue.

Rather than just reporting "2 of 3 worked, 1 didn't," you interpreted the *shape* of store 86's result: more customers without proportionally more sales usually points at a lower average transaction value — possibly a different promotion or price point running in that store at the same time, which is itself a confound you flagged for a human to check rather than quietly ignoring. **This is exactly the kind of nuance that separates "ran the numbers" from "did the analysis."**

### 4.5 How to explain this section in an interview

> "The hard part wasn't the statistics, it was the experimental design. You can't A/B test a store layout the way you'd A/B test a website — you only have three trial stores and can't randomly assign customers. So I used a matched-control-group approach: for each trial store, I scored every other full-year store on two things — how closely its trend correlated with the trial store pre-trial, and how close its absolute sales level was — and picked the best match as a stand-in for 'what would have happened without the trial.' Then I tested whether the gap between the trial store's actual performance and its control during the trial period was bigger than normal pre-trial noise, using a t-test. Two of three stores showed a clean, significant uplift in both sales and customers. The third was the interesting one — customers rose significantly every month, but sales didn't follow — which told me to flag a likely pricing or promotion confound rather than call it a failed trial."

---

## 5. Part 4: Communicating to a Client

### 5.1 The Pyramid Principle (concept)

Developed by Barbara Minto at McKinsey, the core idea is: **executives want the answer first, then the supporting logic, then the detail — not the journey you took to get there.** This is the *opposite* order from how you actually did the analysis (which was necessarily bottom-up: explore data → find patterns → test them → draw conclusions). Good communication means **inverting** that order for the final deliverable.

Structure:
1. **Governing thought** — the one-sentence answer/recommendation, stated up front.
2. **Grouped supporting arguments** — ideally 2–4 main points (the "rule of three" — human working memory handles a small number of grouped ideas far better than a long flat list) that, together, support the governing thought.
3. **Supporting data** — the evidence for each argument, pushed down a level so it doesn't clutter the headline logic.

**How you applied it:** your executive summary slide states the recommendation ("Target Mainstream Young Singles/Couples and roll out the layout") *before* any chart appears, backed by exactly three grouped pillars (segment value, trial result, concrete next steps) — mirroring the pyramid exactly. Every subsequent slide is one piece of supporting evidence for one of those three pillars, in a logical order (category insights, then trial results, then recommendations) rather than the chronological order you actually worked in.

### 5.2 Design consistency and audience awareness (concept)

- **Know your audience's data literacy.** A Category Manager isn't a statistician — so "9.1% more, and we're confident it's a real effect (p < 0.0001)" is better slide copy than "t = 38.11, p = 4.2e-289." The rigor is still there, just translated.
- **Visual consistency builds trust.** If "Mainstream" is coral in one chart and blue in another, a reader has to re-learn your legend every slide, which is friction and looks unpolished. You fixed one color per concept (Budget/Mainstream/Premium; Trial/Control) and held it for the entire deck.
- **Lead with the takeaway, not the chart.** Every content slide's *title* is a full sentence stating the insight ("Mainstream shoppers pay more for the same category"), not a label ("Price by Segment") — so someone skimming just the titles gets the whole argument.

### 5.3 How to explain this section in an interview

> "I used the Pyramid Principle — leading every deliverable with the recommendation, not the methodology, then grouping the supporting evidence into three clear pillars instead of listing everything I found. I also kept strict visual consistency across every chart, and translated statistical language into business language on the slides themselves while keeping the rigorous numbers available for anyone who wanted to dig in — because the audience was a Category Manager, not a data scientist, and good communication means adapting to that."

---

## 6. Part 5: The Full Tool/Skill Inventory

**Languages & core libraries**
- **Python** — the whole analysis
- **pandas** — loading, cleaning, reshaping data (`groupby`, `pivot_table`, `merge`, string/regex methods)
- **numpy** — numerical operations, array math
- **scipy.stats** — t-tests (`ttest_ind`), t-distribution critical values (`t.ppf`)
- **matplotlib** — every chart, styled to a consistent brand palette
- **python-pptx** — programmatically building the PowerPoint deck (templates, native tables, text boxes, images) rather than manually clicking through slides

**Statistical/analytical concepts**
- Data cleaning: type conversion, deduplication, outlier detection, regex feature extraction, entity resolution
- Descriptive statistics & KPI decomposition (driver trees)
- Hypothesis testing: null/alternative hypotheses, t-tests (Welch's vs. Student's), p-values, statistical significance, confounding variables
- Causal inference / experimental design: counterfactual reasoning, matched control groups, correlation vs. magnitude similarity, scaling factors, degrees of freedom, critical values, confidence

**Business/communication concepts**
- Customer segmentation
- The Pyramid Principle
- Audience-aware communication
- Visual design consistency

---

*Next: open `02_INTERVIEW_CHEAT_SHEET.md` for the condensed, quick-scan version — resume bullets, the elevator pitch, and a Q&A bank for the night before an interview.*
