import pytest

from products import Product
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount


@pytest.fixture
def test_product():
    return Product(name="Product", price=10.0, quantity=10)


@pytest.fixture
def test_shp_promotion(test_product):
    """
    shp = second half price
    :return:
    :rtype:
    """
    return SecondHalfPrice(test_product)


@pytest.fixture
def test_tof_promotion(test_product):
    """
    tof = Third One Free
    :return:
    :rtype:
    """
    return ThirdOneFree(test_product)


@pytest.fixture
def test_percent_discount(test_product):
    """
    :return:
    :rtype:
    """
    return PercentDiscount(test_product, percent=30)


# tests for second_half_price class
def test_promotion_second_half_price_with_one(
    test_shp_promotion, test_product
):
    basket_quantity = 1
    current_total = basket_quantity * test_product.price
    total = test_shp_promotion.apply_promotion(current_total, basket_quantity)
    assert total == 10  # no discount


def test_promotion_second_half_price_with_two(
    test_shp_promotion, test_product
):
    basket_quantity = 2
    current_total = basket_quantity * test_product.price
    total = test_shp_promotion.apply_promotion(current_total, basket_quantity)
    assert total == 15  # 10 + 10/2


def test_promotion_second_half_price_with_odd(
    test_shp_promotion, test_product
):
    basket_quantity = 7
    current_total = basket_quantity * test_product.price
    total = test_shp_promotion.apply_promotion(current_total, basket_quantity)
    assert total == 55  # 4*10 + 3*10/2


# tests for third on free class
def test_promotion_third_one_free_less_than_3(
    test_tof_promotion, test_product
):
    basket_quantity = 2
    current_quantity = basket_quantity * test_product.price
    total = test_tof_promotion.apply_promotion(
        current_quantity, basket_quantity
    )
    assert total == 20  # no discount


def test_promotion_third_one_free_with_3(test_tof_promotion, test_product):
    basket_quantity = 3
    current_price = test_product.price * basket_quantity
    total = test_tof_promotion.apply_promotion(current_price, basket_quantity)
    assert total == 20  # 2 * 10 + 1 * free


def test_promotion_third_one_free_with_lots(test_product, test_tof_promotion):
    basket_quantity = 10
    current_price = basket_quantity * test_product.price
    total = test_tof_promotion.apply_promotion(current_price, basket_quantity)
    assert total == 70  # 7 * 10 + 3 * free


# tests for percent discount
def test_promotion_percent_discount(test_product, test_percent_discount):
    basket_quantity = 10
    current_price = basket_quantity * test_product.price
    # discount = 30  % percent
    total = test_percent_discount.apply_promotion(
        current_price, basket_quantity
    )
    assert total == 70  # 10*10 = 100 - 100*(30/100)
