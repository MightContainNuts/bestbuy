"""
promotion.py
This module contains classes representing different types of promotions
that can be applied to shopping baskets to calculate discounts.
"""

# imports
from abc import ABC, abstractmethod


# abstract parent class
class Promotions(ABC):
    """
    Abstract base class for promotions. All promotion types should inherit
    from this classand implement the `apply_promotion` method to define
    their specific discount logic.

    Attributes:
        description (str): used for sorting promotions if multiple
        promotions are applied to a product
        order is:
        01 Third is Free
        02 Second Half price
        03 Discount on all
    """

    def __init__(self, description=None):
        """
        description is stored on instance creation
        :param description:
        :type description:
        """
        self.description = description

    @abstractmethod
    def __str__(self):
        """
        str representtion
        needs to be overwritten for sorting
        :return:
        :rtype:
        """
        return (
            "Promotion: 99_default"
            if not self.description
            else f"Promotion: {self.description}"
        )

    @abstractmethod
    def apply_promotion(self, current_total, basket_quantity):
        """
        abstract method for what the promotion does
        :param current_total:
        :type current_total:
        :param basket_quantity:
        :type basket_quantity:
        :return:
        :rtype:
        """
        pass


# child classes
class SecondHalfPrice(Promotions):
    """
    inherits from Promotion.
    shortened to shp for certain methods
    """

    def __init__(self, description):
        """
        creates instance constant and updates description var
        :param description:
        :type description:
        """
        super().__init__(description)
        self.HALF_PRICE_DIVISOR = 2

    def __str__(self):
        """
        used for sorting for multiple promotions on one product
        :return:
        :rtype:
        """
        return f"Promotion: 02 {self.description}"

    def apply_promotion(
        self, current_total: float, basket_quantity: int
    ) -> float:
        """
        Applies the "second half price" promotion to a shopping basket.

        For every two items in the basket, the second is half-price.

        Args:
            current_total (float): The current total cost of the basket.
            basket_quantity (int): The total number of items in the basket.

        Returns:
            float: The new total after applying the discount.
        """
        price_per_item = current_total / basket_quantity
        discounted_items = basket_quantity // 2
        full_price_items = basket_quantity - discounted_items
        full_price_total = full_price_items * price_per_item
        discounted_total = (
            discounted_items * price_per_item / self.HALF_PRICE_DIVISOR
        )

        total = round(
            full_price_total + discounted_total,
            2,
        )
        return total


class ThirdOneFree(Promotions):

    def __init__(self, description):
        super().__init__(description)
        self.EVERY_N_FREE = 3

    def __str__(self):
        return f"Promotion: 01 {self.description}"

    def apply_promotion(self, current_total, basket_quantity):
        """
        Applies the "third one free" promotion to a shopping basket.

        For every three items in the basket, one of them (the least expensive)
        is free.

        Args:
            current_total (float): The current total cost of the basket.
            basket_quantity (int): The total number of items in the basket.

        Returns:
            float: The new total after applying the discount.
        """
        free_items = basket_quantity // self.EVERY_N_FREE
        full_price_items = basket_quantity - free_items
        total = round(current_total * full_price_items / basket_quantity, 2)
        return total


class PercentDiscount(Promotions):

    def __init__(self, description, percent):
        super().__init__(description)
        self.discount = percent / 100

    def __str__(self):
        return f"Promotion: 03 {self.description}"

    def apply_promotion(self, current_total, basket_quantity):
        """
        Applies a percentage discount promotion to a shopping basket.

        This promotion reduces the total cost by a specified percentage.

        Args:
            current_total (float): The current total cost of the basket.
            basket_quantity (int): The total number of items in the basket
            (not used in calculation).

        Returns:
            float: The new total after applying the discount.
        """
        total = round(current_total * (1 - self.discount), 2)
        return total
