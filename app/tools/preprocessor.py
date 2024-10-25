import math

from models import InputStudentSubjects, InputStudentGroups, InputData


class Preprocessor:

    @classmethod
    def prepare_input_student_subjects(cls, input_data: InputData) -> InputStudentSubjects:

        basic_info = input_data.information.basic_info
        class_info = input_data.information.class_info
        constraints = input_data.information.constraints
        sc_and_res = input_data.information.science_club_and_research

        preferences_subjects = input_data.preferences.preferences_subjects

        student_average = Preprocessor._prepare_student_average(basic_info.student_average)
        student_preferences = Preprocessor._prepare_list_preferences(preferences_subjects,
                                                                     basic_info.section_number,
                                                                     basic_info.subject_section)

        return InputStudentSubjects(
            number_students=len(basic_info.students),
            number_instructors=len(basic_info.instructors),
            number_subjects=len(basic_info.subjects),
            number_class_types=len(basic_info.class_types),
            number_section=basic_info.section_number,
            number_classes=len(class_info.class_subject),
            student_average=student_average,
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
            section_min_subjects=constraints.section_min_subjects,
            class_type_min_students=constraints.class_type_min_students,
            class_type_max_students=constraints.class_type_max_students,
            student_preferences=student_preferences
        )

    @classmethod
    def prepare_input_student_groups(cls, input_data: InputData) -> InputStudentGroups:
        basic_info = input_data.information.basic_info
        class_info = input_data.information.class_info
        constraints = input_data.information.constraints

        friends_info = input_data.preferences.friends_info

        friend_flag = False
        max_number_friends = 0
        preferences_friends = [[] for _ in range(len(basic_info.students))]
        weight = 1

        if friends_info:
            friend_flag = True
            max_number_friends = friends_info.friends_max_number
            preferences_friends = friends_info.preferences_friends
            weight = friends_info.weight

        return InputStudentGroups(
            number_students=len(basic_info.students),
            number_instructors=len(basic_info.instructors),
            number_subjects=len(basic_info.subjects),
            number_class_types=len(basic_info.class_types),
            number_section=basic_info.section_number,
            number_classes=len(class_info.class_subject),
            class_type=class_info.class_type,
            class_subject=class_info.class_subject,
            class_instructor=class_info.class_instructor,
            class_time_h=class_info.class_time_hours,
            instructor_max_h=constraints.instructor_max_hours,
            class_type_min_students=constraints.class_type_min_students,
            class_type_max_students=constraints.class_type_max_students,
            student_subject=None,  # We set this parameter after receiving it from first solver
            friend_flag=friend_flag,
            max_number_friends=max_number_friends,
            student_friend=preferences_friends,
            weight=weight
        )

    @classmethod
    def _prepare_student_average(cls, list_average: list[float]) -> list[int]:

        new_list_average = []

        for avg in list_average:
            new_list_average.append(int(avg * 100))

        return new_list_average

    @classmethod
    def _prepare_list_preferences(cls, list_preferences: list[list[int]], section_number: int,
                                  subject_section: list[int]):

        # how much subjects is in each section
        section_subject_amount = [0 for _ in range(section_number)]

        for section in range(1, section_number + 1):
            for current_section in subject_section:

                if current_section == section:
                    section_subject_amount[section - 1] += 1

        new_list_preferences = []
        for i in range(len(list_preferences)):

            list_student_preferences = []
            for j in range(len(list_preferences[0])):
                list_student_preferences.append(
                    section_subject_amount[subject_section[j] - 1] - list_preferences[i][j] + 1
                )

            new_list_preferences.append(list_student_preferences)

        return new_list_preferences
