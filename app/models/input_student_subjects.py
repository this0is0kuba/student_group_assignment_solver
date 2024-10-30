from pydantic import BaseModel


class InputStudentSubjects(BaseModel):

    # Basic info about classes
    # --------------------------------------------------
    number_students: int
    number_instructors: int
    number_subjects: int
    number_class_types: int
    number_section: int
    number_classes: int

    student_average: list[int]

    subject_section: list[int]

    class_type: list[int]
    class_subject: list[int]
    class_instructor: list[int]
    class_time_h: list[int]
    # --------------------------------------------------

    # Constraints
    # --------------------------------------------------
    instructor_max_h: list[int]

    student_subjects_in_section: list[list[int]]

    class_type_min_students: list[int]
    class_type_max_students: list[int]
    # --------------------------------------------------

    # Preferences
    # --------------------------------------------------
    student_preferences: list[list[int]]
    # --------------------------------------------------
