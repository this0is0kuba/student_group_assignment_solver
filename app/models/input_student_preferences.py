from pydantic import BaseModel


class InputStudentPreferences(BaseModel):

    # Basic info about classes
    # --------------------------------------------------
    number_students: int
    number_instructors: int
    number_subjects: int
    number_class_types: int
    number_section: int
    number_classes: int

    student_average: list[int]

    subject_ects: list[int]
    subject_section: list[int]

    class_type: list[int]
    class_subject: list[int]
    class_instructor: list[int]
    class_time_h: list[int]
    # --------------------------------------------------

    # Info about science club, science research
    # --------------------------------------------------
    science_club_ects: int
    science_research_ects: int
    science_club_section: int
    science_research_section: int

    student_science_club: list[bool]
    student_science_research: list[bool]

    # Constraints
    # --------------------------------------------------
    instructor_max_h: list[int]
    
    section_min_ects: list[int]
    section_max_ects: list[int]

    class_type_min_students: list[int]
    class_type_max_students: list[int]
    # --------------------------------------------------

    # Preferences
    # --------------------------------------------------
    student_preferences: list[list[int]]
    # --------------------------------------------------
