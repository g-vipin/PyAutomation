import pytest
from hamcrest import assert_that, equal_to

@pytest.mark.playwright
def test_playwright(page, config):
    page.goto(config.base_url, timeout=config.timeout * 1000)
    url = page.url
    assert "https://saucelabs.com/" in url
    assert_that(url, equal_to("https://saucelabs.com/"))
