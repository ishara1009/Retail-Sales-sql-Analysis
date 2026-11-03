"""Validate the five CSV files and import them in one transaction."""

import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from mysql.connector import Error

from src.database import get_connection

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SCHEMAS = {
    "categories": ("category_id", "category_name"),
    "customers": ("customer_id", "customer_name", "email", "city"),
    "products": ("product_id", "product_name", "category_id", "unit_price"),
    "orders": ("order_id", "customer_id", "order_date", "status"),
    "order_items": ("order_item_id", "order_id", "product_id", "quantity", "unit_price"),
}
STATUSES = {"completed", "pending", "cancelled"}


def read_csv(table):
    path = DATA_DIR / f"{table}.csv"
    if not path.is_file():
        raise ValueError(f"Missing CSV file: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if tuple(reader.fieldnames or ()) != SCHEMAS[table]:
            raise ValueError(f"{path.name}: expected headers {SCHEMAS[table]}, found {reader.fieldnames}")
        return list(reader)


def positive_int(value, label):
    try:
        number = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must be an integer: {value!r}") from error
    if number <= 0:
        raise ValueError(f"{label} must be positive: {number}")
    return number


def positive_money(value, label):
    try:
        number = Decimal(value)
    except (InvalidOperation, TypeError) as error:
        raise ValueError(f"{label} must be a valid price: {value!r}") from error
    if number <= 0 or number.as_tuple().exponent < -2:
        raise ValueError(f"{label} must be positive with at most 2 decimals: {value!r}")
    return number


def required(value, label):
    text = value.strip()
    if not text:
        raise ValueError(f"{label} is required.")
    return text


def validate_data(raw):
    """Convert values and validate keys and relationships before connecting."""
    data = {name: [] for name in SCHEMAS}
    ids = {name: set() for name in SCHEMAS}
    for table in SCHEMAS:
        key = SCHEMAS[table][0]
        for line, row in enumerate(raw[table], 2):
            row_id = positive_int(row[key], f"{table}.csv line {line} {key}")
            if row_id in ids[table]:
                raise ValueError(f"{table}.csv line {line}: duplicate {key} {row_id}")
            ids[table].add(row_id)
            row[key] = row_id
            data[table].append(row)

    emails = set()
    for row in data["customers"]:
        row["customer_name"] = required(row["customer_name"], "customer name")
        row["email"] = required(row["email"], "email").lower()
        row["city"] = required(row["city"], "city")
        if "@" not in row["email"] or row["email"] in emails:
            raise ValueError(f"Invalid or duplicate customer email: {row['email']}")
        emails.add(row["email"])
    category_ids = ids["categories"]
    for row in data["categories"]:
        row["category_name"] = required(row["category_name"], "category name")
    for row in data["products"]:
        row["product_name"] = required(row["product_name"], "product name")
        row["category_id"] = positive_int(row["category_id"], "product category_id")
        row["unit_price"] = positive_money(row["unit_price"], "product unit_price")
        if row["category_id"] not in category_ids:
            raise ValueError(f"Product {row['product_id']} has unknown category {row['category_id']}")
    customer_ids = ids["customers"]
    for row in data["orders"]:
        row["customer_id"] = positive_int(row["customer_id"], "order customer_id")
        try:
            row["order_date"] = date.fromisoformat(row["order_date"])
        except ValueError as error:
            raise ValueError(f"Order {row['order_id']} has invalid date {row['order_date']!r}") from error
        row["status"] = row["status"].strip().lower()
        if row["customer_id"] not in customer_ids or row["status"] not in STATUSES:
            raise ValueError(f"Order {row['order_id']} has invalid customer or status")
    order_ids, product_ids, pairs = ids["orders"], ids["products"], set()
    for row in data["order_items"]:
        row["order_id"] = positive_int(row["order_id"], "item order_id")
        row["product_id"] = positive_int(row["product_id"], "item product_id")
        row["quantity"] = positive_int(row["quantity"], "item quantity")
        row["unit_price"] = positive_money(row["unit_price"], "item unit_price")
        pair = (row["order_id"], row["product_id"])
        if row["order_id"] not in order_ids or row["product_id"] not in product_ids:
            raise ValueError(f"Order item {row['order_item_id']} has an unknown order or product")
        if pair in pairs:
            raise ValueError(f"Duplicate product {row['product_id']} in order {row['order_id']}")
        pairs.add(pair)
    return data


def import_all():
    raw = {table: read_csv(table) for table in SCHEMAS}
    data = validate_data(raw)
    connection = get_connection()
    cursor = connection.cursor()
    try:
        for table in SCHEMAS:
            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
            if cursor.fetchone()[0] != 0:
                raise ValueError(f"Import stopped: table '{table}' is not empty. No data was changed.")
        # The transaction commits only when every insert succeeds.
        connection.commit()
        connection.start_transaction()
        statements = {
            "categories": "INSERT INTO categories (category_id, category_name) VALUES (%s, %s)",
            "customers": "INSERT INTO customers (customer_id, customer_name, email, city) VALUES (%s, %s, %s, %s)",
            "products": "INSERT INTO products (product_id, product_name, category_id, unit_price) VALUES (%s, %s, %s, %s)",
            "orders": "INSERT INTO orders (order_id, customer_id, order_date, status) VALUES (%s, %s, %s, %s)",
            "order_items": "INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s, %s)",
        }
        for table, columns in SCHEMAS.items():
            values = [tuple(row[column] for column in columns) for row in data[table]]
            cursor.executemany(statements[table], values)
        connection.commit()  # Commit makes all validated rows permanent.
    except Exception:
        connection.rollback()  # Rollback prevents a partial import from remaining.
        raise
    finally:
        cursor.close()
        connection.close()
    for table in SCHEMAS:
        print(f"Inserted {len(data[table]):,} rows into {table}.")


if __name__ == "__main__":
    try:
        import_all()
    except (ValueError, ConnectionError, Error) as error:
        print(f"Import failed: {error}")
