from pydantic import BaseModel


class BasicInfo(BaseModel):
    students: list[str]
    instructors: list[str]
    subjects: list[str]
    class_types: list[str]
    student_average: list[float]
    section_number: int
    subject_section: list[int]


# Single 'class' is a pair: (subject, class_type).
class ClassInfo(BaseModel):
    class_type: list[int]
    class_subject: list[int]
    class_instructor: list[int]
    class_time_hours: list[int]


class Constraints(BaseModel):
    instructor_max_hours: list[int]
    student_subjects_in_section: list[list[int]]
    class_type_min_students: list[int]
    class_type_max_students: list[int]
