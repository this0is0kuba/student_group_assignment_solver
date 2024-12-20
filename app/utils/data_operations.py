import math


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
