from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from typing import Tuple

class BasePage:
    def __init__(self, driver: WebDriver, wait : WebDriverWait):
        self.driver = driver
        self.wait = wait

    def find_element(self, locator : Tuple[str, str]) -> WebElement:
        self.wait.until(EC.visibility_of_element_located(locator))
        return self.driver.find_element(locator)

    def find_elements(self, locator : str) -> list[WebElement]:
        self.wait.until(EC.visibility_of_all_elements_located(locator))
        return self.driver.find_elements(locator)     
            