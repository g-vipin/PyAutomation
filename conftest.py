import json
import pytest
import logging
import os
from Helpers.DriverFactory import DriverFactory as DF

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename= "logs/PyAutomation.txt",
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
    df = DF()
    driver = df.get_Web_driver(browser_name = browser_name)
    driver.maximize_window()
    driver.implicitly_wait(config["timeout"])
    yield driver
    driver.quit()
    logger.info("Driver closed")
