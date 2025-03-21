from typing import Self

from pydantic import BaseModel, Field, model_validator
from models.errors.errors import InvalidInputError


class BasicInfo(BaseModel):
    number_of_students: int = Field(ge=1)
    number_of_instructors: int = Field(ge=1)
    number_of_subjects: int = Field(ge=1)
    number_of_class_types: int = Field(ge=1)
    number_of_sections: int = Field(ge=1)
    student_average: list[float] | None = Field(min_length=1)
    subject_section: list[int] = Field(min_length=1)

    @model_validator(mode="after")
    def check_lengths(self) -> Self:

        if self.student_average and self.number_of_students != len(self.student_average):
            raise InvalidInputError(detail="The numberOfStudents should be equal to length of the studentAverage.")

        if self.number_of_subjects != len(self.subject_section):
            raise InvalidInputError(detail="The numberOfSubjects should be equal to length of the subjectSection.")

        return self

    @model_validator(mode="after")
    def check_students_average_grade(self) -> Self:

        if not self.student_average:
            return self

        for avg in self.student_average:
            if avg < 2 or avg > 5:
                raise InvalidInputError(detail="Each average grade should be between 2.0 and 5.0")

        return self

    @model_validator(mode="after")
    def check_subject_sections(self) -> Self:

        for section in self.subject_section:
            if section < 1 or section > self.number_of_sections:
                raise InvalidInputError(detail="Each value in subjectSection should be between 1 and numberOfSections.")

        return self


# Single 'class' is a pair: (subject, class_type).
class ClassInfo(BaseModel):
    number_of_classes: int = Field(ge=1)
    class_type: list[int] = Field(min_length=1)
    class_subject: list[int] = Field(min_length=1)
    class_instructor: list[int] = Field(min_length=1)
    class_time_hours: list[int] = Field(min_length=1)

    @model_validator(mode="after")
    def check_lengths(self) -> Self:

        n_classes = self.number_of_classes

        if len(self.class_type) != n_classes:
            raise InvalidInputError(detail="The numberOfClasses should be equal to length of the classType.")

        if len(self.class_subject) != n_classes:
            raise InvalidInputError(detail="The numberOfClasses should be equal to length of the classSubject.")

        if len(self.class_instructor) != n_classes:
            raise InvalidInputError(detail="The numberOfClasses should be equal to length of the classInstructor.")

        if len(self.class_time_hours) != n_classes:
            raise InvalidInputError(detail="The numberOfClasses should be equal to length of the classTimeHours.")

        return self


class Constraints(BaseModel):
    instructor_max_hours: list[int] = Field(min_length=1)

    # How much subjects each student has in each section.
    student_subjects_in_section: list[list[int]] = Field(min_length=1)

    class_type_min_students: list[int] = Field(min_length=1)
    class_type_max_students: list[int] = Field(min_length=1)


class Information(BaseModel):

    basic_info: BasicInfo
    class_info: ClassInfo
    constraints: Constraints

    @model_validator(mode="after")
    def check_lengths(self) -> Self:

        c = self.constraints
        b = self.basic_info

        if len(c.instructor_max_hours) != b.number_of_instructors:
            raise InvalidInputError(
                detail="The numberOfInstructors should be equal to length of the instructorMaxHours."
            )

        if len(c.class_type_min_students) != b.number_of_class_types:
            raise InvalidInputError(
                detail="The numberOfClassTypes should be equal to length of the classTypeMinStudents."
            )

        if len(c.class_type_max_students) != b.number_of_class_types:
            raise InvalidInputError(
                detail="The numberOfClassTypes should be equal to length of the classTypeMaxStudents."
            )

        if len(c.student_subjects_in_section) != b.number_of_students:
            raise InvalidInputError(
                detail="The numberOfStudents should be equal to length of the studentSubjectsInSection."
            )

        for subjects in c.student_subjects_in_section:

            if len(subjects) != b.number_of_sections:
                raise InvalidInputError(
                    detail="Each length of list in studentSubjectsInSection should be equal to the numberOfSection."
                )

        return self

    @model_validator(mode="after")
    def check_classes(self) -> Self:

        c = self.class_info
        b = self.basic_info

        for class_type in c.class_type:
            if class_type < 1 or class_type > b.number_of_class_types:
                raise InvalidInputError("Each value in classType should be between 1 and numberOfClassTypes.")

        for subject in c.class_subject:
            if subject < 1 or subject > b.number_of_subjects:
                raise InvalidInputError("Each value in classSubject should be between 1 and numberOfSubjects.")

        for instructor in c.class_instructor:
            if instructor < 1 or instructor > b.number_of_instructors:
                raise InvalidInputError("Each value in classInstructor should be between 1 and numberOfInstructors.")

        return self
