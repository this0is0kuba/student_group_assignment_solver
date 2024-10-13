from models import InputStudentPreferences, Input
from models.input_parallel_groups import InputParallelGroups


def prepare_input_for_student_preferences(input_data: Input) -> InputStudentPreferences:

    basic_info = input_data.information.basic_info
    class_info = input_data.information.class_info
    constraints = input_data.information.constraints
    sc_and_res = input_data.information.science_club_and_research

    preferences_subjects = input_data.preferences.preferences_subjects

    return InputStudentPreferences(
        number_students=len(basic_info.students),
        number_instructors=len(basic_info.instructors),
        number_subjects=len(basic_info.subjects),
        number_class_types=len(basic_info.class_types),
        number_section=basic_info.section_number,
        number_classes=len(class_info.class_subject),
        student_average=basic_info.student_average,
        subject_ects=basic_info.subject_ects,
        subject_section=basic_info.subject_section,
        class_type=class_info.class_type,
        class_subject=class_info.class_subject,
        class_instructor=class_info.class_instructor,
        class_time_h=class_info.class_time_hours,
        science_club_ects=sc_and_res.science_club_ects,
        science_research_ects=sc_and_res.science_research_ects,
        science_club_section=sc_and_res.science_club_section,
        science_research_section=sc_and_res.science_research_section,
        student_science_club=sc_and_res.student_science_club,
        student_science_research=sc_and_res.student_science_research,
        instructor_max_h=constraints.instructor_max_hours,
        section_min_ects=constraints.section_min_ects,
        section_max_ects=constraints.section_max_ects,
        class_type_min_students=constraints.class_type_min_students,
        class_type_max_students=constraints.class_type_max_students,
        student_preferences=preferences_subjects
    )


def prepare_input_for_parallel_groups(input_data: Input) -> InputParallelGroups:

    basic_info = input_data.information.basic_info
    class_info = input_data.information.class_info
    constraints = input_data.information.constraints

    friends_info = input_data.preferences.friends_info

    friend_flag = False
    max_number_friends = 0
    preferences_friends = []
    weight=1

    if friends_info:
        friend_flag = True
        max_number_friends = friends_info.friends_max_number
        preferences_friends = friends_info.preferences_friends
        weight=friends_info.weight


    return InputParallelGroups(
        number_students=len(basic_info.students),
        number_instructors=len(basic_info.instructors),
        number_subjects=len(basic_info.subjects),
        number_class_types=len(basic_info.class_types),
        number_section=basic_info.section_number,
        number_classes=len(class_info.class_subject),
        instructor_max_h=constraints.instructor_max_hours,
        class_type_min_students=constraints.class_type_min_students,
        class_type_max_students=constraints.class_type_max_students,
        student_subject=None,  # We set this parameter after receiving it from first solver
        friend_flag=friend_flag,
        max_number_friends=max_number_friends,
        student_friend=preferences_friends,
        weight=weight
    )