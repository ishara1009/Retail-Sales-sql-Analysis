"""Export four fixed sales reports to CSV."""

import re
from pathlib import Path

import pandas as pd
from mysql.connector import Error

from src.database import get_connection

ROOT = Path(__file__).resolve().parents[1]
SQL_FILE = ROOT / "sql" / "08_sales_analysis.sql"
REPORT_DIR = ROOT / "reports"
REPORTS = {
    "MONTHLY_SALES": "monthly_sales.csv",
    "TOP_PRODUCTS": "top_products.csv",
    "TOP_CUSTOMERS": "top_customers.csv",
    "CATEGORY_REVENUE": "category_revenue.csv",
}


def load_report_query(name):
    text = SQL_FILE.read_text(encoding="utf-8")
    pattern = rf"-- REPORT: {re.escape(name)}\s+(.*?)\s+-- END REPORT"
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Report query section {name} is missing from {SQL_FILE.name}.")
    return match.group(1).strip().rstrip(";")


def export_reports():
    REPORT_DIR.mkdir(exist_ok=True)
    connection = get_connection(); cursor = connection.cursor()
    written = []
    try:
        for section, filename in REPORTS.items():
            cursor.execute(load_report_query(section))
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            # Decimal values float බවට හරවන්නේ නැතිව CSV එකට ලියයි.
            frame = pd.DataFrame(rows, columns=columns)
            path = REPORT_DIR / filename
            frame.to_csv(path, index=False)
            written.append(path)
    finally:
        cursor.close(); connection.close()
    return written


if __name__ == "__main__":
    try:
        for path in export_reports():
            print(f"Exported {path}")
    except (ValueError, ConnectionError, Error) as error:
        print(f"Report export failed: {error}")
