"""Order creation and status updates."""

from datetime import date
from mysql.connector import Error
from src.database import get_connection

STATUSES = {"completed", "pending", "cancelled"}


def create_order(customer_id, items):
    if customer_id <= 0:
        raise ValueError("Customer ID must be positive.")
    if not items:
        raise ValueError("An order needs at least one product.")
    product_ids = []
    clean_items = []
    for product_id, quantity in items:
        if product_id <= 0 or quantity <= 0:
            raise ValueError("Product IDs and quantities must be positive integers.")
        if product_id in product_ids:
            raise ValueError(f"Product {product_id} appears more than once in this order.")
        product_ids.append(product_id); clean_items.append((product_id, quantity))

    connection = get_connection(); cursor = connection.cursor(dictionary=True)
    try:
        connection.start_transaction()
        cursor.execute("SELECT customer_id FROM customers WHERE customer_id=%s", (customer_id,))
        if not cursor.fetchone():
            raise LookupError(f"Customer {customer_id} does not exist.")
        placeholders = ", ".join(["%s"] * len(product_ids))
        cursor.execute(f"SELECT product_id, unit_price FROM products WHERE product_id IN ({placeholders})", tuple(product_ids))
        prices = {row["product_id"]: row["unit_price"] for row in cursor.fetchall()}
        missing = [product_id for product_id in product_ids if product_id not in prices]
        if missing:
            raise LookupError("Unknown product IDs: " + ", ".join(map(str, missing)))
        cursor.execute("INSERT INTO orders (customer_id, order_date, status) VALUES (%s, %s, %s)",
                       (customer_id, date.today(), "pending"))
        order_id = cursor.lastrowid
        for product_id, quantity in clean_items:
            # Historical price: copy today's catalog price into the order item.
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)",
                           (order_id, product_id, quantity, prices[product_id]))
        connection.commit(); return order_id
    except Exception:
        connection.rollback()  # Roll back the entire order if any item fails.
        raise
    finally:
        cursor.close(); connection.close()


def update_order_status(order_id, new_status):
    new_status = new_status.strip().lower()
    if new_status not in STATUSES:
        raise ValueError("Status must be completed, pending or cancelled.")
    connection = get_connection(); cursor = connection.cursor()
    try:
        cursor.execute("SELECT status FROM orders WHERE order_id=%s", (order_id,))
        row = cursor.fetchone()
        if not row:
            raise LookupError(f"Order {order_id} does not exist.")
        if row[0] == new_status:
            return False
        cursor.execute("UPDATE orders SET status=%s WHERE order_id=%s", (new_status, order_id))
        connection.commit(); return True
    except Error:
        connection.rollback(); raise
    finally:
        cursor.close(); connection.close()
