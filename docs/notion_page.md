# 📊 Marketing Campaign ROI & Attribution Analysis

**Type:** Data Analyst / Business Analyst hybrid · **Tools:** Python, SQL, Excel, interactive dashboard · **Status:** Complete

[🔗 Live interactive dashboard](#) · [🔗 GitHub repository](#) · [📄 Insights memo (PDF)](#)

---

### The problem
A marketing team runs campaigns across paid social, paid search, email, and SEO, and needs to know which channel actually drives revenue — not just clicks.

### Business context
The closest project in this portfolio to real hands-on marketing-analytics experience (HubSpot, Google Analytics, Meta Ads Manager reporting) — reframing existing skill directly into Data Analyst methodology.

### What I did
1. **Cleaned** daily campaign data across 4 channels — fixed inconsistent naming, filled missing spend using rolling averages rather than dropping valid rows.
2. **Calculated CAC, ROAS, and conversion rate** by channel in Excel and SQL.
3. **Built a multi-touch attribution model in Python** on 9,000 customer journeys, comparing first-touch, last-touch, and linear credit.
4. **Computed marginal ROAS** (early vs. late period) to test whether returns hold up as spend scales — not just total ROAS.
5. **Modeled a specific, conservative budget reallocation** rather than naively extrapolating an unusually strong result.

### 🔑 Key insight #1: attribution changes which channel "wins"
> SEO ranks **#1** under first-touch attribution but drops to **#4** under last-touch. Email shows the exact opposite. A last-touch-only budget decision would defund SEO — the channel actually bringing people into the funnel.

### 🔑 Key insight #2: Paid Social is over-funded relative to its marginal returns
> Paid Social gets **71%** of budget for only **16.5%** of revenue, and its ROAS fell **25.4%** (2.61x → 1.94x) as spend scaled — genuine diminishing returns other channels don't show.

### Recommendation
Shift €75,000 from Paid Social to Email using Paid Social's real *marginal* ROAS (not its average) and a deliberately conservative estimate of Email's incremental return. Projected blended ROAS lift: **+17.2%**.

### A note on methodology honesty
Email's simulated ROAS (~148x) is unusually high. Rather than extrapolate that number directly, I capped its assumed incremental return at ~1/3 of the observed average to account for real-world constraints (list size, deliverability) the dataset doesn't capture — and said so explicitly in the write-up rather than presenting the optimistic number as fact.

### Business impact
Because this mirrors real marketing-reporting experience directly, it's the easiest project in the portfolio to defend under follow-up questions — every methodology choice here has a specific, defensible reason.

---

**CV / LinkedIn bullet:**
*Built a multi-touch attribution model comparing first-touch vs. last-touch channel credit across 4 marketing channels; identified that Paid Social's marginal ROAS had fallen 25% despite receiving 71% of budget, and recommended a reallocation projected to lift blended ROAS by 17.2%.*

**Skills demonstrated:** Data cleaning · Multi-touch attribution modeling (Python) · SQL · Marginal analysis · Excel (formula-driven dashboards) · Conservative, defensible scenario modeling
