import pytest
from products import Product, NonStockedProducts, LimitedProducts


@pytest.fixture
def test_product_instance():
    return Product(name="Product", price=10.0, quantity=10)


@pytest.fixture
def test_non_stock_product_instance():
    return NonStockedProducts(name="NonStockProduct", price=10.0)


@pytest.fixture
def test_limited_stock_instance():
    return LimitedProducts(name="LimitedProduct", price=10.0, quantity=10)


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


def test_is_active(test_product_instance):
    assert test_product_instance.is_active, "The product should be active"


def test_get_quantity(test_product_instance):
    assert (
        test_product_instance.product_quantity == 10
    ), "The quantity should be 10"


def test_set_quantity(test_product_instance):
    test_product_instance.product_quantity = 10
    assert (
        test_product_instance.product_quantity == 10
    ), "The quantity should be 10"


def test_is_active_on_initialise(test_product_instance):
    test_prod = test_product_instance
    assert test_prod._active, "The product should be active"


def test_product_deactivate(test_product_instance):
    assert (
        test_product_instance._active
    ), "The product should be activated on initialise"
    test_product_instance.deactivate()
    assert (
        not test_product_instance._active
    ), "The product should be deactivated"


def test_product_activate(test_product_instance):
    test_product_instance.deactivate()
    assert (
        not test_product_instance._active
    ), "The product should be deactivated"
    test_product_instance.activate()
    assert test_product_instance._active, "The product should be activated"


def test_show_product(test_product_instance):
    assert (
        test_product_instance.show()
        == "Product                        - 10.0   - 10    "
    ), "The product should be Product - Product                        - 10.0   - 10    "  # noqa: E501


def test_buy(test_product_instance):
    test_shopping = test_product_instance.buy(5)
    assert test_shopping == 50.0, "The total price should be 50.0"
    assert (
        test_product_instance.product_quantity == 5
    ), "The _quantity should be 5"


def test_buy_with_invalid_quantity(test_product_instance):
    with pytest.raises(ValueError, match="Not enough _quantity"):
        test_product_instance.buy(15)
    assert (
        test_product_instance.product_quantity == 10
    ), "The _quantity should be 10"


def test_show_with_non_stocked_product(
    test_non_stock_product_instance: NonStockedProducts,
):
    expected = "NonStockProduct                - 10.0   - On Demand"
    assert (
        test_non_stock_product_instance.show() == expected
    ), "show message is incorrect"  # noqa: E501


def test_show_with_limited_product_instance(
    test_limited_stock_instance: LimitedProducts,
):
    expected = (
        "LimitedProduct                 - 10.0   - 10    (Max per order:1)"
    )
    assert (
        test_limited_stock_instance.show() == expected
    ), "show message is incorrect"  # noqa: E501


def test_is_active_setter_bool(test_product_instance):
    with pytest.raises(ValueError, match="Active should be a boolean"):
        test_product_instance.is_active = 123


def test_product_quantity_negative_int(test_product_instance):
    with pytest.raises(
        ValueError, match="Quantity should be a positive integer"
    ):
        test_product_instance.product_quantity = -1
