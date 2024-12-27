import os


def pytest_configure(config):
    os.environ["TEST_MODE"] = "true"
