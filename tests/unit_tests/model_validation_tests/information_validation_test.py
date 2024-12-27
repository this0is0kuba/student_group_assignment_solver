import copy
import unittest

from models import BasicInfo, InvalidInputError, ClassInfo, Information


class TestBasicInfo(unittest.TestCase):

    valid_data = {
        "number_of_students": 3,
        "number_of_instructors": 2,
        "number_of_subjects": 2,
        "number_of_class_types": 1,
        "number_of_sections": 2,
        "student_average": [4.0, 3.5, 4.5],
        "subject_section": [1, 2]
    }

    def test_valid_basic_info(self):

        data = self.valid_data.copy()
        BasicInfo(**data)

    def test_invalid_lengths(self):

        data = self.valid_data.copy()
        data["student_average"] = [4.0, 3.5]

        with self.assertRaises(InvalidInputError):
            BasicInfo(**data)

    def test_invalid_students_average_grade(self):

        data = self.valid_data.copy()
        data["student_average"] = [4.0, 3.5, 1.9]

        with self.assertRaises(InvalidInputError):
            BasicInfo(**data)

    def test_invalid_subject_section(self):

        data = self.valid_data.copy()
        data["subject_section"] = [0, 1]

        with self.assertRaises(InvalidInputError):
            BasicInfo(**data)


class TestClassInfo(unittest.TestCase):

    valid_data = {
        "number_of_classes": 2,
        "class_type": [1, 2],
        "class_subject": [1, 2],
        "class_instructor": [1, 2],
        "class_time_hours": [3, 4]
    }

    def test_valid_class_info(self):

        data = self.valid_data.copy()
        ClassInfo(**data)

    def test_invalid_length(self):

        data = self.valid_data.copy()
        data["class_subject"] = [1]

        with self.assertRaises(InvalidInputError):
            ClassInfo(**data)


class TestInformation(unittest.TestCase):

    valid_data = {
        "basic_info": {
            "number_of_students": 3,
            "number_of_instructors": 2,
            "number_of_subjects": 2,
            "number_of_class_types": 1,
            "number_of_sections": 2,
            "student_average": [4.0, 3.5, 4.5],
            "subject_section": [1, 2]
        },
        "class_info": {
            "number_of_classes": 2,
            "class_type": [1, 1],
            "class_subject": [1, 2],
            "class_instructor": [1, 2],
            "class_time_hours": [3, 4]
        },
        "constraints": {
            "instructor_max_hours": [10, 15],
            "student_subjects_in_section": [[1, 2], [2, 3], [1, 1]],
            "class_type_min_students": [5],
            "class_type_max_students": [10]
        }
    }

    def test_valid_information(self):

        data = self.valid_data.copy()
        Information(**data)

    def test_invalid_lengths(self):

        data = copy.deepcopy(self.valid_data)
        data["constraints"]["instructor_max_hours"] = [10]

        with self.assertRaises(InvalidInputError):
            Information(**data)

    def test_check_classes(self):

        data = copy.deepcopy(self.valid_data)
        data["class_info"]["class_subject"] = [2, 3]

        with self.assertRaises(InvalidInputError):
            Information(**data)