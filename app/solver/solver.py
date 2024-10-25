from minizinc import Model, Instance, Solver, Result

from models import InputStudentSubjects, InputStudentGroups
from models.minizinc_solution import MinizincSolution


class StudentAssignmentSolver:

    def __init__(self,
                 input_student_subjects: InputStudentSubjects,
                 input_student_groups: InputStudentGroups):

        self.input_student_subjects = input_student_subjects
        self.input_student_groups = input_student_groups

    def solve(self) -> MinizincSolution:

        solver: Solver = Solver.lookup("com.google.ortools.sat")

        result_student_subjects = self._solve_student_subjects(solver)
        result_student_groups = self._solve_student_groups(solver, result_student_subjects)

        return self._get_solution(result_student_groups)

    def _solve_student_subjects(self, solver: Solver) -> Result:

        model: Model = Model(r"./app/solver/minizinc/solvers/student_subjects.mzn")
        instance: Instance = self._create_instance_student_subjects(solver, model)

        return instance.solve()

    def _solve_student_groups(self, solver: Solver, result_student_preferences: Result) -> Result:

        model: Model = Model(r"./app/solver/minizinc/solvers/student_groups.mzn")
        instance: Instance = self._create_instance_student_groups(solver, model, result_student_preferences)

        return instance.solve()

    def _create_instance_student_subjects(self, solver: Solver, model: Model) -> Instance:

        instance = Instance(solver, model)

        for field, value in self.input_student_subjects.dict().items():
            instance[field] = value

        return instance

    def _create_instance_student_groups(
            self,
            solver: Solver,
            model: Model,
            result_student_preferences: Result
    ) -> Instance:

        instance = Instance(solver, model)

        for field, value in self.input_student_groups.dict().items():
            instance[field] = value

        # We have to add student_subject which we get from the first solver
        instance["student_subject"] = result_student_preferences["student_subject"]

        return instance

    def _get_solution(self, result: Result) -> MinizincSolution:
        return result["student_group"]
