from playwright.sync_api import Page, expect


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.get_by_test_id("inventory-item")
        self.names = page.get_by_test_id("inventory-item-name")
        self.prices = page.get_by_test_id("inventory-item-price")
        self.sort = page.get_by_test_id("product-sort-container")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")

    def expect_loaded(self):
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html")
        expect(self.items).to_have_count(6)

    def add_to_cart(self, product_slug: str):
        self.page.get_by_test_id(f"add-to-cart-{product_slug}").click()

    def remove_from_cart(self, product_slug: str):
        self.page.get_by_test_id(f"remove-{product_slug}").click()

    def sort_by(self, option_value: str):
        self.sort.select_option(option_value)

    def price_values(self) -> list[float]:
        return [float(t.replace("$", "")) for t in self.prices.all_inner_texts()]

    def name_values(self) -> list[str]:
        return self.names.all_inner_texts()

    def open_cart(self):
        self.cart_link.click()
