from products import Product


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
        get total quantity of products in store
        :return:
        :rtype:
        """
        total = sum([product.quantity for product in self.products])
        print("\nQuantity of products in store:")
        print("-" * 30)
        print(f"Total quantity: {total}")
        print("-" * 30 + "\n")
        return total

    def get_all_products(self) -> list[Product]:
        """
        get all products in store
        :return:
        :rtype:
        """
        print("\n All products in store:")
        print("-" * 30)
        for idx, product in enumerate(self.products):
            print(f"{idx + 1}:", product.show())
        print("-" * 30 + "\n")
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
            product_num = input("Enter the product number: ")
            if product_num == "":
                break
            try:
                product_num = int(product_num)
                if product_num < 1 or product_num > len(self.products):
                    raise ValueError
            except ValueError:
                print("Invalid product number")
                continue
            product = self.products[product_num - 1]
            quantity = input("Enter the quantity: ")
            try:
                quantity = int(quantity)
                if quantity < 1:
                    raise ValueError
            except ValueError:
                print("Invalid quantity")
                continue
            print(f"Added {product.name} - {quantity} to the shopping list")
            shopping_list.append((product, quantity))
        self.order(shopping_list)
        return shopping_list

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
                if found_product.quantity >= basket_quantity:
                    total += found_product.price * basket_quantity
                    found_product.quantity -= basket_quantity
                    print(
                        f"{product.name} - {product.price} - {basket_quantity}"
                    )
                else:
                    print(
                        f"Error: Unsufficient qty for {product.name}. "
                        f"Available: {found_product.quantity}, Requested: {basket_quantity}"  # noqa E501
                    )

        print("-" * 30)
        print(f"Total: {total} \n")
        return total
