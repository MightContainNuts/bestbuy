from products import Product, NonStockedProducts, LimitedProducts
from store import Store
from helpers import print_menu


def start(store: Store) -> None:
    """
    menu for the store
    :param store:
    :type store:
    :return:
    :rtype:
    """
    menu = {
        1: ("List all products in store", store.get_all_products),
        2: ("Show total amount in store", store.get_total_quantity),
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


if __name__ == "__main__":
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProducts("Windows License", price=125),
        LimitedProducts("Shipping", price=10, quantity=250, maximum=1),
    ]
    best_buy = Store(product_list)
    start(best_buy)
