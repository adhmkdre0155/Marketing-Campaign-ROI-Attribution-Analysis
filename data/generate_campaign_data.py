"""
Generates simulated daily marketing campaign performance data across 4 channels:
Paid Social, Paid Search, Email, SEO (Organic Search).

Built-in realistic pattern (to be discovered, not asserted): Paid Social spend
grows steadily over the period and shows diminishing marginal returns (each
additional euro of spend produces less incremental revenue at high spend
levels) — a genuine saturation effect. Email is comparatively underinvested
with room to grow at strong marginal ROAS.

Intentionally messy: inconsistent channel-name casing, ~2% missing spend rows
(tracking gaps), a handful of duplicate rows, and a few zero-impression days.
"""
import random
import csv
from datetime import date, timedelta

random.seed(55)

PERIOD_START = date(2024, 1, 1)
PERIOD_END = date(2025, 10, 31)
n_days = (PERIOD_END - PERIOD_START).days

CHANNELS = {
    "Paid Social": {
        "base_daily_spend": 900, "spend_growth_per_day": 4.6,   # spend ramps up over time, crosses saturation
        "base_cpm": 8.5, "ctr": 0.012, "cvr": 0.028, "aov": 68,
        "saturation_k": 3200,  # diminishing returns kick in above this daily spend
    },
    "Paid Search": {
        "base_daily_spend": 650, "spend_growth_per_day": 0.15,
        "base_cpm": 22.0, "ctr": 0.035, "cvr": 0.045, "aov": 74,
        "saturation_k": 2600,
    },
    "Email": {
        "base_daily_spend": 90, "spend_growth_per_day": 0.02,
        "base_cpm": 1.2, "ctr": 0.045, "cvr": 0.065, "aov": 61,
        "saturation_k": 999999,  # effectively no saturation in this range — underinvested
    },
    "SEO": {
        "base_daily_spend": 180, "spend_growth_per_day": 0.05,   # mostly content/tooling cost
        "base_cpm": 0.9, "ctr": 0.021, "cvr": 0.031, "aov": 70,
        "saturation_k": 999999,
    },
}

def diminishing_multiplier(spend, k):
    """Returns a multiplier <1 that kicks in as spend approaches/exceeds k (saturation point)."""
    if spend <= k * 0.6:
        return 1.0
    excess = spend - k * 0.6
    return max(0.35, 1.0 - (excess / k) * 0.55)

CASING = lambda name: random.choice([name, name.upper(), name.lower(), name.replace(" ", "_")])

rows = []
for day_offset in range(n_days + 1):
    d = PERIOD_START + timedelta(days=day_offset)
    dow_mult = 0.75 if d.weekday() >= 5 else 1.0  # lighter weekend spend/volume

    for channel, cfg in CHANNELS.items():
        spend = cfg["base_daily_spend"] + cfg["spend_growth_per_day"] * day_offset
        spend *= dow_mult * random.uniform(0.85, 1.15)
        spend = round(max(0, spend), 2)

        sat_mult = diminishing_multiplier(spend, cfg["saturation_k"])

        impressions = int((spend / cfg["base_cpm"]) * 1000 * random.uniform(0.9, 1.1))
        clicks = int(impressions * cfg["ctr"] * random.uniform(0.85, 1.15))
        conversions = int(clicks * cfg["cvr"] * sat_mult * random.uniform(0.85, 1.15))
        revenue = round(conversions * cfg["aov"] * random.uniform(0.9, 1.1), 2)

        # ~2% missing spend tracking (common real-world gap)
        spend_val = "" if random.random() < 0.02 else spend

        channel_raw = CASING(channel) if random.random() < 0.15 else channel

        rows.append([d.strftime("%Y-%m-%d"), channel_raw, spend_val, impressions, clicks,
                     conversions, revenue])

# Inject ~30 duplicate rows (export error)
dupes = random.sample(rows, 30)
rows.extend(dupes)
random.shuffle(rows)

header = ["Date", "Channel", "Spend", "Impressions", "Clicks", "Conversions", "Revenue"]
with open("campaign_performance_raw.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(rows)

print(f"Generated {len(rows)} raw campaign performance rows.")
