def print_shopping_confirmation_start():
    """
    print the shopping confirmation start
    :return:
    :rtype:
    """
    print("-" * 80)
    print(
        "Product".ljust(30),
        "Price".center(15),
        "Qty".center(6),
        "Sub-total".center(10),
    )
    print("-" * 80)


def print_shopping_confirmation_end():
    """
    print the shopping confirmation end
    :return:
    :rtype:
    """
    print("-" * 80)


def print_shopping_confirmation(found_product, basket_quantity):
    """
    print the shopping confirmation
    :param found_product:
    :type found_product:
    :param basket_quantity:
    :type basket_quantity:
    :return:
    :rtype:
    """
    print(
        f"{found_product.name.ljust(30)}\t"
        f"{found_product.price:>10.2f}\t"
        f"{basket_quantity:>4}\t"
        + f"{found_product.price * basket_quantity:>10.2f}\t"
    )


def print_all_products(products) -> None:
    """
    print all products
    :param store:
    :type store:
    :return:
    :rtype:
    """
    print("\nAll products in store:")
    print_shopping_confirmation_start()
    for idx, product in enumerate(products):
        print(f"{idx + 1}:", product.show())
    print_shopping_confirmation_end()


def print_total_quantity(total: int) -> None:
    """
    print the total _quantity
    :param total:
    :type total:
    :return:
    :rtype:
    """
    print("\nQuantity of products in store:")
    print("-" * 30)
    print(f"Total quantity: {total}")
    print("-" * 30 + "\n")


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
