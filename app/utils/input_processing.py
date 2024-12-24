from models import InputSubjects1, InputSubjects2, InputGroups, InputData, InputSubjectsWithAverage, \
    InputGroupsWithFriends, CustomConstraints
from utils.processing_helper import _prepare_list_preferences, _prepare_predetermined_students, \
    _prepare_predetermined_subjects_for_students, _prepare_student_average, _prepare_predetermined_classes, \
    _prepare_predetermined_groups


def prepare_for_subjects_1(input_data: InputData) -> InputSubjects1:

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
            predetermined_groups_for_students=[],
            conditional_students=[]
        )

    return InputSubjects1(
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
        number_conditional_students=len(custom_constraints.conditional_students),
        conditional_students=custom_constraints.conditional_students
    )


def prepare_for_subjects_2(input_data: InputData) -> InputSubjects2:

    input_subjects_1 = prepare_for_subjects_1(input_data)

    return InputSubjects2(
        **input_subjects_1.__dict__,

        # We will set this parameter after receiving it from student_subjects_1 solver
        the_saddest_student_happiness=None
    )


def prepare_for_subjects_with_average(input_data: InputData) -> InputSubjectsWithAverage:

    input_subjects_2 = prepare_for_subjects_2(input_data)
    student_average = _prepare_student_average(input_data.information.basic_info.student_average)

    return InputSubjectsWithAverage(
        **input_subjects_2.__dict__,
        student_average=student_average,

        # We will set this parameter after receiving it from student_subjects_2 solver
        students_happiness=None
    )


def prepare_for_groups(input_data: InputData) -> InputGroups:

    basic_info = input_data.information.basic_info
    class_info = input_data.information.class_info
    constraints = input_data.information.constraints
    custom_constraints = input_data.custom_constraints

    if custom_constraints is None:
        custom_constraints = CustomConstraints(
            predetermined_subjects=[],
            predetermined_subjects_for_students=[],
            predetermined_groups_for_students=[],
            conditional_students=[]
        )

    return InputGroups(
        number_students=basic_info.number_of_students,
        number_instructors=basic_info.number_of_instructors,
        number_subjects=basic_info.number_of_subjects,
        number_class_types=basic_info.number_of_class_types,
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
        number_conditional_students=len(custom_constraints.conditional_students),
        conditional_students=custom_constraints.conditional_students,
        student_subject=None,  # We will set this parameter after receiving it from student_subjects solver
        max_number_of_groups=None,  # We will set this parameter after receiving more info from student_subjects solver
        min_number_of_groups_in_class=None,  # We will set this parameter after receiving more info from
                                             # student_subjects solver
    )


def prepare_for_groups_with_friends(input_data: InputData) -> InputGroupsWithFriends:

    input_groups = prepare_for_groups(input_data)
    friends_info = input_data.preferences.friends_info

    return InputGroupsWithFriends(
        **input_groups.__dict__,
        friends_max_number=friends_info.max_number_friends,
        friends_array=friends_info.friends_array,

        # We will set this parameter after receiving it from student_groups solver
        groups_with_common_students=None
    )