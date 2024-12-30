import pytest

from products import Product, NonStockedProducts, LimitedProducts
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount


@pytest.fixture
def test_product_1():
    return Product(name="Product", price=10.0, quantity=10)


@pytest.fixture
def test_product_2():
    return Product(name="Product2", price=20.0, quantity=10)


@pytest.fixture
def test_non_stock_product():
    return NonStockedProducts(name="NonStockProduct", price=10.0)


@pytest.fixture
def test_limited_stock():
    return LimitedProducts(name="LimitedProduct", price=10.0, quantity=10)


@pytest.fixture
def test_shp_promotion(test_product_1):
    """
    shp = second half price
    :return:
    :rtype:
    """
    return SecondHalfPrice(test_product_1)


@pytest.fixture
def test_tof_promotion(test_product_1):
    """
    tof = Third One Free
    :return:
    :rtype:
    """
    return ThirdOneFree(test_product_1)


@pytest.fixture
def test_percent_discount(test_product_1):
    """
    :return:
    :rtype:
    """
    return PercentDiscount(test_product_1, percent=30)


# tests for _validate methods
def test_validate_name_is_string():
    name = "Product"
    assert Product._validate_name(name), "validate_name should return a string"


def test_validate_name_is_not_empty():
    name = None
    with pytest.raises(
        ValueError, match="Name should be a string and not empty"
    ):
        Product._validate_name(name)


def test_validate_price_is_float():
    price = 10.0
    assert Product._validate_price(
        price
    ), "validate_price should return a float"


def test_validate_price_is_not_empty():
    price = None
    with pytest.raises(ValueError, match="Price should be a positive float"):
        Product._validate_price(price)


def test_validate_price_is_greater_equal_0():
    price = -10.0
    with pytest.raises(ValueError, match="Price should be a positive float"):
        Product._validate_price(price)


def test_validate_quantity_is_int():
    qty = 10
    assert Product._validate_quantity(
        qty
    ), "validate_quantity should return an integer"


def test_validate_quantity_is_greater_equal_0():
    qty = None
    with pytest.raises(
        ValueError, match="Quantity should be a positive integer"
    ):
        Product._validate_quantity(qty)


def test_validate_quantity_is_greater_than_zero():
    qty = -10
    with pytest.raises(
        ValueError, match="Quantity should be a positive integer"
    ):
        Product._validate_quantity(qty)


def test_product_quantity_negative_int(test_product_1):
    with pytest.raises(
        ValueError, match="Quantity should be a positive integer"
    ):
        test_product_1.product_quantity = -1


# tests for instnce creation variables and states
def test_product_instance_with_invalid_name():
    with pytest.raises(
        ValueError, match="Name should be a string and not empty"
    ):
        Product(name="", price=10.0, quantity="10")


def test_product_instance_with_invalid_price():
    with pytest.raises(ValueError, match="Price should be a positive float"):
        Product(name="Name", price="10", quantity=10)


def test_product_instance_with_invalid_quantity():
    with pytest.raises(
        ValueError, match="Quantity should be a positive integer"
    ):
        Product(name="Product", price=10.0, quantity="")


# tests for quantity getter and setter
def test_get_quantity(test_product_1):
    assert test_product_1.product_quantity == 10, "The quantity should be 10"


def test_set_quantity(test_product_1):
    test_product_1.product_quantity = 10
    assert test_product_1.product_quantity == 10, "The quantity should be 10"


# tests for _is_active method getter and setters
def test_is_active(test_product_1):
    assert test_product_1.is_active, "The product should be active"


def test_is_active_on_initialise(test_product_1):
    test_prod = test_product_1
    assert test_prod._active, "The product should be active"


def test_is_active_setter_bool(test_product_1):
    with pytest.raises(ValueError, match="Active should be a boolean"):
        test_product_1.is_active = 123


def test_product_deactivate(test_product_1):
    assert (
        test_product_1._active
    ), "The product should be activated on initialise"
    test_product_1.deactivate()
    assert not test_product_1._active, "The product should be deactivated"


def test_product_activate(test_product_1):
    test_product_1.deactivate()
    assert not test_product_1._active, "The product should be deactivated"
    test_product_1.activate()
    assert test_product_1._active, "The product should be activated"


# tests for ordering product
def test_buy(test_product_1):
    test_shopping = test_product_1.buy(5)
    assert test_shopping == 50.0, "The quantity price should be 50.0"
    assert test_product_1.product_quantity == 5, "The _quantity should be 5"


