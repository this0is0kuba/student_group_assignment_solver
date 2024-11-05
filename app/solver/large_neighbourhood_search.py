from minizinc import Result, Solver, Model, Instance

from models import InputStudentGroups
from models.solution import Solution
from random import sample


class LNS:

    def __init__(self, input_student_groups: InputStudentGroups, student_subjects: Result):

        self.input_student_groups = input_student_groups
        self.student_subjects = student_subjects
        self.solver = Solver.lookup("com.google.ortools.sat")

        self.current_best_solution, self.current_best_score = self._find_initial_groups()

    def solve(self) -> Solution:

        number_of_all_subjects = self.input_student_groups.number_subjects
        number_of_active_subjects = min(4, number_of_all_subjects)

        for i in range(5):

            model: Model = Model(r"./app/solver/minizinc/solvers/student_groups_lns.mzn")
            instance: Instance = self._create_instance_student_groups(self.solver, model)

            frozen_subjects = self._find_random_subjects(number_of_active_subjects)

            instance["number_frozen_subjects"] = number_of_all_subjects - number_of_active_subjects
            instance["frozen_subjects"] = frozen_subjects
            instance["current_best_groups"] = self.current_best_solution

            result = instance.solve()
            solution, score = result["student_group"], result["groups_with_common_students"]

            if score >= self.current_best_score:
                self.current_best_score = score
                self.current_best_solution = solution

            print(i, ". " "score: ", score)

        return self.current_best_solution

    def _find_random_subjects(self, active_subjects):

        all_subjects = self.input_student_groups.number_subjects

        scope = range(1, self.input_student_groups.number_subjects)

        frozen_subjects = sample(scope, all_subjects - active_subjects)
        return frozen_subjects

    def _find_initial_groups(self) -> (Solution, int):

        model: Model = Model(r"./app/solver/minizinc/solvers/student_groups.mzn")
        instance: Instance = self._create_instance_student_groups(self.solver, model)

        initial_solution = instance.solve()

        return initial_solution["student_group"], initial_solution["groups_with_common_students"]

    def _create_instance_student_groups(
            self,
            solver: Solver,
            model: Model
    ) -> Instance:

        instance = Instance(solver, model)

        for field, value in self.input_student_groups.dict().items():
            instance[field] = value

        # We have to add student_subject which we get from the first solver
        instance["student_subject"] = self.student_subjects["student_subject"]

        return instance

