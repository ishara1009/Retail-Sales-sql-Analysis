# Retail Sales Database Analysis using MySQL and Python

A beginner-friendly portfolio project for learning relational database design, SQL analysis, safe Python CRUD operations, transactions and CSV reporting. It uses a synthetic retail dataset; it is educational and is not a production accounting system.

## Technologies

- MySQL 8 and MySQL Workbench
- Python 3, `mysql-connector-python`, `python-dotenv`
- Pandas only for report CSV export
- Python's `csv` module and `Decimal` for validated imports

## Project structure

```text
data/      supplied synthetic CSV files
sql/       schema, learning examples and 15 analyses
src/       database, import, CRUD, orders and reports
reports/   generated report CSV files
docs/      ER diagram, data dictionary and findings
scripts/   optional replacement-data generator
main.py    menu application
```

The supplied files contain 100 customers, 5 categories, 30 products, 500 orders and 1,516 order items. Orders cover January–December 2025. Customers 91–100 have no orders, and products 28–30 have never been ordered.

## Setup on Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` with the local MySQL username and password. Never commit it.

## Setup on macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

## Create the database

In MySQL Workbench, open and run these scripts in order:

1. `sql/01_create_database.sql`
2. `sql/02_create_tables.sql`

The MySQL account needs permission to create/use `retail_sales_db` and to select, insert, update and delete rows in its tables. Normal application startup never creates, resets or truncates tables.

Then import and run the application:

```text
python -m src.import_data
python main.py
python -m src.reports
```

The import is intentionally refused if any target table already has rows. All five CSV files are validated before insertion, and all inserts commit together or roll back together.

## Example CLI session

The following is an example, not captured live output:

```text
Choose an option: 5
  1 | Laptop Basic | Computers | LKR 145,000.00
Choose an option: 7
Customer ID: 1
Product ID: 1
Quantity: 2
Product ID:
Order 501 created as pending.
```

## Business rules

- Revenue includes `completed` orders only.
- Revenue is `quantity × order_items.unit_price`; the current product price is not used for history.
- Average order value first totals each completed order, then averages those totals.
- Monthly results group by year and month and show months with completed sales only.
- New orders start as `pending`; allowed statuses are `completed`, `pending`, and `cancelled`.
- An order cannot repeat a product, and prices and quantities must be positive.
- Taxes, shipping, costs, refunds and profit are not modeled.

## Learning map

| Topic | File |
|---|---|
| Database and table design, keys, constraints | `sql/01_create_database.sql`, `sql/02_create_tables.sql` |
| CRUD | `sql/03_crud_examples.sql`, `src/customers.py` |
| Filtering, sorting, grouping | `sql/04_filtering_and_sorting.sql` |
| INNER/LEFT/RIGHT and multi-table JOINs | `sql/05_joins.sql` |
| SUM, COUNT, AVG, MIN, MAX | `sql/06_aggregate_functions.sql` |
| EXISTS, NOT EXISTS and nested queries | `sql/07_subqueries.sql` |
| Fifteen business analyses | `sql/08_sales_analysis.sql` |
| Transactions and historical prices | `src/import_data.py`, `src/orders.py` |
| CSV report export | `src/reports.py` |

## Troubleshooting

- **Missing database settings:** copy `.env.example` to `.env` and replace every placeholder.
- **Access denied:** verify the MySQL username/password and database permissions.
- **Cannot connect:** start MySQL and confirm host `localhost` and port `3306`.
- **Unknown database/table:** run schema scripts 01 and 02 in Workbench first.
- **Import refused because a table is not empty:** this protects existing data. Use the existing database or create a fresh disposable database; do not delete records casually.
- **CSV header/relationship error:** restore the supplied CSV structure and IDs. Do not edit records merely to bypass validation.
- **Module not found:** activate `.venv` and run `python -m pip install -r requirements.txt`.

`scripts/generate_data.py` is a reproducible replacement generator, not the original generator. It protects supplied files unless `--overwrite` is explicitly given. The project implements **MySQL**, not PostgreSQL.
