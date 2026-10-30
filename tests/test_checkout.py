import re

import pytest
from playwright.sync_api import Page, expect

def go_to_checkout(logged_in_page: Page):
    page = logged_in_page
    page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    page.get_by_test_id("add-to-cart-sauce-labs-bike-light").click()
    page.get_by_test_id("shopping-cart-link").click()
    expect(page).to_have_url(re.compile(r"cart\.html"))
    page.get_by_test_id("checkout").click()
    expect(page).to_have_url(re.compile(r"checkout-step-one.html"))
    expect(page.get_by_test_id("firstName")).to_be_visible()

def test_checkout_happy(logged_in_page: Page):
    go_to_checkout(logged_in_page)
    page = logged_in_page
    page.get_by_test_id("firstName").fill("Fake")
    page.get_by_test_id("lastName").fill("Name")
    page.get_by_test_id("postalCode").fill("14680")
    page.get_by_test_id("continue").click()
    expect(page).to_have_url(re.compile(r"checkout-step-two.html"))
    expect(page.get_by_test_id("payment-info-label")).to_have_text("Payment Information:")
    page.get_by_test_id("finish").click()
    expect(page).to_have_url(re.compile(r"checkout-complete.html"))
    expect(page.get_by_test_id("complete-header")).to_have_text("Thank you for your order!")

@pytest.mark.parametrize("firstname, lastname, postalcode, expected_error",
    [
        ("", "2ndName", "12345", "Error: First Name is required"),
        ("1stName", "", "12345", "Error: Last Name is required"),
        ("1stName", "2ndName", "", "Error: Postal Code is required"),
    ],
    ids=["missing first name", "missing last name", "missing postal code"],
)

def test_missing_fields(logged_in_page: Page, firstname, lastname, postalcode, expected_error):
    go_to_checkout(logged_in_page)
    page = logged_in_page
    page.get_by_test_id("firstName").fill(firstname)
    page.get_by_test_id("lastName").fill(lastname)
    page.get_by_test_id("postalCode").fill(postalcode)
    page.get_by_test_id("continue").click()
    expect(page).to_have_url(re.compile(r"checkout-step-one.html"))
    expect(page.get_by_test_id("firstName")).to_be_visible()
    expect(page.get_by_test_id("error")).to_have_text(expected_error)

def test_cancel_checkout(logged_in_page: Page):
    go_to_checkout(logged_in_page)
    page = logged_in_page
    page.get_by_role("button", name="Cancel", exact=True).click()
    expect(page).to_have_url(re.compile(r"cart\.html"))
    expect(page.get_by_test_id("cart-desc-label")).to_be_visible()
    expect(page.locator(".cart_item")).to_have_count(2)

def test_checkout_total(page: Page):
    page.goto("/")
    page.get_by_test_id("username").fill("standard_user")
    page.get_by_test_id("password").fill("secret_sauce")
    page.get_by_test_id("login-button").click()
    expect(page).to_have_url(re.compile(r"inventory\.html"))

    page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    price_backpack = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack").get_by_test_id("inventory-item-price").inner_text()
    price_backpack_float = round(float(price_backpack.split("$")[1]),2)

    page.get_by_test_id("add-to-cart-sauce-labs-bike-light").click()
    price_light = page.locator(".inventory_item").filter(has_text="Sauce Labs Bike Light").get_by_test_id("inventory-item-price").inner_text()
    price_light_float = round(float(price_light.split("$")[1]),2)

    page.get_by_test_id("shopping-cart-link").click()
    expect(page).to_have_url(re.compile(r"cart\.html"))
    expect(page.locator(".cart_item")).to_have_count(2)

    page.get_by_test_id("checkout").click()
    expect(page).to_have_url(re.compile(r"checkout-step-one\.html"))

    page.get_by_test_id("firstName").fill("Fake")
    page.get_by_test_id("lastName").fill("Name")
    page.get_by_test_id("postalCode").fill("14680")

    page.get_by_test_id("continue").click()
    expect(page).to_have_url(re.compile(r"checkout-step-two\.html"))
    expect(page.get_by_test_id("payment-info-label")).to_have_text("Payment Information:")

    price_total = page.get_by_test_id("subtotal-label").inner_text()
    price_total_float = round(float(price_total.split("$")[1]),2)

    if round(price_backpack_float + price_light_float,2) == round(price_total_float,2):
        tax = round(float(page.get_by_test_id("tax-label").inner_text().split("$")[1]),2)
        total = round(float(page.get_by_test_id("total-label").inner_text().split("$")[1]),2)
        assert round(price_total_float + tax,2) == total
        page.get_by_test_id("finish").click()
        expect(page).to_have_url(re.compile(r"checkout-complete\.html"))

    else:
        pytest.fail("total of inventory items does not match subtotal or total on page does not add up with tax accurately")