# 🧪 Python Test Automation Framework

A **modular, scalable and enterprise-grade test automation framework** built with **Python + pytest**

Supports **UI (Selenium/Appium)**, **API (requests + pydantic)** and **External Service Testing** (SSH, Cloud).
Implements clean separation of concerns, configuration injection and parallelism.

---

## 🚀 Key Features

- 🧱 Modular, layered architecture
- ⚙️ Configuration via `config.json` + `.env`
- 🌐 Web automation with Selenium (POM design)
- 📱 Mobile automation with Appium
- 🔌 API automation using requests + pydantic
- ☁️ Cloud execution (BrowserStack / SauceLabs)
- 🧰 External service integrations (SSH)
- 🧵 Parallel execution (`pytest-xdist`)
- 📊 Reporting (Allure / pytest-html)

---

## 📁 Folder Structure

tests/
├── conftest.py
├── config/
│ ├── init.py
│ ├── config.py
│ ├── config.yaml
│ └── .env
├── drivers/
│ ├── init.py
│ ├── driver_factory.py
│ ├── remote_driver_factory.py
│ └── mobile_driver_factory.py
├── api/
│ ├── init.py
│ ├── base_client.py
│ └── models.py
├── pages/
│ ├── init.py
│ ├── base_page.py
│ └── login_page.py
├── services/
│ ├── init.py
│ ├── ssh_client.py
├── utils/
│ ├── init.py
│ ├── logger.py
│ └── screenshot.py
├── tests/
│ ├── init.py
│ ├── test_login_ui.py
│ ├── test_login_api.py
│ └── test_external_services.py
├── pytest.ini
└── requirements.txt

---

## ⌨️ Commands

- Install Dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
- Run Locally
pytest -m ui --env=default
- Run on BrowserStack
pytest -m ui --env=browserstack
- Run API Tests
pytest -m api
- Run in Parallel
pytest -n auto -m "ui or api"
- 📊 Reporting
🧩 Allure
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
- 📜 HTML
pytest --html=reports/report.html --self-contained-html
- Run all tests:
pytest -n auto

---

## 🧰 Tech Stack Summary
Category	Library
Test Runner	pytest
Web UI	selenium
Mobile	appium-python-client
API	requests, pydantic
Config	PyYAML, python-dotenv
SSH paramiko
Reporting allure-pytest, pytest-html
Parallelism	pytest-xdist
Code Style black, flake8

---

## 📘 References

PEP 8 – Python Style Guide
pytest Docs
Selenium Docs
Appium Python Client
Allure Pytest

---

## 📜 License

MIT License © 2025 [Vipin G]

---