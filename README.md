<div align="center">

```
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                       ║
║   ██████╗ ██╗      █████╗ ███╗   ██╗██╗███████╗██████╗ ██╗  ██╗███████╗██████╗ ███████╗  ║
║   ██╔══██╗██║     ██╔══██╗████╗  ██║██║██╔════╝██╔══██╗██║  ██║██╔════╝██╔══██╗██╔════╝  ║
║   ██████╔╝██║     ███████║██╔██╗ ██║██║███████╗██████╔╝███████║█████╗  ██████╔╝█████╗    ║
║   ██╔═══╝ ██║     ██╔══██║██║╚██╗██║██║╚════██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗██╔══╝    ║
║   ██║     ███████╗██║  ██║██║ ╚████║██║███████║██║     ██║  ██║███████╗██║  ██║███████╗  ║
║   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝  ║
║                                                                                       ║
║        ██╗  ██╗ ██████╗ ████████╗███████╗██╗                                        ║
║        ██║  ██║██╔═══██╗╚══██╔══╝██╔════╝██║                                        ║
║        ███████║██║   ██║   ██║   █████╗  ██║                                        ║
║        ██╔══██║██║   ██║   ██║   ██╔══╝  ██║                                        ║
║        ██║  ██║╚██████╔╝   ██║   ███████╗███████╗                                   ║
║        ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚══════╝                                   ║
║                                                                                       ║
║   ─────────  Python · Selenium · Pytest · Allure · Jenkins · Browsers  ─────────     ║
║                                                                                       ║
║         Enterprise-Grade Web Test Automation Framework                                ║
║                    Built by  Raxit Sharma                                            ║
║                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
```

<br/>

