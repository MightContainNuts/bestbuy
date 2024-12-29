import pytest

from products import Product, NonStockedProducts, LimitedProducts
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount
from store import Store


@pytest.fixture
def test_store():
    return Store()


@pytest.fixture
def test_product_1():
    return Product("MacBook Air M2", price=1450, quantity=100)


@pytest.fixture
def test_product_2():
    return Product("Bose QuietComfort Earbuds", price=250, quantity=500)


@pytest.fixture
def test_non_stock_product():
    return NonStockedProducts(name="NonStockProduct", price=10.0)


@pytest.fixture
def test_limited_stock_product():
    return LimitedProducts(name="LimitedProduct", price=10.0, quantity=10)


@pytest.fixture
def test_promotion_shp(test_product_1):
    return SecondHalfPrice("Second Half Price!")


@pytest.fixture
def test_promotion_tif(test_product_1):
    return ThirdOneFree("Third One Free!")


@pytest.fixture
def test_promotion_pd(test_product_1):
    discount = 30
    return PercentDiscount("30% off!", discount)


def test_store_instance(test_store):
    assert isinstance(test_store, Store)


# test for instance
def test_store_products(test_store):
    assert test_store.products == []


# tests for add_product, remove product.
# TODO might need updating if the methods change to getter, setter
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


# tests for quantity getter, setter
def test_total_quantity(test_store, test_product_1, test_product_2):
    test_store.products = [test_product_1, test_product_2]
    assert test_store.get_total_quantity() == 600


# tests for get all products
def test_get_all_products(test_store, test_product_1, test_product_2):
    test_store.products = [test_product_1, test_product_2]
    assert test_store.get_all_products() == [test_product_1, test_product_2]


def test_get_all_products_empty(test_store):
    assert test_store.get_all_products() == []


# tests for order process
def test_order_empty(test_store):
    assert test_store._order([]) == 0


def test__find_product_return_none(test_store, test_product_1, test_product_2):
    test_store.add_product(test_product_1)
    assert not test_store._find_product(test_product_2)


# tests for applying promotions to shoppping basket
def test_calc_subtotal_stocked_product(test_store, test_product_1):
    basket_quantity = 1
    subtotal = test_store._calc_subtotal_stocked_product(
        test_product_1, basket_quantity
    )
    assert subtotal == 1450


def test_calc_subtotal_with_stocked_product_not_enough_stock(
    test_store, test_product_1, capfd
):
    basket_quantity = 101
    test_store._calc_subtotal_stocked_product(test_product_1, basket_quantity)
    captured = capfd.readouterr()
    expected = "Error: Unsufficient qty for MacBook Air M2. Available: 100, Requested: 101\n"  # noqa E501
    assert captured.out == expected


def test_calc_subtotal_limited_stock(test_store, test_limited_stock_product):
    basket_quantity = 1
    expected_subtotal = basket_quantity * test_limited_stock_product.price
    subtotal = test_store._calc_subtotal_limited_product(
        test_limited_stock_product, basket_quantity
    )
    assert subtotal == expected_subtotal


def test_calc_subtotal_limited_stock_invalid(
    test_store, test_limited_stock_product
):
    basket_quantity = 2
    with pytest.raises(ValueError):
        test_store._calc_subtotal_limited_product(
            test_limited_stock_product, basket_quantity
        )


def test_calc_non_stocked_product(test_store, test_non_stock_product):
    basket_quantity = 2
    expected_subtotal = basket_quantity * test_non_stock_product.price
    subtotal = test_store._calc_subtotal_non_stocked_product(
        test_non_stock_product, basket_quantity
    )
    assert subtotal == expected_subtotal


def test__calc_any_promotions_shp(
    test_promotion_shp, test_store, test_product_1
):
    test_store.add_product(test_product_1)
    test_product_1.add_promotion(test_promotion_shp)
    basket_quantity = 10
    current_subtotal = basket_quantity * test_product_1.price

    result = test_store._calc_any_promotions(
        test_product_1,
        current_subtotal=current_subtotal,
        basket_quantity=basket_quantity,
    )
    assert result == round(
        test_product_1.price * 5 + test_product_1.price / 2 * 5, 2
    )


def test__calc_any_promotions_multiple(
    test_promotion_shp,
    test_promotion_pd,
    test_promotion_tif,
    test_product_1,
    test_store,
):
    test_store.add_product(test_product_1)
    test_product_1.add_promotion(test_promotion_tif)
    test_product_1.add_promotion(test_promotion_shp)
    test_product_1.add_promotion(test_promotion_pd)

    assert test_product_1.promotions == [
        test_promotion_tif,
        test_promotion_shp,
        test_promotion_pd,
    ]
    basket_quantity = 10
    current_subtotal = basket_quantity * test_product_1.price

    result = test_store._calc_any_promotions(
        test_product_1,
        current_subtotal=current_subtotal,
        basket_quantity=basket_quantity,
    )
    print(result)
    # math for calculating tif
    print(f"Current subtotal: {current_subtotal}")
    free_items = basket_quantity // 3
    full_price_items = basket_quantity - free_items
    res_tif = round(current_subtotal * full_price_items / basket_quantity, 2)
    print(f"result tif: {res_tif}")  # 10150
    # math for shp
    price_per_item = res_tif / basket_quantity
    discounted_items = basket_quantity // 2
    full_price_items = basket_quantity - discounted_items
    full_price_total = full_price_items * price_per_item
    discounted_total = discounted_items * price_per_item / 2
    res_shp = round(
        full_price_total + discounted_total,
        2,
    )
    # math for 30%
    res_30 = res_shp * (1 - 0.3)
    print(
        f"Subtotal: {current_subtotal}, after tif: {res_tif} after shp {res_shp} after 30%: {res_30}"  # noqa E501
    )  # 5328.75
    assert result == 5328.75
