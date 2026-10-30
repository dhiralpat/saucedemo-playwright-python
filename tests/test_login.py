import re
import pytest
from playwright.sync_api import Page, expect

def test_standard_user_can_log_in(page: Page):
    page.goto("/") # the / in the line means to read the base_url in the .ini. Otherwise, I would need to put the url each time
    page.get_by_test_id("username").fill("standard_user")
    page.get_by_test_id("password").fill("secret_sauce")
    page.get_by_test_id("login-button").click()
    expect(page).to_have_url(re.compile(r"inventory\.html")) # make sure to use \. or else only a . means the test looks for any character at that value! The r before the quotes tells us to not read newline characters and only look at raw string.
    expect(page.locator(".inventory_item")).to_have_count(6)


@pytest.mark.parametrize("username, password, expected_error",
    [
        ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
        ("standard_user", "wrong_password", "Epic sadface: Username and password do not match any user in this service"),
        ("", "secret_sauce", "Epic sadface: Username is required"),
        ("standard_user", "", "Epic sadface: Password is required"),
    ],
    ids=["locked_out", "wrong_password", "empty_username", "empty_password"], #the readable output name of each run instance of the above logins
)

def test_login_errors(page: Page, username, password, expected_error):
    page.goto("/")
    page.get_by_test_id("username").fill(username)
    page.get_by_test_id("password").fill(password)
    page.get_by_test_id("login-button").click()
    expect(page.get_by_test_id("error")).to_contain_text(expected_error)
    expect(page).to_have_url(re.compile(r"saucedemo\.com/$")) # you want this and previous lines checks to make sure the user is informed why they can't login and that they are still on the login page.

def test_logout_returns_to_login(page: Page):
    page.goto("/")
    page.get_by_test_id("username").fill("standard_user")
    page.get_by_test_id("password").fill("secret_sauce")
    page.get_by_test_id("login-button").click()
    expect(page).to_have_url(re.compile(r"inventory\.html"))
    page.get_by_role("button", name="Open Menu", exact=True).click()
    page.get_by_test_id("logout-sidebar-link").click()
    expect(page).to_have_url(re.compile(r"saucedemo\.com/$"))
    expect(page.get_by_test_id("login-button")).to_be_visible()