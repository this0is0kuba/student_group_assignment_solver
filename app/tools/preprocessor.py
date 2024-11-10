import math

from models import InputStudentSubjects, InputStudentGroups, InputData


class Preprocessor:

    @classmethod
    def prepare_input_student_subjects(cls, input_data: InputData) -> InputStudentSubjects:

        basic_info = input_data.information.basic_info
        class_info = input_data.information.class_info
        constraints = input_data.information.constraints

        preferences_subjects = input_data.preferences.preferences_subjects

        student_average = Preprocessor._prepare_student_average(basic_info.student_average)
        student_preferences = Preprocessor._prepare_list_preferences(preferences_subjects,
                                                                     basic_info.number_of_sections,
                                                                     basic_info.subject_section)

        return InputStudentSubjects(
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
        preferences_friends = [[] for _ in range(basic_info.number_of_students)]
        weight = 1

        if friends_info:
            friend_flag = True
            max_number_friends = friends_info.friends_max_number
            preferences_friends = friends_info.preferences_friends
            weight = friends_info.weight

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
            student_subject=None,  # We will set this parameter after receiving it from first solver
            max_number_of_groups=None,  # We will set this parameter after receiving more info from first solver
            min_number_of_groups_in_class=None,  # We will set this parameter after receiving more info from first solver
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

        max_number_of_subjects = max(section_subject_amount)

        new_list_preferences = []
        for i in range(len(list_preferences)):

            list_student_preferences = []
            for j in range(len(list_preferences[0])):

                reverted_value = section_subject_amount[subject_section[j] - 1] - list_preferences[i][j] + 1
                new_value = round(reverted_value * (max_number_of_subjects / section_subject_amount[subject_section[j] - 1]))

                list_student_preferences.append(
                    new_value
                )

            new_list_preferences.append(list_student_preferences)

        return new_list_preferences

    @classmethod
    def get_number_of_groups_in_each_class(
            cls,
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
