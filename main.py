"""Beginner-friendly command-line interface."""

from mysql.connector import Error

from src import customers, orders, products, reports

MENU = """
1. Add customer
2. View customers
3. Update customer
4. Delete customer
5. View products
6. View products by category
7. Create order
8. Update order status
9. Export sales reports
0. Exit
"""


def read_positive_int(prompt):
    value = int(input(prompt))
    if value <= 0:
        raise ValueError("Enter a positive whole number.")
    return value


def show_customers():
    rows = customers.list_customers()
    for row in rows:
        print(f"{row['customer_id']:>3} | {row['customer_name']} | {row['email']} | {row['city']}")
    if not rows: print("No customers found.")


def show_products(category_id=None):
    rows = products.list_products(category_id)
    for row in rows:
        print(f"{row['product_id']:>3} | {row['product_name']} | {row['category_name']} | {products.format_lkr(row['unit_price'])}")
    if not rows: print("No products found.")


def handle_choice(choice):
    if choice == "1":
        customer_id = customers.add_customer(input("Name: "), input("Email: "), input("City: "))
        print(f"Customer {customer_id} added.")
    elif choice == "2": show_customers()
    elif choice == "3":
        changed = customers.update_customer(read_positive_int("Customer ID: "), input("New name: "), input("New email: "), input("New city: "))
        print("Customer updated." if changed else "No changes were needed.")
    elif choice == "4":
        customers.delete_customer(read_positive_int("Customer ID: ")); print("Customer deleted.")
    elif choice == "5": show_products()
    elif choice == "6": show_products(read_positive_int("Category ID: "))
    elif choice == "7":
        customer_id = read_positive_int("Customer ID: "); items = []
        print("Enter products. Leave product ID blank when finished.")
        while True:
            value = input("Product ID: ").strip()
            if not value: break
            product_id = int(value)
            quantity = read_positive_int("Quantity: ")
            items.append((product_id, quantity))
        print(f"Order {orders.create_order(customer_id, items)} created as pending.")
    elif choice == "8":
        changed = orders.update_order_status(read_positive_int("Order ID: "), input("New status: "))
        print("Order status updated." if changed else "The order already has that status.")
    elif choice == "9":
        for path in reports.export_reports(): print(f"Exported {path.name}")
    else: print("Invalid menu selection. Choose 0 to 9.")


def main():
    while True:
        print(MENU)
        try:
            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye!"); return
            handle_choice(choice)
        except (ValueError, LookupError, ConnectionError, Error) as error:
            print(f"Error: {error}")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!"); return


if __name__ == "__main__":
    main()
