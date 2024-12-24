from dataclasses import dataclass


@dataclass
class InputMinizincBase:

    number_students: int
    number_instructors: int
    number_subjects: int
    number_class_types: int
    number_classes: int
    class_type: list[int]
    class_subject: list[int]
    class_instructor: list[int]
    class_time_h: list[int]
    instructor_max_h: list[int]
    class_type_min_students: list[int]
    class_type_max_students: list[int]
    number_conditional_students: int
    conditional_students: list[int]


@dataclass
class InputSubjects1(InputMinizincBase):

    number_section: int
    subject_section: list[int]
    student_subjects_in_section: list[list[int]]
    student_preferences: list[list[int]]
    number_predetermined_subjects: int
    predetermined_subjects: list[int]
    number_predetermined_students: int
    predetermined_students: list[int]
    predetermined_subjects_for_students: list[list[int]]


@dataclass
class InputSubjects2(InputSubjects1):

    # Info about the saddest student from student_subjects_1 solver
    the_saddest_student_happiness: int | None


@dataclass
class InputSubjectsWithAverage(InputSubjects2):

    student_average: list[int]

    # Info about happiness from student_subjects_2 solver
    students_happiness: int | None


@dataclass
class InputGroups(InputMinizincBase):

    number_predetermined_students: int
    predetermined_students: list[int]
    predetermined_classes_for_students: list[list[int]]
    predetermined_groups_for_students: list[list[int]]
    student_subject: list[list[int]] | None
    max_number_of_groups: int | None
    min_number_of_groups_in_class: list[int] | None


@dataclass
class InputGroupsWithFriends(InputGroups):

    # Info about students' friends
    friends_array: list[list[int]]
    friends_max_number: int

    # Info about groups from student_groups solver
    groups_with_common_students: int | None
