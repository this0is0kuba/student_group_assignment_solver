import os

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, "..", "..")))

APP_DIR = os.path.join(ROOT_DIR, "app")
TEST_DIR = os.path.join(ROOT_DIR, "tests")

UNIT_TESTS_DIR = os.path.join(TEST_DIR, "unit_tests")
MODELS_TESTS_DIR = os.path.join(TEST_DIR, "models_tests")
E2E_DIR = os.path.join(TEST_DIR, "e2e_tests")
