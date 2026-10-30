import re
from playwright.sync_api import Page, expect

from conftest import logged_in_page

def test_add_cart(logged_in_page: Page):
    page = logged_in_page
    page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    page.get_by_test_id("shopping-cart-link").click()
    expect(page).to_have_url(re.compile(r"cart\.html"))
    expect(page.locator(".cart_item")).to_have_count(1) #checks existence of cart item
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("1") #checks count of items in the cart button badge
    expect(page.get_by_test_id("item-4-title-link")).to_have_text("Sauce Labs Backpack")

def test_add_cart_remove(logged_in_page: Page):
    page = logged_in_page
    page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    page.get_by_test_id("add-to-cart-sauce-labs-bike-light").click()
    page.get_by_test_id("add-to-cart-sauce-labs-bolt-t-shirt").click()
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("3")
    page.get_by_test_id("remove-sauce-labs-bolt-t-shirt").click()
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("2")
    page.get_by_test_id("remove-sauce-labs-backpack").click()
    page.get_by_test_id("remove-sauce-labs-bike-light").click()
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_count(0)

def test_verify_cart(logged_in_page: Page):
    page = logged_in_page
    page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    page.get_by_test_id("add-to-cart-sauce-labs-bike-light").click()
    price_backpack = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack").get_by_test_id("inventory-item-price").inner_text() #store price from inventory page of the backpack
    price_light = page.locator(".inventory_item").filter(has_text="Sauce Labs Bike Light").get_by_test_id("inventory-item-price").inner_text() #store price from inventory page of the light
    page.get_by_test_id("shopping-cart-link").click()

    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("2")
    expect(page).to_have_url(re.compile(r"cart\.html"))
    expect(page.get_by_test_id("item-4-title-link")).to_have_text("Sauce Labs Backpack")
    expect(page.get_by_test_id("item-0-title-link")).to_have_text("Sauce Labs Bike Light")
    card_backpack = page.locator(".cart_item").filter(has_text="Sauce Labs Backpack") #zoom us in on checking price for backpack element in cart
    card_light = page.locator(".cart_item").filter(has_text="Sauce Labs Bike Light") #zoom us in on checking price for light element in cart
    expect(card_backpack.get_by_test_id("inventory-item-price")).to_have_text(price_backpack) #check price of backpack in cart page to the price stored from inventory page
    expect(card_light.get_by_test_id("inventory-item-price")).to_have_text(price_light) #check price of light in cart page to the price stored from inventory page

def test_remove_cart(logged_in_page: Page):
    page = logged_in_page
    expect(page).to_have_url(re.compile(r"inventory\.html"))
    page.get_by_test_id("add-to-cart-sauce-labs-fleece-jacket").click()
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_count(1)
    page.get_by_test_id("shopping-cart-link").click()
    expect(page).to_have_url(re.compile(r"cart\.html"))
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_count(1)
    expect(page.locator(".cart_item")).to_have_count(1)
    page.get_by_test_id("remove-sauce-labs-fleece-jacket").click()
    expect(page.locator(".cart_item")).to_have_count(0)
    expect(page.get_by_test_id("item-5-title-link")).not_to_be_visible()
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_count(0) #double check the cart badge disappears