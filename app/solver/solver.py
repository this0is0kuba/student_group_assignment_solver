from minizinc import Model, Instance, Solver, Result

from models import InputStudentPreferences, InputData
from models.input_parallel_groups import InputParallelGroups
from models.minizinc_solution import MinizincSolution


class StudentAssignmentSolver:

    def __init__(self,
                 input_student_preferences: InputStudentPreferences,
                 input_parallel_groups: InputParallelGroups):

        self.input_student_preferences = input_student_preferences
        self.input_parallel_groups = input_parallel_groups

    def solve(self) -> MinizincSolution:

        solver: Solver = Solver.lookup("com.google.ortools.sat")

        result_student_preferences = self._solve_student_preferences(solver)
        result_parallel_groups = self._solve_parallel_groups(solver, result_student_preferences)

        return self._get_solution(result_parallel_groups)

    def _solve_student_preferences(self, solver: Solver) -> Result:

        model: Model = Model(r"./app/solver/minizinc/solvers/student_preferences.mzn")
        instance: Instance = self._create_instance_student_preferences(solver, model)

        return instance.solve()

    def _solve_parallel_groups(self, solver: Solver, result_student_preferences: Result) -> Result:

        model: Model = Model(r"./app/solver/minizinc/solvers/parallel_groups.mzn")
        instance: Instance = self._create_instance_parallel_groups(solver, model, result_student_preferences)

        return instance.solve()

    def _create_instance_student_preferences(self, solver: Solver, model: Model) -> Instance:

        instance = Instance(solver, model)

        for field, value in self.input_student_preferences.dict().items():
            instance[field] = value

        return instance

    def _create_instance_parallel_groups(
            self,
            solver: Solver,
            model: Model,
            result_student_preferences: Result
    ) -> Instance:

        instance = Instance(solver, model)

        for field, value in self.input_parallel_groups.dict().items():
            instance[field] = value

        instance["student_subject"] = result_student_preferences["student_subject"]

        return instance

    def _get_solution(self, result: Result) -> MinizincSolution:
        return result["student_group"]
