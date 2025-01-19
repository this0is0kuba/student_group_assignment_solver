import json
import os

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def load_json_from_file(filepath: str) -> dict:
    with open(filepath, "r") as file:
        return json.load(file)


def test_basic_1():

    payload = load_json_from_file(os.path.join(TEST_DIR, "resources/basic_tests/basic_1.json"))

    response = client.post("/run-solver", json=payload)

    assert response.status_code == 200
