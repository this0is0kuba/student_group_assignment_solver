from pydantic import BaseModel


class BasicInfo(BaseModel):
    number_of_students: int
    number_of_instructors: int
    number_of_subjects: int
    number_of_class_types: int
    number_of_sections: int
    student_average: list[float]
    subject_section: list[int]


# Single 'class' is a pair: (subject, class_type).
class ClassInfo(BaseModel):
    number_of_classes: int
    class_type: list[int]
    class_subject: list[int]
    class_instructor: list[int]
    class_time_hours: list[int]


class Constraints(BaseModel):
    instructor_max_hours: list[int]

    # How much subjects each student has in each section.
    student_subjects_in_section: list[list[int]]

    class_type_min_students: list[int]
    class_type_max_students: list[int]


class Information(BaseModel):

    basic_info: BasicInfo
    class_info: ClassInfo
    constraints: Constraints
