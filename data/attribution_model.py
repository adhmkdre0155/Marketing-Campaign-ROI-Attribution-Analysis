"""
Multi-touch attribution model for the Marketing Campaign ROI & Attribution
Analysis project.

Compares two attribution models on the same underlying customer journeys:
  - First-touch: 100% of revenue credited to the FIRST channel a customer touched
  - Last-touch:  100% of revenue credited to the LAST channel before conversion

The point of this comparison is not to pick a "correct" model — it's to show
that channel-level revenue credit (and therefore any ROAS/budget decision
built on it) depends heavily on which attribution model is used. A channel
that looks weak under one model can look strong under another.
"""
import pandas as pd

df = pd.read_csv("customer_journeys_raw.csv", parse_dates=["Timestamp"])

# Clean: standardize channel names (same messiness could exist here in a real
# extract; this dataset was generated clean, but we still assert the expected
# set defensively)
valid_channels = {"SEO", "Paid Social", "Paid Search", "Email"}
df = df[df["Channel"].isin(valid_channels)]

converted = df[df["Converted"] == "Y"].copy()
converted = converted.sort_values(["CustomerID", "TouchpointOrder"])

# First-touch: first row per CustomerID
first_touch = converted.groupby("CustomerID").first().reset_index()
first_touch_credit = first_touch.groupby("Channel")["Revenue"].sum().round(2)

# Last-touch: last row per CustomerID
last_touch = converted.groupby("CustomerID").last().reset_index()
last_touch_credit = last_touch.groupby("Channel")["Revenue"].sum().round(2)

# Linear (even split across all touchpoints) — a third model for context
converted["TouchCount"] = converted.groupby("CustomerID")["TouchpointOrder"].transform("max")
converted["LinearRevenue"] = converted["Revenue"] / converted["TouchCount"]
linear_credit = converted.groupby("Channel")["LinearRevenue"].sum().round(2)

comparison = pd.DataFrame({
    "FirstTouchRevenue": first_touch_credit,
    "LastTouchRevenue": last_touch_credit,
    "LinearRevenue": linear_credit,
}).fillna(0)

comparison["FirstVsLast_Diff"] = (comparison["FirstTouchRevenue"] - comparison["LastTouchRevenue"]).round(2)
comparison["FirstVsLast_PctDiff"] = (
    (comparison["FirstTouchRevenue"] - comparison["LastTouchRevenue"])
    / comparison["LastTouchRevenue"] * 100
).round(1)

comparison = comparison.sort_values("LastTouchRevenue", ascending=False)
comparison.to_csv("attribution_comparison.csv")

print("=== Attribution Model Comparison ===")
print(comparison.to_string())
print()

n_converted_customers = converted["CustomerID"].nunique()
total_revenue = first_touch["Revenue"].sum()
print(f"Converted customers analyzed: {n_converted_customers}")
print(f"Total attributed revenue: EUR {total_revenue:,.0f}")

# Headline: which channel's ranking flips between models?
ft_rank = comparison["FirstTouchRevenue"].rank(ascending=False)
lt_rank = comparison["LastTouchRevenue"].rank(ascending=False)
print("\nRank under First-Touch vs Last-Touch:")
for ch in comparison.index:
    print(f"  {ch}: First-touch rank {int(ft_rank[ch])}, Last-touch rank {int(lt_rank[ch])}")
