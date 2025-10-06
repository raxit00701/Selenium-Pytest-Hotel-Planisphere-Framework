# runners/run_suite.py
from __future__ import annotations
import sys, os, shlex, shutil, subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml  # already installed per your log

ROOT = Path(__file__).resolve().parents[1]
CFG_PATH = ROOT / "runners" / "suite.yaml"

def load_cfg() -> dict:
    if not CFG_PATH.exists():
        return {
            "browsers": ["chrome", "firefox", "edge"],
            "markers": "",
            "extra_pytest_args": "",
            "tests_path": "src/tests",
        }
    with CFG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def as_list(val) -> list[str]:
    if isinstance(val, str):
        return ["chrome","firefox","edge"] if val.lower() == "all" else [val]
    if isinstance(val, (list, tuple)):
        return [str(x) for x in val]
    return ["chrome","firefox","edge"]

def run_one(browser: str, cfg: dict) -> int:
    tests_path = str(ROOT / cfg.get("tests_path", "src/tests"))
    markers = (cfg.get("markers") or "").strip()
    extra   = (cfg.get("extra_pytest_args") or "").strip()

    # Per-browser output dirs
    res_dir = ROOT / "reports" / "allure-results" / browser
    rep_dir = ROOT / "reports" / "allure-report"  / browser
    art_dir = ROOT / "artifacts"  # shared root; per-test subfolders are lazy

    env = os.environ.copy()
    env["ALLURE_RESULTS_DIR"] = str(res_dir)
    env["ALLURE_REPORT_DIR"]  = str(rep_dir)
    env["ARTIFACTS_DIR"]      = str(art_dir)

    # Ensure results root exists
    (ROOT / "reports" / "allure-results").mkdir(parents=True, exist_ok=True)
    res_dir.mkdir(parents=True, exist_ok=True)

    # IMPORTANT: we now pass --alluredir so JSON is always produced
    cmd = [
        sys.executable, "-m", "pytest",
        tests_path,
        "-n", "1",                               # one session per browser
        f"--browser={browser}",
        "--clean-alluredir",
        "--alluredir", str(res_dir),
    ]
    if markers:
        cmd += ["-m", markers]
    if extra:
        cmd += shlex.split(extra)

    print(f"\n=== Running on {browser} ===")
    print("CMD:", " ".join(shlex.quote(c) for c in cmd))
    rc = subprocess.call(cmd, env=env, cwd=ROOT)
    if rc != 0:
        print(f"[{browser}] pytest exit code: {rc}")

    # Generate per-browser Allure HTML if CLI is available
    allure = shutil.which("allure")
    if allure:
        gen_cmd = [allure, "generate", str(res_dir), "-o", str(rep_dir), "--clean"]
        print("Allure:", " ".join(shlex.quote(c) for c in gen_cmd))
        _ = subprocess.call(gen_cmd, env=env, cwd=ROOT)
    else:
        print(f"[{browser}] Allure CLI not found; skipping HTML generation. (Raw results in {res_dir})")

    return rc

def main() -> int:
    cfg = load_cfg()
    browsers = as_list(cfg.get("browsers", ["chrome","firefox","edge"]))
    browsers = [b.lower() for b in dict.fromkeys(browsers)]

    worst = 0
    with ThreadPoolExecutor(max_workers=len(browsers)) as ex:
        fut = {ex.submit(run_one, b, cfg): b for b in browsers}
        for f in as_completed(fut):
            rc = f.result()
            worst = rc if rc > worst else worst

    print("\nDone. Per-browser reports (if generated): reports/allure-report/<browser>/index.html")
    return worst

if __name__ == "__main__":
    sys.exit(main())
