import pytest
from playwright.async_api import Page,expect

@pytest.mark.playwright
async def test_playwright(page: Page, config):
    await page.goto(config.base_url, timeout=config.timeout * 1000)
    await expect(page).not_to_have_url(config.base_url)