from appium import webdriver

from core import Config


def create_android_driver(config: Config):
    """Create Android driver using UIAutomator2."""
    capabilities = {
        "platformName": "Android",
        "platformVersion": config.platform_version or "12.0",
        "deviceName": config.device_name or "Android Emulator",
        "automationName": "UiAutomator2",
        "app": config.app_path or "/path/to/app.apk",
        "appWaitActivity": "*",
    }
    return webdriver.Remote(command_executor=config.remote_url, desired_capabilities=capabilities)


def create_ios_driver(config):
    """Create iOS driver using XCUITest."""
    capabilities = {
        "platformName": "iOS",
        "platformVersion": config.platform_version or "16.0",
        "deviceName": config.device_name or "iPhone 14",
        "automationName": "XCUITest",
        "app": config.app_path or "/path/to/app.ipa",
    }
    return webdriver.Remote(command_executor=config.remote_url, desired_capabilities=capabilities)


def create_windows_driver(config):
    """Create Windows app driver."""
    capabilities = {
        "platformName": "Windows",
        "deviceName": "WindowsPC",
        "app": config.app_path or "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
    }
    return webdriver.Remote(command_executor=config.remote_url, desired_capabilities=capabilities)
