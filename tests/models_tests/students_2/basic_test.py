from datetime import timedelta

import minizinc
import os

from minizinc import Solver

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestBasicCases:

    # path to model
    path_to_model = os.path.join(TEST_DIR, "../../../app/solver/minizinc/models/subjects_2.mzn")

    # model's parameters
    processes = 8
    solver = Solver.lookup("com.google.ortools.sat")
    timeout = timedelta(seconds=20)

    def test_basic_1(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_1.dzn")
        the_saddest_student, happiness, subjects = self.run_solver(path, 1)

        assert the_saddest_student == 1
        assert happiness == 1
        assert subjects[0][0]

    def test_basic_2(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_2.dzn")
        the_saddest_student, happiness, subjects = self.run_solver(path, 2)

        assert the_saddest_student == 2
        assert subjects[0][0]
        assert not subjects[0][1]
        assert happiness == 2

    def test_basic_3(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_3.dzn")
        the_saddest_student, happiness, subjects = self.run_solver(path, 2)

        assert the_saddest_student == 2

        # student 1
        assert subjects[0][0]
        assert not subjects[0][1]

        # student 2
        assert subjects[1][0]
        assert not subjects[1][1]

        assert happiness == 4

    def test_basic_4(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_4.dzn")
        the_saddest_student, happiness, subjects = self.run_solver(path, 1)

        assert the_saddest_student == 1

        # It should be two students in the most preferred subject.
        assert len([student[0] for student in subjects if student[0]]) == 2

        assert happiness == 5

    def test_basic_5(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_5.dzn")
        the_saddest_student, happiness, subjects = self.run_solver(path, 1)

        assert the_saddest_student == 1

        # It should be only one student in the predetermined subject.
        assert len([student[1] for student in subjects if student[1]]) == 1

        assert happiness == 5

    def test_basic_6(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_6.dzn")
        the_saddest_student, happiness, subjects = self.run_solver(path, 1)

        assert the_saddest_student == 1

        # It should be two students in the predetermined subject
        assert len([student[0] for student in subjects if student[0]]) == 2

        # The first student should be in the subject number 1
        assert subjects[0][0]

        assert happiness == 5

    def test_basic_7(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_7.dzn")
        the_saddest_student, happiness, subjects = self.run_solver(path, 1)

        assert the_saddest_student == 1

        # It should be two students in the predetermined subject
        assert len([student[1] for student in subjects if student[1]]) == 2

        # The last one student should be assigned to the first subject
        assert len([student[0] for student in subjects if student[0]]) == 1

        assert happiness == 4

    def test_basic_8(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_8.dzn")
        the_saddest_student, happiness, subjects = self.run_solver(path, 3)

        assert the_saddest_student == 3
        assert happiness == 4 + 4 + 3 + 3

    def run_solver(self, path_to_input_data, the_saddest_student) -> tuple[int, int, list[list[int]]]:

        model = minizinc.Model()
        model.add_file(self.path_to_model)
        model.add_file(path_to_input_data)

        instance = minizinc.Instance(self.solver, model)

        instance["the_saddest_student_happiness"] = the_saddest_student

        result = instance.solve(processes=self.processes, timeout=self.timeout)

        the_saddest_student = result["the_saddest_student_happiness_var"]
        subjects = result["student_subject"]
        happiness = result["students_happiness"]

        return the_saddest_student, happiness, subjects

