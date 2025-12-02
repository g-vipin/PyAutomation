from selenium.webdriver.remote.webdriver import WebDriver


def save_screenshot(driver: WebDriver, path):
    driver.save_screenshot(path)
