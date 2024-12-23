from products import Product
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
        if not isinstance(product, Product):
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
        return total

    def get_all_products(self) -> list[Product]:
        """
        get all products in store
        :return:
        :rtype:
        """
        return self.products

    def make_an_order(self) -> list[tuple[Product, int]]:
        """
        make an order
        :return:
        :rtype:
        """
        shopping_list = []
        print("Enter the product name and _quantity to order")
        while True:
            product_num = self._validate_prod_qty("product number")
            if product_num is None:
                break

            if product_num < 1 or product_num > len(self.products):
                print("Invalid product number, please enter a valid number")
                continue
            product = self.products[product_num - 1]

            quantity = self._validate_prod_qty("_quantity")
            if quantity is None:
                break

            print(f"Added {product.name} - {quantity} to the shopping list")
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
            user_number = input("Enter the {message}: ")
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
        print("-" * 30)

        total = 0

        for item in shopping_list:
            product, basket_quantity = item
            found_product = None
            for store_product in self.products:
                if store_product.name == product.name:
                    found_product = store_product
                    break
            if found_product:
                if found_product.product_quantity >= basket_quantity:
                    total += found_product.price * basket_quantity
                    found_product.product_quantity -= basket_quantity
                    print(
                        f"{product.name} - {product.price} - {basket_quantity}"
                    )
                else:
                    print(
                        f"Error: Unsufficient qty for {product.name}. "
                        f"Available: {found_product.product_quantity}, Requested: {basket_quantity}"  # noqa E501
                    )

        print("-" * 30)
        print(f"Total: {total} \n")
        return total
