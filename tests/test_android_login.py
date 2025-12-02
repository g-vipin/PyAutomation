from typing import cast

import pytest
from appium.webdriver.webdriver import WebDriver


@pytest.mark.mobile
def test_android_login(driver: WebDriver):
    driver = cast(WebDriver, driver)
    driver.find_element("accessibility id", "username").send_keys("user")
    driver.find_element("accessibility id", "password").send_keys("pass")
    driver.find_element("accessibility id", "login_button").click()
    assert "dashboard" in driver.page_source
