# src/core/utils.py
from __future__ import annotations
import os
import re
import shutil
import sys
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict

# ------------- FS helpers -------------

def ensure_dir(p: Path | str) -> Path:
    """Create a directory if missing; return Path."""
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)
    return p

def slugify(s: str, max_len: int = 120) -> str:
    """
    Turn any id/name/test nodeid into a safe file/dir slug.
    Examples:
      "tests/test_signup_csv.py::test_signup[Row 1]" -> "tests_test_signup_csv_py__test_signup_row_1"
    """
    s = s.strip().lower()
    s = s.replace(os.sep, "_").replace("/", "_").replace("\\", "_").replace("::", "__")
    s = re.sub(r"[^a-z0-9._-]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:max_len] if len(s) > max_len else s

def timestamp(fmt: str = "%Y-%m-%d_%H-%M-%S") -> str:
    return datetime.now().strftime(fmt)

def write_text_safely(path: Path | str, content: str, encoding: str = "utf-8") -> None:
    path = Path(path)
    ensure_dir(path.parent)
    path.write_text(content, encoding=encoding)

# ------------- Test artifact paths -------------

def test_artifact_paths(base_dir: Path, nodeid: str, create: bool = False) -> Dict[str, Path]:
    """
    Build deterministic file paths for the given test nodeid.

    NOTE: By default this is LAZY and DOES NOT create directories.
          Pass create=True when you are about to write something.
    """
    test_slug = slugify(nodeid)
    d = Path(base_dir) / test_slug
    if create:
        ensure_dir(d)
    return {
        "dir": d,
        "screenshot": d / f"{test_slug}.png",
        "video": d / f"{test_slug}.mp4",
        "log": d / f"{test_slug}.log",
    }

# ------------- Allure helpers (history/env) -------------

def copy_allure_history(prev_report_dir: Path | str, new_results_dir: Path | str) -> None:
    """
    Copy history/ from the previous Allure HTML report into the new allure-results,
    so the next generated report shows trends over time.
    """
    prev_history = Path(prev_report_dir) / "history"
    dst = Path(new_results_dir) / "history"
    if prev_history.exists():
        ensure_dir(Path(new_results_dir))
        # clean possible stale history in results
        if dst.exists():
            shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(prev_history, dst)

def get_os_info() -> str:
    return f"{platform.system()} {platform.release()} ({platform.machine()})"

def get_python_info() -> str:
    return f"{platform.python_implementation()} {platform.python_version()}"

def write_allure_environment(env_dir: Path | str, env_dict: Dict[str, str]) -> None:
    """
    Create allure environment.properties from dict.
    """
    env_path = Path(env_dir) / "environment.properties"
    ensure_dir(env_path.parent)
    lines = [f"{k}={v}" for k, v in env_dict.items()]
    write_text_safely(env_path, "\n".join(lines) + "\n")

# ------------- Browser info (for environment.properties) -------------

def browser_env_map(browser_name: str, browser_version: str | None = None) -> Dict[str, str]:
    """
    Returns a small map to merge into environment.properties.
    """
    m = {
        "browser": browser_name,
    }
    if browser_version:
        m["browser.version"] = browser_version
    m["os"] = get_os_info()
    m["python"] = get_python_info()
    return m

# ------------- Misc -------------

def is_headless() -> bool:
    """
    Quick check for CI/headless environment (heuristic).
    Actual headless is controlled in config.yaml via execution.headless.
    """
    return bool(os.environ.get("CI", "")) or "pytest" in sys.argv[0].lower()
