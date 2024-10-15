from pydantic import BaseModel

from models.solution_elements.solution_elements import StudentsInfo, InstructorsInfo


class Solution(BaseModel):
    students_info: list[StudentsInfo]
    instructor_info: list[InstructorsInfo]
