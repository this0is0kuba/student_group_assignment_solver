from pydantic import BaseModel


class StudentGroups(BaseModel):
    subject: str
    subject_id: str
    instructor: str
    instructor_id: str
    group_number: int


class InstructorGroups(BaseModel):
    subject: str
    subject_id: str
    group_number: int
    student_list: list[(str, str)]


class StudentsInfo(BaseModel):
    student_id: str
    name: str
    student_groups: list[StudentGroups]


class InstructorsInfo(BaseModel):
    instructor_id: str
    name: str
    instructor_groups: list[InstructorGroups]