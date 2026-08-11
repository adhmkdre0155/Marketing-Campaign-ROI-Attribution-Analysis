-- ============================================================
-- Marketing Campaign ROI & Attribution Analysis — Queries
-- Table: campaigns (loaded from campaign_performance_clean.csv)
-- ============================================================

-- 1. Channel summary: CAC, ROAS, conversion rate (core diagnostic view)
SELECT
    Channel,
    ROUND(SUM(Spend), 0) AS TotalSpend,
    ROUND(SUM(Revenue), 0) AS TotalRevenue,
    SUM(Conversions) AS TotalConversions,
    ROUND(SUM(Spend) / NULLIF(SUM(Conversions), 0), 2) AS CAC,
    ROUND(SUM(Revenue) / NULLIF(SUM(Spend), 0), 2) AS ROAS,
    ROUND(SUM(Conversions) * 100.0 / NULLIF(SUM(Clicks), 0), 2) AS ConversionRatePct
FROM campaigns
GROUP BY Channel
ORDER BY ROAS DESC;

-- 2. Monthly trend by channel (spend and revenue)
SELECT
    Month,
    Channel,
    ROUND(SUM(Spend), 0) AS MonthlySpend,
    ROUND(SUM(Revenue), 0) AS MonthlyRevenue
FROM campaigns
GROUP BY Month, Channel
ORDER BY Month, Channel;

-- 3. Spend vs. revenue scatter input (daily granularity, for the dashboard)
SELECT
    Channel,
    Date,
    Spend,
    Revenue
FROM campaigns
ORDER BY Channel, Date;

-- 4. Marginal ROAS proxy: earliest vs. latest quarter of the period, per channel
--    (Paid Social's spend grows fastest — this query surfaces whether its
--    ROAS holds up as spend scales, or shows diminishing returns)
WITH ranked AS (
    SELECT
        Channel, Month, SUM(Spend) AS MonthSpend, SUM(Revenue) AS MonthRevenue,
        NTILE(4) OVER (PARTITION BY Channel ORDER BY Month) AS Quartile
    FROM campaigns
    GROUP BY Channel, Month
)
SELECT
    Channel,
    ROUND(SUM(CASE WHEN Quartile = 1 THEN MonthRevenue END) /
          NULLIF(SUM(CASE WHEN Quartile = 1 THEN MonthSpend END), 0), 2) AS EarlyROAS,
    ROUND(SUM(CASE WHEN Quartile = 4 THEN MonthRevenue END) /
          NULLIF(SUM(CASE WHEN Quartile = 4 THEN MonthSpend END), 0), 2) AS LateROAS
FROM ranked
GROUP BY Channel
ORDER BY LateROAS DESC;

-- 5. Total spend share vs. total revenue share by channel — highlights where
--    budget allocation is out of step with revenue contribution
SELECT
    Channel,
    ROUND(SUM(Spend) * 100.0 / (SELECT SUM(Spend) FROM campaigns), 1) AS SpendSharePct,
    ROUND(SUM(Revenue) * 100.0 / (SELECT SUM(Revenue) FROM campaigns), 1) AS RevenueSharePct
FROM campaigns
GROUP BY Channel
ORDER BY SpendSharePct DESC;
