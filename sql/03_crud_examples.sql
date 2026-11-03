USE retail_sales_db;

-- SELECT: read a small customer sample.
SELECT customer_id, customer_name, email, city FROM customers ORDER BY customer_id LIMIT 10;

-- INSERT: this special demo row is safe to rerun.
INSERT INTO customers (customer_name, email, city)
VALUES ('SQL Demo Customer', 'sql.demo@example.com', 'Colombo')
ON DUPLICATE KEY UPDATE email = VALUES(email);

-- UPDATE only the clearly labelled demo customer.
UPDATE customers SET customer_name = 'Updated SQL Demo Customer', city = 'Kandy'
WHERE email = 'sql.demo@example.com';

-- DELETE only when no order refers to the demo customer.
DELETE FROM customers WHERE email = 'sql.demo@example.com'
AND NOT EXISTS (SELECT 1 FROM orders WHERE orders.customer_id = customers.customer_id);
