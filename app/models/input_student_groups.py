from pydantic import BaseModel


class InputStudentGroups(BaseModel):

    # Basic info about classes
    # --------------------------------------------------
    number_students: int
    number_instructors: int
    number_subjects: int
    number_class_types: int
    number_classes: int

    class_type: list[int]
    class_subject: list[int]
    class_instructor: list[int]
    class_time_h: list[int]
    # --------------------------------------------------

    # Constraints
    # --------------------------------------------------
    instructor_max_h: list[int]

    class_type_min_students: list[int]
    class_type_max_students: list[int]
    # --------------------------------------------------

    # Student's subjects
    # --------------------------------------------------
    # None is allowed because we have to wait until we get this info from the earlier solver
    student_subject: list[list[int]] | None
    # --------------------------------------------------
