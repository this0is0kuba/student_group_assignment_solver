import unittest

from models import BasicInfo, InvalidInputError

valid_data = {
            "number_of_students": 3,
            "number_of_instructors": 2,
            "number_of_subjects": 2,
            "number_of_class_types": 1,
            "number_of_sections": 2,
            "student_average": [4.0, 3.5, 4.5],
            "subject_section": [1, 2]
}


class TestBasicInfo(unittest.TestCase):

    def test_valid_basic_info(self):

        data = valid_data.copy()
        BasicInfo(**data)

    def test_invalid_lengths(self):

        data = valid_data.copy()
        data["student_average"] = [4.0, 3.5]

        with self.assertRaises(InvalidInputError):
            BasicInfo(**data)

    def test_invalid_students_average_grade(self):

        data = valid_data.copy()
        data["student_average"] = [4.0, 3.5, 1.9]

        with self.assertRaises(InvalidInputError):
            BasicInfo(**data)

    def test_invalid_subject_section(self):

        data = valid_data.copy()
        data["subject_section"] = [0, 1]

        with self.assertRaises(InvalidInputError):
            BasicInfo(**data)

