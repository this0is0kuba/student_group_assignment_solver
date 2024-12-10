from datetime import timedelta
from minizinc import Model, Instance, Solver

from models import InputGroups, InputSubjectsWithAverage, SolutionSubjects1, SolutionSubjects2, \
    InputSubjects1, InputSubjects2, InputGroupsWithFriends, SolutionGroups, Solution

from tools.data_processing import get_number_of_groups_in_each_class


class StudentAssignmentSolver:

    def __init__(self,
                 input_subjects_1: InputSubjects1,
                 input_subjects_2: InputSubjects2,
                 input_subjects_with_average: InputSubjectsWithAverage,
                 input_groups: InputGroups,
                 input_groups_with_friends: InputGroupsWithFriends | None):

        self.input_subjects_1 = input_subjects_1
        self.input_subjects_2 = input_subjects_2
        self.input_subjects_with_average = input_subjects_with_average
        self.input_groups = input_groups
        self.input_groups_with_friends = input_groups_with_friends

    def solve(self) -> Solution:

        solver = Solver.lookup("com.google.ortools.sat")

        solution_subjects_1 = self._solve_subjects_1(solver)
        print("found student_subjects_1")

        solution_subjects_2 = self._solve_subjects_2(
            solver,
            solution_subjects_1
        )
        print("found student_subjects_2")

        solution_subjects_2 = self._solve_subjects_with_average(
                solver,
                solution_subjects_2
        )
        print("found student_subjects_with_average")

        solution_groups = self._solve_groups(solver, solution_subjects_2)
        print("found student_groups")

        if self.input_groups_with_friends:

            solution_groups = self._solve_groups_with_friends(
                solver,
                solution_subjects_2,
                solution_groups
            )
            print("found student_groups_with_friends")

        return Solution(
            student_subjects=solution_subjects_2.student_subjects,
            student_groups=solution_groups.student_group
        )

    def _solve_subjects_1(self, solver: Solver) -> SolutionSubjects1:

        model = Model(r"./app/solver/minizinc/solvers/subjects_1.mzn")
        instance = Instance(solver, model)

        for field, value in self.input_subjects_1.__dict__.items():
            instance[field] = value

        result = instance.solve(processes=8, timeout=timedelta(seconds=20))

        return SolutionSubjects1(
            the_saddest_student_happiness=result["the_saddest_student_happiness"]
        )

    def _solve_subjects_2(
            self,
            solver: Solver,
            solution_subjects_1: SolutionSubjects1
    ) -> SolutionSubjects2:

        model = Model(r"./app/solver/minizinc/solvers/subjects_2.mzn")
        instance = Instance(solver, model)

        self.input_subjects_2.the_saddest_student_happiness = \
            solution_subjects_1.the_saddest_student_happiness

        for field, value in self.input_subjects_2.__dict__.items():
            instance[field] = value

        result = instance.solve(processes=8, timeout=timedelta(seconds=20))

        print("students_happiness: ", result["students_happiness"])

        return SolutionSubjects2(
            the_saddest_student_happiness=result["the_saddest_student_happiness_var"],
            students_happiness=result["students_happiness"],
            student_subjects=result["student_subject"],
            number_of_students_in_subject=result["number_of_students_in_subject"]
        )

    def _solve_subjects_with_average(
            self,
            solver: Solver,
            solution_subjects: SolutionSubjects2
    ) -> SolutionSubjects2:

        model = Model(r"./app/solver/minizinc/solvers/subjects_with_average.mzn")
        instance = Instance(solver, model)

        self.input_subjects_with_average.students_happiness = solution_subjects.students_happiness
        self.input_subjects_with_average.the_saddest_student_happiness = \
            solution_subjects.the_saddest_student_happiness

        for field, value in self.input_subjects_with_average.__dict__.items():
            instance[field] = value

        result = instance.solve(processes=8, timeout=timedelta(seconds=20))

        return SolutionSubjects2(
            the_saddest_student_happiness=result["the_saddest_student_happiness_var"],
            students_happiness=result["students_happiness_var"],
            student_subjects=result["student_subject"],
            number_of_students_in_subject=result["number_of_students_in_subject"]
        )

    def _solve_groups(
            self,
            solver: Solver,
            solution_subjects: SolutionSubjects2
    ) -> SolutionGroups:

        model = Model(r"./app/solver/minizinc/solvers/groups.mzn")
        instance: Instance = self._create_instance_groups(solver, model, solution_subjects)

        result = instance.solve(processes=8, timeout=timedelta(seconds=20))
        print("groups_with_common_students: ", result["groups_with_common_students"])

        return SolutionGroups(
            student_group=result["student_group"],
            groups_with_common_students=result["groups_with_common_students"]
        )

    def _solve_groups_with_friends(
            self,
            solver: Solver,
            solution_subjects2: SolutionSubjects2,
            solution_groups: SolutionGroups
    ) -> SolutionGroups:

        model: Model = Model(r"./app/solver/minizinc/solvers/groups_with_friends.mzn")
        instance: Instance = self._create_instance_groups_with_friends(
            solver,
            model,
            solution_subjects2,
            solution_groups
        )

        result = instance.solve(processes=8, timeout=timedelta(seconds=20*3))
        print("groups_with_common_students: ", result["groups_with_common_students_var"])

        return SolutionGroups(
            student_group=result["student_group"],
            groups_with_common_students=result["groups_with_common_students_var"]
        )

    def _create_instance_groups(
            self,
            solver: Solver,
            model: Model,
            solution_subjects: SolutionSubjects2
    ) -> Instance:

        instance = Instance(solver, model)

        # We use the info from the first solver
        self.input_groups.student_subject = solution_subjects.student_subjects
        self.input_groups.min_number_of_groups_in_class = get_number_of_groups_in_each_class(
            solution_subjects.number_of_students_in_subject,
            self.input_groups.class_subject,
            self.input_groups.class_type,
            self.input_groups.class_type_max_students
        )
        self.input_groups.max_number_of_groups = max(self.input_groups.min_number_of_groups_in_class)

        for field, value in self.input_groups.__dict__.items():
            instance[field] = value

        return instance

    def _create_instance_groups_with_friends(
            self,
            solver: Solver,
            model: Model,
            solution_subjects: SolutionSubjects2,
            solution_groups: SolutionGroups
    ) -> Instance:

        instance = Instance(solver, model)

        # We use the info from the first solver
        self.input_groups_with_friends.student_subject = solution_subjects.student_subjects
        self.input_groups_with_friends.min_number_of_groups_in_class = get_number_of_groups_in_each_class(
            solution_subjects.number_of_students_in_subject,
            self.input_groups_with_friends.class_subject,
            self.input_groups_with_friends.class_type,
            self.input_groups_with_friends.class_type_max_students
        )

        self.input_groups_with_friends.max_number_of_groups = \
            max(self.input_groups.min_number_of_groups_in_class)

        self.input_groups_with_friends.groups_with_common_students = \
            solution_groups.groups_with_common_students

        for field, value in self.input_groups_with_friends.__dict__.items():
            instance[field] = value

        return instance
