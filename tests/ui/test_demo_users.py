"""Behaviour of SauceDemo's deliberately faulty users.

A test that fails here means the app misbehaves for that user, which is the
point of the demo account. Known defects are marked xfail(strict=True) so the
suite stays green, and so a fix is noticed: an unexpected pass fails the run.
"""
import time

import pytest

from tests.conftest import PASSWORD




@pytest.mark.regression
@pytest.mark.xfail(strict=True, reason="problem_user shows the same image for every product")
def test_problem_user_sees_distinct_product_images(login_page, inventory_page):
    login_page.login("problem_user", PASSWORD)
    inventory_page.expect_loaded()
    sources = inventory_page.page.locator("img.inventory_item_img").evaluate_all(
        "imgs => imgs.map(i => i.getAttribute('src'))"
    )
    assert len(set(sources)) == len(sources)


@pytest.mark.regression
@pytest.mark.xfail(strict=True, reason="problem_user cannot sort products")
def test_problem_user_can_sort_price_low_to_high(login_page, inventory_page):
    login_page.login("problem_user", PASSWORD)
    inventory_page.expect_loaded()
    inventory_page.sort_by("lohi")
    prices = inventory_page.price_values()
    assert prices == sorted(prices)


@pytest.mark.regression
@pytest.mark.performance
def test_performance_glitch_user_logs_in_within_ten_seconds(login_page, inventory_page):
    start = time.perf_counter()
    login_page.login("performance_glitch_user", PASSWORD)
    inventory_page.expect_loaded()
    elapsed = time.perf_counter() - start
    assert elapsed < 10, f"login took {elapsed:.1f}s"
