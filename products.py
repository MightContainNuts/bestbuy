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
        self._quantity = quantity
        self._active = active

    @property
    def product_quantity(self) -> int:
        """
        get the _quantity of the product
        :return:
        :rtype:
        """
        return self._quantity

    @product_quantity.setter
    def product_quantity(self, quantity: int) -> int:
        """
        set the _quantity of the product
        :param quantity:
        :type quantity:
        :return:
        :rtype:
        """
        if quantity < 0:
            raise ValueError("Quantity should be a positive integer")
        self._quantity = quantity

    @property
    def is_active(self) -> bool:
        """
        check if the product is active
        :return:
        :rtype:
        """
        return self._active

    @is_active.setter
    def is_active(self, _active: bool) -> None:
        if not isinstance(_active, bool):
            raise ValueError("Active should be a boolean")
        self._active = _active

    def activate(self) -> None:
        """
        activate the product
        :return:
        :rtype:
        """
        self.is_active = True

    def deactivate(self) -> None:
        """
        deactivate the product
        :return:
        :rtype:
        """
        self.is_active = False

    def show(self) -> str:
        """
        show the product details
        :return:
        :rtype:
        """
        return f"{self.name} - {str(self.price)} - {self.product_quantity}"

    def buy(self, quantity_to_buy: int) -> float:
        """
        buy the product
        :param _quantity:
        :type _quantity:
        :return:
        :rtype:
        """
        self._validate_quantity(quantity_to_buy)
        if self.product_quantity < quantity_to_buy:
            raise ValueError("Not enough _quantity")
        self.product_quantity -= quantity_to_buy
        return round(self.price * quantity_to_buy, 2)

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
        validate the _quantity of the product
        :param quantity:
        :type quantity:
        :return:
        :rtype:
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity should be a positive integer")
        return True
