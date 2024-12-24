from models import PredeterminedSubjectsForStudent, PredeterminedGroupsForStudent


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
