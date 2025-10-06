# src/tests/conftest.py
from __future__ import annotations
import os
import time
import pytest
import yaml
from pathlib import Path
from typing import Dict, Any
import logging, warnings

from src.core.driver_factory import build_driver
from src.core.video_recorder import VideoRecorder
from src.core.logger import get_buffered_logger, materialize_log_to_file, drop_memory_handler
from src.core.utils import (
    ensure_dir, test_artifact_paths, copy_allure_history,
    write_allure_environment, browser_env_map
)
from src.core.csv_loader import read_csv, rows_to_args
from src.core.allure_helpers import attach_file

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _pytest.reports import TestReport

# ---------- Paths & Config ----------
ROOT = Path(__file__).resolve().parents[2]
CFG: Dict[str, Any] = yaml.safe_load((ROOT / "config" / "config.yaml").read_text(encoding="utf-8"))

# Optional: make FFmpeg visible (if provided in config)
_ffmpeg_cfg = (CFG.get("video") or {}).get("ffmpeg_path")
if _ffmpeg_cfg:
    ffdir = str(Path(_ffmpeg_cfg))
    os.environ["FFMPEG_CONFIG_PATH"] = ffdir
    os.environ["PATH"] = ffdir + os.pathsep + os.environ.get("PATH", "")

# Allow runner to override paths per browser via env
ARTIFACTS_ROOT       = Path(os.environ.get("ARTIFACTS_DIR",      CFG["paths"]["artifacts_dir"]))
ALLURE_RESULTS_ROOT  = Path(os.environ.get("ALLURE_RESULTS_DIR", CFG["paths"]["allure_results_dir"]))
ALLURE_REPORT_ROOT   = Path(os.environ.get("ALLURE_REPORT_DIR",  CFG["paths"]["allure_report_dir"]))

# Base dirs may exist; per-test subfolders remain lazy
ARTIFACTS      = ensure_dir(ROOT / ARTIFACTS_ROOT)
ALLURE_RESULTS = ensure_dir(ROOT / ALLURE_RESULTS_ROOT)
ALLURE_REPORT  = ensure_dir(ROOT / ALLURE_REPORT_ROOT)

# --- Silence noisy urllib3 warnings/logs (pool full spam) ---
try:
    from urllib3.exceptions import PoolWarning  # type: ignore
    warnings.filterwarnings("ignore", category=PoolWarning)
except Exception:
    warnings.filterwarnings(
        "ignore",
        message="Connection pool is full, discarding connection",
        category=Warning,
    )
logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)

def pytest_addoption(parser: pytest.Parser):
    # keep default None so we can decide priority ourselves
    parser.addoption("--browser",  action="store",      default=None, help="chrome|firefox|edge|all")
    parser.addoption("--headless", action="store_true", default=CFG["execution"]["headless"], help="Run headless")
    parser.addoption("--no-video", action="store_true", default=False,                         help="Disable video recording")
    parser.addoption("--per-test", action="store_true", default=False,
                     help="Force a fresh browser per test/param (override single-session default)")

def _browsers_from_value(val: str) -> list[str]:
    b = (val or "chrome").strip().lower()
    return ["chrome", "firefox", "edge"] if b == "all" else [b]

def _invoked_single_target(config: pytest.Config) -> bool:
    """True when user invoked pytest with a single file or single node id."""
    try:
        args = list(config.invocation_params.args or [])
    except Exception:
        return False
    fileish = [str(a) for a in args if (".py" in str(a))]
    return len(fileish) == 1

def _resolve_browser_value(config: pytest.Config) -> str:
    """
    Priority:
      1) env BROWSER / PYTEST_BROWSER
      2) CLI --browser
      3) If a single file/node was invoked: execution.default_single_file_browser (default 'chrome')
      4) YAML execution.browser
    """
    env_val = os.environ.get("BROWSER") or os.environ.get("PYTEST_BROWSER")
    if env_val:
        return env_val
    cli_val = config.getoption("--browser")
    if cli_val:
        return cli_val
    if _invoked_single_target(config):
        return str(CFG["execution"].get("default_single_file_browser", "chrome"))
    return str(CFG["execution"].get("browser", "chrome"))

