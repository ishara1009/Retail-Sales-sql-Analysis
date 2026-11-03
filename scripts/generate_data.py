"""Create a reproducible replacement practice dataset.

This is not the original dataset generator. Existing CSV files are protected
unless --overwrite is supplied explicitly.
"""

import argparse
import csv
import random
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RANDOM = random.Random(2025)
CATEGORIES = ["Computers", "Mobile Accessories", "Audio", "Office", "Storage"]


def write_csv(name, headers, rows, overwrite):
    path = DATA / name
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists. Use --overwrite only if replacement is intentional.")
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file); writer.writerow(headers); writer.writerows(rows)


def generate(overwrite=False):
    DATA.mkdir(exist_ok=True)
    customers = [(i, f"Practice Customer {i:03}", f"practice{i:03}@example.com", ["Colombo", "Kandy", "Galle", "Jaffna", "Negombo"][(i-1) % 5]) for i in range(1, 101)]
    categories = list(enumerate(CATEGORIES, 1))
    products = [(i, f"Practice Product {i:02}", ((i-1) % 5)+1, Decimal(1000 + i * 725)) for i in range(1, 31)]
    start = date(2025, 1, 1)
    statuses = ["completed", "completed", "pending", "cancelled"]
    orders = []
    items = []
    item_id = 1
    for order_id in range(1, 501):
        order_date = start + timedelta(days=((order_id - 1) * 364) // 499)
        orders.append((order_id, ((order_id - 1) % 90) + 1, order_date.isoformat(), statuses[(order_id-1) % 4]))
        item_count = 4 if order_id <= 16 else 3  # 16*4 + 484*3 = 1,516
        product_ids = RANDOM.sample(range(1, 28), item_count)
        for product_id in product_ids:
            items.append((item_id, order_id, product_id, RANDOM.randint(1, 4), products[product_id-1][3]))
            item_id += 1
    write_csv("customers.csv", ["customer_id", "customer_name", "email", "city"], customers, overwrite)
    write_csv("categories.csv", ["category_id", "category_name"], categories, overwrite)
    write_csv("products.csv", ["product_id", "product_name", "category_id", "unit_price"], products, overwrite)
    write_csv("orders.csv", ["order_id", "customer_id", "order_date", "status"], orders, overwrite)
    write_csv("order_items.csv", ["order_item_id", "order_id", "product_id", "quantity", "unit_price"], items, overwrite)
    print("Generated a reproducible replacement practice dataset in data/.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", action="store_true", help="replace existing CSV files")
    generate(parser.parse_args().overwrite)
