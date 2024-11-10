from pydantic import BaseModel


class SolutionStudentSubjects(BaseModel):
    student_subjects: list[list[bool]]
    number_of_students_in_subject: list[int]

