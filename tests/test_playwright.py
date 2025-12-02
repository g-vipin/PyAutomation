import pytest
from hamcrest import assert_that, equal_to


@pytest.mark.playwright
@pytest.mark.asyncio
async def test_playwright(page, config):
    await page.goto(config["base_url"], timeout=30000)
    url = await page.url
    assert "https://saucelabs.com/" in url
    assert_that(url, equal_to("https://saucelabs.com/"))
