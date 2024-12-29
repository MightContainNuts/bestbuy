"""
ui)helpers.py
contains all the ui print methods fr displaying to the screen
no inheritance or class related objects. Just in a lass to keep them organised
"""


class UIHelpers:

    @staticmethod
    def print_shopping_confirmation_start():
        """
        print the shopping confirmation start
        :return:
        :rtype:
        """
        print("-" * 80)
        print(f"{'Product':<30}{'Price':^15}{'Qty':^6}{'Sub-quantity':^10}")
        print("-" * 80)

    @staticmethod
    def print_shopping_confirmation_end():
        """
        print the shopping confirmation end
        :return:
        :rtype:
        """
        print("-" * 80)

    @staticmethod
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
            f"{found_product.name:<30}{found_product.price:>15.2f}{basket_quantity:>6}{found_product.price * basket_quantity:>10.2f}\t"  # noqa E501
        )

    @staticmethod
    def print_all_products(products) -> None:
        """
        print all products
        :param store:
        :type store:
        :return:
        :rtype:
        """
        print("\nAll products in store:")
        UIHelpers.print_shopping_confirmation_start()
        for idx, product in enumerate(products):
            print(f"{idx + 1}:", product.show())
        UIHelpers.print_shopping_confirmation_end()

    @staticmethod
    def print_total_quantity(total: int) -> None:
        """
        print the quantity _quantity
        :param total:
        :type total:
        :return:
        :rtype:
        """
        print("\nQuantity of products in store:")
        print("-" * 30)
        print(f"Total quantity: {total}")
        print("-" * 30 + "\n")

    @staticmethod
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
