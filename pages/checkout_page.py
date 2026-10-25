import re

from playwright.sync_api import Page, expect


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.finish_button = page.get_by_test_id("finish")
        self.error = page.get_by_test_id("error")
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.complete_header = page.get_by_test_id("complete-header")

    def fill_details(self, first: str, last: str, postal: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_button.click()

    def finish(self):
        self.finish_button.click()

    def expect_complete(self):
        expect(self.complete_header).to_have_text("Thank you for your order!")

    @staticmethod
    def amount(label) -> float:
        return float(re.search(r"\$([\d.]+)", label.inner_text()).group(1))
