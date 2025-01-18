from datetime import timedelta

import minizinc
import os

from minizinc import Solver, Result

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestBasicCases:

    # path to model
    path_subjects_1 = os.path.join(TEST_DIR, "../../../app/solver/minizinc/models/subjects_1.mzn")

    # model's parameters
    processes = 8
    solver = Solver.lookup("com.google.ortools.sat")
    timeout = timedelta(seconds=20)

    def test_basic_1(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_1.dzn")
        result = self.run_solver(path)

        the_saddest_student = result["the_saddest_student_happiness"]
        subjects = result["student_subject"]

        assert the_saddest_student == 1
        assert subjects[0][0]

    def test_basic_2(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_2.dzn")
        result = self.run_solver(path)

        the_saddest_student = result["the_saddest_student_happiness"]
        subjects = result["student_subject"]

        assert the_saddest_student == 2
        assert subjects[0][0]
        assert not subjects[0][1]

    def test_basic_3(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_3.dzn")
        result = self.run_solver(path)

        the_saddest_student = result["the_saddest_student_happiness"]
        subjects = result["student_subject"]

        assert the_saddest_student == 2

        # student 1
        assert subjects[0][0]
        assert not subjects[0][1]

        # student 2
        assert subjects[1][0]
        assert not subjects[1][1]

    def test_basic_4(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_4.dzn")
        result = self.run_solver(path)

        the_saddest_student = result["the_saddest_student_happiness"]

        assert the_saddest_student == 1

    def test_basic_5(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_5.dzn")
        result = self.run_solver(path)

        the_saddest_student = result["the_saddest_student_happiness"]
        subjects = result["student_subject"]

        assert the_saddest_student == 1

        # It should be at least one student in the predetermined subject.
        assert len([student[1] for student in subjects if student[1]]) > 0

    def test_basic_6(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_6.dzn")
        result = self.run_solver(path)

        the_saddest_student = result["the_saddest_student_happiness"]
        subjects = result["student_subject"]

        assert the_saddest_student == 1

        # It should be two students in the predetermined subject
        assert len([student[0] for student in subjects if student[0]]) > 0

        # The first student should be in the subject number 1
        assert subjects[0][0]

    def test_basic_7(self):

        path = os.path.join(TEST_DIR, "../resources/subjects/basic_7.dzn")
        result = self.run_solver(path)

        the_saddest_student = result["the_saddest_student_happiness"]
        subjects = result["student_subject"]

        assert the_saddest_student == 1

        # It should be two students in the predetermined subject
        assert len([student[1] for student in subjects if student[1]]) == 2

        # The last one student should be assigned to the first subject
        assert len([student[0] for student in subjects if student[0]]) == 1

    def run_solver(self, path_to_input_data) -> Result:

        model = minizinc.Model()
        model.add_file(self.path_subjects_1)
        model.add_file(path_to_input_data)

        instance = minizinc.Instance(self.solver, model)
        result = instance.solve(processes=self.processes, timeout=self.timeout)

        return result

