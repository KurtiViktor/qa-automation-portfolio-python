"""
pytest fixtures offer dramatic improvements
over the classic xUnit style of setup/teardown functions
"""

import pytest
from selene import browser
from selenium import webdriver


@pytest.fixture
def chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--enable-automation")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    browser.set_driver(driver)
    browser.timeout = 2
    yield browser
    browser.close()
