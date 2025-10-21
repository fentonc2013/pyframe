# conftest.py
import os
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def _failed(request) -> bool:
    rep = getattr(request.node, "rep_call", None)
    return bool(rep and rep.failed)


BROWSER = os.getenv("BROWSER", "chromium")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
TRACE_ON_FAIL = os.getenv("TRACE_ON_FAIL", "true").lower() == "true"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = getattr(p, BROWSER).launch(headless=HEADLESS)
        yield b
        b.close()


@pytest.fixture
def page(browser, request, tmp_path_factory):
    context = browser.new_context()

    # start tracing up-front if we may want a failure trace
    if TRACE_ON_FAIL:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    yield page

    # save trace only on failure; otherwise discard
    if TRACE_ON_FAIL:
        if _failed(request):
            out_dir = tmp_path_factory.mktemp("traces")
            trace_path = Path(out_dir) / f"{request.node.name}.zip"
            context.tracing.stop(path=str(trace_path))
        else:
            context.tracing.stop()

    context.close()
