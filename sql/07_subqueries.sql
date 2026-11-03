USE retail_sales_db;

-- Completed orders above the average completed-order value.
SELECT totals.order_id, totals.order_total
FROM (SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS order_total
      FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
      WHERE o.status = 'completed' GROUP BY o.order_id) totals
WHERE totals.order_total >
      (SELECT AVG(x.order_total)
       FROM (SELECT SUM(oi.quantity * oi.unit_price) AS order_total
             FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
             WHERE o.status = 'completed' GROUP BY o.order_id) x)
ORDER BY totals.order_total DESC, totals.order_id;
-- Customers with at least one completed order.
SELECT c.customer_id, c.customer_name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'completed')
ORDER BY c.customer_id;
-- Products never ordered.
SELECT p.product_id, p.product_name FROM products p
WHERE NOT EXISTS (SELECT 1 FROM order_items oi WHERE oi.product_id = p.product_id)
ORDER BY p.product_id;
