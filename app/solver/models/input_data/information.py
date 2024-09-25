from pydantic import BaseModel


class Information(BaseModel):

    class BasicInfo(BaseModel):
        students: list[str]
        instructors: list[str]
        subjects: list[str]
        class_types: list[str]
        section_number: int
        subject_ects: list[int]
        subject_section: list[int]

    # Single 'class' is a pair: (subject, class_type).
    class ClassInfo(BaseModel):
        class_type: list[int]
        class_subject: list[int]
        class_instructor: list[int]
        class_time_hours: list[int]

    class Constraints(BaseModel):
        instructor_max_hours: list[int]
        section_min_ects: list[int]

    class ScienceClubAndResearch(BaseModel):
        student_science_club: list[bool]
        student_conduct_research: list[bool]
        science_club_ects: int
        conduct_research_ects: int
        science_club_section: int
        conduct_research_section: int

    basic_info: BasicInfo
    class_info: ClassInfo
    constraints: Constraints
    science_club_and_research: ScienceClubAndResearch
