import json
import os
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, Page

# Load config JSON from the 'data' directory
CONFIG_PATH = Path(__file__).resolve().parent / "data" / "config.json"
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)


@pytest.fixture(scope="session")
def browser():
    browser_type = CONFIG.get("browser", "chromium")
    headless_mode = CONFIG.get("headless", True)

    with sync_playwright() as p:
        try:
            browser = getattr(p, browser_type).launch(headless=headless_mode)
        except AttributeError:
            raise ValueError(f"Browser type '{browser_type}' is not supported.")
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
