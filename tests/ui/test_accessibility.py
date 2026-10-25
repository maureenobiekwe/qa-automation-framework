"""Automated WCAG 2.1 AA checks with axe-core plus a keyboard-only login.

Automated tools catch roughly a third of accessibility issues, so these tests
complement, not replace, manual screen-reader checks.
"""
import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import expect

WCAG_AA = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]

pytestmark = pytest.mark.a11y


def violations(page):
    result = Axe().run(page, options={"runOnly": {"type": "tag", "values": WCAG_AA}})
    return result.response["violations"]


def describe(found) -> str:
    return "; ".join(f"{v['id']} ({v['impact']}, {len(v['nodes'])} nodes)" for v in found)


def test_login_page_has_no_wcag_aa_violations(login_page):
    found = violations(login_page.page)
    assert not found, describe(found)


def test_inventory_page_has_no_wcag_aa_violations(logged_in):
    found = violations(logged_in.page)
    assert not found, describe(found)


def test_login_works_with_keyboard_only(login_page, inventory_page):
    page = login_page.page
    login_page.username.focus()
    page.keyboard.type("standard_user")
    page.keyboard.press("Tab")
    page.keyboard.type("secret_sauce")
    page.keyboard.press("Enter")
    inventory_page.expect_loaded()


@pytest.mark.xfail(
    strict=True,
    reason="Defect: username field shows no focus indicator (WCAG 2.4.7 Focus Visible)",
)
def test_login_fields_have_a_visible_focus_state(login_page):
    login_page.username.focus()
    expect(login_page.username).to_be_focused()
    outline = login_page.username.evaluate(
        "el => getComputedStyle(el).outlineStyle + '|' + getComputedStyle(el).boxShadow"
    )
    assert outline != "none|none", "focused field shows no outline or shadow"
