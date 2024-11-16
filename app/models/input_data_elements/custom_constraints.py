from pydantic import BaseModel


class PredeterminedSubjectsForStudent(BaseModel):
    student_id: int
    predetermined_subjects_for_student: list[int]


class CustomConstraints(BaseModel):
    predetermined_subjects: list[int]
    predetermined_subjects_for_students: list[PredeterminedSubjectsForStudent]



