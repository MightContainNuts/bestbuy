class Product:
    def __init__(
        self, name: str, price: float, quantity: int, active: bool = True
    ) -> None:
        Product.validate_name(name)
        Product.validate_price(price)
        Product.validate_quantity(quantity)

        self.name = name
        self.price = round(float(price), 2)
        self.quantity = quantity
        self.active = active

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        self.quantity = quantity

    def is_active(self) -> bool:
        return self.active

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def show(self) -> str:
        return f"{self.name} - {self.price} - {self.quantity} - {self.active}"

    def buy(self, quantity: int) -> float:
        self.validate_quantity(quantity)
        if self.quantity < quantity:
            raise ValueError("Not enough quantity")
        self.quantity -= quantity
        return round(self.price * self.quantity, 2)

    @staticmethod
    def validate_name(name: str) -> bool:
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name should be a string and not empty")
        return True

    @staticmethod
    def validate_price(price: float) -> bool:
        if not isinstance(price, (float, int)) or price <= 0:
            raise ValueError("Price should be a positive float")
        return True

    @staticmethod
    def validate_quantity(quantity: int) -> bool:
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity should be a positive integer")
        return True
