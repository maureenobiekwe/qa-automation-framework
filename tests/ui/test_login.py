import pytest

from pages.login_page import LoginPage
from tests.conftest import PASSWORD


@pytest.mark.smoke
def test_standard_user_can_log_in(login_page, inventory_page):
    login_page.login("standard_user", PASSWORD)
    inventory_page.expect_loaded()


@pytest.mark.negative
def test_locked_out_user_is_rejected(login_page):
    login_page.login("locked_out_user", PASSWORD)
    login_page.expect_error("Sorry, this user has been locked out")


@pytest.mark.negative
@pytest.mark.parametrize(
    "username, password, message",
    [
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("no_such_user", PASSWORD, "Username and password do not match"),
        ("", PASSWORD, "Username is required"),
        ("standard_user", "", "Password is required"),
        ("", "", "Username is required"),
    ],
    ids=["bad-password", "unknown-user", "empty-username", "empty-password", "both-empty"],
)
def test_invalid_login_shows_error(login_page, username, password, message):
    login_page.login(username, password)
    login_page.expect_error(message)


@pytest.mark.negative
def test_inventory_requires_login(page):
    page.goto("https://www.saucedemo.com/inventory.html")
    LoginPage(page).expect_error("when you are logged in")
