import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def _options_for(browser, capabilities):
    options = FirefoxOptions() if browser == "firefox" else ChromeOptions()
    for key, value in capabilities.items():
        options.set_capability(key, value)
    return options

def create_browserstack_driver(config):
    """Create a remote WebDriver for BrowserStack."""
    user = os.getenv("BROWSERSTACK_USER") or config.browserstack_user
    key = os.getenv("BROWSERSTACK_KEY") or config.browserstack_key

    capabilities = {
        "browserName": config.browser,
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "Pytest BrowserStack Run",
            "buildName": "Python_Automation_Build_001",
            "userName": user,
            "accessKey": key,
            "debug": True,
            "networkLogs": True,
        },
    }

    return webdriver.Remote(
        command_executor=config.remote_url or "https://hub.browserstack.com/wd/hub",
        options=_options_for(config.browser, capabilities),
    )

def create_saucelabs_driver(config):
    """Create a remote WebDriver for SauceLabs."""
    user = os.getenv("SAUCE_USERNAME")
    key = os.getenv("SAUCE_ACCESS_KEY")

    sauce_options = {
        "build": "Python_Sauce_Run_001",
        "name": "Pytest Run",
        "screenResolution": "1920x1080",
    }

    capabilities = {
        "browserName": config.browser,
        "browserVersion": "latest",
        "platformName": "Windows 11",
        "sauce:options": sauce_options,
    }

    url = f"https://{user}:{key}@ondemand.saucelabs.com:443/wd/hub"
    return webdriver.Remote(command_executor=url, options=_options_for(config.browser, capabilities))
