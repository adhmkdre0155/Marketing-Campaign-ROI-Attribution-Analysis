"""
Cleaning step for the campaign performance dataset.
  1. Standardize channel names (fix casing, underscores)
  2. Remove exact duplicate rows
  3. Handle missing Spend: fill with the channel's 7-day rolling average rather
     than dropping the row (Impressions/Clicks/Conversions/Revenue are still
     valid on days with missing spend tracking — only the cost side is gappy)
  4. Add derived columns: CAC, ROAS, ConversionRate, CTR
"""
import pandas as pd
import numpy as np

df = pd.read_csv("campaign_performance_raw.csv", parse_dates=["Date"])
raw_rows = len(df)

# 1) Standardize channel names
channel_map = {
    "paid social": "Paid Social", "paid_social": "Paid Social", "PAID SOCIAL": "Paid Social",
    "paid search": "Paid Search", "paid_search": "Paid Search", "PAID SEARCH": "Paid Search",
    "email": "Email", "EMAIL": "Email",
    "seo": "SEO", "Seo": "SEO",
}
df["Channel"] = df["Channel"].astype(str).str.strip()
df["Channel"] = df["Channel"].apply(lambda x: channel_map.get(x.lower().replace("_", " "), x))
df["Channel"] = df["Channel"].replace({
    "Paid_Social": "Paid Social", "Paid_Search": "Paid Search",
})

# 2) Remove exact duplicates
df = df.drop_duplicates(subset=["Date", "Channel"], keep="first")
after_dedupe = len(df)

# 3) Fill missing spend using each channel's 7-day rolling average
df = df.sort_values(["Channel", "Date"])
df["Spend"] = pd.to_numeric(df["Spend"], errors="coerce")
df["Spend"] = df.groupby("Channel")["Spend"].transform(
    lambda s: s.fillna(s.rolling(7, min_periods=1, center=True).mean())
)
df["Spend"] = df["Spend"].round(2)

# 4) Derived metrics
df["CAC"] = (df["Spend"] / df["Conversions"].replace(0, np.nan)).round(2)
df["ROAS"] = (df["Revenue"] / df["Spend"].replace(0, np.nan)).round(3)
df["ConversionRate"] = (df["Conversions"] / df["Clicks"].replace(0, np.nan) * 100).round(3)
df["CTR"] = (df["Clicks"] / df["Impressions"].replace(0, np.nan) * 100).round(3)
df["Month"] = df["Date"].dt.to_period("M").astype(str)
df["Week"] = df["Date"].dt.to_period("W").astype(str)

df = df.sort_values("Date").reset_index(drop=True)
df.to_csv("campaign_performance_clean.csv", index=False)

print(f"Raw rows:      {raw_rows}")
print(f"After dedupe:  {after_dedupe}  ({raw_rows - after_dedupe} duplicates removed)")
print(f"Final rows:    {len(df)}")
print(f"Missing spend remaining: {df['Spend'].isna().sum()}")
print(f"Channels: {sorted(df['Channel'].unique())}")
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
