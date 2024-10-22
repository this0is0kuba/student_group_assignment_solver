from pydantic import BaseModel


class StudentInfo(BaseModel):
    student_id: str
    student_name: str


class GroupInfo(BaseModel):
    group_number: int
    students: list[StudentInfo]


class OpenedClass(BaseModel):
    subject: str
    class_type: str
    students: list[GroupInfo]
    instructor_id: str
    instructor_name: str


class Solution(BaseModel):
    classes: list[OpenedClass]
