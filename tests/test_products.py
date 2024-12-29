import pytest

from products import Product, NonStockedProducts, LimitedProducts
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount


@pytest.fixture
def test_product():
    return Product(name="Product", price=10.0, quantity=10)


@pytest.fixture
def test_non_stock_product_instance():
    return NonStockedProducts(name="NonStockProduct", price=10.0)


@pytest.fixture
def test_limited_stock_instance():
    return LimitedProducts(name="LimitedProduct", price=10.0, quantity=10)


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


def test_product_quantity_negative_int(test_product):
    with pytest.raises(
        ValueError, match="Quantity should be a positive integer"
    ):
        test_product.product_quantity = -1


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
def test_get_quantity(test_product):
    assert test_product.product_quantity == 10, "The quantity should be 10"


def test_set_quantity(test_product):
    test_product.product_quantity = 10
    assert test_product.product_quantity == 10, "The quantity should be 10"


# tests for _is_active method getter and setters
def test_is_active(test_product):
    assert test_product.is_active, "The product should be active"


def test_is_active_on_initialise(test_product):
    test_prod = test_product
    assert test_prod._active, "The product should be active"


def test_is_active_setter_bool(test_product):
    with pytest.raises(ValueError, match="Active should be a boolean"):
        test_product.is_active = 123


def test_product_deactivate(test_product):
    assert (
        test_product._active
    ), "The product should be activated on initialise"
    test_product.deactivate()
    assert not test_product._active, "The product should be deactivated"


def test_product_activate(test_product):
    test_product.deactivate()
    assert not test_product._active, "The product should be deactivated"
    test_product.activate()
    assert test_product._active, "The product should be activated"


# tests for ordering product
def test_buy(test_product):
    test_shopping = test_product.buy(5)
    assert test_shopping == 50.0, "The quantity price should be 50.0"
    assert test_product.product_quantity == 5, "The _quantity should be 5"


def test_buy_with_invalid_quantity(test_product):
    with pytest.raises(ValueError, match="Not enough _quantity"):
        test_product.buy(15)
    assert test_product.product_quantity == 10, "The _quantity should be 10"


# tests for show method (updated to implement promotions)
def test_show_with_non_stocked_product(
    test_non_stock_product_instance: NonStockedProducts,
):
    expected = "NonStockProduct                - 10.0   - On Demand\n"
    assert (
        test_non_stock_product_instance.show() == expected
    ), "show message is incorrect"  # noqa: E501


def test_show_with_limited_product_instance(
    test_limited_stock_instance: LimitedProducts,
):
    expected = (
        "LimitedProduct                 - 10.0   - 10    (Max per order:1)\n"
    )
    assert (
        test_limited_stock_instance.show() == expected
    ), "show message is incorrect"  # noqa: E501


def test_show_product_with_promotions(test_product):
    test_product.promotions.append("Second Half price!")
    assert (
        test_product.show()
        == "Product                        - 10.0   - 10    \nSecond Half price!"  # noqa E501
    )


def test_show_product_with_multiple_promotions(test_product):
    test_product.promotions.append("Second Half price!")
    test_product.promotions.append("Third One Free!")
    test_product.promotions.append("30% off!")
    assert (
        test_product.show()
        == "Product                        - 10.0   - 10    \nSecond Half price! - Third One Free! - 30% off!"  # noqa E501
    )


def test_show_product_with_multiple_promotions_order(test_product):
    thirty_percent = PercentDiscount("30% off!", percent=30)
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")

    test_product.add_promotion(second_half_price)
    test_product.add_promotion(third_one_free)
    test_product.add_promotion(thirty_percent)
    assert test_product.promotions == [
        third_one_free,
        second_half_price,
        thirty_percent,
    ]


# tests for product object with promotions method(s)
def test_promotions_with_product_instance(test_product):
    assert test_product.promotions == [], "Promotions should be empty"


def test_add_promotion_with_product_instance(test_product, test_shp_promotion):
    test_product.add_promotion(test_shp_promotion)
    assert test_product.promotions == [
        test_shp_promotion
    ], "Promotion should be added"


def test_remove_promotion_with_product_instance(
    test_product, test_shp_promotion
):
    test_product.add_promotion(test_shp_promotion)
    test_product.remove_promotion(test_shp_promotion)
    assert test_product.promotions == [], "Promotion should be removed"


def test_add_promotion_invalid_obj(test_product):
    with pytest.raises(
        ValueError, match="Promotion must be a valid promotion object"
    ):
        test_product.add_promotion(123)


def test_add_promotion_already_applied(
    test_product, test_shp_promotion, capfd
):
    test_product.add_promotion(test_shp_promotion)
    assert test_product.promotions == [
        test_shp_promotion,
    ]
    expected = f"Promotion already applied to {test_product.name}\n"
    test_product.add_promotion(test_shp_promotion)
    captured = capfd.readouterr()
    assert captured.out == expected


def test_remove_promotion_not_applied(test_product, test_shp_promotion, capfd):
    expected = f"Promotion was not applied to {test_product.name}\n"
    assert test_product.promotions == []
    test_product.remove_promotion(test_shp_promotion)
    captured = capfd.readouterr()
    assert captured.out == expected


def test_promotions_is_instance_list(test_product):
    with pytest.raises(ValueError, match="Promotions should be a list"):
        test_product.promotions = 123
