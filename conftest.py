import pytest
import re
from playwright.sync_api import Playwright, expect


@pytest.fixture(scope="session", autouse=True)
def set_test_id_attribute(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")

@pytest.fixture()
def logged_in_page(page: Page) -> page:
    page.goto("/")
    page.get_by_test_id("username").fill("standard_user")
    page.get_by_test_id("password").fill("secret_sauce")
    page.get_by_test_id("login-button").click()
    expect(page).to_have_url(re.compile(r"inventory\.html"))
    return page