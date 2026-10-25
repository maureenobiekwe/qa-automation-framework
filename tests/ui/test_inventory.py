import pytest
from playwright.sync_api import expect


@pytest.mark.regression
def test_sort_price_low_to_high(logged_in):
    logged_in.sort_by("lohi")
    prices = logged_in.price_values()
    assert prices == sorted(prices)


@pytest.mark.regression
def test_sort_price_high_to_low(logged_in):
    logged_in.sort_by("hilo")
    prices = logged_in.price_values()
    assert prices == sorted(prices, reverse=True)


@pytest.mark.regression
def test_sort_name_z_to_a(logged_in):
    logged_in.sort_by("za")
    names = logged_in.name_values()
    assert names == sorted(names, reverse=True)


@pytest.mark.regression
def test_cart_badge_tracks_adds_and_removes(logged_in):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.add_to_cart("sauce-labs-bike-light")
    expect(logged_in.cart_badge).to_have_text("2")
    logged_in.remove_from_cart("sauce-labs-backpack")
    expect(logged_in.cart_badge).to_have_text("1")
    logged_in.remove_from_cart("sauce-labs-bike-light")
    expect(logged_in.cart_badge).to_have_count(0)
