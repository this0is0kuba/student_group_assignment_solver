from datetime import timedelta

from minizinc import Solver, Model, Instance

from models import InputStudentGroups
from models.solution import Solution
from random import sample

from models.solution_student_subjects import SolutionStudentSubjects
from tools.preprocessor import Preprocessor


class LNS:

    def __init__(self, input_student_groups: InputStudentGroups, solution_student_subjects: SolutionStudentSubjects):

        self.input_student_groups = input_student_groups
        self.solution_student_subjects = solution_student_subjects
        self.solver = Solver.lookup("com.google.ortools.sat")

        self.current_best_solution, self.current_best_score = self._find_initial_groups()

    def solve(self) -> Solution:

        print(-1, ") " "score: ", self.current_best_score, ", best score:", self.current_best_score)

        number_of_all_classes = self.input_student_groups.number_classes
        number_of_active_classes = min(12, number_of_all_classes)

        for i in range(20):

            model: Model = Model(r"./app/solver/minizinc/solvers/student_groups_lns_old.mzn")
            instance: Instance = self._create_instance_student_groups(self.solver, model)

            frozen_classes = self._find_random_classes(number_of_active_classes)
            print(frozen_classes)

            instance["number_frozen_classes"] = number_of_all_classes - number_of_active_classes
            instance["frozen_classes"] = frozen_classes
            instance["current_best_groups"] = self.current_best_solution

            result = instance.solve(processes=8, timeout=timedelta(seconds=20))
            solution, score = result["student_group"], result["groups_with_common_students"]

            if score <= self.current_best_score:
                self.current_best_score = score
                self.current_best_solution = solution

            print(i, ") " "score: ", score, ", best score:", self.current_best_score)

        return self.current_best_solution

    def _find_random_classes(self, active_classes):

        all_classes = self.input_student_groups.number_classes

        scope = range(1, self.input_student_groups.number_classes + 1)

        frozen_classes = sample(scope, all_classes - active_classes)
        return frozen_classes

    def _find_initial_groups(self) -> (Solution, int):

        model: Model = Model(r"./app/solver/minizinc/solvers/student_groups_old.mzn")
        instance: Instance = self._create_instance_student_groups(self.solver, model)

        initial_solution = instance.solve(processes=8)

        return initial_solution["student_group"], initial_solution["groups_with_common_students"]

    def _create_instance_student_groups(
            self,
            solver: Solver,
            model: Model
    ) -> Instance:

        instance = Instance(solver, model)

        # We use the info from the first solver
        self.input_student_groups.student_subject = self.solution_student_subjects.student_subjects
        self.input_student_groups.min_number_of_groups_in_class = Preprocessor.get_number_of_groups_in_each_class(
            self.solution_student_subjects.number_of_students_in_subject,
            self.input_student_groups.class_subject,
            self.input_student_groups.class_type,
            self.input_student_groups.class_type_max_students
        )
        self.input_student_groups.max_number_of_groups = max(self.input_student_groups.min_number_of_groups_in_class)

        for field, value in self.input_student_groups.dict().items():
            instance[field] = value

        return instance

