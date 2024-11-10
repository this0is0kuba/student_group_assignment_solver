from datetime import timedelta

from minizinc import Model, Instance, Solver, Result

from models import InputStudentSubjects, InputStudentGroups
from models.solution import Solution
from models.solution_student_subjects import SolutionStudentSubjects
from tools.preprocessor import Preprocessor


class StudentAssignmentSolver:

    def __init__(self,
                 input_student_subjects: InputStudentSubjects,
                 input_student_groups: InputStudentGroups):

        self.input_student_subjects = input_student_subjects
        self.input_student_groups = input_student_groups

    def solve(self) -> Solution:

        solver: Solver = Solver.lookup("com.google.ortools.sat")

        solution_student_subjects: SolutionStudentSubjects = self._solve_student_subjects(solver)
        print("found student subjects")
        print("number_of_students_in_subject: ", solution_student_subjects.number_of_students_in_subject)
        print()

        solution_student_groups: Solution = self._solve_student_groups(solver, solution_student_subjects)
        return solution_student_groups

    def _solve_student_subjects(self, solver: Solver) -> SolutionStudentSubjects:

        model: Model = Model(r"./app/solver/minizinc/solvers/student_subjects.mzn")
        instance = Instance(solver, model)

        for field, value in self.input_student_subjects.dict().items():
            instance[field] = value

        result = instance.solve(processes=8, timeout=timedelta(seconds=20))

        return SolutionStudentSubjects(
            student_subjects=result["student_subject"],
            number_of_students_in_subject=result["number_of_students_in_subject"]
        )

    def _solve_student_groups(self, solver: Solver, solution_student_subjects: SolutionStudentSubjects) -> Solution:

        model: Model = Model(r"./app/solver/minizinc/solvers/student_groups_old.mzn")
        instance: Instance = self._create_instance_student_groups(solver, model, solution_student_subjects)

        initial_solution = instance.solve(processes=8, timeout=timedelta(seconds=20))
        print("groups_with_common_students: ", initial_solution["groups_with_common_students"])

        return Solution(student_group=initial_solution["student_group"])

    def _create_instance_student_groups(
            self,
            solver: Solver,
            model: Model,
            solution_student_subjects: SolutionStudentSubjects
    ) -> Instance:

        instance = Instance(solver, model)

        # We use the info from the first solver
        self.input_student_groups.student_subject = solution_student_subjects.student_subjects
        self.input_student_groups.min_number_of_groups_in_class = Preprocessor.get_number_of_groups_in_each_class(
            solution_student_subjects.number_of_students_in_subject,
            self.input_student_groups.class_subject,
            self.input_student_groups.class_type,
            self.input_student_groups.class_type_max_students
        )
        self.input_student_groups.max_number_of_groups = max(self.input_student_groups.min_number_of_groups_in_class)

        for field, value in self.input_student_groups.dict().items():
            instance[field] = value

        return instance
