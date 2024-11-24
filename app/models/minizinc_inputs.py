from pydantic import BaseModel


class InputStudentSubjects1(BaseModel):

    # Basic info about classes
    # --------------------------------------------------
    number_students: int
    number_instructors: int
    number_subjects: int
    number_class_types: int
    number_section: int
    number_classes: int

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

    # Custom constraints
    # --------------------------------------------------
    number_predetermined_subjects: int
    predetermined_subjects: list[int]

    number_predetermined_students: int
    predetermined_students: list[int]
    predetermined_subjects_for_students: list[list[int]]
    # --------------------------------------------------


class InputStudentSubjects2(BaseModel):

    # Basic info about classes
    # --------------------------------------------------
    number_students: int
    number_instructors: int
    number_subjects: int
    number_class_types: int
    number_section: int
    number_classes: int

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

    # Custom constraints
    # --------------------------------------------------
    number_predetermined_subjects: int
    predetermined_subjects: list[int]

    number_predetermined_students: int
    predetermined_students: list[int]
    predetermined_subjects_for_students: list[list[int]]
    # --------------------------------------------------

    # Info about the saddest student from student_subjects_1 solver
    # --------------------------------------------------
    the_saddest_student_happiness: int | None
    # --------------------------------------------------


class InputStudentSubjectsWithAverage(BaseModel):

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

    # Custom constraints
    # --------------------------------------------------
    number_predetermined_subjects: int
    predetermined_subjects: list[int]

    number_predetermined_students: int
    predetermined_students: list[int]
    predetermined_subjects_for_students: list[list[int]]
    # --------------------------------------------------

    # Info about happiness from student_subjects_2 solver
    # --------------------------------------------------
    the_saddest_student_happiness: int | None
    students_happiness: int | None
    # --------------------------------------------------


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

    # Custom constraints
    # --------------------------------------------------
    number_predetermined_students: int
    predetermined_students: list[int]
    predetermined_classes_for_students: list[list[int]]
    predetermined_groups_for_students: list[list[int]]
    # --------------------------------------------------

    # Student's subjects - from student_subjects solver
    # --------------------------------------------------
    student_subject: list[list[int]] | None
    max_number_of_groups:  int | None
    min_number_of_groups_in_class: list[int] | None
    # --------------------------------------------------


class InputStudentGroupsWithFriends(BaseModel):

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

    # Custom constraints
    # --------------------------------------------------
    number_predetermined_students: int
    predetermined_students: list[int]
    predetermined_classes_for_students: list[list[int]]
    predetermined_groups_for_students: list[list[int]]
    # --------------------------------------------------

    # Info about students' friends
    # --------------------------------------------------
    friends_array: list[list[int]]
    friends_max_number: int
    # --------------------------------------------------

    # Student's subjects - from student_subjects solver
    # --------------------------------------------------
    student_subject: list[list[int]] | None
    max_number_of_groups:  int | None
    min_number_of_groups_in_class: list[int] | None
    # --------------------------------------------------

    # Info about groups from student_groups solver
    # --------------------------------------------------
    groups_with_common_students: int | None
    # --------------------------------------------------
