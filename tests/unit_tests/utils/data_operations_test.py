import pytest
from app.utils.data_operations import get_number_of_groups_in_each_class


@pytest.mark.parametrize(
    "number_of_students_in_subject, class_subject, class_type, class_type_max_students, expected",
    [
        ([1], [1], [1], [1], [1]),
        ([2, 2], [1, 1, 2, 2], [1, 2, 1, 2], [2, 1], [1, 2, 1, 2]),
        ([10, 5, 5], [1, 1, 2, 2, 3, 3], [1, 2, 1, 2, 1, 2], [10, 3], [1, 4, 1, 2, 1, 2]),
        (
                [40, 40, 30, 30],
                [1, 1, 1, 2, 2, 3, 3, 3, 4, 4],
                [1, 2, 3, 1, 2, 1, 2, 4, 2, 3],
                [40, 8, 16, 16],
                [1, 5, 3, 1, 5, 1, 4, 2, 4, 2]
        )
    ]
)
def test_number_of_groups(
        number_of_students_in_subject,
        class_subject,
        class_type,
        class_type_max_students,
        expected
):

    assert get_number_of_groups_in_each_class(
        number_of_students_in_subject,
        class_subject,
        class_type,
        class_type_max_students
    ) == expected
