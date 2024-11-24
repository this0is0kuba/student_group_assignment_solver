import math

from models import InputStudentSubjects1, InputStudentSubjects2, InputStudentGroups, InputData, \
    InputStudentSubjectsWithAverage, InputStudentGroupsWithFriends
from models.input_data_elements.custom_constraints import PredeterminedSubjectsForStudent, CustomConstraints, \
    PredeterminedGroupsForStudent


def prepare_input_student_subjects_1(input_data: InputData) -> InputStudentSubjects1:
    basic_info = input_data.information.basic_info
    class_info = input_data.information.class_info
    constraints = input_data.information.constraints
    custom_constraints = input_data.custom_constraints

    preferences_subjects = input_data.preferences.preferences_subjects

    student_preferences = _prepare_list_preferences(preferences_subjects,
                                                    basic_info.number_of_sections,
                                                    basic_info.subject_section)

    if custom_constraints is None:
        custom_constraints = CustomConstraints(
            predetermined_subjects=[],
            predetermined_subjects_for_students=[],
            predetermined_groups_for_students=[]
        )

    return InputStudentSubjects1(
        number_students=basic_info.number_of_students,
        number_instructors=basic_info.number_of_instructors,
        number_subjects=basic_info.number_of_subjects,
        number_class_types=basic_info.number_of_class_types,
        number_section=basic_info.number_of_sections,
        number_classes=class_info.number_of_classes,
        subject_section=basic_info.subject_section,
        class_type=class_info.class_type,
        class_subject=class_info.class_subject,
        class_instructor=class_info.class_instructor,
        class_time_h=class_info.class_time_hours,
        instructor_max_h=constraints.instructor_max_hours,
        student_subjects_in_section=constraints.student_subjects_in_section,
        class_type_min_students=constraints.class_type_min_students,
        class_type_max_students=constraints.class_type_max_students,
        student_preferences=student_preferences,
        number_predetermined_subjects=len(custom_constraints.predetermined_subjects),
        predetermined_subjects=custom_constraints.predetermined_subjects,
        number_predetermined_students=len(custom_constraints.predetermined_subjects_for_students),
        predetermined_students=_prepare_predetermined_students(
            custom_constraints.predetermined_subjects_for_students
        ),
        predetermined_subjects_for_students=_prepare_predetermined_subjects_for_students(
            custom_constraints.predetermined_subjects_for_students,
            basic_info.number_of_subjects
        ),
    )


def prepare_input_student_subjects_2(input_data: InputData) -> InputStudentSubjects2:
    basic_info = input_data.information.basic_info
    class_info = input_data.information.class_info
    constraints = input_data.information.constraints
    custom_constraints = input_data.custom_constraints

    preferences_subjects = input_data.preferences.preferences_subjects

    student_preferences = _prepare_list_preferences(preferences_subjects,
                                                    basic_info.number_of_sections,
                                                    basic_info.subject_section)

    if custom_constraints is None:
        custom_constraints = CustomConstraints(
            predetermined_subjects=[],
            predetermined_subjects_for_students=[],
            predetermined_groups_for_students=[]
        )

    return InputStudentSubjects2(
        number_students=basic_info.number_of_students,
        number_instructors=basic_info.number_of_instructors,
        number_subjects=basic_info.number_of_subjects,
        number_class_types=basic_info.number_of_class_types,
        number_section=basic_info.number_of_sections,
        number_classes=class_info.number_of_classes,
        subject_section=basic_info.subject_section,
        class_type=class_info.class_type,
        class_subject=class_info.class_subject,
        class_instructor=class_info.class_instructor,
        class_time_h=class_info.class_time_hours,
        instructor_max_h=constraints.instructor_max_hours,
        student_subjects_in_section=constraints.student_subjects_in_section,
        class_type_min_students=constraints.class_type_min_students,
        class_type_max_students=constraints.class_type_max_students,
        student_preferences=student_preferences,
        number_predetermined_subjects=len(custom_constraints.predetermined_subjects),
        predetermined_subjects=custom_constraints.predetermined_subjects,
        number_predetermined_students=len(custom_constraints.predetermined_subjects_for_students),
        predetermined_students=_prepare_predetermined_students(
            custom_constraints.predetermined_subjects_for_students
        ),
        predetermined_subjects_for_students=_prepare_predetermined_subjects_for_students(
            custom_constraints.predetermined_subjects_for_students,
            basic_info.number_of_subjects
        ),
        the_saddest_student_happiness=None
    )


