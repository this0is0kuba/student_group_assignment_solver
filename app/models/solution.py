from pydantic import BaseModel


class StudentInfo:
    student_id: str
    student_name: str


class GroupInfo:
    group_number: int
    students: list[StudentInfo]


class ClassInfo:
    subject: str
    class_type: str
    students: list[GroupInfo]
    instructor_id: str
    instructor_name: str


class Solution(BaseModel):
    class_list: list[str]
