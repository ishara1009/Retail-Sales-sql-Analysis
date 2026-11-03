USE retail_sales_db;

-- WHERE and AND
SELECT * FROM products WHERE category_id = 1 AND unit_price > 100000;
-- OR and IN
SELECT * FROM orders WHERE status = 'pending' OR status = 'cancelled';
SELECT * FROM orders WHERE status IN ('pending', 'cancelled');
-- BETWEEN
SELECT * FROM orders WHERE order_date BETWEEN '2025-01-01' AND '2025-03-31';
-- LIKE
SELECT * FROM customers WHERE customer_name LIKE 'Demo%';
-- IS NULL
SELECT c.customer_id, c.customer_name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id WHERE o.order_id IS NULL;
-- ORDER BY and LIMIT
SELECT * FROM products ORDER BY unit_price DESC, product_id ASC LIMIT 5;
-- GROUP BY and HAVING
SELECT customer_id, COUNT(*) AS order_count FROM orders
GROUP BY customer_id HAVING COUNT(*) > 5 ORDER BY order_count DESC, customer_id;