def test_buy_with_invalid_quantity(test_product_1):
    with pytest.raises(ValueError, match="Not enough _quantity"):
        test_product_1.buy(15)
    assert test_product_1.product_quantity == 10, "The _quantity should be 10"


# tests for show method (updated to implement promotions)
def test_show_product(test_product_1):
    expected = "Product                        - 10.0   - 10    \n"
    actual = test_product_1.show()
    actual_str = str(test_product_1)
    assert actual == expected
    assert actual_str == expected


def test_show_with_non_stocked_product(
    test_non_stock_product: NonStockedProducts,
):
    expected = "NonStockProduct                - 10.0   - On Demand\n"
    actual = str(test_non_stock_product)
    assert actual == expected


def test_show_with_limited_product_instance(
    test_limited_stock: LimitedProducts,
):
    expected = (
        "LimitedProduct                 - 10.0   - 10    (Max per order:1)\n"
    )
    actual = str(test_limited_stock)
    assert actual == expected


def test_show_product_with_promotions(test_product_1):
    test_product_1.promotions.append("Second Half price!")
    expected = (
        "Product                        - 10.0   - 10    \nSecond Half price!"
    )
    actual = str(test_product_1)
    assert actual == expected


def test_show_product_with_multiple_promotions(test_product_1):
    test_product_1.promotions.append("Second Half price!")
    test_product_1.promotions.append("Third One Free!")
    test_product_1.promotions.append("30% off!")
    expected = "Product                        - 10.0   - 10    \nSecond Half price! - Third One Free! - 30% off!"  # noqa E501
    actual = str(test_product_1)
    assert actual == expected


def test_show_product_with_multiple_promotions_order(test_product_1):
    thirty_percent = PercentDiscount("30% off!", percent=30)
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")

    test_product_1.add_promotion(second_half_price)
    test_product_1.add_promotion(third_one_free)
    test_product_1.add_promotion(thirty_percent)
    assert test_product_1.promotions == [
        third_one_free,
        second_half_price,
        thirty_percent,
    ]


# tests for product object with promotions method(s)
def test_promotions_with_product_instance(test_product_1):
    assert test_product_1.promotions == [], "Promotions should be empty"


def test_add_promotion_with_product_instance(
    test_product_1, test_shp_promotion
):
    test_product_1.add_promotion(test_shp_promotion)
    assert test_product_1.promotions == [
        test_shp_promotion
    ], "Promotion should be added"


def test_remove_promotion_with_product_instance(
    test_product_1, test_shp_promotion
):
    test_product_1.add_promotion(test_shp_promotion)
    test_product_1.remove_promotion(test_shp_promotion)
    assert test_product_1.promotions == [], "Promotion should be removed"


def test_add_promotion_invalid_obj(test_product_1):
    with pytest.raises(
        ValueError, match="Promotion must be a valid promotion object"
    ):
        test_product_1.add_promotion(123)


def test_add_promotion_already_applied(
    test_product_1, test_shp_promotion, capfd
):
    test_product_1.add_promotion(test_shp_promotion)
    assert test_product_1.promotions == [
        test_shp_promotion,
    ]
    expected = f"Promotion already applied to {test_product_1.name}\n"
    test_product_1.add_promotion(test_shp_promotion)
    captured = capfd.readouterr()
    assert captured.out == expected


def test_remove_promotion_not_applied(
    test_product_1, test_shp_promotion, capfd
):
    expected = f"Promotion was not applied to {test_product_1.name}\n"
    assert test_product_1.promotions == []
    test_product_1.remove_promotion(test_shp_promotion)
    captured = capfd.readouterr()
    assert captured.out == expected


def test_promotions_is_instance_list(test_product_1):
    with pytest.raises(ValueError, match="Promotions should be a list"):
        test_product_1.promotions = 123


# bonus stuff


def test_product_comparison_greater_than(test_product_1, test_product_2):
    """
    test_product price1 =10, test_product price 2 = 20
    check if price product 1 > product 2"""

    # expected = False
    assert not test_product_1 > test_product_2


def test_product_comparison_less_than(test_product_1, test_product_2):
    """
    test_product price1 =10, test_product price 2 = 20
    check if price product 1 > product 2"""
    # expected = True
    assert test_product_1 < test_product_2
