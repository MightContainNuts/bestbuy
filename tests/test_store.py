from store import Store
from products import Product
import pytest
from unittest.mock import patch


@pytest.fixture
def test_store():
    return Store()


@pytest.fixture
def test_product_1():
    return Product("MacBook Air M2", price=1450, quantity=100)


@pytest.fixture
def test_product_2():
    return Product("Bose QuietComfort Earbuds", price=250, quantity=500)


def test_store_instance(test_store):
    assert isinstance(test_store, Store)


def test_store_products(test_store):
    assert test_store.products == []


def test_add_product(test_store, test_product_1):
    assert test_store.products == []
    test_store.add_product(test_product_1)
    assert test_store.products == [test_product_1]


def test_add_product_not_instance(test_store):
    with pytest.raises(
        ValueError, match="Product should be an instance of Product"
    ):
        test_store.add_product("Product")


def test_remove_product(test_store, test_product_1):
    test_store.products = [test_product_1]
    test_store.remove_product(test_product_1)
    assert test_store.products == []


def test_total_quantity(test_store, test_product_1, test_product_2):
    test_store.products = [test_product_1, test_product_2]
    assert test_store.get_total_quantity() == 600


def test_get_all_products(test_store, test_product_1, test_product_2):
    test_store.products = [test_product_1, test_product_2]
    assert test_store.get_all_products() == [test_product_1, test_product_2]


def test_get_all_products_empty(test_store):
    assert test_store.get_all_products() == []


def test_order_empty(test_store):
    assert test_store.order([]) == 0


def test_order(test_store, test_product_1, test_product_2):
    test_store.products = [test_product_1, test_product_2]
    assert test_store.order([(test_product_1, 1), (test_product_2, 2)]) == 1950


def test_order_not_enough_stock(
    test_store, test_product_1, test_product_2, capfd
):
    test_store.products = [test_product_1, test_product_2]
    shopping_list = [(test_product_1, 10), (test_product_2, 600)]
    test_store.order(shopping_list)
    captured = capfd.readouterr()
    assert "Error: Unsufficient qty for" in captured.out
    assert "Available: 500, Requested: 600" in captured.out
    assert "Total: 14500" in captured.out


def test_make_an_order(test_store, test_product_1, test_product_2):
    test_store.products = [test_product_1, test_product_2]
    # shopping_list = [(test_product_1, 1), (test_product_2, 2)]
    with patch("builtins.input", side_effect=["1", "1", "2", "2", ""]):
        shopping_list = test_store.make_an_order()
    assert shopping_list == [(test_product_1, 1), (test_product_2, 2)]


def test_make_an_order_invalid_quantity(
    test_store, test_product_1, test_product_2, capfd
):
    test_store.products = [test_product_1, test_product_2]
    with patch("builtins.input", side_effect=["0", "1"]):
        test_store._validate_prod_qty("message")
        captured = capfd.readouterr()
        assert "Invalid message, please enter a valid number" in captured.out


def test_make_an_order_not_in_store(
    test_store, test_product_1, test_product_2, capfd
):
    test_store.products = [test_product_1, test_product_2]
    with patch("builtins.input", side_effect=["3", "1", "2", ""]):
        test_store.make_an_order()
        captured = capfd.readouterr()
        assert (
            "Invalid product number, please enter a valid number"
            in captured.out
        )
