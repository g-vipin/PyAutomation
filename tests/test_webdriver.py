from selenium.webdriver.remote.webdriver import WebDriver
from hamcrest import assert_that, equal_to

def test_example(browser: WebDriver, config):
    browser.get(config["base_url"])
    assert "https://saucelabs.com/" in browser.current_url
    assert_that("https://saucelabs.com/", equal_to(browser.current_url))