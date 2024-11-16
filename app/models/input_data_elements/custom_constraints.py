from pydantic import BaseModel


class PredeterminedSubjectsForStudent(BaseModel):
    student_id: int
    predetermined_subjects_for_student: list[int]


class CustomConstraints(BaseModel):
    student_predetermined_subjects: list[PredeterminedSubjectsForStudent] | None
    predetermined_subjects: list[int] | None



