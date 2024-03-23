# """
# 1. Frontend automation task:

# Using the following URL https://www.saucedemo.com please write an end-to-end test
# for the following flows:
# Using standard_user, select two random items from “PRODUCTS” page, add them to cart
# and proceed to checkout.
# At the “Checkout overview” page, validate that “item  total” price
# is equal to the price of items added on the “PRODUCTS” page.
# Write a test as  well for the locked_out_user.
# """
# import random
# import re
# import time

# import allure
# import pytest
# from assertpy import assert_that
# from attr import define
# from faker import Faker

# from config import settings

# fake = Faker()


# @define
# class CheckoutPage:
#     driver: browser

#     @allure.step
#     def checkout_scroll_postal_code(self):
#         s('#checkout').click()
#         time.sleep(settings.DELAY)
#         fio = fake.name().split()
#         s('#first-name').set_value(fio[0])
#         time.sleep(settings.DELAY)
#         s('#last-name').set_value(fio[1])
#         time.sleep(settings.DELAY)
#         s('#postal-code').set_value(fake.postcode())
#         time.sleep(settings.DELAY)
#         s('#continue').scroll_to().click()

#     @allure.step
#     def summary_subtotal(self):
#         elem = s(
#             '#checkout_summary_container>div>div.summary_info>div.summary_subtotal_label'
#         ).scroll_to()
#         x = re.search(r'^Item total: \$(.+?)$', elem.text).group(1)
#         print(f'{elem.text=}{x=}')
#         return float(x)

#     @allure.step
#     def summary_tax(self):
#         elem = s(
#             '#checkout_summary_container>div>div.summary_info>div.summary_tax_label'
#         ).scroll_to()
#         x = re.search(r'^Tax: \$(.+?)$', elem.text).group(1)
#         print(f'{elem.text=}{x=}')
#         return float(x)

#     @allure.step
#     def summary_total(self):
#         elem = s(
#             '#checkout_summary_container>div>div.summary_info>div.summary_total_label'
#         ).scroll_to()
#         x = re.search(r'^Total: \$(.+?)$', elem.text).group(1)
#         print(f'{elem.text=}{x=}')
#         return float(x)

#     @allure.step
#     def get_prices(self) -> tuple:
#         self.checkout_scroll_postal_code()
#         time.sleep(settings.DELAY)
#         sum_of_prices = self.summary_subtotal()
#         time.sleep(settings.DELAY)
#         tax = self.summary_tax()
#         time.sleep(settings.DELAY)
#         total_price = self.summary_total()
#         time.sleep(settings.DELAY)
#         s('#cancel').click()
#         return sum_of_prices, tax, total_price


# @define
# class ProductsPage:
#     driver: browser

#     @allure.step
#     def reset_app_state(self):
#         s("#react-burger-menu-btn").click()
#         s("#reset_sidebar_link").click()
#         s("#react-burger-cross-btn").click()

#     @allure.step
#     def select_two_random_items(self) -> CheckoutPage:
#         items = ss('#inventory_container>div>div.inventory_item')
#         size = items.size()-1
#         counter = 0
#         while counter < 2:
#             random_item_number = random.randint(0, size)
#             random_item = items[random_item_number].scroll_to()
#             random_item.s(by.text('Add to cart')).scroll_to().click()
#             counter += 1
#         s('#shopping_cart_container>a').scroll_to().click()
#         return CheckoutPage(self.driver)


# @define
# class LoginPage:
#     driver: browser

#     @allure.step
#     def login(self, user, password) -> ProductsPage:
#         self.driver.open_url(settings.GUI_URL)
#         s("#user-name").should(be.blank)
#         s("#user-name").set_value(user).press_enter()
#         s("#password").should(be.blank)
#         s("#password").set_value(password).press_enter()
#         s("#login-button").click()
#         return ProductsPage(self.driver)

#     @allure.step
#     def logout(self):
#         s("#react-burger-menu-btn").click()
#         s("#logout_sidebar_link").click()


# @pytest.mark.gui
# @pytest.mark.component
# class TestSaucedemoGUI:

#     @allure.step
#     def purchase(self, driver, user, password) -> tuple:
#         login_page = LoginPage(driver)
#         time.sleep(settings.DELAY)
#         products_page = login_page.login(user, password)
#         time.sleep(settings.DELAY)
#         products_page.reset_app_state()
#         time.sleep(settings.DELAY)
#         checkout_page = products_page.select_two_random_items()
#         time.sleep(settings.DELAY)
#         result = checkout_page.get_prices()
#         time.sleep(settings.DELAY)
#         login_page.logout()
#         return result

#     @pytest.mark.qa
#     @pytest.mark.test_id("Component-9")
#     def test_standard_user(self, chrome):
#         sum_of_prices, tax, total_price = self.purchase(
#             driver=chrome,
#             user=settings.STANDARD_USER,
#             password=settings.PASSWORD
#         )
#         assert_that(sum_of_prices + tax).is_equal_to(total_price)

#     @pytest.mark.test_id("Component-10")
#     def test_locked_out_user(self, chrome):
#         sum_of_prices, tax, total_price = self.purchase(
#             driver=chrome,
#             user=settings.LOCKED_OUT_USER,
#             password=settings.PASSWORD
#         )
#         assert_that(sum_of_prices + tax).is_equal_to(total_price)
