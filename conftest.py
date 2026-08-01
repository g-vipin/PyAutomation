import os
import allure
import pytest
from config.config import Config
from drivers.driver_factory import get_driver
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger("conftest")

def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--env", action="store", default=os.getenv("TEST_ENV", "default"))

@pytest.fixture(scope="session")
def config(request: pytest.FixtureRequest):
    env = request.config.getoption("--env")
    return Config(env)

@pytest.fixture(scope="session")
def base_url(config):
    return config.base_url

@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest, config):
    drv = get_driver(config)
    logger.info("Starting driver")
    try:
        yield drv
    finally:
        rep_call = getattr(request.node, "rep_call", None)

        if rep_call and getattr(rep_call, "failed", False):
            try:
                png = drv.get_screenshot_as_png()
                allure.attach(png, name="screenshot", attachment_type=allure.attachment_type.PNG)
            except Exception:
                logger.exception("Failed to capture screenshot")

        drv.quit()

@pytest.fixture
def login_page(driver, base_url):
    return LoginPage(driver, base_url)

@pytest.fixture(scope="function")
def ssh_client(config):
    pytest.importorskip("paramiko", reason="Install paramiko to run external SSH service tests.")
    from services.ssh_client import SSHClient
    client = SSHClient(host=config.ssh_host, username=config.ssh_user, password=config.ssh_password)
    yield client
    client.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

# def pytest_sessionstart(session):
#     print("\nRunning code quality checks...")
#     black_result = subprocess.run(["black", "--check", "."], capture_output=True, text=True)
#     flake8_result = subprocess.run(["flake8", "."], capture_output=True, text=True)
#     if black_result.returncode != 0 or flake8_result.returncode != 0:
#         pytest.exit("Linting failed. Fix issues before running tests.")
