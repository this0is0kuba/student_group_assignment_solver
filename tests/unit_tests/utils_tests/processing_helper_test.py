import pytest

from models import PredeterminedSubjectsForStudent, PredeterminedGroupsForStudent
from utils.processing_helper import prepare_predetermined_students, prepare_predetermined_subjects_for_students, \
    prepare_student_average, prepare_list_preferences, prepare_predetermined_groups, prepare_predetermined_classes


class TestProcessingHelper:

    @pytest.mark.parametrize(
        "predetermined_subjects_for_students, expected",
        [
            (
                [
                    PredeterminedSubjectsForStudent(
                        student_id=1,
                        predetermined_subjects_for_student=[1, 2, 3]
                    ),
                    PredeterminedSubjectsForStudent(
                        student_id=4,
                        predetermined_subjects_for_student=[6]
                    ),
                    PredeterminedSubjectsForStudent(
                        student_id=10,
                        predetermined_subjects_for_student=[10]
                    )
                ],
                [1, 4, 10]
            ),
            ([], [])
        ]
    )
    def test_prepare_predetermined_students(self, predetermined_subjects_for_students, expected):
        assert expected == prepare_predetermined_students(predetermined_subjects_for_students)

    @pytest.mark.parametrize(
        "predetermined_subjects_for_students, number_of_subjects, expected",
        [
            (
                [
                    PredeterminedSubjectsForStudent(
                        student_id=1,
                        predetermined_subjects_for_student=[1, 2, 3]
                    ),
                    PredeterminedSubjectsForStudent(
                        student_id=4,
                        predetermined_subjects_for_student=[6]
                    ),
                    PredeterminedSubjectsForStudent(
                        student_id=10,
                        predetermined_subjects_for_student=[10]
                    )
                ],
                12,
                [
                    [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
            ),
            ([], 0, [])
        ]
    )
    def test_prepare_predetermined_subjects_for_students(
            self,
            predetermined_subjects_for_students,
            number_of_subjects,
            expected
    ):

        prepared_subjects_for_students = prepare_predetermined_subjects_for_students(
            predetermined_subjects_for_students,
            number_of_subjects
        )

        assert expected == prepared_subjects_for_students

    @pytest.mark.parametrize(
        "list_average, expected",
        [
            ([3.20, 3.50, 3.61, 4.56, 2.91], [320, 350, 361, 456, 291]),
            ([4.1235, 2.611333, 3, 4.000001], [412, 261, 300, 400]),
            ([], [])
        ]
    )
    def test_prepare_student_average(self, list_average, expected):
        assert expected == prepare_student_average(list_average)

    @pytest.mark.parametrize(
        "list_preferences, section_number, subject_section, expected",
        [
            (
                [[1]], 1, [1], [[1]],
            ),
            (
                [[1, 2, 3], [2, 3, 1]], 1, [1, 1, 1], [[3, 2, 1], [2, 1, 3]]
            ),
            (
                [
                    [1, 2, 3, 4, 1, 2],
                    [4, 3, 1, 2, 2, 1],
                    [1, 2, 4, 3, 1, 2]
                ],
                2,
                [1, 1, 1, 1, 2, 2],
                [
                    [4, 3, 2, 1, 4, 2],
                    [1, 2, 4, 3, 2, 4],
                    [4, 3, 1, 2, 4, 2]
                ]
            )
        ]
    )
    def test_prepare_list_preferences(self, list_preferences, section_number, subject_section, expected):
        assert expected == prepare_list_preferences(list_preferences, section_number, subject_section)

    @pytest.mark.parametrize(
        "predetermined_groups_for_students, number_of_classes, expected_classes, expected_groups",
        [
            (
                [
                    PredeterminedGroupsForStudent(
                        student_id=1,
                        predetermined_classes_for_student=[1],
                        predetermined_groups_for_student=[1]
                    )
                ],
                1,
                [[1]],
                [[1]]
            ),
            (
                [
                    PredeterminedGroupsForStudent(
                        student_id=1,
                        predetermined_classes_for_student=[1, 2, 3],
                        predetermined_groups_for_student=[1, 1, 2]
                    ),
                    PredeterminedGroupsForStudent(
                        student_id=2,
                        predetermined_classes_for_student=[1, 2],
                        predetermined_groups_for_student=[1, 2]
                    ),
                    PredeterminedGroupsForStudent(
                        student_id=5,
                        predetermined_classes_for_student=[1],
                        predetermined_groups_for_student=[3]
                    )
                ],
                5,
                [[1, 2, 3, 0, 0], [1, 2, 0, 0, 0], [1, 0, 0, 0, 0]],
                [[1, 1, 2, 0, 0], [1, 2, 0, 0, 0], [3, 0, 0, 0, 0]]
            )
        ]
    )
    def test_predetermined_classes_and_groups(
            self,
            predetermined_groups_for_students,
            number_of_classes,
            expected_classes,
            expected_groups
    ):

        assert prepare_predetermined_classes(predetermined_groups_for_students, number_of_classes) == expected_classes
        assert prepare_predetermined_groups(predetermined_groups_for_students, number_of_classes) == expected_groups
