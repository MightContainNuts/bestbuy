"""
promotions.py contains all methods and classes for the products
Product class is for the main products
Limited are those that have restrictions on amount per order
Non Stocked contain items that have no physical presence in the store
"""

# imports
from promotions import Promotions


class Product:
    def __init__(
        self,
        name: str,
        price: float,
        quantity: int,
        active: bool = True,
        promotions: Promotions = None,
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
        self._promotions = promotions if promotions is not None else []

    def __str__(self):
        """
        refactored in bonus step to use str instead of show method
        :return:
        :rtype:
        """
        promotion_text = self.create_promotion_text()
        return (
            f"{self.name.ljust(30)} - {str(self.price).ljust(6)} - {str(self.product_quantity).ljust(6)}\n"  # noqa E501
            + promotion_text  # noqa E501
        )

    def __gt__(self, other):
        """
        bonus step add comparison gt and lt
        :param other:
        :type other:
        :return:
        :rtype:
        """
        if not isinstance(other, Product):
            return NotImplemented
        return self.price > other.price

    def __lt__(self, other):
        """
        bonus step add comparison gt and lt
        :param other:
        :type other:
        :return:
        :rtype:
        """
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

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

    @property
    def promotions(self) -> list[Promotions]:
        """
        get the promotions of the product
        :return:
        :rtype:
        """
        return self._promotions

    @promotions.setter
    def promotions(self, promotions: list) -> None:
        """
        set the promotions of the product
        :param promotions:
        :type promotions:
        :return:
        :rtype:
        """
        if not isinstance(promotions, list):
            raise ValueError("Promotions should be a list")
        self._promotions = promotions

    def create_promotion_text(self) -> str:
        """create promotion text"""
        return " - ".join(str(promotion) for promotion in self.promotions)

    # public methods
    def add_promotion(self, promotion: Promotions) -> None:
        """
        add a new product promotion to a list
        :param promotion:
        :type promotion:
        :return:
        :rtype:
        """
        if not isinstance(promotion, Promotions):
            raise ValueError("Promotion must be a valid promotion object")
        if promotion not in self.promotions:
            self.promotions.append(promotion)
            self.promotions.sort(key=lambda promo: str(promo))
        else:
            print(f"Promotion already applied to {self.name}")

    def remove_promotion(self, promotion: Promotions) -> None:
        """
        remove an existing promotion for a product
        :param promotion:
        :type promotion:
        :return:
        :rtype:
        """
        if not isinstance(promotion, Promotions):
            raise ValueError("Promotion must be a valid promotion object")
        if promotion in self.promotions:
            self.promotions.remove(promotion)
        else:
            print(f"Promotion was not applied to {self.name}")

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
        promotion_text = self.create_promotion_text()
        return (
            f"{self.name.ljust(30)} - {str(self.price).ljust(6)} - {str(self.product_quantity).ljust(6)}\n"  # noqa E501
            + promotion_text  # noqa E501
        )

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

    # private methods
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


class NonStockedProducts(Product):

    def __init__(self, name: str, price: float, active: bool = True) -> None:
        super().__init__(name, price, active)
        self._quantity = 0

    def __str__(self):
        """
        customized str override for show method
        :return:
        :rtype:
        """
        promotion_text = self.create_promotion_text()
        return (
            f"{self.name.ljust(30)} - {str(self.price).ljust(6)} - On Demand\n"
            + promotion_text
        )  # noqa E501

    def show(self) -> str:
        """
        show the product details
        :return:
        :rtype:
        """
        promotion_text = self.create_promotion_text()
        return (
            f"{self.name.ljust(30)} - {str(self.price).ljust(6)} - On Demand\n"
            + promotion_text
        )  # noqa E501


class LimitedProducts(Product):

    def __init__(
        self,
        name: str,
        price: float,
        quantity: int,
        active: bool = True,
        maximum: int = 1,
    ) -> None:
        super().__init__(name, price, quantity, active)
        self.maximum = maximum

    def __str__(self):
        """
        override str method
        :return:
        :rtype:
        """
        promotion_text = self.create_promotion_text()
        return (
            f"{self.name.ljust(30)} - {str(self.price).ljust(6)} - {str(self.product_quantity).ljust(6)}(Max per order:{self.maximum})\n"  # noqa E501
            + promotion_text
        )

    def show(self) -> str:
        """
        show the product details
        :return:
        :rtype:
        """
        promotion_text = self.create_promotion_text()
        return (
            f"{self.name.ljust(30)} - {str(self.price).ljust(6)} - {str(self.product_quantity).ljust(6)}(Max per order:{self.maximum})\n"  # noqa E501
            + promotion_text  # noqa E501
        )
