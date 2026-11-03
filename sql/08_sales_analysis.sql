USE retail_sales_db;

-- 1. What is total revenue from completed orders?
SELECT COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_revenue
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id WHERE o.status = 'completed';

-- 2. How many orders are completed?
SELECT COUNT(*) AS completed_order_count FROM orders WHERE status = 'completed';

-- 3. What is the average completed-order value?
SELECT AVG(t.order_total) AS average_order_value
FROM (SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS order_total
      FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
      WHERE o.status = 'completed' GROUP BY o.order_id) t;

-- 4. What is completed-sales revenue by month?
-- REPORT: MONTHLY_SALES
SELECT YEAR(o.order_date) AS sales_year, MONTH(o.order_date) AS sales_month,
       SUM(oi.quantity * oi.unit_price) AS revenue
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY YEAR(o.order_date), MONTH(o.order_date)
ORDER BY sales_year, sales_month;
-- END REPORT

-- 5. Which ten products earn the most completed-sales revenue?
-- REPORT: TOP_PRODUCTS
SELECT p.product_id, p.product_name,
       SUM(oi.quantity) AS quantity_sold,
       SUM(oi.quantity * oi.unit_price) AS revenue
FROM products p JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id WHERE o.status = 'completed'
GROUP BY p.product_id, p.product_name
ORDER BY revenue DESC, p.product_id ASC LIMIT 10;
-- END REPORT

-- 6. Which ten products sold the greatest quantity in completed orders?
SELECT p.product_id, p.product_name, SUM(oi.quantity) AS quantity_sold
FROM products p JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id WHERE o.status = 'completed'
GROUP BY p.product_id, p.product_name
ORDER BY quantity_sold DESC, p.product_id ASC LIMIT 10;

-- 7. Which ten customers spent the most on completed sales?
-- REPORT: TOP_CUSTOMERS
SELECT c.customer_id, c.customer_name,
       SUM(oi.quantity * oi.unit_price) AS total_spending
FROM customers c JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id WHERE o.status = 'completed'
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spending DESC, c.customer_id ASC LIMIT 10;
-- END REPORT

-- 8. How much completed-sales revenue did each category earn?
-- REPORT: CATEGORY_REVENUE
SELECT c.category_id, c.category_name,
       COALESCE(SUM(CASE WHEN o.status = 'completed'
                        THEN oi.quantity * oi.unit_price ELSE 0 END), 0) AS revenue
FROM categories c LEFT JOIN products p ON p.category_id = c.category_id
LEFT JOIN order_items oi ON oi.product_id = p.product_id
LEFT JOIN orders o ON o.order_id = oi.order_id
GROUP BY c.category_id, c.category_name
ORDER BY revenue DESC, c.category_id ASC;
-- END REPORT

-- 9. How many orders are in each status?
SELECT status, COUNT(*) AS order_count FROM orders GROUP BY status ORDER BY status;

-- 10. Which customers have no orders?
SELECT c.customer_id, c.customer_name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL ORDER BY c.customer_id;

-- 11. Which products have never been ordered?
SELECT p.product_id, p.product_name FROM products p
WHERE NOT EXISTS (SELECT 1 FROM order_items oi WHERE oi.product_id = p.product_id)
ORDER BY p.product_id;

-- 12. Which completed orders are above the average completed-order value?
SELECT t.order_id, t.order_total
FROM (SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS order_total
      FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
      WHERE o.status = 'completed' GROUP BY o.order_id) t
WHERE t.order_total >
      (SELECT AVG(x.order_total) FROM
          (SELECT SUM(oi.quantity * oi.unit_price) AS order_total
           FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
           WHERE o.status = 'completed' GROUP BY o.order_id) x)
ORDER BY t.order_total DESC, t.order_id;

-- 13. What is completed-sales revenue by customer city?
SELECT c.city, SUM(oi.quantity * oi.unit_price) AS revenue
FROM customers c JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id WHERE o.status = 'completed'
GROUP BY c.city ORDER BY revenue DESC, c.city ASC;

-- 14. How many completed orders has each customer made, including zero?
SELECT c.customer_id, c.customer_name,
       COUNT(DISTINCT CASE WHEN o.status = 'completed' THEN o.order_id END) AS completed_orders
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY completed_orders DESC, c.customer_id;

-- 15. What are the lowest and highest completed-order totals?
SELECT MIN(t.order_total) AS lowest_order_total, MAX(t.order_total) AS highest_order_total
FROM (SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS order_total
      FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
      WHERE o.status = 'completed' GROUP BY o.order_id) t;
