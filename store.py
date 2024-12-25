from products import Product, NonStockedProducts, LimitedProducts
from ui_helpers import UIHelpers
from typing import Union


class Store:
    """
    Store class
    """

    def __init__(self, products: list[Product] = None) -> None:
        """
        initialise store with products
        :param products:
        :type products:
        """
        self.products = products if products else []

    def add_product(self, product: Product) -> None:
        """
        add product to store
        :param product:
        :type product:
        :return:
        :rtype:
        """
        if not isinstance(
            product, (Product, NonStockedProducts, LimitedProducts)
        ):
            raise ValueError("Product should be an instance of Product")
        self.products.append(product)

    def remove_product(self, product: Product) -> None:
        """
        remove product from store
        :param product:
        :type product:
        :return:
        :rtype:
        """
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        """
        get total _quantity of products in store
        :return:
        :rtype:
        """
        total = sum([product.product_quantity for product in self.products])
        UIHelpers.print_total_quantity(total)
        return total

    def get_all_products(self) -> list[Product]:
        """
        get all products in store
        :return:
        :rtype:
        """
        products = self.products
        UIHelpers.print_all_products(products)
        return self.products

    def make_an_order(self) -> list[tuple[Product, int]]:
        """
        make an order
        :return:
        :rtype:
        """
        shopping_list = []
        print("Enter the product name and quantity to order")
        while True:
            self.get_all_products()
            product_num = self._validate_prod_qty("product number")
            if product_num is None:
                break

            if product_num < 1 or product_num > len(self.products):
                print("Invalid product number, please enter a valid number")
                continue
            product = self.products[product_num - 1]

            quantity = self._validate_prod_qty("quantity")
            if quantity is None:
                break
            UIHelpers.print_shopping_confirmation(product, quantity)
            print("Added to the shopping list")
            shopping_list.append((product, quantity))
        self.order(shopping_list)
        return shopping_list

    def _validate_prod_qty(self, message: str) -> Union[None, int]:
        """
        validate the order
        :param pot_number:
        :type pot_number:
        :return:
        :rtype:
        """
        while True:
            user_number = input(f"Enter the {message}: ")
            if user_number == "":
                return None
            try:
                user_number = int(user_number)
                if user_number < 1:
                    print(f"Invalid {message}, please enter a valid number")
                    continue
                return user_number
            except ValueError:
                print(f"Invalid {message}, please enter a valid number")
                continue

    def order(self, shopping_list: list[tuple[Product, int]]) -> float:
        """
        finalise order and print summary
        :param shopping_list:
        :type shopping_list:
        :return:
        :rtype:
        """
        print("\nOrder summary:")
        print("-" * 70)
        UIHelpers.print_shopping_confirmation_start()

        total = 0

        for item in shopping_list:
            product, basket_quantity = item
            found_product = None
            for store_product in self.products:
                if store_product.name == product.name:
                    found_product = store_product
                    break
            if found_product:
                if isinstance(found_product, NonStockedProducts):
                    total += found_product.price * basket_quantity
                    UIHelpers.print_shopping_confirmation(
                        found_product, basket_quantity
                    )

                elif (
                    isinstance(found_product, LimitedProducts)
                    and found_product.product_quantity >= 1
                ):
                    MAX = 1
                    if basket_quantity > 1:
                        print(
                            f"*{found_product.name} can only be applied {MAX} time(s) per order (ordered {basket_quantity} time(s))"  # noqa E501
                        )  # noqa E501
                        basket_quantity = MAX

                    total += found_product.price * basket_quantity
                    found_product.product_quantity -= 1
                    UIHelpers.print_shopping_confirmation(
                        found_product, basket_quantity
                    )
                elif (
                    isinstance(found_product, Product)
                    and found_product.product_quantity >= basket_quantity
                ):
                    total += found_product.price * basket_quantity
                    found_product.product_quantity -= basket_quantity
                    UIHelpers.print_shopping_confirmation(
                        found_product, basket_quantity
                    )
                else:
                    print(
                        f"Error: Unsufficient qty for {product.name}. "
                        f"Available: {found_product.product_quantity}, Requested: {basket_quantity}"  # noqa E501
                    )

        UIHelpers.print_shopping_confirmation_end()
        print(f"Total: {total} \n")
        return total
