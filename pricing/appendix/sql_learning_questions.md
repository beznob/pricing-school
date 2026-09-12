# Learning Questions: SQL, Data Analysis & Pricing Insights

A progressive journey from basic queries to advanced analytical thinking. Work through these in order, running SQL in Jupyter or directly against `meridian.db`. The goal is to both upskill in SQL and develop intuition about pricing dynamics.

---

## Part 1: Foundation (SQL Basics + Data Exploration)

### 1.1 Data Familiarity
**What:** Count rows and describe the grain of each table.
```sql
SELECT 'fct_daily' as table_name, COUNT(*) as row_count FROM fct_daily
UNION ALL
SELECT 'fct_quotes', COUNT(*) FROM fct_quotes
UNION ALL
SELECT 'fct_transactions', COUNT(*) FROM fct_transactions
UNION ALL
SELECT 'dim_sites', COUNT(*) FROM dim_sites
UNION ALL
SELECT 'dim_customers', COUNT(*) FROM dim_customers
```
**Why:** Understand the scale and grain (day×site×product vs quote-level vs transaction-level) of your data.
**Insight:** What's the ratio of quotes to transactions? What does that tell you about conversion?

---

### 1.2 Dimension Exploration
**Question:** What are the 6 sites, 3 products, and 4 customer segments in the data?
```sql
SELECT * FROM dim_sites;
SELECT * FROM dim_products;
SELECT * FROM dim_segments;
```
**Why:** Know your business structure before analyzing it.
**Insight:** Which sites are airports? Which have the highest base margin? Which segment has the largest population share?

---

### 1.3 Date Range
**Question:** What date range does the data cover?
```sql
SELECT MIN(date) as start_date, MAX(date) as end_date, COUNT(DISTINCT date) as unique_days
FROM fct_daily;
```
**Why:** Understand what period you're analyzing (2 years? 1 month?).
**Insight:** Is it enough data to see seasonality? Full years or partial?

---

### 1.4 Daily Volume Patterns
**Question:** How do daily quotes and orders vary across the year? Pick one site.
```sql
SELECT
    date,
    quotes,
    orders,
    ROUND(100.0 * orders / NULLIF(quotes, 0), 1) as conversion_rate_pct
FROM fct_daily
WHERE site_id = 'S01' AND product_id = 'EUR_CASH'
ORDER BY date
LIMIT 30;
```
**Why:** Learn to filter, calculate rates, and spot patterns in time series.
**Insight:** Does volume correlate with time of year? Are there spikes or troughs?

---

## Part 2: Joins & Multi-Table Thinking

### 2.1 Enrich Daily with Site Names
**Question:** For the top 3 sites by turnover, show date, site name, and revenue.
```sql
SELECT
    d.date,
    d.site_id,
    s.site_name,
    s.region,
    d.product_id,
    d.turnover_gbp,
    d.gross_revenue_gbp
FROM fct_daily d
LEFT JOIN dim_sites s ON d.site_id = s.site_id
WHERE d.date >= date('now', '-30 days')
ORDER BY d.turnover_gbp DESC
LIMIT 100;
```
**Why:** JOIN is the core operation in real SQL work. Learn to map IDs to names.
**Insight:** Which regions drive revenue? Is it concentrated (one site) or distributed?

---

### 2.2 Competitor Comparison
**Question:** On a given day, how do our margins compare to the best competitor in each market?
```sql
SELECT
    p.date,
    p.site_id,
    p.product_id,
    p.our_margin_pp,
    p.comp_best_margin_pp,
    (p.our_margin_pp - p.comp_best_margin_pp) as margin_diff_pp,
    s.market
FROM fct_price_board p
LEFT JOIN dim_sites s ON p.site_id = s.site_id
WHERE p.date = '2024-06-15'
ORDER BY margin_diff_pp DESC;
```
**Why:** Real business questions require layering multiple facts and dimensions.
**Insight:** Are we typically cheaper or more expensive? Does it vary by market?

---

### 2.3 Customer Attributes in Quotes
**Question:** Show quotes with customer tenure and segment info.
```sql
SELECT
    q.quote_id,
    q.date,
    q.segment,
    c.tenure_years,
    c.digital_engaged,
    q.order_value_gbp,
    q.converted
FROM fct_quotes q
LEFT JOIN dim_customers c ON q.customer_id = c.customer_id
WHERE q.date = '2024-01-15'
LIMIT 20;
```
**Why:** Learn to enrich fine-grain facts with dimension attributes.
**Insight:** Do digitally-engaged customers convert more? Do long-tenure customers order larger amounts?

