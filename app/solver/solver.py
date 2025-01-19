import os

from minizinc import Model, Instance, Solver

from dependencies.definitions import APP_DIR
from dependencies.logger import logger
from models import InputGroups, InputSubjectsWithAverage, SolutionSubjects1, SolutionSubjects2, \
    InputSubjects1, InputSubjects2, InputGroupsWithFriends, SolutionGroups, Solution

from utils.data_operations import get_number_of_groups_in_each_class
from utils.minizinc_helper import solve_using_minizinc, get_path_to_model


class StudentAssignmentSolver:

    def __init__(
            self,
            input_subjects_1: InputSubjects1,
            input_subjects_2: InputSubjects2,
            input_subjects_with_average: InputSubjectsWithAverage,
            input_groups: InputGroups,
            input_groups_with_friends: InputGroupsWithFriends | None
    ):

        self.input_subjects_1 = input_subjects_1
        self.input_subjects_2 = input_subjects_2
        self.input_subjects_with_average = input_subjects_with_average
        self.input_groups = input_groups
        self.input_groups_with_friends = input_groups_with_friends

    def solve(self) -> Solution:

        solver = Solver.lookup("com.google.ortools.sat")

        solution_subjects_1 = self._solve_subjects_1(solver)

        solution_subjects_2 = self._solve_subjects_2(
            solver,
            solution_subjects_1
        )

        if self.input_subjects_with_average:
            solution_subjects_2 = self._solve_subjects_with_average(
                solver,
                solution_subjects_2
            )

        solution_groups = self._solve_groups(solver, solution_subjects_2)

        if self.input_groups_with_friends:
            solution_groups = self._solve_groups_with_friends(
                solver,
                solution_subjects_2,
                solution_groups
            )

        logger.info(
            "found solution with student_groups: %s",
            solution_groups.student_group
        )

        return Solution(
            student_groups=solution_groups.student_group
        )

    def _solve_subjects_1(self, solver: Solver) -> SolutionSubjects1:

        path_to_model = get_path_to_model("subjects_1")
        model = Model(path_to_model)

        instance = self._create_instance_subjects_1(solver, model)

        result = solve_using_minizinc(instance, seconds=20)

        logger.info(
            "found subjects_1 with the_saddest_student_happiness: %s",
            result["the_saddest_student_happiness"]
        )

        return SolutionSubjects1(
            the_saddest_student_happiness=result["the_saddest_student_happiness"]
        )

    def _solve_subjects_2(
            self,
            solver: Solver,
            solution_subjects_1: SolutionSubjects1
    ) -> SolutionSubjects2:

        path_to_model = get_path_to_model("subjects_2")
        model = Model(path_to_model)

        instance = self._create_instance_subjects_2(solver, model, solution_subjects_1)

        result = solve_using_minizinc(instance, seconds=20)

        logger.info(
            "found subjects_2 with students_happiness: %s",
            result["students_happiness"]
        )

        return SolutionSubjects2(
            the_saddest_student_happiness=result["the_saddest_student_happiness_var"],
            students_happiness=result["students_happiness"],
            student_subjects=result["student_subject"],
            number_of_students_in_subject=result["number_of_students_in_subject"]
        )

    def _solve_subjects_with_average(
            self,
            solver: Solver,
            solution_subjects_2: SolutionSubjects2
    ) -> SolutionSubjects2:

        path_to_model = get_path_to_model("subjects_with_average")
        model = Model(path_to_model)

        instance = self._create_instance_subjects_with_average(solver, model, solution_subjects_2)

        result = solve_using_minizinc(instance, seconds=20)

        logger.info(
            "found subjects_with_average with students_happiness_with_average: %s",
            result["students_happiness_with_average"]
        )

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

        path_to_model = get_path_to_model("groups")
        model = Model(path_to_model)

        instance: Instance = self._create_instance_groups(solver, model, solution_subjects)

        result = solve_using_minizinc(instance, seconds=20)

        logger.info(
            "found groups with groups_with_common_students: %s",
            result["groups_with_common_students"],
        )

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

        path_to_model = get_path_to_model("groups_with_friends")
        model = Model(path_to_model)

        instance: Instance = self._create_instance_groups_with_friends(
            solver,
            model,
            solution_subjects2,
            solution_groups
        )

        result = solve_using_minizinc(instance, seconds=20 * 2)

        logger.info(
            "found groups with number_of_friends: %s",
            result["number_of_friends"],
        )

        return SolutionGroups(
            student_group=result["student_group"],
            groups_with_common_students=result["groups_with_common_students_var"]
        )

    def _create_instance_subjects_1(
            self,
            solver: Solver,
            model: Model
    ) -> Instance:

        instance = Instance(solver, model)

        for field, value in self.input_subjects_1.__dict__.items():
            instance[field] = value

        return instance

    def _create_instance_subjects_2(
            self,
            solver: Solver,
            model: Model,
            solution_subjects_1: SolutionSubjects1
    ) -> Instance:

        instance = Instance(solver, model)

        self.input_subjects_2.the_saddest_student_happiness = \
            solution_subjects_1.the_saddest_student_happiness

        for field, value in self.input_subjects_2.__dict__.items():
            instance[field] = value

        return instance

    def _create_instance_subjects_with_average(
            self,
            solver: Solver,
            model: Model,
            solution_subjects_2: SolutionSubjects2
    ) -> Instance:

        instance = Instance(solver, model)

        self.input_subjects_with_average.students_happiness = solution_subjects_2.students_happiness
        self.input_subjects_with_average.the_saddest_student_happiness = \
            solution_subjects_2.the_saddest_student_happiness

        for field, value in self.input_subjects_with_average.__dict__.items():
            instance[field] = value

        return instance

    def _create_instance_groups(
            self,
            solver: Solver,
            model: Model,
            solution_subjects_2: SolutionSubjects2
    ) -> Instance:

        instance = Instance(solver, model)

        # We use the info from the first solver
        self.input_groups.student_subject = solution_subjects_2.student_subjects
        self.input_groups.min_number_of_groups_in_class = get_number_of_groups_in_each_class(
            solution_subjects_2.number_of_students_in_subject,
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
            solution_subjects_2: SolutionSubjects2,
            solution_groups: SolutionGroups
    ) -> Instance:

        instance = Instance(solver, model)

        # We use the info from the first solver
        self.input_groups_with_friends.student_subject = solution_subjects_2.student_subjects
        self.input_groups_with_friends.min_number_of_groups_in_class = get_number_of_groups_in_each_class(
            solution_subjects_2.number_of_students_in_subject,
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
