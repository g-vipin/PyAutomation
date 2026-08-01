import pytest
from hamcrest import assert_that, equal_to
from selenium.webdriver.remote.webdriver import WebDriver

@pytest.mark.selenium
def test_selenium(driver: WebDriver, config):
    driver.get(config.base_url)
    assert "https://saucelabs.com/" in driver.current_url
    assert_that(driver.current_url, equal_to("https://saucelabs.com/"))