---

## Part 3: Aggregation & Metrics (GROUP BY)

### 3.1 Conversion by Site
**Question:** What is the daily conversion rate by site, averaged over the last 30 days?
```sql
SELECT
    site_id,
    ROUND(100.0 * SUM(orders) / NULLIF(SUM(quotes), 0), 2) as conversion_rate_pct,
    SUM(turnover_gbp) as total_turnover,
    ROUND(AVG(avg_order_value_gbp), 2) as avg_order_value
FROM fct_daily
WHERE date >= date('now', '-30 days')
GROUP BY site_id
ORDER BY conversion_rate_pct DESC;
```
**Why:** GROUP BY is how you roll up data to actionable metrics.
**Insight:** Do conversion rates vary by location? Which site converts best?

---

### 3.2 Revenue by Channel
**Question:** Compare revenue, margin, and profitability across branch vs online channels.
```sql
SELECT
    s.channel,
    COUNT(DISTINCT d.date) as days,
    SUM(d.turnover_gbp) as total_turnover,
    SUM(d.gross_revenue_gbp) as total_revenue,
    SUM(d.variable_cost_gbp) as total_cost,
    SUM(d.contribution_gbp) as total_contribution,
    ROUND(100.0 * SUM(d.contribution_gbp) / NULLIF(SUM(d.gross_revenue_gbp), 0), 1) as contribution_margin_pct
FROM fct_daily d
LEFT JOIN dim_sites s ON d.site_id = s.site_id
WHERE d.date >= date('now', '-90 days')
GROUP BY s.channel
ORDER BY total_contribution DESC;
```
**Why:** Business decisions happen at aggregated levels (channel, region, product).
**Insight:** Which channel is more profitable? Is it volume or margin?

---

### 3.3 Segment Behavior
**Question:** How do customer segments differ in order size, conversion, and spend by product?
```sql
SELECT
    q.segment,
    q.product_id,
    COUNT(DISTINCT q.quote_id) as quotes,
    SUM(CASE WHEN q.converted = 1 THEN 1 ELSE 0 END) as orders,
    ROUND(100.0 * SUM(CASE WHEN q.converted = 1 THEN 1 ELSE 0 END) / COUNT(DISTINCT q.quote_id), 1) as conversion_rate_pct,
    ROUND(AVG(q.order_value_gbp), 2) as avg_order_value,
    ROUND(AVG(CASE WHEN q.converted = 1 THEN q.order_value_gbp END), 2) as avg_order_value_converted
FROM fct_quotes q
WHERE q.date >= date('now', '-60 days')
GROUP BY q.segment, q.product_id
ORDER BY segment, conversion_rate_pct DESC;
```
**Why:** Segments respond to price differently; this is pricing strategy 101.
**Insight:** Which segment is most price-sensitive? Which has the largest orders?

---

## Part 4: Filtering, Windowing & Trend Analysis

### 4.1 Daily Trend Analysis
**Question:** What was the week-over-week change in conversion rate and average order value?
```sql
SELECT
    d.date,
    strftime('%W', d.date) as week,
    ROUND(100.0 * SUM(d.orders) / NULLIF(SUM(d.quotes), 0), 2) as conversion_rate_pct,
    ROUND(AVG(d.avg_order_value_gbp), 2) as avg_order_value,
    LAG(ROUND(100.0 * SUM(d.orders) / NULLIF(SUM(d.quotes), 0), 2)) OVER (ORDER BY strftime('%W', d.date))
        as prev_week_conversion_pct
FROM fct_daily d
WHERE d.date >= date('now', '-90 days')
GROUP BY strftime('%W', d.date)
ORDER BY week DESC;
```
**Why:** Window functions (LAG, ROW_NUMBER) let you compare rows to each other, not just aggregate.
**Insight:** Are conversion and order value getting better or worse? What's the momentum?

---

