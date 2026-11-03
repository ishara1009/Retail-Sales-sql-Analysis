# Database Diagram

```mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    CATEGORIES ||--o{ PRODUCTS : contains
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : appears_in

    CUSTOMERS { int customer_id PK string customer_name string email UK string city }
    CATEGORIES { int category_id PK string category_name UK }
    PRODUCTS { int product_id PK string product_name int category_id FK decimal unit_price }
    ORDERS { int order_id PK int customer_id FK date order_date enum status }
    ORDER_ITEMS { int order_item_id PK int order_id FK int product_id FK int quantity decimal unit_price }
```

A customer can place many orders and a category can contain many products.
`order_items` resolves the many-to-many relationship between orders and products.
No cascading delete is used, so order history cannot be erased accidentally.
