import copy
import unittest

from models import InputData, InvalidInputError


class TestInputData(unittest.TestCase):

    valid_data = {

        "information": {

            "basic_info": {
                "number_of_students": 30,
                "number_of_instructors": 8,
                "number_of_subjects": 6,
                "number_of_class_types": 4,
                "number_of_sections": 2,
                "student_average": [3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00,
                                    4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00,
                                    5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
                "subject_section": [1, 1, 1, 2, 2, 2]
            },

            "class_info": {
                "number_of_classes": 13,
                "class_type": [1, 2, 4, 1, 2, 1, 3, 1, 2, 1, 3, 1, 2],
                "class_subject": [1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
                "class_instructor": [1, 2, 2, 3, 4, 3, 4, 5, 6, 7, 7, 8, 8],
                "class_time_hours": [28, 14, 14, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28]
            },

            "constraints": {
                "instructor_max_hours": [336, 140, 336, 336, 336, 336, 336, 336],
                "student_subjects_in_section": [[0, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2],
                                                [2, 2], [1, 2], [2, 2], [2, 2],
                                                [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [1, 2], [2, 2],
                                                [2, 2], [2, 2], [2, 2], [2, 2],
                                                [2, 2], [2, 2], [2, 2], [2, 1]],
                "class_type_min_students": [1, 2, 5, 5],
                "class_type_max_students": [30, 5, 10, 10]
            }

        },

        "preferences": {
            "preferences_subjects": [[2, 1, 3, 1, 2, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [3, 1, 2, 3, 1, 2],
                                     [3, 1, 2, 3, 1, 2],
                                     [2, 1, 3, 3, 1, 2],
                                     [2, 1, 3, 3, 1, 2],
                                     [2, 1, 3, 1, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [3, 1, 2, 3, 1, 2],
                                     [3, 1, 2, 3, 1, 2],
                                     [2, 1, 3, 3, 1, 2],
                                     [2, 1, 3, 3, 1, 2],
                                     [2, 1, 3, 1, 2, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [2, 1, 3, 2, 1, 3],
                                     [3, 1, 2, 3, 1, 2],
                                     [3, 1, 2, 3, 1, 2],
                                     [2, 1, 3, 3, 1, 2],
                                     [2, 1, 3, 3, 1, 2]],
            "friends_info": {
                "friends_array": [[2, 3, 0],
                                  [1, 3, 0],
                                  [1, 2, 4],
                                  [5, 0, 0],
                                  [4, 0, 0],
                                  [7, 6, 0],
                                  [6, 8, 0],
                                  [6, 7, 0],
                                  [8, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, 0],
                                  [26, 27, 28],
                                  [25, 27, 28],
                                  [25, 26, 28],
                                  [25, 26, 27],
                                  [30, 0, 0],
                                  [29, 0, 0]],
                "max_number_friends": 3
            }
        },

        "custom_constraints": {
            "predetermined_subjects": [3, 6],
            "predetermined_subjects_for_students": [
                {
                    "student_id": 2,
                    "predetermined_subjects_for_student": [3, 6]
                }
            ],

            "predetermined_groups_for_students": [
                {
                    "student_id": 2,
                    "predetermined_classes_for_student": [7],
                    "predetermined_groups_for_student": [1]
                }
            ],

            "conditional_students": [1, 2, 3, 4, 5, 6, 7]
        }
    }

    def test_valid_input(self):

        data = copy.deepcopy(self.valid_data)
        InputData(**data)

    def test_length_preferences(self):

        data = copy.deepcopy(self.valid_data)
        del data["preferences"]["preferences_subjects"][-1]

        with self.assertRaises(InvalidInputError):
            InputData(**data)

    def test_length_friends(self):

        data = copy.deepcopy(self.valid_data)
        data["preferences"]["friends_info"]["friends_array"][0] = [2, 3, 0, 0]

        with self.assertRaises(InvalidInputError):
            InputData(**data)

    def test_preferences(self):

        data = copy.deepcopy(self.valid_data)
        data["preferences"]["preferences_subjects"][0][0] = 7

        with self.assertRaises(InvalidInputError):
            InputData(**data)

    def test_friends(self):

        data = copy.deepcopy(self.valid_data)
        data["preferences"]["friends_info"]["friends_array"][0][0] = 31

        with self.assertRaises(InvalidInputError):
            InputData(**data)

    def test_custom_constraints(self):

        data = copy.deepcopy(self.valid_data)
        data["custom_constraints"]["predetermined_subjects"][0] = 7

        with self.assertRaises(InvalidInputError):
            InputData(**data)

    def test_custom_subjects(self):

        data = copy.deepcopy(self.valid_data)
        data["custom_constraints"]["predetermined_subjects_for_students"][0]["student_id"] = 31

        with self.assertRaises(InvalidInputError):
            InputData(**data)

    def test_custom_groups(self):

        data = copy.deepcopy(self.valid_data)

        data["custom_constraints"]["predetermined_groups_for_students"][0]["predetermined_classes_for_student"][0] = 14

        with self.assertRaises(InvalidInputError):
            InputData(**data)

    def test_missing_classes(self):

        data = copy.deepcopy(self.valid_data)

        data["custom_constraints"]["predetermined_subjects"] = [1]

        with self.assertRaises(InvalidInputError):
            InputData(**data)

    def test_missing_groups(self):

        data = copy.deepcopy(self.valid_data)

        data["custom_constraints"]["predetermined_subjects"] = [1]

        with self.assertRaises(InvalidInputError):
            InputData(**data)
