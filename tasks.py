# pylint: disable=invalid-name

"""
Invoke is a Python (2.7 and 3.4+) library for managing shell-oriented subprocesses
and organizing executable Python code into CLI-invokable tasks.
"""

from invoke import task


@task
def clean(c):
    c.run("rm -rf reports test-results testruns")


@task
def run_tests(c):
    c.run("python -m pytest --tb=short")


@task
def create_report(c):
    c.run("allure serve report/allure_results")
