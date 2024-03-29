"""
1. Frontend automation task:

Using the following URL https://www.saucedemo.com please write an end-to-end test
for the following flows:
Using standard_user, select two random items from “PRODUCTS” page, add them to cart
and proceed to checkout.
At the “Checkout overview” page, validate that “item  total” price
is equal to the price of items added on the “PRODUCTS” page.
Write a test as  well for the locked_out_user.
"""

import random
import re

import allure
import pytest
from assertpy import assert_that
from faker import Faker
from playwright.sync_api import Page, expect

from config import settings

fake = Faker()


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        expect(self.page).to_have_url(re.compile(r".*/cart.html"))

    @allure.step
    def review_your_cart(self):
        button = self.page.locator('[data-test="checkout"]')
        button.scroll_into_view_if_needed()
        button.click()

    @allure.step
    def set_client_info(self):
        expect(self.page).to_have_url(re.compile(r".*/checkout-step-one.html"))
        fio = fake.name().split()
        self.page.locator('[data-test="firstName"]').fill(fio[0])
        self.page.locator('[data-test="lastName"]').fill(fio[1])
        self.page.locator('[data-test="postalCode"]').fill(fake.postcode())
        self.page.locator('[data-test="continue"]').click()

    @allure.step
    def get_value(self, locator: str):
        text = self.page.locator(locator).inner_text()
        string_number = text.split(":")[-1]
        string_number = string_number.replace("$", "")
        return float(string_number)

    @allure.step
    def subtotal(self):
        return self.get_value('[data-test="subtotal-label"]')

    @allure.step
    def tax(self):
        return self.get_value('[data-test="tax-label"]')

    @allure.step
    def total(self):
        return self.get_value('[data-test="total-label"]')

    @allure.step
    def get_prices(self) -> tuple:
        expect(self.page).to_have_url(re.compile(r".*/checkout-step-two.html"))
        sum_of_prices = self.subtotal()
        tax = self.tax()
        total_price = self.total()
        self.page.locator('[data-test="cancel"]').click()
        return sum_of_prices, tax, total_price


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        expect(self.page).to_have_url(re.compile(r".*/inventory.html"))

    @allure.step
    def reset_app_state(self):
        self.page.get_by_role("button", name="Open Menu").click()
        self.page.locator('[data-test="reset-sidebar-link"]').click()
        self.page.get_by_role("button", name="Close Menu").click()

    @allure.step
    def select_random_item(self) -> None:
        inventory = self.page.locator('[data-test="inventory-list"]')
        buttons = inventory.get_by_role("button", name="Add to cart")
        random_number = random.randint(0, buttons.count() - 1)
        button = buttons.nth(random_number)
        button.scroll_into_view_if_needed()
        button.click()

    @allure.step
    def select_random_items(self, amount: int) -> CheckoutPage:
        counter = 0
        while counter < amount:
            self.select_random_item()
            counter += 1
        self.page.locator('[data-test="shopping-cart-link"]').click()
        return CheckoutPage(self.page)


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step
    def navigate(self):
        self.page.goto(settings.GUI_URL)
        expect(self.page).to_have_url(settings.GUI_URL)

    @allure.step
    def login(self, user, password) -> ProductsPage:
        self.navigate()
        self.page.locator('[data-test="username"]').fill(user)
        self.page.locator('[data-test="password"]').fill(password)
        self.page.locator('[data-test="login-button"]').click()
        return ProductsPage(self.page)

    @allure.step
    def logout(self):
        self.page.get_by_role("button", name="Open Menu").click()
        self.page.locator('[data-test="logout-sidebar-link"]').click()


@pytest.mark.gui
@pytest.mark.component
class TestSaucedemoGUI:
    @allure.step
    def purchase(
        self,
        page: Page,
        user: str = settings.STANDARD_USER,
        password: str = settings.PASSWORD,
        amount: int = 2,
    ) -> tuple:
        login = LoginPage(page)
        products = login.login(user, password)
        products.reset_app_state()
        checkout = products.select_random_items(amount)
        checkout.review_your_cart()
        checkout.set_client_info()
        result = checkout.get_prices()
        login.logout()
        return result

    @pytest.mark.testid("Component-9")
    def test_standard_user(self, page: Page):
        sum_, tax, total = self.purchase(page, amount=2)
        assert_that(sum_ + tax).is_close_to(total, 0.0005)

    @pytest.mark.testid("Component-10")
    def test_locked_out_user(self, page: Page):
        sum_, tax, total = self.purchase(page, user=settings.LOCKED_OUT_USER)
        assert_that(sum_ + tax).is_close_to(total, 0.0005)
