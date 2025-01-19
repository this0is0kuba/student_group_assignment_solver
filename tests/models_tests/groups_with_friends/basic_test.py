from datetime import timedelta

import minizinc
import os

from minizinc import Solver

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestBasicCases:

    # path to model
    path_to_model = os.path.join(TEST_DIR, "../../../app/solver/minizinc/models/groups_with_friends.mzn")

    # model's parameters
    processes = 8
    solver = Solver.lookup("com.google.ortools.sat")
    timeout = timedelta(seconds=20)

    # students' friends
    friends_max_numbers = [0, 1, 1, 1, 2]

    friends_arrays = [
        [[]],
        [[2], [1]],
        [[2], [1], [0], [0]],
        [[2], [1], [4], [3]],
        [[3, 0], [0, 0], [1, 0], [0, 0]],
    ]

    def test_basic_1(self):

        path = os.path.join(TEST_DIR, "../resources/groups/basic_1.dzn")
        groups_with_common_students, number_of_friends, groups = self.run_solver(path, 0, 1)

        assert groups_with_common_students == 0
        assert groups[0][0] == 1
        assert number_of_friends == 0

    def test_basic_2(self):

        path = os.path.join(TEST_DIR, "../resources/groups/basic_2.dzn")
        groups_with_common_students, number_of_friends, groups = self.run_solver(path, 0, 2)

        assert groups_with_common_students == 0

        # student 1
        assert groups[0][0] == 1
        assert groups[0][1] == 0

        # student 2
        assert groups[1][0] == 1
        assert groups[0][1] == 0

        assert number_of_friends == 2

    def test_basic_3(self):

        path = os.path.join(TEST_DIR, "../resources/groups/basic_3.dzn")
        groups_with_common_students, number_of_friends, _ = self.run_solver(path, 0, 3)

        assert groups_with_common_students == 0
        assert number_of_friends == 2

    def test_basic_4(self):

        path = os.path.join(TEST_DIR, "../resources/groups/basic_4.dzn")
        groups_with_common_students, number_of_friends, groups = self.run_solver(path, 2, 4)

        assert groups_with_common_students == 2
        assert groups[0][0]
        assert number_of_friends == 8

    def test_basic_5(self):
        path = os.path.join(TEST_DIR, "../resources/groups/basic_5.dzn")
        groups_with_common_students, number_of_friends, groups = self.run_solver(path, 2, 5)

        assert groups_with_common_students == 2

        # student 1 and 3 are friends, so they should be in the same group
        assert groups[0][0]
        assert groups[2][0]

        assert len([student[0] for student in groups if student[0] == 1]) > 1
        assert number_of_friends == 4

    def run_solver(
            self,
            path_to_input_data,
            groups_with_common_students,
            test_data_number
    ) -> tuple[int, int, list[list[int]]]:

        model = minizinc.Model()
        model.add_file(self.path_to_model)
        model.add_file(path_to_input_data)

        instance = minizinc.Instance(self.solver, model)
        instance["groups_with_common_students"] = groups_with_common_students
        instance["friends_max_number"] = self.friends_max_numbers[test_data_number - 1]
        instance["friends_array"] = self.friends_arrays[test_data_number - 1]

        result = instance.solve(processes=self.processes, timeout=self.timeout)

        groups_with_common_students_result = result["groups_with_common_students_var"]
        number_of_friends = result["number_of_friends"]
        groups = result["student_group"]

        return groups_with_common_students_result, number_of_friends, groups

