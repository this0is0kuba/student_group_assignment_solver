from pydantic import BaseModel


class Input(BaseModel):

    # basic
    students: list[str]
    instructors: list[str]
    subjects: list[str]
    types: list[str]
    section_number: int

    # connections
    class_type: list[int]
    class_subject: list[int]
    class_instructor: list[int]
    class_time: list[float]
    subject_ects: list[int]
    subject_section: list[int]

    # constraints
    instructor_max_hours: list[float]
    section_min_ects: list[int]

    # more info about science club and conducting research
    student_science_club: list[bool]
    student_conduct_research: list[bool]
    science_club_ects: int
    conduct_research_ects: int
    science_club_section: int
    conduct_research_section: int

    # preferences
    student_preferences: list[list[int]]

    # additional preferences
    student_preferences_friends: list[list[int]] | None = None




