from pydantic import BaseModel


class InputParallelGroups(BaseModel):

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
    # None is allowed because we have to wait until we get this info from the solver
    student_subject: list[int, int] | None
    # --------------------------------------------------

    # Student's friends
    # --------------------------------------------------
    friend_flag: bool = False
    max_number_friends: int | None

    student_friend = list[int, int] | None
    # --------------------------------------------------

    # Importance of parallel groups
    # --------------------------------------------------
    weight: int
    # --------------------------------------------------
