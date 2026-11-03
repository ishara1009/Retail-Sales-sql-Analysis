# Data Dictionary

| Table | Column | MySQL type | Key/rule | Meaning |
|---|---|---|---|---|
| customers | customer_id | INT | PK, AUTO_INCREMENT | Customer identifier |
| customers | customer_name | VARCHAR(100) | NOT NULL | Customer display name |
| customers | email | VARCHAR(255) | NOT NULL, UNIQUE | Contact email |
| customers | city | VARCHAR(100) | NOT NULL | Customer city |
| categories | category_id | INT | PK, AUTO_INCREMENT | Category identifier |
| categories | category_name | VARCHAR(100) | NOT NULL, UNIQUE | Category name |
| products | product_id | INT | PK, AUTO_INCREMENT | Product identifier |
| products | product_name | VARCHAR(150) | NOT NULL | Product name |
| products | category_id | INT | FK, NOT NULL | Parent category |
| products | unit_price | DECIMAL(12,2) | Positive, NOT NULL | Current catalog price in LKR |
| orders | order_id | INT | PK, AUTO_INCREMENT | Order identifier |
| orders | customer_id | INT | FK, NOT NULL | Customer who placed the order |
| orders | order_date | DATE | NOT NULL | Order date |
| orders | status | ENUM | NOT NULL | `completed`, `pending`, or `cancelled` |
| order_items | order_item_id | INT | PK, AUTO_INCREMENT | Line identifier |
| order_items | order_id | INT | FK, NOT NULL | Parent order |
| order_items | product_id | INT | FK, NOT NULL | Ordered product |
| order_items | quantity | INT | Positive, NOT NULL | Units ordered |
| order_items | unit_price | DECIMAL(12,2) | Positive, NOT NULL | Historical sale price in LKR |

`products.unit_price` may change with the catalog. `order_items.unit_price` is the copied price at sale time and is used for historical revenue. The unique `(order_id, product_id)` rule prevents repeated product lines in one order.
