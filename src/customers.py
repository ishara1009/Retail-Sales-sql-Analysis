"""Customer CRUD operations."""

import re
from mysql.connector import IntegrityError
from src.database import get_connection

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_customer(name, email, city):
    values = [value.strip() for value in (name, email, city)]
    if not all(values):
        raise ValueError("Name, email and city are required.")
    if not EMAIL_PATTERN.match(values[1]):
        raise ValueError("Enter a basic valid email address, such as name@example.com.")
    return values[0], values[1].lower(), values[2]


def add_customer(name, email, city):
    name, email, city = validate_customer(name, email, city)
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # %s placeholders user input එක SQL code එකක් වීම වළක්වයි.
        cursor.execute("INSERT INTO customers (customer_name, email, city) VALUES (%s, %s, %s)", (name, email, city))
        connection.commit()
        return cursor.lastrowid
    except IntegrityError as error:
        connection.rollback()
        if error.errno == 1062:
            raise ValueError("That email address already belongs to a customer.") from error
        raise
    finally:
        cursor.close(); connection.close()


def list_customers():
    connection = get_connection(); cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT customer_id, customer_name, email, city FROM customers ORDER BY customer_id")
        return cursor.fetchall()
    finally:
        cursor.close(); connection.close()


def update_customer(customer_id, name, email, city):
    name, email, city = validate_customer(name, email, city)
    connection = get_connection(); cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT customer_name, email, city FROM customers WHERE customer_id = %s", (customer_id,))
        current = cursor.fetchone()
        if not current:
            raise LookupError(f"Customer {customer_id} does not exist.")
        if (current["customer_name"], current["email"], current["city"]) == (name, email, city):
            return False
        cursor.execute("UPDATE customers SET customer_name=%s, email=%s, city=%s WHERE customer_id=%s", (name, email, city, customer_id))
        connection.commit(); return True
    except IntegrityError as error:
        connection.rollback()
        if error.errno == 1062:
            raise ValueError("That email address already belongs to a customer.") from error
        raise
    finally:
        cursor.close(); connection.close()


def delete_customer(customer_id):
    connection = get_connection(); cursor = connection.cursor()
    try:
        cursor.execute("SELECT customer_id FROM customers WHERE customer_id=%s", (customer_id,))
        if not cursor.fetchone():
            raise LookupError(f"Customer {customer_id} does not exist.")
        # Foreign key සම්බන්ධ order history එක අහම්බෙන් මැකීම වළක්වයි.
        cursor.execute("SELECT COUNT(*) FROM orders WHERE customer_id=%s", (customer_id,))
        if cursor.fetchone()[0]:
            raise ValueError("This customer has orders and cannot be deleted.")
        cursor.execute("DELETE FROM customers WHERE customer_id=%s", (customer_id,))
        connection.commit()
    except IntegrityError as error:
        connection.rollback()
        raise ValueError("This customer is referenced by other records and cannot be deleted.") from error
    finally:
        cursor.close(); connection.close()
