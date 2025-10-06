# src/core/driver_factory.py
from __future__ import annotations
from typing import Tuple, Optional
import os
import platform

from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService


def _pls_value(pls: Optional[str]) -> Optional[str]:
    """Normalize page load strategy strings."""
    if not pls:
        return None
    v = pls.strip().lower()
    return v if v in ("normal", "eager", "none") else "normal"


def _maybe_service_with_env(var_name: str, service_cls):
    """
    If the environment variable points to a driver executable, use it.
    Otherwise, return a default Service() so Selenium Manager can resolve the driver.
    """
    path = os.environ.get(var_name)
    if path and os.path.exists(path):
        return service_cls(executable_path=path)
    return service_cls()  # Selenium Manager


# -----------------------------
# Chrome
# -----------------------------
def _chrome(headless: bool, incognito: bool, maximize: bool, pls: str) -> Tuple[webdriver.Chrome, str]:
    opts = ChromeOptions()

    # Optional: use a specific Chrome binary (e.g., Beta/Dev) if provided
    chrome_bin = os.environ.get("CHROME_BINARY")
    if chrome_bin and os.path.exists(chrome_bin):
        opts.binary_location = chrome_bin

    # Headless & window sizing
    if headless:
        opts.add_argument("--headless=new")  # modern headless
        opts.add_argument("--window-size=1920,1080")
        if platform.system() == "Windows":
            opts.add_argument("--disable-gpu")

    if incognito:
        opts.add_argument("--incognito")
    if maximize and not headless:
        opts.add_argument("--start-maximized")

    # Stability / perf
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-background-networking")
    # Reduce log spam on Windows
    try:
        opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    except Exception:
        pass

    pls_val = _pls_value(pls)
    if pls_val:
        opts.set_capability("pageLoadStrategy", pls_val)

    # Prefer Selenium Manager; allow explicit override via CHROMEDRIVER
    service = _maybe_service_with_env("CHROMEDRIVER", ChromeService)
    drv = webdriver.Chrome(service=service, options=opts)

    # Ensure big window when headless+maximize
    if headless and maximize:
        try:
            drv.set_window_size(1920, 1080)
        except Exception:
            pass

    ver = drv.capabilities.get("browserVersion") or drv.capabilities.get("version", "")
    return drv, str(ver)


# -----------------------------
# Firefox (speed tuned)
# -----------------------------
def _firefox(headless: bool, incognito: bool, maximize: bool, pls: str) -> Tuple[webdriver.Firefox, str]:
    opts = FirefoxOptions()

    # Optional: specific Firefox binary (e.g., ESR/Nightly)
    ff_bin = os.environ.get("FIREFOX_BINARY")
    if ff_bin and os.path.exists(ff_bin):
        opts.binary_location = ff_bin

    if headless:
        opts.add_argument("-headless")

    # --- Perf-oriented, test-safe prefs ---
    # Faster startup & blank first page
    opts.set_preference("browser.shell.checkDefaultBrowser", False)
    opts.set_preference("browser.startup.page", 0)                # 0=blank
    opts.set_preference("browser.startup.homepage", "about:blank")
    opts.set_preference("startup.homepage_welcome_url", "about:blank")
    opts.set_preference("startup.homepage_welcome_url.additional", "")

    # Cut features/background work not needed in tests
    opts.set_preference("browser.tabs.warnOnOpen", False)
    opts.set_preference("dom.webnotifications.enabled", False)
    opts.set_preference("dom.push.enabled", False)
    opts.set_preference("media.autoplay.default", 0)              # do not block media
    opts.set_preference("permissions.default.desktop-notification", 2)  # block prompts

    # Reduce update/telemetry overhead (OK for CI/test profiles)
    opts.set_preference("app.update.auto", False)
    opts.set_preference("app.update.enabled", False)
    opts.set_preference("datareporting.healthreport.uploadEnabled", False)
    opts.set_preference("toolkit.telemetry.reportingpolicy.firstRun", False)
    opts.set_preference("toolkit.telemetry.enabled", False)
    opts.set_preference("browser.urlbar.suggest.searches", False)
    opts.set_preference("browser.urlbar.shortcuts.quickactions", False)

    # Keep private mode if requested for clean storage
    if incognito:
        opts.set_preference("browser.privatebrowsing.autostart", True)

    # Keep process/IPC lean (optional; helps consistency in CI)
    # Increase if your AUT truly needs many heavy tabs/iframes.
    opts.set_preference("dom.ipc.processCount", 1)

    # Stable headless viewport sizing via env (some CIs respect these better)
    os.environ.setdefault("MOZ_HEADLESS_WIDTH", "1920")
    os.environ.setdefault("MOZ_HEADLESS_HEIGHT", "1080")

    # Cut geckodriver log spam (minor I/O win, cleaner logs)
    os.environ.setdefault("GECKODRIVER_LOG_LEVEL", "SEVERE")

    # Page load strategy
    pls_val = _pls_value(pls)
    if pls_val:
        opts.set_capability("pageLoadStrategy", pls_val)

    # Prefer Selenium Manager; allow explicit override via GECKODRIVER
    service = _maybe_service_with_env("GECKODRIVER", FirefoxService)
    drv = webdriver.Firefox(service=service, options=opts)

    # Maximize or enforce size in headless
    try:
        if maximize and not headless:
            drv.maximize_window()
        elif headless and maximize:
            drv.set_window_size(1920, 1080)
    except Exception:
        pass

    ver = drv.capabilities.get("browserVersion") or drv.capabilities.get("version", "")
    return drv, str(ver)


