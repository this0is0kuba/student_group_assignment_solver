from minizinc import Model, Instance, Solver, Result

from models import InputStudentSubjects, InputStudentGroups
from models.solution import Solution
from solver.large_neighbourhood_search import LNS


class StudentAssignmentSolver:

    def __init__(self,
                 input_student_subjects: InputStudentSubjects,
                 input_student_groups: InputStudentGroups):

        self.input_student_subjects = input_student_subjects
        self.input_student_groups = input_student_groups

    def solve(self) -> Solution:

        solver: Solver = Solver.lookup("com.google.ortools.sat")

        result_student_subjects = self._solve_student_subjects(solver)
        print("found student subjects")

        lns = LNS(self.input_student_groups, result_student_subjects)
        student_groups = lns.solve()

        return student_groups

    def _solve_student_subjects(self, solver: Solver) -> Result:

        model: Model = Model(r"./app/solver/minizinc/solvers/student_subjects.mzn")
        instance = Instance(solver, model)

        for field, value in self.input_student_subjects.dict().items():
            instance[field] = value

        return instance.solve(processes=8)
