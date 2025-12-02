import pytest
from hamcrest import assert_that, equal_to
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.mark.selenium
def test_selenium(selenium_browser: WebDriver, config):
    selenium_browser.get(config["base_url"])
    assert "https://saucelabs.com/" in selenium_browser.current_url
    assert_that("https://saucelabs.com/", equal_to(selenium_browser.current_url))
