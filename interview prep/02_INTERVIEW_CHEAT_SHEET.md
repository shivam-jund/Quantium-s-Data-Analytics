# Interview & Resume Cheat Sheet
### Quick-scan version. Read the full guide first — this is for the night before.

---

## The Elevator Pitch (memorize this, 30 seconds)

> "I ran an end-to-end retail analytics project for a supermarket chip category — cleaned and merged two real-world datasets covering 265,000 transactions and 72,000 customers, segmented customers to find who actually drives sales and proved a pricing insight with a statistical test, then designed a matched-control-group experiment to evaluate a store layout trial across three test stores — which is real causal inference, not just A/B testing — and packaged the findings into a client-ready presentation using the Pyramid Principle. It's the full pipeline: data cleaning, statistics, experimental design, and business communication."

---

## Key Numbers to Have Ready

| Fact | Number |
|---|---|
| Transactions analyzed | 264,836 raw → 249,667 after cleaning |
| Customers | 71,517 |
| Total category sales | $1,819,778.40 (1 year) |
| Distinct brands after cleaning | 20 (from 28 raw text variants) |
| Price premium finding | Mainstream pays **9.1% more** per packet than Budget/Premium (Young + Midage Singles/Couples only) |
| Statistical significance | t = 38.1, **p < 0.0001** |
| Trial stores | 77, 86, 88 |
| Control stores selected | 233, 155, 237 (via correlation + magnitude-distance matching) |
| Trial result | 2 of 3 stores (77, 88) significant uplift in sales **and** customers; store 86 significant in customers only |
| Candidate control pool | 260 stores (of 272) with a full 12-month history |
| Confidence level used | 95% (critical t-value, 7 degrees of freedom) |

---

## Resume Bullet Points (pick 3-4, tailor to the role)

**If the role is more data/technical:**
- Cleaned and merged two real-world retail datasets (265K+ transactions, 72K+ customers) in Python/pandas, engineering features via regex extraction and resolving data-quality issues including entity resolution (brand name consolidation) and category-scope misclassification
- Performed customer segmentation across 21 lifecycle × spend-tier segments and validated a 9.1% pricing-premium finding using a two-sample Welch's t-test (p < 0.0001), controlling for lifestage as a confounding variable
- Designed and executed a matched-control-group causal inference study to evaluate a retail store trial across 3 test stores, building a correlation + magnitude-distance scoring function to select statistically comparable controls from a pool of 260 candidate stores, then t-tested trial-period significance against pre-trial noise
- Built a 16-slide executive presentation programmatically (python-pptx) with a consistent brand system and Pyramid Principle structure, translating statistical findings into business-ready recommendations

**If the role is more business/product/consulting-flavored:**
- Delivered a data-driven category strategy recommendation for a retail chip category, identifying a high-value target customer segment worth 16%+ of category sales from just 20% of customers
- Ran a rigorous experiment to test whether a store layout change caused a real sales uplift (not just correlation), using matched control stores as a counterfactual benchmark — found significant uplift in 2 of 3 trial stores and flagged a likely pricing confound in the third rather than over-generalizing
- Presented findings and recommendations to a (simulated) Category Manager stakeholder using the Pyramid Principle, translating statistical rigor into clear, actionable business language

---

## Q&A Bank

**"Walk me through a project you're proud of."**
→ Use the elevator pitch, then let them steer into whichever part (cleaning / stats / experiment / presentation) they want to go deeper on.

