"""
The next example puts the fixture function
into a separate conftest.py file so that tests
from multiple test modules in the directory
can access the fixture function.
"""

import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args, "args": ["--start-maximized"]}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "no_viewport": True,
        # "viewport": {
        #     "width": 1920,
        #     "height": 1080,
        # },
    }