### 4.2 Promotion Impact
**Question:** What is the lift from the promotion? Compare promo days to non-promo days.
```sql
SELECT
    promo_flag,
    COUNT(DISTINCT date) as days,
    ROUND(100.0 * SUM(orders) / NULLIF(SUM(quotes), 0), 2) as conversion_rate_pct,
    ROUND(AVG(avg_order_value_gbp), 2) as avg_order_value,
    SUM(contribution_gbp) as total_contribution
FROM fct_daily
WHERE site_id IN ('S01', 'S02', 'S03') AND product_id = 'EUR_CASH'
GROUP BY promo_flag
ORDER BY promo_flag DESC;
```
**Why:** A/B comparisons are how you measure impact. Segment by treatment vs control.
**Insight:** Did the promotion increase orders? Decrease margins? Net contribution up or down?

---

### 4.3 Margin Elasticity Observation
**Question:** Do higher margins correlate with lower conversion rates?
```sql
SELECT
    ROUND(our_margin_pp, 1) as margin_bucket,
    COUNT(DISTINCT quote_id) as quotes,
    ROUND(100.0 * SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) / COUNT(DISTINCT quote_id), 2) as conversion_rate_pct,
    ROUND(AVG(CASE WHEN converted = 1 THEN order_value_gbp END), 2) as avg_converted_order_value
FROM fct_quotes
WHERE date >= date('now', '-60 days')
GROUP BY ROUND(our_margin_pp, 1)
ORDER BY margin_bucket;
```
**Why:** This is your first step toward elasticity estimation ([lab 1.2](../01_set_the_rate/lab_02_demand_and_elasticity.ipynb)).
**Insight:** Is there a price-demand trade-off in your data? How strong?

---

## Part 5: Complex Joins & Quote-to-Transaction Flow

### 5.1 Quote Completion Rate
**Question:** What % of quotes turn into transactions? Trace through the funnel.
```sql
SELECT
    q.date,
    COUNT(DISTINCT q.quote_id) as total_quotes,
    COUNT(DISTINCT CASE WHEN q.converted = 1 THEN q.quote_id END) as converted_quotes,
    COUNT(DISTINCT t.txn_id) as completed_transactions,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN q.converted = 1 THEN q.quote_id END) / COUNT(DISTINCT q.quote_id), 2) as quote_conversion_pct,
    ROUND(100.0 * COUNT(DISTINCT t.txn_id) / NULLIF(COUNT(DISTINCT CASE WHEN q.converted = 1 THEN q.quote_id END), 0), 2) as transaction_completion_pct
FROM fct_quotes q
LEFT JOIN fct_transactions t ON q.quote_id = t.txn_id
WHERE q.date >= date('now', '-30 days')
GROUP BY q.date
ORDER BY q.date DESC;
```
**Why:** Real business has multiple stages. Not all conversions = revenue.
**Insight:** How many quotes don't convert? How many converted quotes don't complete? Where's the leak?

---

### 5.2 Stockout Impact
**Question:** When we run out of stock, how many sales do we lose?
```sql
SELECT
    s.date,
    s.site_id,
    s.stockout_flag,
    COUNT(*) as days_in_period,
    s.stock_limit_gbp,
    s.value_sold_gbp,
    ROUND(100.0 * s.value_sold_gbp / NULLIF(s.stock_limit_gbp, 0), 1) as utilization_pct,
    (SELECT SUM(contribution_gbp) FROM fct_stock s2
     WHERE s2.site_id = s.site_id AND s2.date >= date('now', '-30 days') AND s2.stockout_flag = s.stockout_flag) as contribution_by_stockout
FROM fct_stock s
WHERE s.date >= date('now', '-30 days')
GROUP BY s.site_id, s.stockout_flag
ORDER BY s.date DESC, s.site_id;
```
**Why:** Operational constraints matter. Subqueries let you nest aggregations.
**Insight:** How often do we stockout? What's the revenue impact? Is increasing stock limit worth it?

---

## Part 6: Window Functions & Time-Series Analysis

### 6.1 Rolling Averages
**Question:** Show 7-day and 30-day rolling average of conversion rate.
```sql
SELECT
    date,
    ROUND(100.0 * orders / NULLIF(quotes, 0), 2) as daily_conversion_pct,
    ROUND(100.0 * AVG(orders) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) /
          NULLIF(AVG(quotes) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 0), 2) as ma7_conversion_pct,
    ROUND(100.0 * AVG(orders) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) /
          NULLIF(AVG(quotes) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW), 0), 2) as ma30_conversion_pct
FROM fct_daily
WHERE site_id = 'S01' AND product_id = 'EUR_CASH'
ORDER BY date DESC;
```
**Why:** Smoothing removes noise and reveals trends.
**Insight:** Is the trend up or down? Has velocity changed recently?

