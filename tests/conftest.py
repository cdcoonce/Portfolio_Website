"""Shared fixtures for the Playwright/pytest E2E suite.

The site is an Astro + React tabbed SPA that builds to ``dist/``. These fixtures
build the site once per session, serve the built output over HTTP, and hand each
test a Playwright page that has finished hydrating.

Set ``E2E_SKIP_BUILD=1`` to serve an already-built ``dist/`` (CI builds once in a
separate step, so it skips the in-fixture rebuild).
"""

import os
import socket
import subprocess
import time
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from helpers import wait_hydrated

REPO = Path(__file__).resolve().parent.parent
DIST = REPO / "dist"


def _free_port() -> int:
    """Reserve an ephemeral loopback port, then release it for the child server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def _wait_until_up(url: str, timeout: float = 30.0) -> None:
    deadline = time.time() + timeout
    last_err: Exception | None = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url) as resp:  # noqa: S310 (loopback only)
                if resp.status == 200:
                    return
        except Exception as err:  # noqa: BLE001 — retry any connection error
            last_err = err
            time.sleep(0.2)
    raise RuntimeError(f"static server never answered {url}: {last_err}")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Build (unless E2E_SKIP_BUILD) and serve dist/ on an ephemeral port."""
    if not os.environ.get("E2E_SKIP_BUILD"):
        subprocess.run(["npm", "run", "build"], cwd=REPO, check=True)
    if not (DIST / "index.html").exists():
        raise RuntimeError(
            "dist/index.html missing — run `npm run build` or unset E2E_SKIP_BUILD"
        )

    port = _free_port()
    proc = subprocess.Popen(
        [
            "python3",
            "-m",
            "http.server",
            str(port),
            "--bind",
            "127.0.0.1",
            "--directory",
            str(DIST),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    url = f"http://127.0.0.1:{port}"
    try:
        _wait_until_up(f"{url}/index.html")
        yield url
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:  # noqa: BLE001
            proc.kill()


@pytest.fixture(scope="session")
def browser():
    """Shared headless Chromium for the session."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(browser, base_url):
    """Fresh, hydrated page on the homepage for each test."""
    page = browser.new_page()
    page.goto(base_url)
    wait_hydrated(page)
    yield page
    page.close()
