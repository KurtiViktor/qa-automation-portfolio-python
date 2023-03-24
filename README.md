# VKurti-Coding-Task

## Documentation

* \docs\QASTRATEGY.md -- Test Strategy.
* \docs\bugs -- Examples of bugs.
* \docs\cases -- Examples of test cases.
* \report -- Allure and Html pytest report.
* settings.toml -- Global settings for autotests.
* task.py -- CI/CD for autotests.
* pyproject.toml -- Dependency manager for autotests.

## Technical stack

* Lang: Python 3.10.9
* Test runner: Pytest https://docs.pytest.org/en/7.2.x/
* Boilerplate reducing: attrs https://www.attrs.org/en/stable/examples.html
* Pretty assertions: assertpy https://github.com/assertpy/assertpy
* Pretty configs: dynaconf https://www.dynaconf.com/
* Data parsing: cattrs https://catt.rs/en/stable/, pandas https://pandas.pydata.org/
* Makes it easy to repeat a single test: pytest-repeat https://github.com/pytest-dev/pytest-repeat
* Standard api calls: requests https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request
* Standard report: pytest-html https://pytest-html.readthedocs.io/en/latest/
* Standard report: allure-pytest https://github.com/allure-framework/allure-python
* CI/CD: Invoke https://docs.pyinvoke.org/en/stable/getting-started.html
* Webdriver test framework: selene https://github.com/yashaka/selene

## Installation and Running

1. Download VKurti-Coding-Task.
2. Install poetry: https://python-poetry.org/docs/.
3. Initialising a pre-existing project: `poetry install`.
4. Path to chromedriver.exe must be in $PATH.
5. Clean Report: `invoke clean`.
6. Run tests: `invoke run-tests`.
7. Install Allure: https://docs.qameta.io/allure/#_installing_a_commandline.
8. Dynamical Report: `invoke create-report`.
9. Statical Report: /report/pytest_html.html.
