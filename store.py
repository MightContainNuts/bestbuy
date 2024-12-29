# imports
from typing import Union

from products import Product, NonStockedProducts, LimitedProducts
from promotions import Promotions
from ui_helpers import UIHelpers

# types
Subtotal = float
Quantity = int
ShoppingList = list[tuple[Product, int]]


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

    def get_total_quantity(self) -> Quantity:
        """
        get quantity _quantity of products in store
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

    def make_an_order(self) -> ShoppingList:
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
        self._order(shopping_list)
        return shopping_list

    # private methods
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

    def _order(self, shopping_list: ShoppingList) -> float:
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
        for product, basket_quantity in shopping_list:
            found_product = self._find_product(product)
            subtotal = 0
            if found_product:
                if isinstance(found_product, NonStockedProducts):
                    subtotal = self._calc_subtotal_non_stocked_product(
                        found_product, basket_quantity
                    )
                    UIHelpers.print_shopping_confirmation(
                        found_product, basket_quantity
                    )
                elif isinstance(found_product, LimitedProducts):
                    subtotal = self._calc_subtotal_limited_product(
                        found_product, basket_quantity
                    )
                    UIHelpers.print_shopping_confirmation(
                        found_product, basket_quantity
                    )
                elif isinstance(found_product, Product):
                    subtotal = self._calc_subtotal_stocked_product(
                        found_product, basket_quantity
                    )
                    UIHelpers.print_shopping_confirmation(
                        found_product, basket_quantity
                    )
            if found_product.promotions:
                discounted_subtotal = self._calc_any_promotions(
                    found_product, subtotal, basket_quantity
                )
                total += discounted_subtotal
            else:
                total += subtotal
        UIHelpers.print_shopping_confirmation_end()
        print(f"Total: {total} \n")
        return total

    def _find_product(self, product):
        """
        find the product in inventory
        :param product:
        :type product:
        :return:
        :rtype:
        """
        for store_product in self.products:
            if store_product.name == product.name:
                return store_product
            else:
                return None

    def _calc_subtotal_non_stocked_product(
        self, found_product: Product, basket_quantity: int
    ) -> Subtotal:
        """
        logic for calculating total for non stocked products
        :param found_product:
        :type found_product:
        :param basket_quantity:
        :type basket_quantity:
        :return:
        :rtype:
        """
        return found_product.price * basket_quantity

    def _calc_subtotal_limited_product(
        selfself, found_product: Product, basket_quantity: int
    ) -> Subtotal:
        """
        logic for calculating subtotal for limited products
        :param found_product:
        :type found_product:
        :param basket_quantity:
        :type basket_quantity:
        :return:
        :rtype:
        """
        MAX = 1
        if basket_quantity > MAX:
            raise ValueError(
                f"{found_product.name} can only be applied {MAX} time(s) per order (ordered {basket_quantity} time(s))"  # noqa E501
            )
        found_product.product_quantity -= basket_quantity
        return found_product.price * basket_quantity

    def _calc_subtotal_stocked_product(
        self, found_product: Product, basket_quantity: int
    ) -> Subtotal:
        """
        logic for calculating stocked products subtotal
        :param found_product:
        :type found_product:
        :param basket_quantity:
        :type basket_quantity:
        :return:
        :rtype:
        """
        if found_product.product_quantity >= basket_quantity:

            found_product.product_quantity -= basket_quantity
            return found_product.price * basket_quantity
        else:
            print(
                f"Error: Unsufficient qty for {found_product.name}. "
                f"Available: {found_product.product_quantity}, Requested: {basket_quantity}"  # noqa E501
            )

    def _calc_any_promotions(
        self,
        found_product: Product,
        current_subtotal: float,
        basket_quantity: int,
    ) -> Subtotal:
        """
        logic for calc subtotal for items with promotions
        :param found_product:
        :type found_product:
        :param basket_quantity:
        :type basket_quantity:
        :return:
        :rtype:
        """

        for promotion in found_product.promotions:
            if isinstance(promotion, Promotions):
                subtotal_after_promotion = promotion.apply_promotion(
                    current_subtotal, basket_quantity
                )
                current_subtotal = subtotal_after_promotion

        return current_subtotal
