import pytest
from ui_helpers import UIHelpers
from store import Store
from products import Product


@pytest.fixture
def test_store():
    return Store()


@pytest.fixture
def test_product_1():
    return Product("MacBook Air M2", price=1450, quantity=100)


@pytest.fixture
def test_product_2():
    return Product("Bose QuietComfort Earbuds", price=250, quantity=500)


def test_print_total_quantity(
    capsys, test_store, test_product_1, test_product_2
):
    test_store.products = [test_product_1, test_product_2]
    total = test_store.get_total_quantity()
    assert total == 600
    captured = capsys.readouterr()
    assert (
        captured.out
        == "\nQuantity of products in store:\n------------------------------\nTotal quantity: 600\n------------------------------\n\n"  # noqa E501
    )


def test_print_shopping_start(capsys):
    UIHelpers.print_shopping_confirmation_start()
    captured = capsys.readouterr()
    expected_output = (
        "-" * 80
        + "\n"
        + "Product".ljust(30)
        + "Price".center(15)
        + "Qty".center(6)
        + "Sub-quantity".center(10)
        + "\n"
        + "-" * 80
        + "\n"
    )
    assert captured.out == expected_output


def test_print_shopping_end(capsys):
    UIHelpers.print_shopping_confirmation_end()
    captured = capsys.readouterr()
    expected_output = "-" * 80 + "\n"
    assert captured.out == expected_output


def test_print_shopping_confirmation(capsys, test_product_1):
    UIHelpers.print_shopping_confirmation(test_product_1, 1)
    captured = capsys.readouterr()
    expected_output = f"{test_product_1.name:<30}{test_product_1.price:>15.2f}{1:>6}{test_product_1.price * 1:>10.2f}\t\n"  # noqa E501
    assert captured.out == expected_output