def pytest_generate_tests(metafunc: pytest.Metafunc):
    # per-browser param (session-scoped so each browser gets ONE session)
    if "browser_name" in metafunc.fixturenames:
        val = _resolve_browser_value(metafunc.config)
        browsers = _browsers_from_value(val)
        metafunc.parametrize("browser_name", browsers, ids=browsers, scope="session")

    # CSV parametrization helper
    m = metafunc.definition.get_closest_marker("csv")
    if m:
        cols = m.kwargs.get("cols") or []
        path = m.kwargs.get("path")
        if not path:
            raise RuntimeError("@pytest.mark.csv requires 'path'")
        rows = read_csv(path, has_header=True)
        if "data" in metafunc.fixturenames and not set(cols) - {"data"}:
            metafunc.parametrize("data", rows, ids=[f"row-{i+1}" for i in range(len(rows))])
        else:
            missing = [c for c in cols if c not in metafunc.fixturenames]
            if missing:
                raise RuntimeError(f"CSV columns {missing} are not in test function args {metafunc.fixturenames}")
            arg_tuples = list(rows_to_args(rows, *cols, require_all=True))
            metafunc.parametrize(",".join(cols), arg_tuples, ids=[f"row-{i+1}" for i in range(len(arg_tuples))])

# ---------- Session-level Allure prep ----------
def pytest_sessionstart(session: pytest.Session):
    if CFG["allure"]["enable"] and CFG["allure"]["carry_history"]:
        copy_allure_history(ALLURE_REPORT, ALLURE_RESULTS)

@pytest.fixture(scope="session", autouse=True)
def _allure_env():
    if not CFG["allure"]["enable"] or not CFG["allure"]["write_environment"]:
        yield
        return
    write_allure_environment(ALLURE_RESULTS, {**CFG["allure"].get("extra_env", {})})
    yield

# ---------- Base URL ----------
@pytest.fixture(scope="session")
def base_url() -> str:
    return CFG["base_url"]

# ---------- Allure metadata & grouping (browser → module → class) ----------
@pytest.fixture(autouse=True)
def _allure_metadata(request):
    """
    - Group results by parent_suite(browser) → suite(module) → sub_suite(class)
    - Short, clean titles: "<test_function> · <param-id>" when param'd
    - Mask/truncate params shown in Allure
    - Map pytest markers to Allure severity
    """
    try:
        import allure  # type: ignore
        from allure_commons.types import Severity, ParameterMode  # type: ignore
    except Exception:
        yield
        return

    # ---- Grouping
    browser = request.node.funcargs.get("browser_name", None)
    mod_file = getattr(request.node.module, "__file__", None)
    module_name = Path(mod_file).stem if mod_file else getattr(request.node.module, "__name__", "module")
    if "." in module_name:
        module_name = module_name.split(".")[-1]
    cls = getattr(request.node, "cls", None)
    class_name = getattr(cls, "__name__", "functions")

    try:
        if browser:
            allure.dynamic.parent_suite(browser)
        allure.dynamic.suite(module_name)
        allure.dynamic.sub_suite(class_name)
        allure.dynamic.label("browser", browser or "n/a")
    except Exception:
        pass

    # ---- Short title
    base = getattr(request.node, "originalname", request.node.name)
    param_id = None
    try:
        callspec = getattr(request.node, "callspec", None)
        if callspec:
            param_id = callspec.id  # e.g., "row-1"
    except Exception:
        pass
    short_title = f"{base} · {param_id}" if param_id else base
    try:
        allure.dynamic.title(short_title)
    except Exception:
        pass

    # ---- Parameters (mask sensitive + truncate long)
    def _should_mask(key: str) -> bool:
        k = key.lower()
        return any(t in k for t in ("pass", "pwd", "password", "secret", "token", "key"))

    def _safe_str(v, limit=60) -> str:
        s = str(v)
        return s if len(s) <= limit else (s[:limit - 1] + "…")

    try:
        callspec = getattr(request.node, "callspec", None)
        if callspec:
            for k, v in callspec.params.items():
                if k == "browser_name":
                    continue
                if _should_mask(k):
                    allure.dynamic.parameter(k, "<masked>", mode=ParameterMode.MASKED)
                else:
                    allure.dynamic.parameter(k, _safe_str(v))
    except Exception:
        pass

    # ---- Marker → severity mapping
    try:
        sev_map = {
            "blocker": "blocker",
            "critical": "critical",
            "normal":   "normal",
            "minor":    "minor",
            "trivial":  "trivial",
            # convenience aliases
            "smoke":      "critical",
            "sanity":     "critical",
            "regression": "normal",
        }
        rank = {"blocker":5, "critical":4, "normal":3, "minor":2, "trivial":1}
        chosen = None
        for m in request.node.iter_markers():
            lvl = sev_map.get(m.name.lower())
            if lvl and (chosen is None or rank[lvl] > rank[chosen]):
                chosen = lvl
        if chosen:
            # Allure commons accepts string severity names as well
            allure.dynamic.severity(chosen)  # type: ignore
    except Exception:
        pass

    yield

