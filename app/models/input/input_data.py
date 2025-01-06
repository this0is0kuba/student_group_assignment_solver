from typing import Self

from pydantic import BaseModel, model_validator

from utils.data_operations import get_number_of_groups_in_each_class
from models.input.input_data_elements.custom_constraints import CustomConstraints
from models.input.input_data_elements.information import Information
from models.input.input_data_elements.preferences import StudentPreferences
from models.errors.errors import InvalidInputError


class InputData(BaseModel):
    information: Information
    preferences: StudentPreferences
    custom_constraints: CustomConstraints | None

    @model_validator(mode="after")
    def check_length_preferences(self) -> Self:

        preferences = self.preferences.preferences_subjects
        basic = self.information.basic_info

        if len(preferences) != basic.number_of_students:
            raise InvalidInputError(
                detail="The numberOfStudents should be equal to length of the preferencesSubjects."
            )

        for subjects in preferences:
            if len(subjects) != basic.number_of_subjects:
                raise InvalidInputError(
                    detail="Each length of list in preferencesSubjects should be equal to the numberOfSubjects."
                )

        return self

    @model_validator(mode="after")
    def check_length_friends(self) -> Self:

        friends = self.preferences.friends_info
        basic = self.information.basic_info

        if friends is None:
            return self

        if friends.max_number_friends > basic.number_of_students:
            raise InvalidInputError(
                detail="The maxNumberFriends should be grater than numberOfStudents."
            )

        if len(friends.friends_array) != basic.number_of_students:
            raise InvalidInputError(
                detail="The numberOfStudents should be equal to length of the friendsArray."
            )

        for friends_list in friends.friends_array:
            if len(friends_list) != friends.max_number_friends:
                raise InvalidInputError(
                    detail="Each length of list in friends_list should be equal to length of the maxNumberFriends."
                )

        return self

    @model_validator(mode="after")
    def check_preferences(self) -> Self:

        preferences = self.preferences.preferences_subjects
        basic = self.information.basic_info

        map_section_to_number_of_subjects = {}

        for section in range(1, basic.number_of_sections + 1):
            map_section_to_number_of_subjects.update({section: 0})

        for section in basic.subject_section:
            number_of_subjects = map_section_to_number_of_subjects.get(section) + 1
            map_section_to_number_of_subjects.update({section: number_of_subjects})

        for student_preferences in preferences:
            for i, subject_number in enumerate(student_preferences):

                section = basic.subject_section[i]

                if subject_number < 1 or subject_number > map_section_to_number_of_subjects.get(section):
                    raise InvalidInputError(
                        detail="Each value in studentPreferences should be between 1 and number of subjects in the" +
                               "section to which this item belongs."
                    )

        return self

    @model_validator(mode="after")
    def check_friends(self):

        friends_info = self.preferences.friends_info
        basic = self.information.basic_info

        if friends_info is None:
            return self

        for friends in friends_info.friends_array:
            for student_number in friends:

                if student_number < 0 or student_number > basic.number_of_students:
                    raise InvalidInputError(
                        detail="Each value in friendsArray should be between 0 and numberOfStudents."
                    )

        return self

    @model_validator(mode="after")
    def check_custom_constraints(self):

        custom_constraints = self.custom_constraints
        basic = self.information.basic_info

        if custom_constraints is None:
            return self

        for subject in custom_constraints.predetermined_subjects:
            if subject < 1 or subject > basic.number_of_subjects:
                raise InvalidInputError(
                    detail="Each value in predeterminedSubjects should be between 1 and numberOfSubjects."
                )

        for student in custom_constraints.conditional_students:
            if student < 1 or student > basic.number_of_students:
                raise InvalidInputError(
                    detail="Each value in conditionalStudents should be between 1 and numberOfStudents."
                )

        return self

    @model_validator(mode="after")
    def check_custom_subjects(self):

        if self.custom_constraints is None:
            return self

        pre_subjects = self.custom_constraints.predetermined_subjects_for_students
        basic = self.information.basic_info

        for pre_subject in pre_subjects:

            if pre_subject.student_id > basic.number_of_students:
                raise InvalidInputError(
                    detail="Each studentId in predeterminedSubjectsForStudents should be lower than numberOfStudents."
                )

            for subject in pre_subject.predetermined_subjects_for_student:

                if subject < 1 or subject > basic.number_of_subjects:
                    raise InvalidInputError(
                        detail="Each value in predeterminedSubjectsForStudents should be between 1 and " +
                               "numberOfSubjects."
                    )

        return self

    @model_validator(mode="after")
    def check_custom_groups(self):

        if self.custom_constraints is None:
            return self

        pre_groups = self.custom_constraints.predetermined_groups_for_students
        basic = self.information.basic_info
        class_info = self.information.class_info
        constraints = self.information.constraints

        number_of_groups_list = get_number_of_groups_in_each_class(
            [basic.number_of_students for _ in range(class_info.number_of_classes)],
            class_info.class_subject,
            class_info.class_type,
            constraints.class_type_max_students
        )

        for pre_group in pre_groups:

            if pre_group.student_id > basic.number_of_students:
                raise InvalidInputError(
                    detail="Each studentId in predeterminedGroupsForStudents should be lower than numberOfStudents."
                )

            if len(pre_group.predetermined_classes_for_student) != len(pre_group.predetermined_groups_for_student):
                raise InvalidInputError(
                    detail="The length of predeterminedClassesForStudent should be equal to length of the " +
                           "predeterminedGroupsForStudent."
                )

            for class_number, group_number in zip(
                    pre_group.predetermined_classes_for_student,
                    pre_group.predetermined_groups_for_student
            ):

                if class_number < 1 or class_number > class_info.number_of_classes:
                    raise InvalidInputError(
                        detail="Each value in predeterminedClassesForStudent should be between 1 and numberOfClasses."
                    )

                if group_number < 0 or group_number > number_of_groups_list[class_number - 1]:
                    raise InvalidInputError(
                        detail=f"The value for group: {group_number} in predeterminedGroupsForStudent should be " +
                               f"between 0 and {number_of_groups_list[class_number]}."
                    )

        return self

    @model_validator(mode="after")
    def validate_custom_subjects(self) -> Self:

        if self.custom_constraints is None:
            return self

        pre_subjects = self.custom_constraints.predetermined_subjects_for_students

        all_pre_subjects = set()

        for pre_subject in pre_subjects:
            all_pre_subjects.update(pre_subject.predetermined_subjects_for_student)

        missing_subjects = all_pre_subjects.difference(set(self.custom_constraints.predetermined_subjects))

        if missing_subjects:
            raise InvalidInputError("There are predetermined subjects for students which are not defined in " +
                                    "predetermined subjects. If you want to assign some student to particular " +
                                    "subject then first you have to put this subject to predeterminedSubjects list. ")

        return self

    @model_validator(mode="after")
    def validate_custom_groups(self) -> Self:

        if self.custom_constraints is None:
            return self

        pre_groups = self.custom_constraints.predetermined_groups_for_students
        class_info = self.information.class_info

        all_pre_classes = set()

        for pre_group in pre_groups:
            all_pre_classes.update(pre_group.predetermined_classes_for_student)

        all_pre_subjects = set([class_info.class_subject[c - 1] for c in all_pre_classes])

        missing_subjects = all_pre_subjects.difference(set(self.custom_constraints.predetermined_subjects))

        # there is no need to put some subject to predeterminedSubjects if only groups with number "0" belong to it.
        missing_subjects_with_only_0 = set()

        groups_and_classes = [
            (group, class_number)
            for pre_group in pre_groups
            for group, class_number in
            zip(pre_group.predetermined_groups_for_student, pre_group.predetermined_classes_for_student)
        ]

        for subject in missing_subjects:

            classes_in_subject = []

            for c, sub in enumerate(class_info.class_subject):
                if sub == subject:
                    classes_in_subject.append(c + 1)

            filtered_groups = [
                group_and_class[0]
                for group_and_class in groups_and_classes
                if group_and_class[1] in classes_in_subject
            ]

            if len([group for group in filtered_groups if group > 0]) == 0:
                missing_subjects_with_only_0.add(subject)

        missing_subjects = missing_subjects.difference(missing_subjects_with_only_0)

        if missing_subjects:
            raise InvalidInputError("There are predetermined classes for students which are not defined in " +
                                    "predetermined subjects. If you want to assign some student to particular " +
                                    "class by assigning some group, then first you have to put this subject to " +
                                    "predeterminedSubjects list.")

        return self
