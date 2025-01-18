from datetime import timedelta

import minizinc
import os

from minizinc import Solver

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestBasicCases:

    # path to model
    path_to_model = os.path.join(TEST_DIR, "../../../app/solver/minizinc/models/groups.mzn")

    # model's parameters
    processes = 8
    solver = Solver.lookup("com.google.ortools.sat")
    timeout = timedelta(seconds=20)

    def test_basic_1(self):

        path = os.path.join(TEST_DIR, "../resources/groups/basic_1.dzn")
        groups_with_common_students, groups = self.run_solver(path)

        assert groups_with_common_students == 0
        assert groups[0][0] == 1

    def test_basic_2(self):

        path = os.path.join(TEST_DIR, "../resources/groups/basic_2.dzn")
        groups_with_common_students, groups = self.run_solver(path)

        assert groups_with_common_students == 0

        # student 1
        assert groups[0][0] == 1
        assert groups[0][1] == 0

        # student 2
        assert groups[1][0] == 1
        assert groups[0][1] == 0

    def test_basic_3(self):

        path = os.path.join(TEST_DIR, "../resources/groups/basic_3.dzn")
        groups_with_common_students, _ = self.run_solver(path)

        assert groups_with_common_students == 0

    def test_basic_4(self):

        path = os.path.join(TEST_DIR, "../resources/groups/basic_4.dzn")
        groups_with_common_students, groups = self.run_solver(path)

        assert groups_with_common_students == 2
        assert groups[0][0]

    def test_basic_5(self):

        path = os.path.join(TEST_DIR, "../resources/groups/basic_4.dzn")
        groups_with_common_students, groups = self.run_solver(path)

        assert groups_with_common_students == 2
        assert groups[0][0]
        assert len([student[0] for student in groups if student[0] == 1]) > 1

    def run_solver(self, path_to_input_data) -> tuple[int, list[list[int]]]:

        model = minizinc.Model()
        model.add_file(self.path_to_model)
        model.add_file(path_to_input_data)

        instance = minizinc.Instance(self.solver, model)

        result = instance.solve(processes=self.processes, timeout=self.timeout)

        return result["groups_with_common_students"], result["student_group"]

