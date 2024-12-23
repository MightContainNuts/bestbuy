from products import Product
from store import Store


def start(store: Store) -> None:
    """
    menu for the store
    :param store:
    :type store:
    :return:
    :rtype:
    """
    menu = {
        1: ("List all products in store", lambda: print_all_products(store)),
        2: ("Show total amount in store", lambda: print_total_quantity(store)),
        3: ("Make an order ", store.make_an_order),
        4: ("Quit", exit),
    }
    while True:
        print_menu(menu)
        choice = input("Enter your choice: ")
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid choice")
            continue
        if choice in menu:
            func = menu[choice][1]
            func()


def print_menu(menu: dict) -> None:
    """
    print the menu
    :param menu:
    :type menu:
    :return:
    :rtype:
    """
    print("Menu:")
    for key, value in menu.items():
        print(f"{key}: {value[0]}")


def print_total_quantity(store: Store) -> None:
    """
    print the total _quantity
    :param total:
    :type total:
    :return:
    :rtype:
    """
    total = store.get_total_quantity()
    print("\nQuantity of products in store:")
    print("-" * 30)
    print(f"Total _quantity: {total}")
    print("-" * 30 + "\n")


def print_all_products(store: Store) -> None:
    """
    print all products
    :param store:
    :type store:
    :return:
    :rtype:
    """
    products = store.get_all_products()
    print("\nAll products in store:")
    print("-" * 30)
    for idx, product in enumerate(products):
        print(f"{idx + 1}:", product.show())
    print("-" * 30 + "\n")


if __name__ == "__main__":
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
    ]
    best_buy = Store(product_list)
    start(best_buy)
