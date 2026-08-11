"""
Generates simulated customer journey (multi-touchpoint) data for the
first-touch vs. last-touch attribution comparison.

Built-in realistic pattern: SEO and Paid Social skew toward the START of the
journey (discovery/awareness), while Email and Paid Search skew toward the
END of the journey (consideration/close) — a standard, realistic funnel
pattern that produces genuine, discoverable divergence between first-touch
and last-touch attribution, rather than an asserted conclusion.
"""
import random
import csv
from datetime import date, timedelta, datetime

random.seed(77)

CHANNELS = ["SEO", "Paid Social", "Paid Search", "Email"]

# Position weighting: how likely each channel is to appear early vs late in a journey
EARLY_WEIGHT = {"SEO": 0.42, "Paid Social": 0.34, "Paid Search": 0.14, "Email": 0.10}
LATE_WEIGHT  = {"SEO": 0.12, "Paid Social": 0.16, "Paid Search": 0.30, "Email": 0.42}

PERIOD_START = date(2024, 1, 1)
PERIOD_END = date(2025, 10, 31)
n_days = (PERIOD_END - PERIOD_START).days

AOV_BY_CHANNEL_MIX = 70  # baseline; actual revenue randomized per journey

rows = []
customer_id = 800000
N_JOURNEYS = 9000

for _ in range(N_JOURNEYS):
    customer_id += 1
    n_touches = random.choices([1, 2, 3, 4, 5], weights=[0.20, 0.30, 0.25, 0.15, 0.10], k=1)[0]
    converted = random.random() < 0.62  # journeys in this extract are the ones that eventually convert or drop

    start_day = random.randint(0, n_days - 14)
    journey_date = PERIOD_START + timedelta(days=start_day)

    touches = []
    for t in range(n_touches):
        position_frac = t / max(1, n_touches - 1) if n_touches > 1 else 0.5
        # Blend early/late weighting based on position in the journey
        weights = {c: EARLY_WEIGHT[c] * (1 - position_frac) + LATE_WEIGHT[c] * position_frac for c in CHANNELS}
        total = sum(weights.values())
        weights = {c: w / total for c, w in weights.items()}
        channel = random.choices(CHANNELS, weights=list(weights.values()), k=1)[0]
        ts = journey_date + timedelta(days=t * random.randint(1, 4),
                                        hours=random.randint(8, 20))
        touches.append((channel, ts))

    revenue = round(random.uniform(35, 220), 2) if converted else 0

    for i, (channel, ts) in enumerate(touches):
        rows.append([
            customer_id, i + 1, channel, ts.strftime("%Y-%m-%d %H:%M"),
            "Y" if converted else "N", revenue if converted else 0
        ])

random.shuffle(rows)
header = ["CustomerID", "TouchpointOrder", "Channel", "Timestamp", "Converted", "Revenue"]
with open("customer_journeys_raw.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(rows)

print(f"Generated {len(rows)} touchpoint rows across {N_JOURNEYS} customer journeys.")
