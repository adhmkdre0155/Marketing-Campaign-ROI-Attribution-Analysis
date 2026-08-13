# Marketing Campaign ROI & Attribution Analysis

**Data Analyst / Business Analyst hybrid portfolio project — Adham AlHers**
[Live interactive dashboard](https://adhmkdre0155.github.io/Marketing-Campaign-ROI-Attribution-Analysis/dashboard/index.html) · [LinkedIn](https://www.linkedin.com/in/adhamalhers/) · [Portfolio home](https://app.notion.com/p/Data-Business-Analyst-Portfolio-Adham-AlHers-3b63ac1ddec780c1b2d6c221c6bcbb59)

## Problem statement
A marketing team runs campaigns across paid social, paid search, email, and SEO, and needs to know which channel actually drives revenue — not just clicks.

## Business context
This is the closest project in the portfolio to real hands-on marketing-analytics experience (HubSpot, Google Analytics, Meta Ads Manager reporting) — it reframes that existing skill directly into Data Analyst language and methodology.

## Dataset
Two simulated datasets, generated to produce genuine, discoverable patterns rather than scripted conclusions:
- **[Clean Campaign Performance](campaign_performance_clean.csv)** — 2,680 cleaned daily rows (2024–2025) across 4 channels: Channel, Spend, Impressions, Clicks, Conversions, Revenue.
- **[Raw Customer Journeys](customer_journeys_raw.csv)** — 23,708 touchpoints across 9,000 simulated customer journeys, used for the attribution model. Built with a realistic funnel pattern (SEO/Paid Social skew early in the journey, Email/Paid Search skew late) rather than asserting the attribution result directly.

## Tools
Python (pandas) for cleaning and the attribution model · SQL (SQLite) for channel-level analysis · Excel (openpyxl, formula-driven) for the KPI dashboard · Chart.js for the interactive dashboard (standing in for Power BI — see note below).

## Repository structure
```
├── data/
│   ├── generate_campaign_data.py       # Generates daily campaign performance (with built-in saturation effect)
│   ├── generate_customer_journeys.py   # Generates multi-touch customer journeys
│   ├── clean_campaign_data.py          # Cleaning: channel names, duplicates, missing spend
│   ├── attribution_model.py            # First-touch vs. last-touch vs. linear attribution comparison
│   ├── campaign_performance_clean.csv
│   ├── customer_journeys_raw.csv
│   ├── attribution_comparison.csv
│   └── marginal_roas.csv
├── sql/
│   └── queries.sql                     # CAC/ROAS/conversion rate by channel, marginal ROAS, spend-vs-revenue share
├── excel/
│   └── Marketing_ROI_Dashboard.xlsx    # Formula-driven KPI dashboard with charts
├── dashboard/
│   └── index.html                      # Self-contained interactive web dashboard
└── docs/
    └── insights_memo.pdf
```

## Step-by-step approach
1. **Cleaned the data** — standardized inconsistent channel-name casing, removed duplicate rows, and filled ~2% missing spend using each channel's 7-day rolling average rather than dropping valid conversion/revenue data alongside it.
2. **Calculated CAC, ROAS, and conversion rate by channel** in both Excel (SUMIF-based) and SQL.
3. **Built a multi-touch attribution model in Python** comparing first-touch, last-touch, and linear credit across the same 9,000 customer journeys — showing that channel "performance" depends heavily on which model is used, not just on the underlying data.
4. **Computed marginal ROAS** (early-period vs. late-period ROAS per channel) to test whether each channel's returns hold up as spend scales — the metric that actually should drive a budget decision, not total ROAS or total revenue.
5. **Modeled a specific budget reallocation** with an explicit, conservative assumption about Email's incremental returns, rather than extrapolating its very high average ROAS naively.

**Note on "Power BI":** Power BI Desktop wasn't accessible in this environment to publish from, so the same visual outcome (channel ROI comparison, spend-vs-revenue trend, attribution comparison) was built as a self-contained interactive HTML dashboard instead — fully interactive, hostable for free, no Power BI license required to view.

## Key insight #1: attribution model choice changes which channel "wins"
SEO ranks **#1** in revenue credit under first-touch attribution but drops to **#4** under last-touch. Email shows the exact opposite pattern. A budget decision based on last-touch data alone would systematically defund SEO — the channel actually bringing new people into the funnel.

## Key insight #2: Paid Social is over-funded relative to its marginal returns
Paid Social receives **71.0%** of total budget but generates only **16.5%** of revenue. Its ROAS fell from 2.61x to 1.94x (**-25.4%**) as spend scaled up — genuine diminishing returns, while Email, SEO, and Paid Search show no equivalent decline.

## Recommendation
Shift a modest €75,000 from Paid Social to Email, using Paid Social's actual **marginal** ROAS (1.94x, not its inflated historical average) for what's given up, and a deliberately conservative estimate of Email's incremental return (capped at ~1/3 of its observed average, to account for list-size/deliverability limits not captured in this dataset). Projected blended ROAS lift: **+17.2%**.

## Business impact
Because this mirrors real HubSpot/GA/Meta Ads reporting experience directly, it's the project in this portfolio easiest to defend under follow-up questions in an interview — every methodology choice here (why marginal ROAS over total ROAS, why cap Email's assumed return, why attribution model choice matters) has a specific, defensible reason attached.

---
*Datasets are simulated for portfolio purposes, with the attribution divergence and diminishing-returns pattern generated from the underlying simulation rather than scripted into the summary. All cleaning, modeling, and SQL logic is fully reproducible.*
