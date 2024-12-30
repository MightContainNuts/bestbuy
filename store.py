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
        self.stores = {}

    def __contains__(self, product):
        """
        implements product in products
                :param item:
                :type item:
                :return:
                :rtype:
        """
        return product in self.products

    def __add__(self, other):
        """
        Combine two _stores using the + operator.
        :param other: Another store instance
        :type other: Store
        :return: A new store with combined products
        :rtype: Store
        """
        if not isinstance(other, Store):
            raise ValueError("Can only combine with another Store instance.")

        # Create a new store
        combined_store = Store()

        # Add products from both _stores
        combined_store.products = self.products + other.products

        return combined_store

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


class StoreManager:
    def __init__(self):
        self._stores = {}  # Dictionary to store {store_name: Store instance}

    @property
    def stores(self):
        return self._stores

    @stores.setter
    def stores(self, store_dict):
        # setter for stores
        if not isinstance(store_dict, dict):
            raise ValueError("Stores must be a dictionary")
        self._stores = store_dict

    def add_two_stores(self):
        """
        Combine two stores into a new store.
        :return: The combined store name
        :rtype: str
        """
        print("Adding two stores to make a combination")

        # Validate and retrieve the first store
        store_1 = None
        while not store_1:
            store_name_1 = input("Enter name for store 1: ").strip()
            store_1 = self.stores.get(store_name_1)
            if not store_1:
                print(f"{store_name_1}' doesn't exist. Creating a new store.")
                store_1 = Store()
                self._add_store(store_name_1, store_1)

        # Validate and retrieve the second store
        store_2 = None
        while not store_2:
            store_name_2 = input("Enter name for store 2: ").strip()
            store_2 = self.stores.get(store_name_2)
            if not store_2:
                print(f"{store_name_2} doesn't exist. Creating new store.")
                store_2 = Store()
                self._add_store(store_name_2, store_2)

        # Combine the stores
        combined_store = store_1 + store_2
        combined_store_name = f"{store_name_1}_{store_name_2}_combined"
        print(f"Creating combined store: {combined_store_name}")

        # Add the combined store to the manager
        self._add_store(combined_store_name, combined_store)
        print(
            f"Stores combined successfully! {combined_store_name} added to Store Manager"  # noqa E501
        )

        return combined_store_name

    def _add_store(self, store_name: str, new_store_instance: Store) -> None:
        if store_name in self.stores:
            print("Store name already exists!")
        else:
            self.stores[store_name] = new_store_instance
            print(f"{store_name} created and added to Store Manager:")

    def _is_store_name(self, store_name) -> bool:
        """
        Check if store name exists.
        :param store_name: Name of the store
        :type store_name: str
        :return: True if the store exists, False otherwise
        :rtype: bool
        """
        return store_name in self._stores

    def _validate_store_name(self, store_name_number):
        """
        Validate or create a store based on the name.
        :param store_name_number: Number indicating which store (1 or 2)
        :type store_name_number: int
        :return: The store instance
        :rtype: Store
        """
        while True:
            store_name = input(
                f"Enter name for store {store_name_number}: "
            ).strip()
            if not store_name:
                print("Store name cannot be empty. Please try again.")
                continue

            if self._is_store_name(store_name):
                print(f"Store found: {store_name}")
                return self._stores[store_name]
            else:
                print(f"Store {store_name} does not exist.")
                return None  # Return None if the store doesn't exist
