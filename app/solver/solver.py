from minizinc import Model, Instance, Solver, Result

from models import InputStudentSubjects, InputStudentGroups
from models.solution import Solution
from models.solution_student_subjects import SolutionStudentSubjects
from solver.large_neighbourhood_search import LNS


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

        lns = LNS(self.input_student_groups, solution_student_subjects)
        student_groups = lns.solve()

        return student_groups

    def _solve_student_subjects(self, solver: Solver) -> SolutionStudentSubjects:

        model: Model = Model(r"./app/solver/minizinc/solvers/student_subjects.mzn")
        instance = Instance(solver, model)

        for field, value in self.input_student_subjects.dict().items():
            instance[field] = value

        result = instance.solve(processes=8)

        return SolutionStudentSubjects(
            student_subjects=result["student_subject"],
            number_of_students_in_subject=result["number_of_students_in_subject"]
        )
