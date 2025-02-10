import json
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium. webdriver.firefox.options import Options as FirefoxOptions

logging.basicConfig(
    filename= "logs/PyAutomation.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(level)s - %(message)s"
    )
logger = logging.getLogger()

@pytest.fixture(scope="session", autouse=True)
def config():
    with open("config/config.json") as file:
        config_data = json.load(file)
    logger.info("Configuration loaded successfully")
    return config_data

@pytest.fixture(scope="function")
def browser(config):
    browser_name: str = config["browser"]
    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        service = ChromeService()
        driver = webdriver.Chrome(options= options, service= service)
    elif browser_name.lower() == "firefox":
        options = FirefoxOptions()
        service = FirefoxService()
        driver = webdriver.Firefox(options=options, service = service)
    else:
        raise ValueError(f"Unsupported browser type {browser_name}") 

    driver.maximize_window()
    driver.implicitly_wait(config["timeout"])
    yield driver
    driver.quit()
    logger.info("Driver closed")
