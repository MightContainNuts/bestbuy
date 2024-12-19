import pytest
from products import Product


@pytest.fixture
def test_product_instance():
    return Product(name="Product", price=10.0, quantity=10)


def test_validate_name_is_string():
    name = "Product"
    assert Product.validate_name(name), "validate_name should return a string"


def test_validate_name_is_not_empty():
    name = None
    with pytest.raises(
        ValueError, match="Name should be a string and not empty"
    ):
        Product.validate_name(name)


def test_validate_price_is_float():
    price = 10.0
    assert Product.validate_price(
        price
    ), "validate_price should return a float"


def test_validate_price_is_not_empty():
    price = None
    with pytest.raises(ValueError, match="Price should be a positive float"):
        Product.validate_price(price)


def test_validate_price_is_greater_equal_0():
    price = -10.0
    with pytest.raises(ValueError, match="Price should be a positive float"):
        Product.validate_price(price)


def test_validate_quantity_is_int():
    qty = 10
    assert Product.validate_quantity(
        qty
    ), "validate_quantity should return an integer"


def test_validate_quantity_is_greater_equal_0():
    qty = None
    with pytest.raises(
        ValueError, match="Quantity should be a positive integer"
    ):
        Product.validate_quantity(qty)


def test_validate_quantity_is_greater_than_zero():
    qty = -10
    with pytest.raises(
        ValueError, match="Quantity should be a positive integer"
    ):
        Product.validate_quantity(qty)


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


def test_get_quantity(test_product_instance):
    assert (
        test_product_instance.get_quantity() == 10
    ), "The quantity should be 10"


def test_set_quantity(test_product_instance):
    assert (
        test_product_instance.get_quantity() == 10
    ), "The quantity should be 10"


def test_is_active_on_initialise(test_product_instance):
    test_prod = test_product_instance
    assert test_prod.active, "The product should be active"


def test_product_deactivate(test_product_instance):
    assert (
        test_product_instance.active
    ), "The product should be activated on initialise"
    test_product_instance.deactivate()
    assert (
        not test_product_instance.active
    ), "The product should be deactivated"


def test_product_activate(test_product_instance):
    assert (
        test_product_instance.active
    ), "The product should be activated on itialise"
    test_product_instance.deactivate()
    assert (
        not test_product_instance.active
    ), "The product should be deactivated"
    test_product_instance.activate()
    assert test_product_instance.active, "The product should be activated"


def test_show(test_product_instance):
    assert (
        test_product_instance.show() == "Product - 10.0 - 10 - True"
    ), "The product should be Product - 10.0 - 10 - True"


def test_buy(test_product_instance):
    test_buy = test_product_instance.buy(5)
    assert test_buy == 50.0, "The total price should be 50.0"
    assert test_product_instance.quantity == 5, "The quantity should be 5"


def test_buy_with_invalid_quantity(test_product_instance):
    with pytest.raises(ValueError, match="Not enough quantity"):
        test_product_instance.buy(15)
    assert test_product_instance.quantity == 10, "The quantity should be 10"