# ---------- Browser fixtures ----------
@pytest.fixture(scope="session")
def browser_name(request) -> str:
    val = _resolve_browser_value(request.config)
    return _browsers_from_value(val)[0]

@pytest.fixture(scope="session")
def _session_driver_obj(request, browser_name):
    headless  = bool(request.config.getoption("--headless"))
    incognito = bool(CFG["execution"]["incognito"])
    maximize  = bool(CFG["execution"]["maximize"])
    pls       = CFG["execution"]["page_load_strategy"]

    drv, ver = build_driver(browser_name, headless=headless, incognito=incognito, maximize=maximize, page_load_strategy=pls)

    # implicit wait kept small; use explicit waits for real syncs
    try:
        drv.implicitly_wait(int(CFG["execution"].get("implicit_wait_sec", 0)))
    except Exception:
        pass

    try:
        write_allure_environment(ALLURE_RESULTS, browser_env_map(browser_name, ver))
    except Exception:
        pass

    yield drv

    try:
        drv.quit()
    except Exception:
        pass

# Small warm-up so first data-sample is faster (DNS/TLS/cache)
@pytest.fixture(scope="session", autouse=True)
def _warm_up_session(_session_driver_obj, base_url):
    drv = _session_driver_obj
    try:
        drv.get("about:blank")
        warm_url = base_url + ("&" if "?" in base_url else "?") + "warmup=1"
        drv.get(warm_url)
        end = time.time() + 2.0
        while time.time() < end:
            ready = drv.execute_script("return document.readyState")
            if ready in ("interactive", "complete"):
                break
            time.sleep(0.05)
        try:
            WebDriverWait(drv, 1).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except Exception:
            pass
        drv.get("about:blank")
    except Exception:
        pass
    yield

@pytest.fixture
def driver(request, browser_name, _session_driver_obj):
    """
    DEFAULT: reuse the one browser session per browser.
    Opt-out: --per-test for fresh driver per test.
    """
    if not request.config.getoption("--per-test"):
        drv = _session_driver_obj
        _ = WebDriverWait(drv, CFG["execution"]["wait_timeout_sec"])
        yield drv
        return

    headless  = bool(request.config.getoption("--headless"))
    incognito = bool(CFG["execution"]["incognito"])
    maximize  = bool(CFG["execution"]["maximize"])
    pls       = CFG["execution"]["page_load_strategy"]

    drv, ver = build_driver(browser_name, headless=headless, incognito=incognito, maximize=maximize, page_load_strategy=pls)
    try:
        drv.implicitly_wait(int(CFG["execution"].get("implicit_wait_sec", 0)))
    except Exception:
        pass
    _ = WebDriverWait(drv, CFG["execution"]["wait_timeout_sec"])
    try:
        write_allure_environment(ALLURE_RESULTS, browser_env_map(browser_name, ver))
    except Exception:
        pass

    yield drv

    try:
        drv.quit()
    except Exception:
        pass

