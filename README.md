# Selenium-Pytest-Hotel-Planisphere-Framework
A production-grade, batteries-included Selenium + Pytest framework built to run the same test suite across Chrome, Firefox, and Edge with fast warm-ups,Page Object Factory Approach, crisp Allure reports,Jenkins CI/CD integration, per-test artifacts (screenshots, video, logs), CSV-driven data, and a simple “single file = Chrome only, full suite = all browsers” workflow.

Highlights

Multi-browser: Chrome, Firefox, Edge (or a single browser) with a single flag.

Smart default: running one test file automatically uses Chrome only; suites use all.

Speed: session reuse per browser, warm-up navigation (DNS/TLS/cache), optimized driver options.

Allure reporting out of the box:

Grouped by Browser → Module → Class.

Short titles for parametrized tests (test_login · row-3).

Masked sensitive params (passwords/tokens) & truncated long values.

Markers → severity mapping (e.g. @pytest.mark.smoke → critical).

Per-browser HTML & an optional merged report.

Integrated with Jenkins CI/CD

Artifacts:

Per-test folder with screenshot on fail/skip.

Video recording powered by FFmpeg (viewport screenshots for sharp frames).

Buffered logs attached only on fail/skip (no console spam on pass).

CSV data: one-line decorator for table-driven tests.

Parallel: sane defaults for xdist, session reuse, and artifact isolation.

.
├── config/
│   └── config.yaml                 # Global settings (browsers, waits, paths, video, etc.)
├── runners/
│   └── run_suite.py                # Orchestrates per-browser runs and builds merged Allure report
│   └── suite.yaml                  # Optional: suite-level options (browsers, markers, extra args)
├── src/
│   ├── core/
│   │   ├── driver_factory.py       # Builds Chrome/Firefox/Edge with tuned options
│   │   ├── utils.py                # FS helpers, Allure env writer, path builders…
│   │   ├── csv_loader.py           # CSV → rows → test args
│   │   ├── logger.py               # Buffered logging (memory → file on fail/skip)
│   │   ├── video_recorder.py       # FFmpeg-based recorder; uses driver screenshots for frames
│   │   └── allure_helpers.py       # Safe attach, step context, links/labels
│   └── tests/
│       ├── conftest.py             # All fixtures, warm-up, grouping, masking, artifacts & hooks
│       └── test_*.py               # Your tests
└── reports/                        # Allure JSON/HTML output (auto-created)
└── artifacts/                      # Per-test artifacts (auto-created lazily)
Requirements

Python 3.10+ recommended

pip packages (install with your preferred tool):

pytest pytest-xdist allure-pytest selenium pyyaml

Optional: colorlog (prettier console), mss (fallback region capture)

FFmpeg (for video) available on PATH or set in config.yaml

Allure CLI (optional but recommended) for pretty HTML:

Install from Qameta’s releases or via package managers

Noise-free output: urllib3 “connection pool full” warnings are silenced.

Configuration first: everything lives in config/config.yaml, overridable by CLI/env.

Env/CLI overrides

--browser=chrome|firefox|edge|all (CLI beats YAML)

BROWSER or PYTEST_BROWSER (env beats CLI)

--headless, --per-test, --no-video

ALLURE_RESULTS_DIR, ALLURE_REPORT_DIR, ARTIFACTS_DIR (env redirects output)

Drivers & binaries

src/core/driver_factory.py uses Selenium Manager by default (no manual driver setup).
You can force a specific driver/binary via env vars:

Drivers: CHROMEDRIVER, GECKODRIVER, EDGEDRIVER

Browser binaries: CHROME_BINARY, FIREFOX_BINARY, EDGE_BINARY

Useful when running Beta/Dev builds or in offline/locked-down CI.

Warm-up & speed

On session start we ping the base URL quickly (warmup=1), wait for DOM to be interactive, then go about:blank.
This primes DNS/TLS, JIT, caches—so the first test is fast.

Session reuse per browser unless you pass --per-test.

Firefox is tuned (headless, private browsing, big viewport if headless).
See driver_factory.py for flags; if you still need more speed, try:

page_load_strategy: "none" for pure XHR/SPA pages (tests must wait explicitly).

Headless + 1920×1080 viewport.

Disable heavy extensions/telemetry in your local FF profile.
