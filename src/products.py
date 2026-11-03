"""Product queries."""

from src.database import get_connection


def list_products(category_id=None):
    connection = get_connection(); cursor = connection.cursor(dictionary=True)
    try:
        sql = """SELECT p.product_id, p.product_name, c.category_name, p.unit_price
                 FROM products p JOIN categories c ON c.category_id = p.category_id"""
        params = ()
        if category_id is not None:
            if category_id <= 0:
                raise ValueError("Category ID must be positive.")
            sql += " WHERE p.category_id = %s"
            params = (category_id,)
        sql += " ORDER BY p.product_id"
        cursor.execute(sql, params)
        return cursor.fetchall()
    finally:
        cursor.close(); connection.close()


def format_lkr(value):
    return f"LKR {value:,.2f}"
