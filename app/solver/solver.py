from datetime import timedelta

from minizinc import Model, Instance, Solver

from models import InputStudentGroups, InputStudentSubjectsWithAverage, SolutionStudentSubjects1, \
    SolutionStudentSubjects2, InputStudentSubjects1, InputStudentSubjects2, InputStudentGroupsWithFriends, \
    SolutionStudentGroups, Solution
from tools.data_processing import get_number_of_groups_in_each_class


class StudentAssignmentSolver:

    def __init__(self,
                 input_student_subjects_1: InputStudentSubjects1,
                 input_student_subjects_2: InputStudentSubjects2,
                 input_student_subjects_with_average: InputStudentSubjectsWithAverage,
                 input_student_groups: InputStudentGroups,
                 input_student_groups_with_friends: InputStudentGroupsWithFriends | None):

        self.input_student_subjects_1 = input_student_subjects_1
        self.input_student_subjects_2 = input_student_subjects_2
        self.input_student_subjects_with_average = input_student_subjects_with_average
        self.input_student_groups = input_student_groups
        self.input_student_groups_with_friends = input_student_groups_with_friends

    def solve(self) -> Solution:

        solver: Solver = Solver.lookup("com.google.ortools.sat")

        solution_student_subjects_1: SolutionStudentSubjects1 = self._solve_student_subjects_1(solver)
        print("found student_subjects_1")

        solution_student_subjects_2: SolutionStudentSubjects2 = self._solve_student_subjects_2(
            solver,
            solution_student_subjects_1
        )
        print("found student_subjects_2")

        solution_student_subjects_2 = self._solve_student_subjects_with_average(
                solver,
                solution_student_subjects_2
        )
        print("found student_subjects_with_average")

        solution_student_groups: SolutionStudentGroups = self._solve_student_groups(solver, solution_student_subjects_2)
        print("found student_groups")

        if self.input_student_groups_with_friends:
            solution_student_groups_with_average = self._solve_student_groups_with_friends(
                solver,
                solution_student_subjects_2,
                solution_student_groups
            )
            solution_student_groups = solution_student_groups_with_average
            print("found student_groups_with_friends")

        return Solution(
            student_subjects=solution_student_subjects_2.student_subjects,
            student_groups=solution_student_groups.student_group
        )

    def _solve_student_subjects_1(self, solver: Solver) -> SolutionStudentSubjects1:

        model: Model = Model(r"./app/solver/minizinc/solvers/student_subjects_1.mzn")
        instance = Instance(solver, model)

        for field, value in self.input_student_subjects_1.dict().items():
            instance[field] = value

        result = instance.solve(processes=8, timeout=timedelta(seconds=20))

        return SolutionStudentSubjects1(
            the_saddest_student_happiness=result["the_saddest_student_happiness"]
        )

    def _solve_student_subjects_2(self, solver: Solver, solution_student_subjects_1: SolutionStudentSubjects1) -> \
            SolutionStudentSubjects2:

        model: Model = Model(r"./app/solver/minizinc/solvers/student_subjects_2.mzn")
        instance = Instance(solver, model)

        self.input_student_subjects_2.the_saddest_student_happiness = solution_student_subjects_1.the_saddest_student_happiness

        for field, value in self.input_student_subjects_2.dict().items():
            instance[field] = value

        result = instance.solve(processes=8, timeout=timedelta(seconds=20))

        print("students_happiness: ", result["students_happiness"])

        return SolutionStudentSubjects2(
            the_saddest_student_happiness=result["the_saddest_student_happiness_var"],
            students_happiness=result["students_happiness"],
            student_subjects=result["student_subject"],
            number_of_students_in_subject=result["number_of_students_in_subject"]
        )

    def _solve_student_subjects_with_average(
            self,
            solver: Solver,
            solution_student_subjects: SolutionStudentSubjects2
    ) -> SolutionStudentSubjects2:

        model: Model = Model(r"./app/solver/minizinc/solvers/student_subjects_with_average.mzn")
        instance = Instance(solver, model)

        self.input_student_subjects_with_average.students_happiness = solution_student_subjects.students_happiness
        self.input_student_subjects_with_average.the_saddest_student_happiness = solution_student_subjects.the_saddest_student_happiness

        for field, value in self.input_student_subjects_with_average.dict().items():
            instance[field] = value

        result = instance.solve(processes=8, timeout=timedelta(seconds=20))

        return SolutionStudentSubjects2(
            the_saddest_student_happiness=result["the_saddest_student_happiness_var"],
            students_happiness=result["students_happiness_var"],
            student_subjects=result["student_subject"],
            number_of_students_in_subject=result["number_of_students_in_subject"]
        )

    def _solve_student_groups(self, solver: Solver, solution_student_subjects: SolutionStudentSubjects2) -> SolutionStudentGroups:

        model: Model = Model(r"./app/solver/minizinc/solvers/student_groups.mzn")
        instance: Instance = self._create_instance_student_groups(solver, model, solution_student_subjects)

        result = instance.solve(processes=8, timeout=timedelta(seconds=20))
        print("groups_with_common_students: ", result["groups_with_common_students"])

        return SolutionStudentGroups(
            student_group=result["student_group"],
            groups_with_common_students=result["groups_with_common_students"]
        )

    def _solve_student_groups_with_friends(self, solver: Solver, solution_student_subjects: SolutionStudentSubjects2, solution_student_groups: SolutionStudentGroups) -> SolutionStudentGroups:

        model: Model = Model(r"./app/solver/minizinc/solvers/student_groups_with_friends.mzn")
        instance: Instance = self._create_instance_student_groups_with_friends(solver, model, solution_student_subjects, solution_student_groups)

        result = instance.solve(processes=8, timeout=timedelta(seconds=20*3))
        print("groups_with_common_students: ", result["groups_with_common_students_var"])

        return SolutionStudentGroups(
            student_group=result["student_group"],
            groups_with_common_students=result["groups_with_common_students_var"]
        )

    def _create_instance_student_groups(
            self,
            solver: Solver,
            model: Model,
            solution_student_subjects: SolutionStudentSubjects2
    ) -> Instance:

        instance = Instance(solver, model)

        # We use the info from the first solver
        self.input_student_groups.student_subject = solution_student_subjects.student_subjects
        self.input_student_groups.min_number_of_groups_in_class = get_number_of_groups_in_each_class(
            solution_student_subjects.number_of_students_in_subject,
            self.input_student_groups.class_subject,
            self.input_student_groups.class_type,
            self.input_student_groups.class_type_max_students
        )
        self.input_student_groups.max_number_of_groups = max(self.input_student_groups.min_number_of_groups_in_class)

        for field, value in self.input_student_groups.dict().items():
            instance[field] = value

        return instance

    def _create_instance_student_groups_with_friends(
            self,
            solver: Solver,
            model: Model,
            solution_student_subjects: SolutionStudentSubjects2,
            solution_student_groups: SolutionStudentGroups
    ) -> Instance:

        instance = Instance(solver, model)

        # We use the info from the first solver
        self.input_student_groups_with_friends.student_subject = solution_student_subjects.student_subjects
        self.input_student_groups_with_friends.min_number_of_groups_in_class = get_number_of_groups_in_each_class(
            solution_student_subjects.number_of_students_in_subject,
            self.input_student_groups_with_friends.class_subject,
            self.input_student_groups_with_friends.class_type,
            self.input_student_groups_with_friends.class_type_max_students
        )
        self.input_student_groups_with_friends.max_number_of_groups = max(self.input_student_groups.min_number_of_groups_in_class)
        self.input_student_groups_with_friends.groups_with_common_students = solution_student_groups.groups_with_common_students

        for field, value in self.input_student_groups_with_friends.dict().items():
            instance[field] = value

        return instance
