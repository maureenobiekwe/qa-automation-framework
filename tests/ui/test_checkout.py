import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_complete_purchase_end_to_end(logged_in, cart_page, checkout_page):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.open_cart()
    cart_page.expect_items(["Sauce Labs Backpack"])
    cart_page.checkout()
    checkout_page.fill_details("Test", "User", "10001")
    checkout_page.finish()
    checkout_page.expect_complete()


@pytest.mark.regression
def test_order_total_is_subtotal_plus_tax(logged_in, cart_page, checkout_page):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.add_to_cart("sauce-labs-onesie")
    logged_in.open_cart()
    cart_page.checkout()
    checkout_page.fill_details("Test", "User", "10001")

    subtotal = checkout_page.amount(checkout_page.subtotal)
    assert subtotal == pytest.approx(29.99 + 7.99)
    assert checkout_page.amount(checkout_page.total) == pytest.approx(
        subtotal + checkout_page.amount(checkout_page.tax)
    )


@pytest.mark.negative
@pytest.mark.parametrize(
    "first, last, postal, message",
    [
        ("", "User", "10001", "First Name is required"),
        ("Test", "", "10001", "Last Name is required"),
        ("Test", "User", "", "Postal Code is required"),
    ],
    ids=["no-first-name", "no-last-name", "no-postal-code"],
)
def test_checkout_requires_all_details(logged_in, cart_page, checkout_page, first, last, postal, message):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.open_cart()
    cart_page.checkout()
    checkout_page.fill_details(first, last, postal)
    expect(checkout_page.error).to_contain_text(message)
