from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.names = page.get_by_test_id("inventory-item-name")
        self.checkout_button = page.get_by_test_id("checkout")

    def expect_items(self, names: list[str]):
        expect(self.names).to_have_text(names)

    def checkout(self):
        self.checkout_button.click()