[![Python](https://img.shields.io/badge/Python-3.12%20|%203.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.41.0-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://selenium.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-8.3.2-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-2.x-FF6B35?style=for-the-badge&logo=qameta&logoColor=white)](https://allurereport.org/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?style=for-the-badge&logo=jenkins&logoColor=white)](https://jenkins.io/)

[![Chrome](https://img.shields.io/badge/Chrome-Supported-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)](https://google.com/chrome/)
[![Firefox](https://img.shields.io/badge/Firefox-Supported-FF7139?style=for-the-badge&logo=firefox&logoColor=white)](https://mozilla.org/)
[![Edge](https://img.shields.io/badge/Edge-Supported-0078D7?style=for-the-badge&logo=microsoftedge&logoColor=white)](https://microsoft.com/edge/)
[![License](https://img.shields.io/badge/License-Proprietary%20%C2%A9%202026%20Raxit%20Sharma-B22222?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](#-license)

<br/>

> *Enterprise-grade Selenium automation for the Hotel Planisphere web app — multi-browser,*
> *multi-environment, CSV-driven, with Allure reporting, video capture, and Jenkins CI out of the box.*

<br/>

</div>

---

## 📋 Table of Contents

- [🔍 Project Overview](#-project-overview)
- [✨ Key Features](#-key-features)
- [🛠 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙️ Prerequisites & Installation](#️-prerequisites--installation)
- [🔧 Configuration](#-configuration)
- [📂 Test Data (CSV-Driven)](#-test-data-csv-driven)
- [▶️ Running Tests](#️-running-tests)
- [🌐 Browser Support](#-browser-support)
- [🌍 Environment Support](#-environment-support)
- [👁️ Headless & Headed Mode](#️-headless--headed-mode)
- [🔧 Jenkins CI/CD Integration](#-jenkins-cicd-integration)
- [📊 Allure Reporting](#-allure-reporting)
- [🎥 Video Recording & Screenshots](#-video-recording--screenshots)
- [📝 Logging](#-logging)
- [🏗️ Page Object Model](#️-page-object-model-pom)
- [🔀 Test Suites & Parallel Execution](#-test-suites--parallel-execution)
- [📦 Artifacts](#-artifacts)
- [🧩 conftest.py — Fixture Architecture](#-conftestpy--fixture-architecture)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## 🔍 Project Overview

**Hotel Planisphere** is a production-grade, end-to-end Selenium test automation framework targeting the [Hotel Planisphere](https://hotel.testplanisphere.dev/) web application. Built with Python and Pytest, it is designed for **enterprise CI/CD pipelines** — supporting multi-browser execution, environment-specific configurations, Allure reports with rich media attachments, and fully data-driven test execution via CSV.

### Test Coverage at a Glance

| Module | Journey | Data Rows |
|:---|:---|:---:|
| `test_signup.py` | New user registration — full form validation | 5 |
| `test_login.py` | Authentication — valid & invalid credential scenarios | 4 |
| `test_reserve.py` | Hotel room reservation — end-to-end booking workflow | 2 |

### Why This Framework Stands Out

| Challenge | Solution |
|:---|:---|
| Testing across multiple browsers | Single config change — `browser: chrome/firefox/edge` |
| Environment-specific test runs | `environment: test/preprod/prod` with injected Allure metadata |
| Scaling tests without code changes | CSV-driven `@pytest.mark.parametrize` — add rows, not code |
| Flaky test handling | `pytest-rerunfailures` with configurable retry + delay |
| Proving what failed in CI | Screenshot + MP4 video attached directly in Allure report |
| Parallel execution bottlenecks | `pytest-xdist` with `-n auto` worker scaling |
| Brittle locator maintenance | Page Object Model — one file to update, all tests adapt |

---

## ✨ Key Features

<div align="center">

| Feature | Description |
|:---|:---|
| 🌐 **Multi-Browser** | Chrome, Firefox, and Edge — swap with a single config value |
| 🌍 **Multi-Environment** | `test`, `preprod`, `prod` — same suite, any environment |
| 👁️ **Headless / Headed** | Toggle visibility for CI or local debugging — zero code changes |
| 🔁 **Data-Driven** | CSV-powered parametrization across all test modules |
| 📊 **Allure Reports** | Rich HTML reports: environment info, history trends, timelines |
| 🎥 **Video Recording** | Auto MP4 capture for failed test sessions via `mss` + `imageio` |
| 📸 **Screenshots** | Auto-attached to Allure on test failure |
| 📝 **Structured Logging** | Per-test log files, attached inline to every Allure test case |
| ⚙️ **Jenkins CI/CD** | Full parameterized pipeline — browser, env, headless toggle |
| 🔀 **Parallel Execution** | Multi-worker execution via `pytest-xdist` |
| 🔄 **Auto-Retry** | Flaky test retry via `pytest-rerunfailures` |
| ⏱️ **Timeout Control** | Global and per-test timeouts via `pytest-timeout` |
| 📋 **Test Ordering** | Deterministic execution order via `pytest-order` |
| 🏗️ **POM Architecture** | Clean Page Object Model — maintainable as the UI evolves |

</div>

---

## 🛠 Tech Stack

<div align="center">

| Layer | Technology | Version |
|:---|:---|:---:|
| **Language** | Python | 3.12 / 3.14 |
| **Browser Automation** | Selenium WebDriver | 4.41.0 |
| **Test Framework** | Pytest | 8.3.2 |
| **Driver Management** | WebDriver Manager | 4.0.2 |
| **Reporting** | Allure (allure-pytest) | 2.x |
| **HTML Reports** | pytest-html | 4.1.1 |
| **Parallel Execution** | pytest-xdist | 3.6.1 |
| **Retry Logic** | pytest-rerunfailures | 14.0 |
| **Test Ordering** | pytest-order | 1.3.0 |
| **Timeout Control** | pytest-timeout | 2.4.0 |
| **Test Metadata** | pytest-metadata | 3.1.1 |
| **Video Recording** | mss + imageio | latest |
| **Config Parsing** | PyYAML | 6.0.2 |
| **HTTP Client** | Requests | 2.32.5 |
| **Async Support** | Trio | 0.31.0 |
| **Env Variables** | python-dotenv | 1.1.1 |
| **CI/CD** | Jenkins | — |

</div>

---

## 📁 Project Structure

```
hotel_selenium/
│
├── config/
│   └── config.yaml                   # Master config: URL, browser, env, headless flag
│
├── data/
│   ├── login.csv                     # Login test data — valid & invalid credentials
│   ├── signup.csv                    # Signup data — 5 user registration rows
│   ├── reserve.csv                   # Reservation test data
│   └── reservation.csv               # Extended reservation scenarios
│
├── runners/
│   ├── run_suite.py                  # Python entry point to trigger test suites
│   └── suite.yaml                    # Suite definition — order, markers, browser, env
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/                         # Framework engine
│   │   ├── allure_helpers.py         # Allure attachment utilities (screenshot, log, video)
│   │   ├── csv_loader.py             # CSV reader → pytest parametrize input
│   │   ├── driver_factory.py         # WebDriver factory — browser + headless toggle
│   │   ├── logger.py                 # Structured per-test logger
│   │   ├── utils.py                  # Shared utility functions
│   │   ├── video_recorder.py         # Screen capture & MP4 export via mss/imageio
│   │   └── __init__.py
│   │
│   ├── pages/                        # Page Object Model layer
│   │   ├── Homepage.py               # All page interactions — one class per screen
│   │   └── __init__.py
│   │
│   └── tests/                        # Test modules
│       ├── conftest.py               # Fixtures — driver setup, teardown, Allure hooks
│       ├── test_login.py             # Login test cases — 4 CSV rows
│       ├── test_signup.py            # Signup test cases — 5 CSV rows
│       ├── test_reserve.py           # Reservation test cases — 2 CSV rows
│       └── __init__.py
│
├── artifacts/                        # Auto-generated test run artifacts
│   └── <test_id>/
│       └── *.mp4                     # Per-test video recordings
│
├── reports/
│   ├── allure-results/               # Raw Allure result JSONs — per browser
│   │   ├── chrome/
│   │   ├── edge/
│   │   ├── firefox/
│   │   └── merged/
│   │
│   └── allure-report/                # Generated HTML reports
│       ├── chrome/
│       ├── edge/
│       ├── firefox/
│       └── merged/                   # Unified cross-browser report
│
└── .venv/                            # Virtual environment
```

---

## ⚙️ Prerequisites & Installation

### System Requirements

```
✔  Python 3.12+ or 3.14+   → https://python.org/downloads/
✔  Java 8+                  → Required for Allure CLI
✔  Git                      → https://git-scm.com/
✔  Jenkins (for CI)         → https://www.jenkins.io/
```

### Browser Driver Support

| Browser | Driver | Auto-Managed? |
|:---|:---|:---:|
| Google Chrome | ChromeDriver | ✅ via `webdriver-manager` |
| Mozilla Firefox | GeckoDriver | ✅ via `webdriver-manager` |
| Microsoft Edge | EdgeDriver | ✅ via `webdriver-manager` |

No manual driver downloads needed — `webdriver-manager` handles it automatically.

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/<your-username>/hotel_selenium.git
cd hotel_selenium
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

| Platform | Command |
|:---|:---|
| **Windows (cmd)** | `.venv\Scripts\activate.bat` |
| **Windows (PowerShell)** | `.venv\Scripts\Activate.ps1` |
| **macOS / Linux** | `source .venv/bin/activate` |

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install selenium==4.41.0 pytest==8.3.2 allure-pytest webdriver-manager \
            pytest-xdist pytest-rerunfailures pytest-order pytest-timeout \
            pytest-html pytest-metadata pyyaml python-dotenv requests mss imageio
```

### Step 4 — Install Allure CLI

```bash
# macOS (Homebrew)
brew install allure

# Windows (Scoop)
scoop install allure

# Manual → https://github.com/allure-framework/allure2/releases
# Download, extract, and add /bin to your PATH
```

---

## 🔧 Configuration

All framework settings live in `config/config.yaml`. Change one value — everything follows.

```yaml
# config/config.yaml

base_url: "https://hotel.testplanisphere.dev"

browser:      "chrome"    # chrome | firefox | edge
environment:  "test"      # test | preprod | prod
headless:     false       # true = CI-friendly, false = local debugging

implicit_wait:      10    # seconds
page_load_timeout:  30    # seconds

video_on_failure:      true   # record MP4 only on failure
screenshot_on_failure: true   # capture PNG on failure
log_level:            "INFO"  # DEBUG | INFO | WARNING | ERROR
```

### Environment URL Mapping

| `environment` Value | Resolved Base URL |
|:---|:---|
| `test` | `https://hotel.testplanisphere.dev` |
| `preprod` | Configurable pre-production URL |
| `prod` | Configurable production URL |

> Override at runtime via CLI flags or Jenkins parameters — no need to edit `config.yaml` in CI.

---

## 📂 Test Data (CSV-Driven)

Every test in this framework is **100% data-driven**. CSV files in `data/` feed directly into `@pytest.mark.parametrize`. Adding a new scenario is a one-line edit to a spreadsheet — no Python required.

### `data/signup.csv` — 5 rows

```csv
email,password,username,rank,address,tel,gender,birthday,notification,agree
test1@example.com,password123,TestUser1,Normal,123 Main St,090-1234-5678,male,1990-01-01,true,true
```

### `data/login.csv` — 4 rows

```csv
email,password,expected_result
valid@example.com,validpass,success
invalid@example.com,wrongpass,failure
```

### `data/reserve.csv` — 2 rows

```csv
room_type,checkin_date,checkout_date,head_count,username,email,contact
Standard,2025-01-10,2025-01-12,2,John Doe,john@test.com,optional
```

### How the CSV Loader Works

```python
# src/core/csv_loader.py
import csv

def load_csv(filepath: str) -> list[dict]:
    with open(filepath, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))
```

Tests consume it via `@pytest.mark.parametrize`, and each CSV row becomes an independent parametrized test case in the Allure report — clearly labelled, individually retried, and individually reported.

---

## ▶️ Running Tests

### Run All Tests (Default Config)

```bash
pytest src/tests/
```

### Run a Specific Test File

```bash
pytest src/tests/test_login.py
pytest src/tests/test_signup.py
pytest src/tests/test_reserve.py
```

### Run with Allure Output

```bash
pytest src/tests/ --alluredir=reports/allure-results/chrome
```

### Generate & Open Allure Report

```bash
allure generate reports/allure-results/chrome -o reports/allure-report/chrome --clean
allure open reports/allure-report/chrome

# Or serve live (opens browser automatically):
allure serve reports/allure-results/chrome
```

### Run with HTML Report (pytest-html)

```bash
pytest src/tests/ --html=reports/report.html --self-contained-html
```

### Override Config at Runtime

```bash
pytest src/tests/ --browser=firefox --env=preprod --headless=true
```

---

## 🌐 Browser Support

Switch browsers without touching a single test file.

### Set in Config

```yaml
browser: "edge"   # chrome | firefox | edge
```

### Override at Runtime

```bash
pytest src/tests/ --browser=chrome
pytest src/tests/ --browser=firefox
pytest src/tests/ --browser=edge
```

### How the Driver Factory Works

`src/core/driver_factory.py` uses `webdriver-manager` to auto-download and cache the correct binary:

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def create_driver(browser: str, headless: bool):
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

The same test suite validates across your full delivery pipeline — `test`, `preprod`, and `prod` — with no code changes.

### Set in Config

```yaml
environment: "preprod"   # test | preprod | prod
```

### Override at Runtime

```bash
pytest src/tests/ --env=test
pytest src/tests/ --env=preprod
pytest src/tests/ --env=prod
```

### Environment Properties Injected into Allure

`reports/allure-results/<browser>/environment.properties` is auto-generated per run:

```properties
Browser=Chrome
Environment=preprod
Base.URL=https://preprod.hotel.example.com
Python.Version=3.14
Platform=Windows 10
```

This surfaces in the **Allure Dashboard Environment widget** so every report is self-documenting — you always know exactly what was tested and where.

---

## 👁️ Headless & Headed Mode

| Mode | When to Use |
|:---|:---|
| **Headed** (`headless: false`) | Local development, debugging failures, visual verification |
| **Headless** (`headless: true`) | Jenkins pipeline, Docker containers, remote CI agents |

### Set in Config

```yaml
headless: true    # CI/Jenkins
headless: false   # Local debugging
```

### Override at Runtime

```bash
pytest src/tests/ --headless=true   # CI
pytest src/tests/ --headless=false  # Local
```

---

## 🔧 Jenkins CI/CD Integration

### Pipeline Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Code Push  │───▶│  Checkout   │───▶│  Setup Env  │───▶│  Run Tests  │
│   (Git)     │    │  from Git   │    │  pip install│    │   (pytest)  │
└─────────────┘    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                 │
              ┌─────────────┐    ┌─────────────┐               │
              │  Notify Team│◀───│  Allure      │◀─────────────┘
              │ (Email/Slack│    │  Report Gen  │
              └─────────────┘    └─────────────┘
```

### Jenkinsfile

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER',
               choices: ['chrome', 'firefox', 'edge'],
               description: 'Target browser for this run')
        choice(name: 'ENVIRONMENT',
               choices: ['test', 'preprod', 'prod'],
               description: 'Deployment environment to test against')
        booleanParam(name: 'HEADLESS',
                     defaultValue: true,
                     description: 'Run headless (true = CI mode, false = debug mode)')
    }

    environment {
        ALLURE_RESULTS = "reports/allure-results/${params.BROWSER}"
        ALLURE_REPORT  = "reports/allure-report/${params.BROWSER}"
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
                        --alluredir=${ALLURE_RESULTS}
                        --reruns=2
                        --reruns-delay=1
                        -v
                """
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat "allure generate ${ALLURE_RESULTS} -o ${ALLURE_REPORT} --clean"
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure([
                    includeProperties: true,
                    jdk: '',
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: "${ALLURE_RESULTS}"]]
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'artifacts/**/*.mp4', allowEmptyArchive: true
            archiveArtifacts artifacts: 'reports/**/*',      allowEmptyArchive: true
            junit 'reports/**/*.xml'
        }
        failure {
            emailext(
                subject: "❌ Tests FAILED — ${params.BROWSER} / ${params.ENVIRONMENT} — Build #${env.BUILD_NUMBER}",
                body: "Build ${env.BUILD_NUMBER} failed.\n\nAllure Report: ${env.BUILD_URL}allure\nConsole: ${env.BUILD_URL}console",
                to: 'qa-team@yourcompany.com'
            )
        }
        success {
            emailext(
                subject: "✅ Tests PASSED — ${params.BROWSER} / ${params.ENVIRONMENT} — Build #${env.BUILD_NUMBER}",
                body: "All tests passed.\n\nAllure Report: ${env.BUILD_URL}allure",
                to: 'qa-team@yourcompany.com'
            )
        }
    }
}
```

### Jenkins Parameterized Build Parameters

| Parameter | Type | Options | Default |
|:---|:---|:---|:---|
| `BROWSER` | Choice | `chrome`, `firefox`, `edge` | `chrome` |
| `ENVIRONMENT` | Choice | `test`, `preprod`, `prod` | `test` |
| `HEADLESS` | Boolean | `true`, `false` | `true` |

QA engineers can trigger targeted runs directly from the Jenkins UI — no code edits, no config commits required.

---

## 📊 Allure Reporting

### Per-Browser Report Structure

```
reports/allure-report/
├── chrome/     ← Chrome-only results
├── firefox/    ← Firefox-only results
├── edge/       ← Edge-only results
└── merged/     ← Unified cross-browser report
```

### Report Sections

| Section | What You See |
|:---|:---|
| **Dashboard** | Pass/fail summary, environment info, executor details |
| **Suites** | Tests grouped by module and class |
| **Behaviors** | Tests grouped by Allure `@feature` and `@story` |
| **Timeline** | Parallel execution timeline with worker distribution |
| **Packages** | Test hierarchy by Python package structure |
| **History Trend** | Pass/fail trend across last N Jenkins builds |
| **Categories** | Automatic failure categorisation — broken, failed, flaky |

### Allure Decorators in Tests

```python
import allure

@allure.feature("User Authentication")
@allure.story("Valid Login")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_valid(driver, login_data):
    with allure.step("Navigate to login page"):
        ...
    with allure.step("Enter valid credentials"):
        ...
    with allure.step("Assert successful redirect"):
        ...
```

### What's Attached to Each Test Case

```
📸  Screenshot (PNG)        — on failure
🎥  Video Recording (MP4)   — on failure (or always, if configured)
📝  Test Log (TXT)          — always, for full traceability
```

### Generate, Merge & Serve

```bash
# Single browser
allure generate reports/allure-results/chrome -o reports/allure-report/chrome --clean
allure serve reports/allure-results/chrome

# Merged cross-browser report
allure generate reports/allure-results/chrome \
               reports/allure-results/firefox \
               reports/allure-results/edge \
               -o reports/allure-report/merged --clean
```

---

## 🎥 Video Recording & Screenshots

### Video Recording

Powered by `mss` (screen capture) and `imageio` (MP4 encoding) inside `src/core/video_recorder.py`.

- **Location:** `artifacts/<test_id>/<test_name>.mp4`
- **Trigger:** On failure by default (`video_on_failure: true`); configurable to always record
- **Allure attachment:** Embedded directly in the failing test's detail view

Artifact naming convention:
```
artifacts/
└── src_tests_test_login.py_test_login_edge-row-3/
    └── src_tests_test_login.py_test_login_edge-row-3.mp4
```

### Screenshots

Captured using Selenium's native API in `src/core/allure_helpers.py`:

```python
import allure
from selenium.webdriver.remote.webdriver import WebDriver

def attach_screenshot(driver: WebDriver, name: str = "Screenshot"):
    screenshot = driver.get_screenshot_as_png()
    allure.attach(
        screenshot,
        name=name,
        attachment_type=allure.attachment_type.PNG
    )
```

Screenshots render inline in the Allure test case detail — no downloading, no digging through CI artifacts.

---

## 📝 Logging

`src/core/logger.py` sets up a structured per-test logger that writes to both console and a file, then attaches the log to Allure.

```python
from src.core.logger import get_logger
logger = get_logger(__name__)

logger.debug("Entering checkout flow")
logger.info("Room selected: Standard — 2 nights")
logger.warning("Price element took 8s — may be a performance issue")
logger.error("Booking confirmation not found — test will fail")
```

Full log output is attached to each test case in the Allure report as a `.txt` attachment, giving complete traceability without SSH access to the test runner.

---

## 🏗️ Page Object Model (POM)

All UI interactions are encapsulated in `src/pages/Homepage.py`. Test code stays readable and intent-focused; locator changes happen in one place.

```python
# src/pages/Homepage.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:

    # ── Locators ─────────────────────────────────────────────────────────
    SIGNUP_LINK  = (By.LINK_TEXT, "Sign up")
    LOGIN_LINK   = (By.LINK_TEXT, "Log in")
    RESERVE_BTN  = (By.CSS_SELECTOR, ".btn-primary")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    # ── Actions ───────────────────────────────────────────────────────────
    def go_to_signup(self):
        self.wait.until(EC.element_to_be_clickable(self.SIGNUP_LINK)).click()

    def go_to_login(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_LINK)).click()

    def click_reserve(self):
        self.wait.until(EC.element_to_be_clickable(self.RESERVE_BTN)).click()
```

**Benefits of POM:**
- Single location for all locator definitions — one UI change, one code update
- Reusable action methods shared across all test modules
- Test files read like plain English — intent is always clear
- Failures point to the page method, not a raw `find_element` buried in test code

---

## 🔀 Test Suites & Parallel Execution

### Suite Definition

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

### Run the Full Suite

```bash
python runners/run_suite.py
```

`run_suite.py` reads `suite.yaml` and invokes pytest programmatically per browser — isolating results into separate Allure result directories automatically.

### Parallel Execution

```bash
# Fixed worker count
pytest src/tests/ -n 4

# Auto-detect workers (1 per CPU core)
pytest src/tests/ -n auto
```

### Retry Flaky Tests

```bash
# Retry each failure up to 2 times with a 1s delay between attempts
pytest src/tests/ --reruns=2 --reruns-delay=1
```

### Deterministic Test Ordering

```python
import pytest

@pytest.mark.order(1)
def test_signup_row_1(driver, signup_data): ...

@pytest.mark.order(2)
def test_signup_row_2(driver, signup_data): ...
```

---

## 📦 Artifacts

All run artifacts are saved under `artifacts/`, namespaced by test ID:

```
artifacts/
├── src_tests_test_login.py_test_login_edge-row-1/        # passed — empty
├── src_tests_test_login.py_test_login_edge-row-2/        # passed — empty
├── src_tests_test_login.py_test_login_edge-row-3/
│   └── src_tests_test_login.py_test_login_edge-row-3.mp4 # ← failure video
├── src_tests_test_login.py_test_login_edge-row-4/        # passed — empty
├── src_tests_test_reserve.py_test_reserve_edge-row-1/
├── src_tests_test_reserve.py_test_reserve_edge-row-2/
├── src_tests_test_signup.py_test_signup_edge-row-1/
├── src_tests_test_signup.py_test_signup_edge-row-2/
├── src_tests_test_signup.py_test_signup_edge-row-3/
├── src_tests_test_signup.py_test_signup_edge-row-4/
└── src_tests_test_signup.py_test_signup_edge-row-5/
```

**Naming convention:** `<test_file>_<test_function>_<browser>-row-<csv_row_number>`

---

## 🧩 conftest.py — Fixture Architecture

`src/tests/conftest.py` is the central fixture hub that wires together driver setup, video recording, Allure attachments, and teardown:

```python
import pytest
import yaml
from src.core.driver_factory  import create_driver
from src.core.video_recorder  import VideoRecorder
from src.core.allure_helpers  import attach_screenshot, attach_log
from src.core.logger          import get_logger

logger = get_logger(__name__)

@pytest.fixture(scope="session")
def config():
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="function")
def driver(request, config):
    browser  = config["browser"]
    headless = config["headless"]

    drv      = create_driver(browser, headless)
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
```

Everything — capture, cleanup, and attachment — is handled automatically. Test functions stay focused purely on assertions.

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/add-booking-edge-case`
3. **Add** test data rows to the relevant CSV in `data/`
4. **Write** your test in `src/tests/`
5. **Add** any new page interactions to `src/pages/Homepage.py`
6. **Run** locally: `pytest src/tests/ -v`
7. **Commit**: `git commit -m "Add: negative booking scenario for invalid dates"`
8. **Push** and open a **Pull Request**

When reporting a bug, please include: browser, environment, Python version, failing test ID, and the relevant Allure attachment or console output.

---

## 📜 License

<div align="center">

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║                  PROPRIETARY SOFTWARE LICENSE                  ║
║                                                                ║
║            All Rights Reserved © 2026 Raxit Sharma             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

</div>

This project is **proprietary and protected by copyright**.

**All Rights Reserved © 2026 Raxit Sharma**

No permission is granted to use, copy, modify, distribute, or create derivative works from this code without explicit written permission from the author.

Unauthorized use, reproduction, or distribution of this software, in whole or in part, may result in severe civil and criminal penalties and will be prosecuted to the maximum extent possible under the law.

For licensing inquiries, contact the author directly.

---

<div align="center">

```
─────────────────────────────────────────────────────────────────────
  Built with precision. Tested with purpose.
  Hotel Planisphere — Selenium Test Automation Framework
  © 2026 Raxit Sharma — All Rights Reserved
─────────────────────────────────────────────────────────────────────
```

⭐ **If this framework helped you, consider starring the repository.**

</div>
