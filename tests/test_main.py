from main import print_menu, print_total_quantity, print_all_products, start
from store import Store
from products import Product

import pytest


@pytest.fixture
def test_store():
    return Store()


@pytest.fixture
def test_product_1():
    return Product("MacBook Air M2", price=1450, quantity=100)


@pytest.fixture
def test_product_2():
    return Product("Bose QuietComfort Earbuds", price=250, quantity=500)


def test_print_menu(capsys):
    menu = {
        1: ("Print total _quantity", print_total_quantity),
        2: ("Print all products", print_all_products),
        3: ("Start", start),
        4: ("Quit", exit),
    }
    print_menu(menu)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Menu:\n1: Print total _quantity\n2: Print all products\n3: Start\n4: Quit\n"  # noqa E501
    )


def test_print_total_quantity(
    capsys, test_store, test_product_1, test_product_2
):
    test_store.products = [test_product_1, test_product_2]
    print_total_quantity(test_store)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "\nQuantity of products in store:\n------------------------------\nTotal _quantity: 600\n------------------------------\n\n"  # noqa E501
    )
