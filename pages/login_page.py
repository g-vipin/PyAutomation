from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    USER = (By.ID, "username")
    PASS = (By.ID, "password")
    SUBMIT = (By.CSS_SELECTOR, "button[type=submit]")

    def login(self, username, password):
        self.find(self.USER).send_keys(username)
        self.find(self.PASS).send_keys(password)
        self.find(self.SUBMIT).click()
