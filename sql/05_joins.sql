USE retail_sales_db;

-- INNER JOIN: products paired with category names.
SELECT p.product_id, p.product_name, c.category_name
FROM products p INNER JOIN categories c ON c.category_id = p.category_id;
-- LEFT JOIN: every customer, including customers without orders.
SELECT c.customer_id, c.customer_name, o.order_id
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id;
-- RIGHT JOIN: preserve every customer from the right table.
SELECT o.order_id, c.customer_id, c.customer_name
FROM orders o RIGHT JOIN customers c ON c.customer_id = o.customer_id;
-- Customers with no orders.
SELECT c.customer_id, c.customer_name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL ORDER BY c.customer_id;
-- Products never ordered.
SELECT p.product_id, p.product_name FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.product_id
WHERE oi.order_item_id IS NULL ORDER BY p.product_id;
-- Multi-table order details. JOIN එකෙන් related tables එක result එකකට සම්බන්ධ කරයි.
SELECT o.order_id, o.order_date, c.customer_name, p.product_name,
       oi.quantity, oi.unit_price, oi.quantity * oi.unit_price AS line_total
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
ORDER BY o.order_id, oi.order_item_id;