---

### 6.2 Rank Sites by Performance
**Question:** Rank sites by contribution, and show their percentile.
```sql
SELECT
    site_id,
    SUM(contribution_gbp) as total_contribution,
    RANK() OVER (ORDER BY SUM(contribution_gbp) DESC) as rank,
    ROUND(100.0 * PERCENT_RANK() OVER (ORDER BY SUM(contribution_gbp) DESC), 1) as percentile,
    ROUND(100.0 * SUM(contribution_gbp) / SUM(SUM(contribution_gbp)) OVER (), 1) as pct_of_total
FROM fct_daily
WHERE date >= date('now', '-90 days')
GROUP BY site_id
ORDER BY total_contribution DESC;
```
**Why:** Window functions let you rank and calculate shares without subqueries.
**Insight:** Is profit concentrated in 1-2 sites or spread? Pareto principle at work?

---

## Part 7: Advanced: Hypothesis Testing & Causal Thinking

### 7.1 A/B Test Analysis
**Question:** Did the experiment (ONLINE-RATE-2025Q1) increase conversion or revenue?
```sql
SELECT
    arm,
    COUNT(DISTINCT quote_id) as quotes,
    SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) as conversions,
    ROUND(100.0 * SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) / COUNT(DISTINCT quote_id), 2) as conversion_rate_pct,
    ROUND(AVG(CASE WHEN converted = 1 THEN order_value_gbp END), 2) as avg_order_value,
    SUM(CASE WHEN arm != '' THEN 1 ELSE 0 END) as orders_in_arm,
    (SELECT SUM(contribution_gbp) FROM fct_transactions t
     WHERE t.arm = q.arm AND t.arm != '') as contribution
FROM fct_quotes q
WHERE arm != ''
GROUP BY arm
ORDER BY conversion_rate_pct DESC;
```
**Why:** Experiments are how you de-risk decisions. Learn to read results carefully.
**Insight:** Which arm won? By how much? Is it statistically significant? (Needs a power calculation, see [lab 2.4](../02_prove_the_change/lab_04_experiments_and_ab_testing.ipynb).)

---

### 7.2 Price Sensitivity by Segment
**Question:** Which segment is most price-elastic?
```sql
SELECT
    segment,
    ROUND(our_margin_pp, 1) as margin_pp,
    COUNT(DISTINCT quote_id) as quotes,
    SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) as conversions,
    ROUND(100.0 * SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) / COUNT(DISTINCT quote_id), 2) as conversion_rate_pct
FROM fct_quotes
WHERE date >= date('now', '-90 days')
GROUP BY segment, ROUND(our_margin_pp, 1)
ORDER BY segment, margin_pp;
```
**Why:** Different customers respond differently to price. Segment analysis is pricing strategy.
**Insight:** Which segment's conversion drops most as you raise margin? That's your elastic segment.

---

### 7.3 Contribution per Dollar of Cost
**Question:** Which site has the best operating efficiency?
```sql
SELECT
    d.site_id,
    s.site_name,
    SUM(d.gross_revenue_gbp) as total_revenue,
    SUM(d.variable_cost_gbp) as variable_cost,
    SUM(d.contribution_gbp) as contribution,
    ROUND(100.0 * SUM(d.contribution_gbp) / NULLIF(SUM(d.gross_revenue_gbp), 0), 1) as contribution_margin_pct,
    s.fixed_cost_month_gbp * 12 as annual_fixed_cost,
    SUM(d.contribution_gbp) - (s.fixed_cost_month_gbp * 12) as annual_operating_profit
FROM fct_daily d
LEFT JOIN dim_sites s ON d.site_id = s.site_id
WHERE d.date >= '2024-01-01'
GROUP BY d.site_id, s.site_name, s.fixed_cost_month_gbp
ORDER BY annual_operating_profit DESC;
```
**Why:** P&L thinking. Not all revenue is profit. Fixed costs matter.
**Insight:** Which site is truly most profitable after covering overheads? Should you close any?

---

## Part 8: Deep Dives (Bring It Together)

