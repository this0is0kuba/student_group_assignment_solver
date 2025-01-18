from datetime import timedelta

import minizinc
import os

from minizinc import Solver

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestBasicCases:

    # path to model
    path_to_model = os.path.join(TEST_DIR, "../../../app/solver/minizinc/models/subjects_with_average.mzn")

    # model's parameters
    processes = 8
    solver = Solver.lookup("com.google.ortools.sat")
    timeout = timedelta(seconds=20)

    student_average = [
        [300],
        [400],
        [400, 450],
        [350, 400, 500],
        [500, 400, 300],
        [300, 450, 400],
        [400, 400, 500],
        [400, 500, 300, 300]
    ]

    def test_basic_1(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_1.dzn")
        the_saddest_student, happiness, happiness_with_average, subjects = self.run_solver(path, 1, 1, 1)

        assert the_saddest_student == 1
        assert subjects[0][0]
        assert happiness == 1
        assert happiness_with_average == 300

    def test_basic_2(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_2.dzn")
        the_saddest_student, happiness, happiness_with_average, subjects = self.run_solver(path, 2, 2, 2)

        assert the_saddest_student == 2
        assert subjects[0][0]
        assert not subjects[0][1]
        assert happiness == 2
        assert happiness_with_average == 400 * 2

    def test_basic_3(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_3.dzn")
        the_saddest_student, happiness, happiness_with_average, subjects = self.run_solver(path, 2, 4, 3)

        assert the_saddest_student == 2

        # student 1
        assert subjects[0][0]
        assert not subjects[0][1]

        # student 2
        assert subjects[1][0]
        assert not subjects[1][1]

        assert happiness == 4
        assert happiness_with_average == 400 * 2 + 450 * 2

    def test_basic_4(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_4.dzn")
        the_saddest_student, happiness, happiness_with_average, subjects = self.run_solver(path, 1, 5, 4)

        assert the_saddest_student == 1

        # student 1
        assert not subjects[0][0]
        assert subjects[0][1]

        # student 2
        assert subjects[1][0]
        assert not subjects[1][1]

        # student 3
        assert subjects[2][0]
        assert not subjects[2][1]

        assert happiness == 5
        assert happiness_with_average == 350 * 1 + 400 * 2 + 500 * 2

    def test_basic_5(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_5.dzn")
        the_saddest_student, happiness, happiness_with_average, subjects = self.run_solver(path, 1, 5, 5)

        assert the_saddest_student == 1

        # student 1
        assert subjects[0][0]
        assert not subjects[0][1]

        # student 2
        assert subjects[1][0]
        assert not subjects[1][1]

        # student 3
        assert not subjects[2][0]
        assert subjects[2][1]

        assert happiness == 5
        assert happiness_with_average == 500 * 2 + 400 * 2 + 300 * 1

    def test_basic_6(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_6.dzn")
        the_saddest_student, happiness, happiness_with_average, subjects = self.run_solver(path, 1, 5, 6)

        assert the_saddest_student == 1

        # student 1
        assert subjects[0][0]
        assert not subjects[0][1]

        # student 2
        assert subjects[1][0]
        assert not subjects[1][1]

        # student 3
        assert not subjects[2][0]
        assert subjects[2][1]

        assert happiness == 5
        assert happiness_with_average == 300 * 2 + 450 * 2 + 400 * 1

    def test_basic_7(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_7.dzn")
        the_saddest_student, happiness, happiness_with_average, subjects = self.run_solver(path, 1, 4, 7)

        assert the_saddest_student == 1

        # student 1
        assert not subjects[0][0]
        assert subjects[0][1]

        # student 2
        assert not subjects[1][0]
        assert subjects[1][1]

        # student 3
        assert subjects[2][0]
        assert not subjects[2][1]

        assert happiness == 4
        assert happiness_with_average == 400 * 1 + 400 * 1 + 500 * 2

    def test_basic_8(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_8.dzn")
        the_saddest_student, happiness, happiness_with_average, subjects = self.run_solver(path, 3, 14, 8)

        assert the_saddest_student == 3
        assert happiness == 4 + 4 + 3 + 3
        assert happiness_with_average == 400 * 4 + 500 * 4 + 300 * 3 + 300 * 3

        # As student 3 has the lowest grade average should be in one of the less preferred subjects.
        assert subjects[2][0] or subjects[2][2]

    def run_solver(self, path_to_input_data, the_saddest_student, happiness, test_data_number) -> tuple[int, int, int, list[list[int]]]:

        model = minizinc.Model()
        model.add_file(self.path_to_model)
        model.add_file(path_to_input_data)

        instance = minizinc.Instance(self.solver, model)

        instance["the_saddest_student_happiness"] = the_saddest_student
        instance["students_happiness"] = happiness
        instance["student_average"] = self.student_average[test_data_number - 1]

        result = instance.solve(processes=self.processes, timeout=self.timeout)

        the_saddest_student = result["the_saddest_student_happiness_var"]
        subjects = result["student_subject"]
        happiness = result["students_happiness_var"]
        happiness_with_average = result["students_happiness_with_average"]

        return the_saddest_student, happiness, happiness_with_average,  subjects

