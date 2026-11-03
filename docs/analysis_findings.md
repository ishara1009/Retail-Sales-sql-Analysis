# Analysis Findings

## Measured findings

These values were measured from the supplied CSV data after a successful import into MySQL on 2026-11-03.

1. Total completed-sales revenue: **LKR 88,297,905.00**
2. Completed order count: **397**
3. Average completed-order value: **LKR 222,412.86**
4. Strongest sales month: **September 2025 — LKR 8,793,600.00**
5. Highest-revenue product: **Laptop Pro (ID 2) — LKR 29,351,000.00**
6. Highest-quantity product: **Bluetooth Speaker (ID 15) — 145 units**
7. Highest-spending customer: **Demo Customer 049 (ID 49) — LKR 3,525,750.00**
8. Highest-revenue category: **Computers (ID 1) — LKR 68,555,325.00**

All queries are in [`../sql/08_sales_analysis.sql`](../sql/08_sales_analysis.sql). Revenue includes completed orders only and uses each order item's historical sale price. Monthly output includes only months having completed sales. Taxes, shipping, costs, refunds and profit are outside this data model.
