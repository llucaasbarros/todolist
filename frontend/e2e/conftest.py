import os
from datetime import datetime
from uuid import uuid4

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

SELENIUM_REMOTE_URL = os.environ.get("SELENIUM_REMOTE_URL", "http://localhost:4444/wd/hub")
BASE_URL = os.environ.get("E2E_BASE_URL", "http://frontend/")
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def unique_username():
    return f"seluser_{uuid4().hex[:8]}"


@pytest.fixture
def driver(request):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    # The built frontend bundle calls http://localhost:8000/api (correct for a
    # browser on the host). Inside the selenium container "localhost" is the
    # container itself, so remap it to the backend service on the compose network.
    options.add_argument("--host-resolver-rules=MAP localhost:8000 backend:8000")

    remote_driver = webdriver.Remote(command_executor=SELENIUM_REMOTE_URL, options=options)

    yield remote_driver

    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        filename = os.path.join(
            SCREENSHOTS_DIR, f"{request.node.name}_{datetime.now():%Y%m%d_%H%M%S}.png"
        )
        remote_driver.save_screenshot(filename)

    remote_driver.quit()
