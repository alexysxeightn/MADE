# see: https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--skip-slow", action="store_true", default=False, help="skip slow tests"
    )
    parser.addoption(
        "--skip-integration", action="store_true", default=False, help="skip integration tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")
    config.addinivalue_line("markers", "integration_test: mark test as integration test")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--skip-slow"):
        skip_slow = pytest.mark.skip(reason="you need to remove --skip-slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

    if config.getoption("--skip-integration"):
        skip_slow = pytest.mark.skip(reason="you need to remove --skip-integration option to run")
        for item in items:
            if "integration_test" in item.keywords:
                item.add_marker(skip_slow)
