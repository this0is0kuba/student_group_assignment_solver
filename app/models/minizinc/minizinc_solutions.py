from dataclasses import dataclass


@dataclass
class SolutionSubjects1:
    the_saddest_student_happiness: int


@dataclass
class SolutionSubjects2(SolutionSubjects1):
    students_happiness: int
    student_subjects: list[list[bool]]
    number_of_students_in_subject: list[int]


@dataclass
class SolutionGroups:

    # 2 dimensional array about students' groups.
    # Example:
    # student_group[1, 2] = 3 means that student with index 1 is assigned to group number 3 for subject with number 2
    student_group: list[list[int]]
    groups_with_common_students: int
