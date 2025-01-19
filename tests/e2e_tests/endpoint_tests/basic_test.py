import json
import os

from fastapi.testclient import TestClient

from dependencies.definitions import E2E_DIR
from main import app
from models import Solution

RESOURCES_DIR = os.path.join(E2E_DIR, "resources", "basic_tests")


class TestBasicCases:

    client = TestClient(app)

    def test_basic_1(self):

        path = get_path("basic_1")
        payload = load_json_from_file(path)

        response = self.client.post("/run-solver", json=payload)

        assert response.status_code == 200

        solution = Solution(**response.json())
        groups = solution.student_groups

        assert groups[0][0] == 1

        response.json()

    def test_basic_2(self):

        path = get_path("basic_2")
        payload = load_json_from_file(path)

        response = self.client.post("/run-solver", json=payload)

        assert response.status_code == 200

        solution = Solution(**response.json())
        groups = solution.student_groups

        assert groups == [[0, 0, 0, 1, 1], [1, 1, 1, 0, 0], [1, 1, 1, 0, 0], [0, 0, 0, 1, 1]]

    def test_basic_3(self):

        path = get_path("basic_3")
        payload = load_json_from_file(path)

        response = self.client.post("/run-solver", json=payload)

        assert response.status_code == 200

        solution = Solution(**response.json())
        groups = solution.student_groups

        assert groups[0] == groups[1]
        assert groups[2] == groups[3]

    def test_basic_4(self):

        path = get_path("basic_4")
        payload = load_json_from_file(path)

        response = self.client.post("/run-solver", json=payload)

        assert response.status_code == 200

        solution = Solution(**response.json())
        groups = solution.student_groups

        # student 1 and 4 should be in the same groups
        assert groups[0] == groups[3]

        # student 1 should be in the first group of class 4
        assert groups[0][3] == 1

        # all students should be assigned only to subject 2
        for student in groups:

            assert student[0] == 0
            assert student[1] == 0
            assert student[2] == 0
            assert student[3] != 0
            assert student[4] != 0


def get_path(name: str) -> str:
    return os.path.join(RESOURCES_DIR, name + ".json")


def load_json_from_file(filepath: str) -> dict:
    with open(filepath, "r") as file:
        return json.load(file)

