import os


def test_environment_variable():
    assert os.getenv("TEST_MODE") == "true"
