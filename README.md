# SDET Portfolio: Python Test Engine

## Overview
Welcome to a cutting-edge demo showcasing the automation of testing for graphical user interfaces and API. Designed for testers and developers alike, this project leverages modern technologies to streamline and enhance testing processes.

## Features
- **GUI and API Testing**
- **Modern Technology Stack**
- **Easy to Use**

## Documentation
- **[Test Strategy](/docs/QASTRATEGY.md)**
- **[Bug Examples](/docs/bugs)**
- **[Test Cases](/docs/cases)**
- **[Test Runs Artifacts](/testruns)**

## Technical Stack
Utilizing a robust stack of technologies to ensure high-quality testing:
- **Language:** Python 3.10+
- **Test Runner:** [Pytest](https://docs.pytest.org/en/7.2.x/)
- **Utilities:** [attrs](https://www.attrs.org/en/stable/examples.html), [assertpy](https://github.com/assertpy/assertpy), [dynaconf](https://www.dynaconf.com/), [pandas](https://pandas.pydata.org/), [pytest-repeat](https://github.com/pytest-dev/pytest-repeat), [requests](https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request)
- **Reporting:** [pytest-html](https://pytest-html.readthedocs.io/en/latest/), [allure-pytest](https://github.com/allure-framework/allure-python)
- **Web testing:** [Playwright](https://playwright.dev/python/docs/intro)
- **CI/CD:** [Invoke](https://docs.pyinvoke.org/en/stable/getting-started.html)

## Getting Started
Follow these steps to set up the Python Test Engine in your environment:
1. **Download the Project:** Start by downloading the project to your local machine.
2. **Install Dependencies:**
   - Install poetry following the instructions at [Python Poetry](https://python-poetry.org/docs/).
   - Run `poetry install` to initialize the project with the necessary dependencies.
3. **Test Execution:**
   - Install Playwright as per the [official documentation](https://playwright.dev/python/docs/intro).
   - Use `invoke clean` to clear any previous reports.
   - Execute tests with `invoke run-tests`.
4. **Reporting:**
   - Install Allure Report using [Allure Documentation](https://docs.qameta.io/allure/#_installing_a_commandline).
   - Generate dynamic reports with `invoke create-report`.
   - Access static reports at `/report/pytest_html.html`.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support
Thank you for exploring the SDET Portfolio: Python Test Engine!