**"Tell me about a time you found a mistake in your own work."**
→ The salsa/dip story (Complete Guide, §2.2, Fix #5). Naive filter would've deleted 2 legitimate products; you checked pack sizes, found the 7 real dips all shared a telltale 300g size, fixed the rule. Shows verification instinct, not just "I followed the steps."

**"Tell me about a bug you had to debug."**
→ The t-value formula story (Complete Guide, §4.3). Validated your control-store selection against known expected answers, results matched — then validated the significance test the same way, and it *didn't* match. Treated that as a signal to re-derive the math rather than assume the reference was wrong. Found you needed the signed (not absolute) percentage difference. Re-ran, everything matched.

**"What's a p-value, in plain English?"**
→ "It's the probability of seeing a difference this big — or bigger — by pure chance, if there were actually no real effect. A small p-value means that would be a very unlikely coincidence, so the effect is probably real. Under 0.05 is the usual bar; I got under 0.0001."

**"How do you know a result is statistically significant vs. just noise?"**
→ Explain t-test as a signal-to-noise ratio: measure the natural variation you'd expect anyway (I used the pre-trial period's own spread as the noise baseline), then check whether the observed effect is large relative to that baseline. If it's many multiples of the normal noise, it's unlikely to be chance.

**"How would you test whether a change actually *caused* an outcome, not just correlated with it?"** (this is the big one — shows causal thinking)
→ "You need a counterfactual — an estimate of what would have happened without the change. I couldn't run a true randomized experiment on store layouts, so I built a matched control group: found stores that historically moved almost identically to each trial store, using both trend correlation and absolute-level similarity, then used that control's trial-period behavior as my best estimate of what the trial store would have done anyway. The gap between actual and that estimate, tested against normal pre-trial noise, is the causal effect."

**"Why not just compare the trial store's sales before vs. after?"**
→ "Because anything else that changed over that time window — seasonality, a broader trend, competitor activity — would get mixed into your estimate of the trial's effect, and you'd have no way to separate them. A control group that experienced the same time period but not the treatment lets you net that out."

**"Why did you need both correlation AND magnitude distance for matching stores — why not just one?"**
→ "Correlation alone can be fooled — two stores of very different sizes can still move up and down together and score a perfect correlation, but they're not really comparable in absolute terms. Magnitude alone can also be fooled — two stores could have similar average sales but be totally uncorrelated month to month, moving independently. You need both a similar trend *and* a similar scale for a control to be a fair stand-in."

**"What are the limitations of your approach? What would you do differently with more time?"**
→ Good honest answers: only one year of data limits your ability to see a multi-year trend vs. a one-off blip; only 3 trial stores means you can't statistically generalize "trials always work this way"; a single best-match control store is more fragile than a weighted blend of several similar stores (a fuller "synthetic control" approach); monthly granularity could be tightened to weekly for more data points; adding cost/margin data (not just revenue) would sharpen the ROI case for brand recommendations.

**"How do you communicate technical findings to a non-technical audience?"**
→ Pyramid Principle: lead with the answer, not the method. Translate statistics into plain business language on the slide itself, but keep the rigorous numbers available for anyone who wants to verify. Use consistent visual language throughout so the reader isn't re-learning your chart legend every slide.

**"What was the most surprising finding?"**
→ Two good options: (1) Mainstream shoppers — not Premium — pay the most per packet, which is counterintuitive on the label alone. (2) Store 86: customers up significantly every month, but sales not following — a result that *looks* like a clean failure until you dig into the shape of it and realize it's more likely a pricing/promo confound than a failed layout.

**"Why does this project matter / what's the business impact?"**
→ Two concrete, executable recommendations: (1) a specific customer segment to prioritize with specific brands to range/promote, backed by a significant, quantified pricing insight; (2) a statistically validated go/no-go on a real capital decision (store layout rollout), with an honest flag on the one store that needs more investigation before generalizing — exactly the kind of nuanced, defensible recommendation a real stakeholder needs to act on.

---

## If They Ask You to Whiteboard/Explain the Math

**T-test formula (conceptually):** `t = (difference between group means) / (standard error of that difference)` — a signal-to-noise ratio.

**Magnitude distance formula (the one you implemented):**
```
1 - (|observed difference| - min possible difference) / (max possible difference - min possible difference)
```
Rescales any raw difference onto a clean 0-to-1 "similarity" scale, where 1 = identical, 0 = the least similar candidate available.

**Trial significance t-value (the one you implemented):**
```
t = (this month's % difference vs. scaled control) / (std dev of % differences during the pre-trial period)
```
