"""
main.py
contains the start menu and executables
"""

# imports
from products import Product, NonStockedProducts, LimitedProducts
from promotions import PercentDiscount, SecondHalfPrice, ThirdOneFree
from store import Store, StoreManager
from ui_helpers import UIHelpers


def start(
    store: Store,
    store_manager: StoreManager,
    test_mode: bool = False,
    test_iterations: int = 5,
) -> None:
    """
    menu for the store
    :param store:
    :type store:
    :return:
    :rtype:
    """
    menu = {
        1: ("List all products in store", store.get_all_products),
        2: ("Show quantity amount in store", store.get_total_quantity),
        3: ("Make an order ", store.make_an_order),
        4: ("Combine two stores ", store_manager.add_two_stores),
        5: ("Quit", exit),
    }
    iterations = 0
    while True:
        UIHelpers.print_menu(menu)
        choice = input("Enter your choice: ")
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid choice")
            continue
        if choice in menu:
            func = menu[choice][1]
            func()
        if test_mode:
            iterations += 1
            if iterations >= test_iterations:
                break


def exit():
    """
    exit the program
    :return:
    :rtype:
    """
    print("Exiting program")
    raise SystemExit


def main():
    macbook = Product("MacBook Air M2", price=1450, quantity=100)
    bose_headphones = Product(
        "Bose QuietComfort Earbuds", price=250, quantity=500
    )
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    windows_licence = NonStockedProducts("Windows License", price=125)
    shipping = LimitedProducts("Shipping", price=10, quantity=250, maximum=1)

    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")
    thirty_percent = PercentDiscount("30% off!", percent=30)

    macbook.add_promotion(second_half_price)
    bose_headphones.add_promotion(third_one_free)
    pixel.add_promotion(thirty_percent)
    shipping.add_promotion(third_one_free)
    store_manager = StoreManager()
    best_buy = Store()
    store_manager._add_store("Best Buy", best_buy)
    start(best_buy, store_manager)
    best_buy.add_product(macbook)
    best_buy.add_product(bose_headphones)
    best_buy.add_product(pixel)
    best_buy.add_product(windows_licence)
    best_buy.add_product(shipping)
    start(best_buy)


if __name__ == "__main__":
    # setup initial stock of inventory

    main()
