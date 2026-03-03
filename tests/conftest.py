import pytest
import subprocess
import time
from playwright.sync_api import sync_playwright


@pytest.fixture(scope='session')
def server():
    """Start a local HTTP server for the static site."""
    proc = subprocess.Popen(
        ['python3', '-m', 'http.server', '8000'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)
    yield 'http://localhost:8000'
    proc.terminate()


@pytest.fixture(scope='session')
def browser():
    """Provide a shared Playwright browser instance."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(browser, server):
    """Provide a fresh page loaded with the site for each test."""
    page = browser.new_page()
    page.goto(server)
    yield page
    page.close()


@pytest.fixture
def projects_page(browser, server):
    """Provide a fresh page loaded with the projects page."""
    page = browser.new_page()
    page.goto(f'{server}/projects.html')
    yield page
    page.close()
