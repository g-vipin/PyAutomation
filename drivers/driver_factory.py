from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from drivers.mobile_driver_factory import create_android_driver, create_ios_driver, create_windows_driver
from drivers.remote_driver_factory import create_browserstack_driver, create_saucelabs_driver

def create_local_chrome(headless=False):
    opts = ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
    return webdriver.Chrome(options=opts)


def create_local_firefox(headless=False):
    opts = FirefoxOptions()
    if headless:
        opts.add_argument("-headless")
    return webdriver.Firefox(options=opts)


def get_browser_options(browser, headless=False):
    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        return options
    if browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        return options
    raise ValueError(f"Unsupported browser: {browser}")


def create_remote(remote_url, browser, headless=False):
    return webdriver.Remote(command_executor=remote_url, options=get_browser_options(browser, headless=headless))

FACTORY_MAP = {
    "chrome": create_local_chrome,
    "firefox": create_local_firefox,
}

def get_driver(config):
    if config.remote:
        if config.remote_type == "browserstack":
            return create_browserstack_driver(config)
        elif config.remote_type == "saucelabs":
            return create_saucelabs_driver(config)
        elif config.remote_type:
            raise ValueError(f"Unsupported remote type: {config.remote_type}")
        return create_remote(config.remote_url, config.browser, headless=config.headless)
    else:
        if config.platform == "android":
            return create_android_driver(config)
        elif config.platform == "ios":
            return create_ios_driver(config)
        elif config.platform == "windows":
            return create_windows_driver(config)
    factory = FACTORY_MAP.get(config.browser)
    if not factory:
        raise ValueError(f"Unsupported browser: {config.browser}")
    return factory(headless=config.headless)