def prepare_input_student_subjects_with_average(input_data: InputData) -> InputStudentSubjectsWithAverage:
    basic_info = input_data.information.basic_info
    class_info = input_data.information.class_info
    constraints = input_data.information.constraints
    custom_constraints = input_data.custom_constraints

    preferences_subjects = input_data.preferences.preferences_subjects

    student_average = _prepare_student_average(basic_info.student_average)
    student_preferences = _prepare_list_preferences(preferences_subjects,
                                                    basic_info.number_of_sections,
                                                    basic_info.subject_section)

    if custom_constraints is None:
        custom_constraints = CustomConstraints(
            predetermined_subjects=[],
            predetermined_subjects_for_students=[],
            predetermined_groups_for_students=[]
        )

    return InputStudentSubjectsWithAverage(
        number_students=basic_info.number_of_students,
        number_instructors=basic_info.number_of_instructors,
        number_subjects=basic_info.number_of_subjects,
        number_class_types=basic_info.number_of_class_types,
        number_section=basic_info.number_of_sections,
        number_classes=class_info.number_of_classes,
        student_average=student_average,
        subject_section=basic_info.subject_section,
        class_type=class_info.class_type,
        class_subject=class_info.class_subject,
        class_instructor=class_info.class_instructor,
        class_time_h=class_info.class_time_hours,
        instructor_max_h=constraints.instructor_max_hours,
        student_subjects_in_section=constraints.student_subjects_in_section,
        class_type_min_students=constraints.class_type_min_students,
        class_type_max_students=constraints.class_type_max_students,
        student_preferences=student_preferences,
        number_predetermined_subjects=len(custom_constraints.predetermined_subjects),
        predetermined_subjects=custom_constraints.predetermined_subjects,
        number_predetermined_students=len(custom_constraints.predetermined_subjects_for_students),
        predetermined_students=_prepare_predetermined_students(
            custom_constraints.predetermined_subjects_for_students
        ),
        predetermined_subjects_for_students=_prepare_predetermined_subjects_for_students(
            custom_constraints.predetermined_subjects_for_students,
            basic_info.number_of_subjects
        ),
        students_happiness=None,  # We will set this parameter after receiving it from student_subjects solver
        the_saddest_student_happiness=None  # We will set this parameter after receiving it from student_subjects solver
    )


def prepare_input_student_groups(input_data: InputData) -> InputStudentGroups:
    basic_info = input_data.information.basic_info
    class_info = input_data.information.class_info
    constraints = input_data.information.constraints
    custom_constraints = input_data.custom_constraints

    if custom_constraints is None:
        custom_constraints = CustomConstraints(
            predetermined_subjects=[],
            predetermined_subjects_for_students=[],
            predetermined_groups_for_students=[]
        )

    return InputStudentGroups(
        number_students=basic_info.number_of_students,
        number_instructors=basic_info.number_of_instructors,
        number_subjects=basic_info.number_of_subjects,
        number_class_types=basic_info.number_of_class_types,
        number_section=basic_info.number_of_sections,
        number_classes=class_info.number_of_classes,
        class_type=class_info.class_type,
        class_subject=class_info.class_subject,
        class_instructor=class_info.class_instructor,
        class_time_h=class_info.class_time_hours,
        instructor_max_h=constraints.instructor_max_hours,
        class_type_min_students=constraints.class_type_min_students,
        class_type_max_students=constraints.class_type_max_students,
        number_predetermined_students=len(custom_constraints.predetermined_groups_for_students),
        predetermined_students=[
            groups_info.student_id for groups_info in custom_constraints.predetermined_groups_for_students
        ],
        predetermined_classes_for_students=_prepare_predetermined_classes(
            custom_constraints.predetermined_groups_for_students,
            class_info.number_of_classes
        ),
        predetermined_groups_for_students=_prepare_predetermined_groups(
            custom_constraints.predetermined_groups_for_students,
            class_info.number_of_classes
        ),
        student_subject=None,  # We will set this parameter after receiving it from student_subjects solver
        max_number_of_groups=None,  # We will set this parameter after receiving more info from student_subjects solver
        min_number_of_groups_in_class=None,  # We will set this parameter after receiving more info from
                                             # student_subjects solver
    )


