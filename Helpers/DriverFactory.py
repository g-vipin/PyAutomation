from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

class DriverFactory:
    def get_Web_driver(self, browser_name: str):
        match browser_name.lower():
            case "chrome":
                options = ChromeOptions()
                service = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(options=options, service=service)
            case "firefox":
                options = FirefoxOptions()
                service = FirefoxService(GeckoDriverManager().install())
                return webdriver.Firefox(options=options, service=service)
            case _:
                raise ValueError(f"Unsupported Browser type {browser_name}")