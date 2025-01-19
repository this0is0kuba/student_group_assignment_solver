import json
import os

from fastapi.testclient import TestClient

from dependencies.definitions import E2E_DIR
from main import app

RESOURCES_DIR = os.path.join(E2E_DIR, "resources", "basic_tests")


class TestBasicCases:

    client = TestClient(app)

    def test_basic_1(self):

        path = get_path("basic_1")
        payload = load_json_from_file(path)

        response = self.client.post("/run-solver", json=payload)

        assert response.status_code == 200


def get_path(name: str) -> str:
    return os.path.join(RESOURCES_DIR, name + ".json")


def load_json_from_file(filepath: str) -> dict:
    with open(filepath, "r") as file:
        return json.load(file)

