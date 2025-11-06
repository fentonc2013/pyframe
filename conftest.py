# conftest.py
import os
import pytest
from playwright.sync_api import sync_playwright
from utils.data_loader import get_config


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def config():
    """Load and provide configuration from config.json."""
    return get_config()


@pytest.fixture(scope="session")
def browser():
    """Initialize browser settings from config.json"""
    with sync_playwright() as p:
        browser_type = get_config().get("browser", "chromium")
        headless = get_config().get("headless", True)
        browser = getattr(p, browser_type).launch(headless=headless)
        yield browser
        browser.close()


@pytest.fixture
def page(browser, config, request):
    """New playwright page for each test."""
    base_output = os.path.join(os.getcwd(), "output")
    trace_dir = os.path.join(base_output, "traces")
    screenshot_dir = os.path.join(base_output, "screenshots")

    os.makedirs(trace_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)

    context = browser.new_context()
    page = context.new_page()

    trace_on_fail = config.get("trace_on_fail", True)
    screenshot_on_fail = config.get("screenshot_on_fail", True)

    if trace_on_fail:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    # Handle test failures cleanly
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        test_name = request.node.name.replace("/", "_")

        if trace_on_fail:
            trace_path = f"traces/{test_name}_trace.zip"
            context.tracing.stop(path=trace_path)
            print(f"Saved trace: {trace_path}")

        if screenshot_on_fail:
            screenshot_path = f"screenshots/{test_name}.png"
            page.screenshot(path=screenshot_path)
            print(f"Saved screenshot: {screenshot_path}")
    else:
        if trace_on_fail:
            context.tracing.stop()

    context.close()