# -----------------------------
# Edge (Chromium)
# -----------------------------
def _edge(headless: bool, incognito: bool, maximize: bool, pls: str) -> Tuple[webdriver.Edge, str]:
    opts = EdgeOptions()
    # Some envs don’t expose this attribute; be defensive
    try:
        opts.use_chromium = True
    except Exception:
        pass

    # Optional: specific Edge binary (stable/beta/dev/canary)
    edge_bin = os.environ.get("EDGE_BINARY")
    if edge_bin and os.path.exists(edge_bin):
        opts.binary_location = edge_bin

    if headless:
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
    if incognito:
        opts.add_argument("--inprivate")
    if maximize and not headless:
        opts.add_argument("--start-maximized")

    # Stability / perf (shared Chromium flags)
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-background-networking")

    pls_val = _pls_value(pls)
    if pls_val:
        opts.set_capability("pageLoadStrategy", pls_val)

    # Prefer Selenium Manager; allow explicit override via EDGEDRIVER
    service = _maybe_service_with_env("EDGEDRIVER", EdgeService)
    drv = webdriver.Edge(service=service, options=opts)

    if headless and maximize:
        try:
            drv.set_window_size(1920, 1080)
        except Exception:
            pass

    ver = drv.capabilities.get("browserVersion") or drv.capabilities.get("version", "")
    return drv, str(ver)


# -----------------------------
# Public factory
# -----------------------------
def build_driver(browser: str, headless: bool, incognito: bool, maximize: bool, page_load_strategy: str):
    """
    Factory returning (driver, version) for chrome|firefox|edge.

    Strategy:
      - Use Selenium Manager by default (empty Service()).
      - Allow driver path overrides via CHROMEDRIVER / GECKODRIVER / EDGEDRIVER.
      - Allow binary overrides via CHROME_BINARY / FIREFOX_BINARY / EDGE_BINARY.
      - Headless uses a large viewport for stable screenshots & layout.
    """
    browser = (browser or "chrome").strip().lower()
    if browser in ("chrome", "chromium"):
        return _chrome(headless, incognito, maximize, page_load_strategy)
    if browser in ("ff", "firefox"):
        return _firefox(headless, incognito, maximize, page_load_strategy)
    if browser in ("edge", "msedge", "microsoft-edge"):
        return _edge(headless, incognito, maximize, page_load_strategy)
    raise ValueError(f"Unsupported browser: {browser}")
