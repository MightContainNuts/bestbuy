from products import Product


class Store:

    def __init__(self, products: list[Product] = None) -> None:
        self.products = products if products else []

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise ValueError("Product should be an instance of Product")
        self.products.append(product)

    def remove_product(self, product: Product) -> None:
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        return sum([product.quantity for product in self.products])

    def get_all_products(self) -> list[Product]:
        return self.products

    def order(self, shopping_list: list[tuple[Product, int]]) -> float:
        total = 0
        for item in shopping_list:
            product, basket_quantity = item
            found_product = None
            for store_product in self.products:
                if store_product.name == product.name:
                    found_product = store_product
                    break
            if found_product and found_product.quantity >= basket_quantity:
                total += found_product.price * basket_quantity
            else:
                raise ValueError(
                    f"Not enough quantity or product not found: {product.name}"
                )
        return total
