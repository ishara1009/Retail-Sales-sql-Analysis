USE retail_sales_db;

-- SUM: completed-sales revenue using historical item prices.
SELECT SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM order_items oi JOIN orders o ON o.order_id = oi.order_id WHERE o.status = 'completed';
-- COUNT: number of completed orders.
SELECT COUNT(*) AS completed_order_count FROM orders WHERE status = 'completed';
-- AVG: average current catalog price.
SELECT AVG(unit_price) AS average_product_price FROM products;
-- MIN and MAX: catalog price range.
SELECT MIN(unit_price) AS lowest_price, MAX(unit_price) AS highest_price FROM products;
-- COUNT DISTINCT: customers who placed an order.
SELECT COUNT(DISTINCT customer_id) AS ordering_customers FROM orders;