def prepare_input_student_groups_with_friends(input_data: InputData) -> InputStudentGroupsWithFriends:
    basic_info = input_data.information.basic_info
    class_info = input_data.information.class_info
    constraints = input_data.information.constraints
    custom_constraints = input_data.custom_constraints

    friends_info = input_data.preferences.friends_info

    if custom_constraints is None:
        custom_constraints = CustomConstraints(
            predetermined_subjects=[],
            predetermined_subjects_for_students=[],
            predetermined_groups_for_students=[]
        )

    return InputStudentGroupsWithFriends(
        number_students=basic_info.number_of_students,
        number_instructors=basic_info.number_of_instructors,
        number_subjects=basic_info.number_of_subjects,
        number_class_types=basic_info.number_of_class_types,
        number_section=basic_info.number_of_sections,
        number_classes=class_info.number_of_classes,
        class_type=class_info.class_type,
        class_subject=class_info.class_subject,
        class_instructor=class_info.class_instructor,
        class_time_h=class_info.class_time_hours,
        instructor_max_h=constraints.instructor_max_hours,
        class_type_min_students=constraints.class_type_min_students,
        class_type_max_students=constraints.class_type_max_students,
        number_predetermined_students=len(custom_constraints.predetermined_groups_for_students),
        predetermined_students=[
            groups_info.student_id for groups_info in custom_constraints.predetermined_groups_for_students
        ],
        predetermined_classes_for_students=_prepare_predetermined_classes(
            custom_constraints.predetermined_groups_for_students,
            class_info.number_of_classes
        ),
        predetermined_groups_for_students=_prepare_predetermined_groups(
            custom_constraints.predetermined_groups_for_students,
            class_info.number_of_classes
        ),
        student_subject=None,  # We will set this parameter after receiving it from student_subjects solver
        max_number_of_groups=None,  # We will set this parameter after receiving more info from student_subjects solver
        min_number_of_groups_in_class=None,  # We will set this parameter after receiving more info from
                                             # student_subjects solver
        friends_max_number=friends_info.max_number_friends,
        friends_array=friends_info.friends_array,
        groups_with_common_students=None  # We will set this parameter after receiving it from student_groups solver
    )


def get_number_of_groups_in_each_class(
        number_of_students_in_subject: list[int],
        class_subject: list[int],
        class_type: list[int],
        class_type_max_students: list[int]
) -> list[int]:
    number_of_groups_in_class = []

    for i in range(len(class_subject)):
        n = number_of_students_in_subject[class_subject[i] - 1]
        max_n_in_class = class_type_max_students[class_type[i] - 1]

        number_of_groups_in_class.append(math.ceil(n / max_n_in_class))

    return number_of_groups_in_class


def _prepare_predetermined_students(
    predetermined_subjects_for_students: list[PredeterminedSubjectsForStudent],
) -> list[int]:

    prepared_list = []

    for predetermined_subjects in predetermined_subjects_for_students:

        student_id = predetermined_subjects.student_id
        prepared_list.append(student_id)

    return prepared_list


def _prepare_predetermined_subjects_for_students(
        predetermined_subjects_for_students: list[PredeterminedSubjectsForStudent],
        number_of_subjects: int
) -> list[list[int]]:

    prepared_list = []

    for i in range(len(predetermined_subjects_for_students)):

        subjects = predetermined_subjects_for_students[i].predetermined_subjects_for_student
        prepared_subjects = subjects[:]

        # Fill the rest of list with zeroes for minizinc
        prepared_subjects.extend([0 for _ in range(number_of_subjects - len(subjects))])
        prepared_list.append(prepared_subjects)

    return prepared_list


def _prepare_student_average(list_average: list[float]) -> list[int]:
    new_list_average = []

    for avg in list_average:
        new_list_average.append(int(avg * 100))

    return new_list_average


def _prepare_list_preferences(
        list_preferences: list[list[int]], section_number: int,
        subject_section: list[int]
):
    # how much subjects is in each section
    section_subject_amount = [0 for _ in range(section_number)]

    for section in range(1, section_number + 1):
        for current_section in subject_section:

            if current_section == section:
                section_subject_amount[section - 1] += 1

    max_number_of_subjects = max(section_subject_amount)

    new_list_preferences = []
    for i in range(len(list_preferences)):

        list_student_preferences = []
        for j in range(len(list_preferences[0])):
            reverted_value = section_subject_amount[subject_section[j] - 1] - list_preferences[i][j] + 1
            new_value = round(
                reverted_value * (max_number_of_subjects / section_subject_amount[subject_section[j] - 1]))

            list_student_preferences.append(
                new_value
            )

        new_list_preferences.append(list_student_preferences)

    return new_list_preferences


def _prepare_predetermined_classes(
        predetermined_groups_for_students: list[PredeterminedGroupsForStudent],
        number_of_classes: int
):
    prepared_list: list[list[int]] = []

    for group_info in predetermined_groups_for_students:

        classes = group_info.predetermined_classes_for_student
        prepared_classes = classes[:]

        # Fill the rest of list with zeroes for minizinc
        prepared_classes.extend([0 for _ in range(number_of_classes - len(classes))])
        prepared_list.append(prepared_classes)

    return prepared_list


def _prepare_predetermined_groups(
        predetermined_groups_for_students: list[PredeterminedGroupsForStudent],
        number_of_classes: int
):
    prepared_list: list[list[int]] = []

    for group_info in predetermined_groups_for_students:

        groups = group_info.predetermined_groups_for_student
        prepared_groups = groups[:]

        # Fill the rest of list with zeroes for minizinc
        prepared_groups.extend([0 for _ in range(number_of_classes - len(groups))])
        prepared_list.append(prepared_groups)

    return prepared_list