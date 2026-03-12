# 🏨 Hotel Planisphere — Selenium Test Automation Framework

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%20%7C%203.14-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Selenium-4.41.0-43B02A?logo=selenium&logoColor=white" />
  <img src="https://img.shields.io/badge/Pytest-8.3.2-0A9EDC?logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/Allure-2.x-orange?logo=qameta&logoColor=white" />
  <img src="https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins&logoColor=white" />
  <img src="https://img.shields.io/badge/Browsers-Chrome%20%7C%20Firefox%20%7C%20Edge-4285F4?logo=googlechrome&logoColor=white" />
</p>

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [Tech Stack](#-tech-stack)
4. [Project Structure](#-project-structure)
5. [Prerequisites & Installation](#-prerequisites--installation)
6. [Configuration](#-configuration)
7. [Test Data (CSV-Driven)](#-test-data-csv-driven)
8. [Running Tests](#-running-tests)
9. [Browser Support](#-browser-support)
10. [Environment Support](#-environment-support)
11. [Headless & Headed Mode](#-headless--headed-mode)
12. [Jenkins CI/CD Integration](#-jenkins-cicd-integration)
13. [Allure Reporting](#-allure-reporting)
14. [Video Recording & Screenshots](#-video-recording--screenshots)
15. [Logging](#-logging)
16. [Page Object Model (POM)](#-page-object-model-pom)
17. [Test Suites & Parallel Execution](#-test-suites--parallel-execution)
18. [Artifacts](#-artifacts)
19. [Contributing](#-contributing)

---

## 🔍 Project Overview

**Hotel Planisphere** is a production-grade, end-to-end Selenium test automation framework built with Python and Pytest, targeting the [Hotel Planisphere](https://hotel.testplanisphere.dev/) web application.

The framework tests three critical user journeys:

| Test Module | Coverage |
|---|---|
| `test_signup.py` | New user registration flow (5 data rows) |
| `test_login.py` | User authentication — valid & invalid scenarios (4 data rows) |
| `test_reserve.py` | Hotel room reservation workflow (2 data rows) |

It is designed for **enterprise-grade CI/CD pipelines**, supporting multi-browser execution, environment-specific configurations, dynamic Allure reports with rich media attachments, and fully data-driven test execution via CSV files.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🌐 **Multi-Browser** | Runs on Chrome, Firefox, and Edge with a single config change |
| 🌍 **Multi-Environment** | Supports `test`, `preprod`, and `prod` environments dynamically |
| 👁️ **Headless / Headed Mode** | Toggle UI visibility via configuration — no code changes needed |
| 🔁 **Data-Driven Testing** | CSV-powered parametrization for all test modules |
| 📊 **Allure Reports** | Rich HTML reports with environment info, history trends, and test timelines |
| 🎥 **Video Recording** | Automatic MP4 capture for failed (and optionally all) test cases |
| 📸 **Screenshots** | Auto-attached to Allure on test failure |
| 📝 **Structured Logging** | Per-test log files captured and attached to Allure report |
| ⚙️ **Jenkins CI/CD** | Full pipeline integration with parameterized builds |
| 🔀 **Parallel Execution** | Multi-worker test execution via `pytest-xdist` |
| 🔄 **Auto-Retry** | Flaky test retry support via `pytest-rerunfailures` |
| ⏱️ **Timeout Control** | Global and per-test timeouts via `pytest-timeout` |
| 📋 **Test Ordering** | Deterministic test ordering via `pytest-order` |
| 🏗️ **POM Architecture** | Clean Page Object Model for maintainability |

---

## 🛠 Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.12 / 3.14 |
| Browser Automation | Selenium WebDriver | 4.41.0 |
| Test Framework | Pytest | 8.3.2 |
| Driver Management | WebDriver Manager | 4.0.2 |
| Report Generation | Allure (pytest-allure) | 2.x |
| Parallel Execution | pytest-xdist | 3.6.1 |
| Retry Logic | pytest-rerunfailures | 14.0 |
| Test Ordering | pytest-order | 1.3.0 |
| Timeout Control | pytest-timeout | 2.4.0 |
| HTML Reports | pytest-html | 4.1.1 |
| Test Metadata | pytest-metadata | 3.1.1 |
| Video Recording | mss + imageio | latest |
| Config Parsing | PyYAML | 6.0.2 |
| Data Parsing | Python csv (built-in) | — |
| HTTP Client | Requests | 2.32.5 |
| Async Support | Trio | 0.31.0 |
| Env Variables | python-dotenv | 1.1.1 |
| CI/CD | Jenkins | — |

---

## 📁 Project Structure

```
hotel_selenium/
│
├── config/
│   └── config.yaml                  # Master config: base URL, browser, env, headless flag
│
├── data/
│   ├── login.csv                    # Login test data (valid/invalid credentials)
│   ├── signup.csv                   # Signup test data (5 user registration rows)
│   ├── reserve.csv                  # Reservation test data
│   └── reservation.csv              # Extended reservation data
│
├── runners/
│   ├── run_suite.py                 # Python entry point to trigger test suites
│   └── suite.yaml                  # Suite definition file (order, markers, browser, env)
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/                        # Framework core utilities
│   │   ├── allure_helpers.py        # Allure attachment utilities (screenshot, log, video)
│   │   ├── csv_loader.py            # CSV reader for data-driven parametrization
│   │   ├── driver_factory.py        # WebDriver factory (Chrome/Firefox/Edge, headless toggle)
│   │   ├── logger.py                # Structured logger setup (per-test log files)
│   │   ├── utils.py                 # Shared utility functions
│   │   ├── video_recorder.py        # Screen capture & MP4 export using mss/imageio
│   │   └── __init__.py
│   │
│   ├── pages/                       # Page Object Model layer
│   │   ├── Homepage.py              # POM class for all page interactions
│   │   └── __init__.py
│   │
│   └── tests/                       # Test modules
│       ├── conftest.py              # Pytest fixtures (driver setup, teardown, Allure hooks)
│       ├── test_login.py            # Login test cases (4 CSV rows)
│       ├── test_signup.py           # Signup test cases (5 CSV rows)
│       ├── test_reserve.py          # Reservation test cases (2 CSV rows)
│       └── __init__.py
│
├── artifacts/                        # Test run artifacts (auto-generated)
│   └── <test_id>/
│       └── *.mp4                    # Video recordings per failed test
│
├── reports/
│   ├── allure-results/              # Raw Allure result JSONs (per browser)
│   │   ├── chrome/
│   │   ├── edge/
│   │   ├── firefox/
│   │   └── merged/
│   │
│   └── allure-report/               # Generated HTML Allure reports
│       ├── chrome/
│       ├── edge/
│       ├── firefox/
│       └── merged/                  # Cross-browser merged report
│
└── .venv/                           # Virtual environment (Python packages)
    └── Lib/site-packages/           # All installed dependencies
```

---

## ⚙️ Prerequisites & Installation

### System Requirements

- Python **3.12+** or **3.14+**
- Java **8+** (required for Allure CLI)
- Node.js (optional, for local Allure server)
- Git
- Jenkins (for CI/CD — see [Jenkins section](#-jenkins-cicd-integration))

### Browser Requirements

| Browser | Driver | Auto-managed? |
|---|---|---|
| Google Chrome | ChromeDriver | ✅ Yes (webdriver-manager) |
| Mozilla Firefox | GeckoDriver | ✅ Yes (webdriver-manager) |
| Microsoft Edge | EdgeDriver | ✅ Yes (webdriver-manager) |

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/hotel_selenium.git
cd hotel_selenium
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

- **Windows (cmd):** `.venv\Scripts\activate.bat`
- **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
- **macOS/Linux:** `source .venv/bin/activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> If you don't have a `requirements.txt`, install key packages directly:

```bash
pip install selenium==4.41.0 pytest==8.3.2 allure-pytest webdriver-manager \
            pytest-xdist pytest-rerunfailures pytest-order pytest-timeout \
            pytest-html pytest-metadata pyyaml python-dotenv requests mss imageio
```

### 4. Install Allure CLI

**macOS (Homebrew):**
```bash
brew install allure
```

**Windows (Scoop):**
```bash
scoop install allure
```

**Manual:** Download from [Allure GitHub Releases](https://github.com/allure-framework/allure2/releases) and add to PATH.

---

## 🔧 Configuration

All framework-level settings live in `config/config.yaml`:

```yaml
# config/config.yaml

base_url: "https://hotel.testplanisphere.dev"

browser: "chrome"           # Options: chrome | firefox | edge
environment: "test"         # Options: test | preprod | prod
headless: false             # true = headless mode, false = headed mode

implicit_wait: 10           # Implicit wait in seconds
page_load_timeout: 30       # Page load timeout in seconds

video_on_failure: true      # Record video only on failure
screenshot_on_failure: true # Capture screenshot on failure
log_level: "INFO"           # Logging level: DEBUG | INFO | WARNING | ERROR
```

### Environment-Specific URLs

The `driver_factory.py` and conftest resolve URLs based on the `environment` key:

| Environment | Base URL |
|---|---|
| `test` | `https://hotel.testplanisphere.dev` |
| `preprod` | Configurable pre-production URL |
| `prod` | Configurable production URL |

To override at runtime without editing `config.yaml`, pass arguments via CLI or Jenkins parameters (see below).

---

## 📂 Test Data (CSV-Driven)

All tests are **100% data-driven** using CSV files located in the `data/` directory. The `csv_loader.py` utility reads these files and parametrizes tests automatically.

### `data/signup.csv` — 5 rows
```csv
email,password,username,rank,address,tel,gender,birthday,notification,agree
test1@example.com,password123,TestUser1,Normal,123 Main St,090-1234-5678,male,1990-01-01,true,true
...
```

### `data/login.csv` — 4 rows
```csv
email,password,expected_result
valid@example.com,validpass,success
invalid@example.com,wrongpass,failure
...
```

### `data/reserve.csv` / `data/reservation.csv` — 2 rows
```csv
room_type,checkin_date,checkout_date,head_count,username,email,contact
Standard,2025-01-10,2025-01-12,2,John Doe,john@test.com,optional
...
```

### How CSV Loader Works

```python
# src/core/csv_loader.py (simplified)
import csv

def load_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
```

Tests are then parametrized using `@pytest.mark.parametrize` with the loaded rows, making it trivial to add new test scenarios by simply appending rows to the CSV.

---

## ▶️ Running Tests

### Basic Run (Default Config)

```bash
pytest src/tests/
```

### Run Specific Test File

```bash
pytest src/tests/test_login.py
pytest src/tests/test_signup.py
pytest src/tests/test_reserve.py
```

### Run with Allure Results Output

```bash
pytest src/tests/ --alluredir=reports/allure-results/chrome
```

### Generate & Open Allure Report

```bash
allure generate reports/allure-results/chrome -o reports/allure-report/chrome --clean
allure open reports/allure-report/chrome
```

### Run with HTML Report (pytest-html)

```bash
pytest src/tests/ --html=reports/report.html --self-contained-html
```

---

## 🌐 Browser Support

The browser is driven by `config/config.yaml` or overridden via CLI using the `--browser` flag (configured in `conftest.py`).

### Change Browser in Config

```yaml
# config/config.yaml
browser: "edge"   # chrome | firefox | edge
```

### Override at Runtime

```bash
pytest src/tests/ --browser=chrome
pytest src/tests/ --browser=firefox
pytest src/tests/ --browser=edge
```

### How Driver Factory Works

`src/core/driver_factory.py` uses `webdriver-manager` to automatically download and cache the correct driver binary:

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def create_driver(browser, headless):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Firefox(GeckoDriverManager().install(), options=options)

    elif browser == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        return webdriver.Edge(EdgeChromiumDriverManager().install(), options=options)
```

---

## 🌍 Environment Support

The framework supports three deployment environments, allowing the same test suite to validate across the full delivery pipeline.

### Set Environment in Config

```yaml
# config/config.yaml
environment: "preprod"   # test | preprod | prod
```

### Override at Runtime

```bash
pytest src/tests/ --env=test
pytest src/tests/ --env=preprod
pytest src/tests/ --env=prod
```

The environment value is also **injected into the Allure report** as environment metadata, so every report clearly shows which environment was tested.

### Environment Properties in Allure

The file `reports/allure-results/<browser>/environment.properties` is auto-generated by the framework and contains entries like:

```properties
Browser=Chrome
Environment=preprod
Base.URL=https://preprod.hotel.example.com
Python.Version=3.14
Platform=Windows 10
```

This data surfaces on the **Allure Dashboard Environment widget**.

---

## 👁️ Headless & Headed Mode

Switch between headless (no visible browser window — ideal for CI) and headed (visible browser — ideal for debugging) without changing test code.

### Set in Config

```yaml
# config/config.yaml
headless: true    # CI/Jenkins
headless: false   # Local debugging
```

### Override at Runtime

```bash
# Run headless
pytest src/tests/ --headless=true

# Run headed (default for local dev)
pytest src/tests/ --headless=false
```

### Use Cases

| Mode | When to Use |
|---|---|
| **Headed** | Local development, debugging test failures, visual verification |
| **Headless** | Jenkins pipeline, Docker containers, remote CI agents, performance |

---

## 🔧 Jenkins CI/CD Integration

The project is fully integrated with **Jenkins CI** for automated test execution on every code push or scheduled run.

### Jenkins Pipeline Overview

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Code Push   │───▶│  Checkout    │───▶│  Install Deps│───▶│  Run Tests   │
│  (Git)       │    │  from Git    │    │  (pip install│    │  (pytest)    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                                                                    │
                    ┌──────────────┐    ┌──────────────┐           │
                    │  Notify Team │◀───│  Allure      │◀──────────┘
                    │  (Email/Slack│    │  Report Gen  │
                    └──────────────┘    └──────────────┘
```

### Sample Jenkinsfile

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER',      choices: ['chrome', 'firefox', 'edge'], description: 'Target browser')
        choice(name: 'ENVIRONMENT',  choices: ['test', 'preprod', 'prod'],   description: 'Target environment')
        booleanParam(name: 'HEADLESS', defaultValue: true,                   description: 'Run headless?')
    }

    environment {
        ALLURE_RESULTS_DIR = "reports/allure-results/${params.BROWSER}"
        ALLURE_REPORT_DIR  = "reports/allure-report/${params.BROWSER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/<your-org>/hotel_selenium.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat '''
                    python -m venv .venv
                    .venv\\Scripts\\activate.bat
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                    .venv\\Scripts\\activate.bat &&
                    pytest src/tests/
                        --browser=${params.BROWSER}
                        --env=${params.ENVIRONMENT}
                        --headless=${params.HEADLESS}
                        --alluredir=${ALLURE_RESULTS_DIR}
                        --reruns=2
                        --reruns-delay=1
                        -v
                """
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat "allure generate ${ALLURE_RESULTS_DIR} -o ${ALLURE_REPORT_DIR} --clean"
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure([
                    includeProperties: true,
                    jdk: '',
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: "${ALLURE_RESULTS_DIR}"]]
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'artifacts/**/*.mp4', allowEmptyArchive: true
            archiveArtifacts artifacts: 'reports/**/*',      allowEmptyArchive: true
        }
        failure {
            emailext(
                subject: "❌ Test Suite FAILED — ${params.BROWSER} / ${params.ENVIRONMENT}",
                body: "Build ${env.BUILD_NUMBER} failed. Check Allure report: ${env.BUILD_URL}allure",
                to: 'qa-team@yourcompany.com'
            )
        }
    }
}
```

### Jenkins Parameterized Build

The pipeline exposes three build parameters visible in the Jenkins UI:

| Parameter | Type | Options |
|---|---|---|
| `BROWSER` | Choice | `chrome`, `firefox`, `edge` |
| `ENVIRONMENT` | Choice | `test`, `preprod`, `prod` |
| `HEADLESS` | Boolean | `true`, `false` |

This enables QA engineers and developers to trigger targeted test runs directly from the Jenkins UI **without modifying any code or config files**.

---

## 📊 Allure Reporting

The framework generates **rich, interactive Allure HTML reports** for each browser and optionally a **merged cross-browser report**.

### Report Structure

```
reports/allure-report/
├── chrome/       # Chrome-only report
├── firefox/      # Firefox-only report
├── edge/         # Edge-only report
└── merged/       # Unified cross-browser report
```

### Report Sections

| Section | Contents |
|---|---|
| **Dashboard** | Summary, pass/fail stats, environment info, executor details |
| **Suites** | Tests grouped by module and class |
| **Behaviors** | Tests grouped by Allure features and stories |
| **Timeline** | Test execution timeline with parallel workers |
| **Packages** | Test hierarchy by Python package structure |
| **History Trend** | Pass/fail trend across last N builds |
| **Categories** | Automatic failure categorization (broken, failed, flaky) |

### Allure Annotations in Tests

Tests use Allure decorators for rich metadata:

```python
import allure

@allure.feature("User Authentication")
@allure.story("Valid Login")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_valid(driver, login_data):
    with allure.step("Navigate to login page"):
        ...
    with allure.step("Enter credentials"):
        ...
    with allure.step("Assert successful login"):
        ...
```

### Attachments Per Test

Each test case automatically attaches:
- 📸 **Screenshot** (PNG) — on failure
- 🎥 **Video Recording** (MP4) — on failure (or all, if configured)
- 📝 **Test Log** (TXT) — always

### Generate & View Report

```bash
# Generate from results
allure generate reports/allure-results/chrome -o reports/allure-report/chrome --clean

# Serve locally (opens browser automatically)
allure serve reports/allure-results/chrome

# Merge all browser results into one report
allure generate reports/allure-results/chrome \
               reports/allure-results/firefox \
               reports/allure-results/edge \
               -o reports/allure-report/merged --clean
```

---

## 🎥 Video Recording & Screenshots

### Video Recording

Powered by `mss` (screen capture) and `imageio` (MP4 encoding), `src/core/video_recorder.py` records the full test session screen.

- **Location:** `artifacts/<test_id>/<test_name>.mp4`
- **Trigger:** Configurable — on failure only (`video_on_failure: true`) or always
- **Allure attachment:** Video is attached directly to the failing test case in the Allure report

Example artifact path:
```
artifacts/src_tests_test_login.py_test_login_edge-row-3/
    └── src_tests_test_login.py_test_login_edge-row-3.mp4
```

### Screenshots

Captured by Selenium's built-in screenshot API in `src/core/allure_helpers.py`:

```python
import allure
from selenium.webdriver.remote.webdriver import WebDriver

def attach_screenshot(driver: WebDriver, name: str = "Screenshot"):
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
```

Screenshots are attached to the Allure report as inline images, visible directly in the test case detail view.

---

## 📝 Logging

`src/core/logger.py` sets up a structured, per-test logger that writes to both the console and a file.

### Log Levels

```python
import logging

# Usage in any module
from src.core.logger import get_logger
logger = get_logger(__name__)

logger.debug("Detailed debug information")
logger.info("Test step executed successfully")
logger.warning("Element took longer than expected")
logger.error("Element not found — test will fail")
```

### Log Attachment to Allure

After each test, the log content is attached to the Allure report as a `.txt` attachment, providing full traceability without needing to SSH into the test runner.

---

## 🏗️ Page Object Model (POM)

All UI interactions are encapsulated in `src/pages/Homepage.py`, following the Page Object Model pattern. This separates test logic from page interaction logic, making the suite maintainable as the application evolves.

### Structure

```python
# src/pages/Homepage.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    # Locators
    SIGNUP_LINK      = (By.LINK_TEXT, "Sign up")
    LOGIN_LINK       = (By.LINK_TEXT, "Log in")
    RESERVE_BTN      = (By.CSS_SELECTOR, ".btn-primary")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def go_to_signup(self):
        self.wait.until(EC.element_to_be_clickable(self.SIGNUP_LINK)).click()

    def go_to_login(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_LINK)).click()

    def click_reserve(self):
        self.wait.until(EC.element_to_be_clickable(self.RESERVE_BTN)).click()
```

### Benefits

- **Single place to update locators** when UI changes
- **Reusable methods** shared across multiple test files
- **Readable tests** — test code reads like plain English
- **Easier debugging** — failures point directly to the page method, not a raw `find_element` call

---

## 🔀 Test Suites & Parallel Execution

### Suite Definition (`runners/suite.yaml`)

```yaml
# runners/suite.yaml
suite:
  name: "Full Regression"
  browsers:
    - chrome
    - edge
    - firefox
  environment: test
  headless: true
  tests:
    - src/tests/test_signup.py
    - src/tests/test_login.py
    - src/tests/test_reserve.py
```

### Suite Runner (`runners/run_suite.py`)

```bash
python runners/run_suite.py
```

This script reads `suite.yaml` and programmatically invokes pytest with the correct arguments per browser.

### Parallel Execution (pytest-xdist)

```bash
# Run with 4 parallel workers
pytest src/tests/ -n 4

# Run with auto-detected worker count (1 per CPU core)
pytest src/tests/ -n auto
```

### Retry Flaky Tests

```bash
# Retry each failing test up to 2 times with a 1-second delay
pytest src/tests/ --reruns=2 --reruns-delay=1
```

### Test Ordering

```python
# src/tests/test_signup.py
import pytest

@pytest.mark.order(1)
def test_signup_row_1(driver, signup_data): ...

@pytest.mark.order(2)
def test_signup_row_2(driver, signup_data): ...
```

---

## 📦 Artifacts

All test run artifacts are saved under the `artifacts/` directory, organized by test ID:

```
artifacts/
├── src_tests_test_login.py_test_login_edge-row-1/       # (empty — test passed)
├── src_tests_test_login.py_test_login_edge-row-2/       # (empty — test passed)
├── src_tests_test_login.py_test_login_edge-row-3/
│   └── src_tests_test_login.py_test_login_edge-row-3.mp4   # ← Video of failure
├── src_tests_test_login.py_test_login_edge-row-4/       # (empty — test passed)
├── src_tests_test_reserve.py_test_reserve_edge-row-1/
├── src_tests_test_reserve.py_test_reserve_edge-row-2/
├── src_tests_test_signup.py_test_signup_edge-row-1/
├── src_tests_test_signup.py_test_signup_edge-row-2/
├── src_tests_test_signup.py_test_signup_edge-row-3/
├── src_tests_test_signup.py_test_signup_edge-row-4/
└── src_tests_test_signup.py_test_signup_edge-row-5/
```

Artifact naming convention: `<test_file>_<test_function>_<browser>-row-<csv_row_number>`

---

## 🧩 conftest.py — Fixture Architecture

`src/tests/conftest.py` is the central fixture hub for the entire suite:

```python
import pytest
from src.core.driver_factory import create_driver
from src.core.video_recorder import VideoRecorder
from src.core.allure_helpers import attach_screenshot, attach_log
from src.core.csv_loader import load_csv
from src.core.logger import get_logger

logger = get_logger(__name__)

@pytest.fixture(scope="function")
def driver(request, config):
    browser  = config["browser"]
    headless = config["headless"]
    drv = create_driver(browser, headless)
    drv.get(config["base_url"])
    recorder = VideoRecorder()
    recorder.start()
    yield drv
    if request.node.rep_call.failed:
        attach_screenshot(drv)
        recorder.stop_and_save(request.node.nodeid)
        attach_log(request.node.nodeid)
    else:
        recorder.stop()
    drv.quit()

@pytest.fixture(scope="session")
def config():
    import yaml
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)
```

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** your feature branch: `git checkout -b feature/my-new-test`
3. **Add** test data to the appropriate CSV in `data/`
4. **Write** your test in `src/tests/`
5. **Add** page interactions to `src/pages/Homepage.py` if needed
6. **Run** tests locally: `pytest src/tests/ -v`
7. **Commit** your changes: `git commit -m "Add: new reservation edge case"`
8. **Push** and **open a Pull Request**

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ using Selenium, Pytest & Allure · Hotel Planisphere Test Automation Framework
</p>
