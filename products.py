class Product:
    def __init__(
        self, name: str, price: float, quantity: int, active: bool = True
    ) -> None:
        """
        initialize a product
        :param name:
        :type name:
        :param price:
        :type price:
        :param quantity:
        :type quantity:
        :param active:
        :type active:
        """
        Product._validate_name(name)
        Product._validate_price(price)
        Product._validate_quantity(quantity)

        self.name = name
        self.price = round(float(price), 2)
        self.quantity = quantity
        self.active = active

    def get_quantity(self) -> int:
        """
        get the quantity of the product
        :return:
        :rtype:
        """
        return self.quantity

    def set_quantity(self, quantity: int) -> int:
        """
        set the quantity of the product
        :param quantity:
        :type quantity:
        :return:
        :rtype:
        """
        self.quantity = quantity
        return self.quantity

    def is_active(self) -> bool:
        """
        check if the product is active
        :return:
        :rtype:
        """
        return self.active

    def activate(self) -> None:
        """
        activate the product
        :return:
        :rtype:
        """
        self.active = True

    def deactivate(self) -> None:
        """
        deactivate the product
        :return:
        :rtype:
        """
        self.active = False

    def show(self) -> str:
        """
        show the product details
        :return:
        :rtype:
        """
        return f"{self.name} - {str(self.price)} - {self.quantity}"

    def buy(self, quantity: int) -> float:
        """
        buy the product
        :param quantity:
        :type quantity:
        :return:
        :rtype:
        """
        self._validate_quantity(quantity)
        if self.quantity < quantity:
            raise ValueError("Not enough quantity")
        self.quantity -= quantity
        return round(self.price * self.quantity, 2)

    @staticmethod
    def _validate_name(name: str) -> bool:
        """
        validate the name of the product
        :param name:
        :type name:
        :return:
        :rtype:
        """
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name should be a string and not empty")
        return True

    @staticmethod
    def _validate_price(price: float) -> bool:
        """
        validate the price of the product
        :param price:
        :type price:
        :return:
        :rtype:
        """
        if not isinstance(price, (float, int)) or price <= 0:
            raise ValueError("Price should be a positive float")
        return True

    @staticmethod
    def _validate_quantity(quantity: int) -> bool:
        """
        validate the quantity of the product
        :param quantity:
        :type quantity:
        :return:
        :rtype:
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity should be a positive integer")
        return True