### 8.1 Full Customer Journey
**Question:** For customers who bought once, how often do they come back?
```sql
SELECT
    t1.customer_id,
    COUNT(DISTINCT t1.date) as purchase_days,
    COUNT(DISTINCT t1.txn_id) as total_orders,
    SUM(t1.contribution_gbp) as lifetime_contribution,
    ROUND(AVG(t1.order_value_gbp), 2) as avg_order_value,
    MAX(t1.date) as last_purchase_date,
    JULIANDAY('now') - JULIANDAY(MAX(t1.date)) as days_since_last_purchase
FROM fct_transactions t1
GROUP BY t1.customer_id
HAVING COUNT(DISTINCT t1.txn_id) >= 1
ORDER BY lifetime_contribution DESC
LIMIT 50;
```
**Why:** Customer lifetime value (CLV) is the most important metric for retention.
**Insight:** Are you building loyalty? Repeat customers or one-time buyers?

---

### 8.2 Seasonality Effect
**Question:** How much of the variance in orders is explained by season vs other factors?
```sql
SELECT
    ROUND(season_z, 1) as season_percentile,
    COUNT(DISTINCT d.date) as days,
    SUM(d.quotes) as total_quotes,
    SUM(d.orders) as total_orders,
    ROUND(100.0 * SUM(d.orders) / NULLIF(SUM(d.quotes), 0), 2) as conversion_pct,
    ROUND(AVG(d.avg_order_value_gbp), 2) as avg_order_value
FROM fct_daily d
GROUP BY ROUND(season_z, 1)
ORDER BY season_percentile;
```
**Why:** External factors (season, holidays) move your business. Isolate them before testing.
**Insight:** How much bigger is demand at peak season vs trough? What's the elasticity of seasonality?

---

### 8.3 Competitive Positioning
**Question:** How often are we cheaper than competitors by product and market?
```sql
SELECT
    p.product_id,
    s.market,
    COUNT(*) as day_site_product_combos,
    SUM(CASE WHEN p.our_margin_pp < p.comp_best_margin_pp THEN 1 ELSE 0 END) as days_we_cheaper,
    ROUND(100.0 * SUM(CASE WHEN p.our_margin_pp < p.comp_best_margin_pp THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_days_cheaper,
    ROUND(AVG(p.our_margin_pp - p.comp_best_margin_pp), 2) as avg_margin_diff_pp
FROM fct_price_board p
LEFT JOIN dim_sites s ON p.site_id = s.site_id
WHERE p.date >= date('now', '-180 days')
GROUP BY p.product_id, s.market
ORDER BY pct_days_cheaper DESC;
```
**Why:** Competitive strategy. You need to know your position.
**Insight:** Are you a price leader or follower? Does it vary by market/product?

---

## Part 9: Synthesis (Build Your Own Questions)

By now you've learned:
- ✅ Basic queries (SELECT, WHERE, ORDER BY)
- ✅ JOINs (enriching facts with dimensions)
- ✅ GROUP BY & aggregation (rolling up to metrics)
- ✅ Window functions (trends, ranks, comparisons)
- ✅ Subqueries (nested logic)
- ✅ Time-series analysis (rolling averages, trend detection)
- ✅ A/B testing (experimental design)

**Your turn:** Ask yourself these questions and write the SQL:

1. **What was our best day ever?** (revenue, contribution, conversion)
2. **Is customer tenure related to order size?**
3. **Did the promotion work better in some sites than others?**
4. **What if we raised margins by 0.5pp? How many sales would we lose?** (Use your elasticity estimates from Q7.2)
5. **Which customer segment is the most valuable?** (CLV approach from 8.1)
6. **How much revenue do stockouts cost us annually?**
7. **Is there a weekend effect?** (Weekday vs weekend behavior)
8. **How do our costs scale with volume?** (Variable vs fixed cost analysis)

---

## Answers & Insights Repository

As you work through these questions:
- Save your SQL queries in a notebook cell or text file.
- Document insights ("found that X correlates with Y").
- Compare your hypotheses to the `truth.json` answer key in later notebooks.
- Revisit elastic segments: your Q7.2 findings will drive pricing strategy in [lab 1.3](../01_set_the_rate/lab_03_price_optimisation.ipynb).

---

## Next Steps

1. **Notebook 07** uses this data to build a pricing model.
2. **Notebook 08** estimates elasticity (your Q7.2 findings matter here).
3. **Notebook 09** runs A/B tests and power calculations.
4. **Notebook 10** optimizes margins using your elasticity estimates.

The questions above are preparation. By the time you reach the causal inference lab ([2.5](../02_prove_the_change/lab_05_causal_inference.ipynb)), you'll know your data intimately.