# ---------- Per-test artifacts: logger & video ----------
@pytest.fixture(autouse=True)
def artifact_paths(request) -> dict[str, Path]:
    return test_artifact_paths(ARTIFACTS, request.node.nodeid, create=False)

@pytest.fixture(autouse=True)
def test_logger(artifact_paths):
    logger, mem = get_buffered_logger("tests")
    return {"logger": logger, "mem": mem, "log_path": artifact_paths["log"]}

# Use browser viewport frames for video (works in headless)
@pytest.fixture(autouse=True)
def video_recorder(request, artifact_paths, driver):
    if request.config.getoption("--no-video") or not CFG["video"]["enable"]:
        yield None
        return

    vr = VideoRecorder(
        outfile=artifact_paths["video"],
        fps=CFG["video"]["fps"],
        region=CFG["video"]["region"]
    )

    try:
        vr.set_screenshot_provider(lambda: driver.get_screenshot_as_png())
    except Exception:
        pass

    try:
        vr.start()
    except Exception:
        vr = None

    yield vr

    try:
        if vr:
            vr.stop()
    except Exception:
        pass

# ---------- Failure/Skip attachments ----------
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep: TestReport = outcome.get_result()

    if rep.when in ("setup", "call") and (rep.failed or rep.skipped):
        setattr(item, "_had_failure", True)

    ap = item.funcargs.get("artifact_paths") or test_artifact_paths(ARTIFACTS, rep.nodeid, create=False)
    tl = item.funcargs.get("test_logger")

    def _rm_empty_dir(p: Path):
        try:
            if p and p.exists() and p.is_dir() and not any(p.iterdir()):
                p.rmdir()
        except Exception:
            pass

    def _attach_log_if_nonempty(log_path: Path):
        try:
            if log_path.exists() and log_path.stat().st_size > 0:
                attach_file(log_path, name="test.log")
            else:
                if log_path.exists():
                    log_path.unlink(missing_ok=True)
        except Exception:
            pass

    if rep.when in ("setup", "call"):
        if rep.failed or rep.skipped:
            ensure_dir(ap["dir"])

            # Screenshot
            drv = item.funcargs.get("driver")
            if drv:
                try:
                    drv.save_screenshot(str(ap["screenshot"]))
                    attach_file(ap["screenshot"], name="screenshot.png")
                except Exception:
                    pass

            # Logging: write an always-present failure/skip summary, then flush buffer to file
            if tl:
                try:
                    logger = tl["logger"]
                    mem    = tl["mem"]
                    status = "FAILED" if rep.failed else "SKIPPED"
                    reason = None
                    try:
                        # longreprtext is best-effort; may be None
                        reason = getattr(rep, "longreprtext", None) or str(getattr(rep, "longrepr", "") or "")
                    except Exception:
                        reason = ""
                    logger.error("%s: %s", status, rep.nodeid)
                    if reason:
                        logger.error("Reason:\n%s", reason)
                    # flush buffered log to disk and keep the file handler
                    materialize_log_to_file(logger, mem, tl["log_path"])
                except Exception:
                    pass
                # attach only if non-empty (and remove if empty)
                _attach_log_if_nonempty(ap["log"])

    elif rep.when == "teardown":
        had_failure = bool(getattr(item, "_had_failure", False))
        if had_failure:
            try:
                if ap["video"].exists():
                    attach_file(ap["video"], name="test.mp4")
            except Exception:
                pass
        else:
            if tl:
                drop_memory_handler(tl["logger"], tl["mem"])
            try:
                if ap["log"].exists() and ap["log"].stat().st_size == 0:
                    ap["log"].unlink(missing_ok=True)
            except Exception:
                pass
            try:
                if ap["video"].exists():
                    ap["video"].unlink(missing_ok=True)
            except Exception:
                pass
            _rm_empty_dir(ap["dir"])
