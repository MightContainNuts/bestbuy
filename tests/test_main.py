from ui_helpers import UIHelpers
from main import start, exit
from store import Store
from products import Product

import pytest
from unittest.mock import patch, MagicMock


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
        1: ("Print total _quantity", UIHelpers.print_total_quantity),
        2: ("Print all products", UIHelpers.print_all_products),
        3: ("Start", start),
        4: ("Quit", exit),
    }
    UIHelpers.print_menu(menu)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Menu:\n1: Print total _quantity\n2: Print all products\n3: Start\n4: Quit\n"  # noqa E501
    )


def test_start():
    mock_store = MagicMock()
    mock_store.get_all_products = MagicMock()
    mock_store.get_total_quantity = MagicMock()
    mock_store.make_an_order = MagicMock()

    # Mock input sequence: 1, 2, 4 (Quit)
    with patch("builtins.input", side_effect=["1", "2", "4"]), patch(
        "builtins.exit"
    ):
        with pytest.raises(SystemExit):
            start(mock_store)

    mock_store.get_all_products.assert_called_once()
    mock_store.get_total_quantity.assert_called_once()
    mock_store.make_an_order.assert_not_called()
