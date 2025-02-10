from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium. webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from conftest import config

class DriverFactory:
    def __init__(self):
        pass
    def get_Web_driver(self):
        browser_name: str = config["browser"]
        match browser_name.lower():
            case "chrome":
                options = ChromeOptions()
                service = ChromeService()
                return webdriver.Chrome(options, service, ChromeDriverManager().install())
            case "firefox":
                options = FirefoxOptions()
                service = FirefoxService()
                return webdriver.Firefox(options, service, GeckoDriverManager().install())
            case _: 
                raise ValueError("Unsupprted Browser type {browser_name}",browser_name)
