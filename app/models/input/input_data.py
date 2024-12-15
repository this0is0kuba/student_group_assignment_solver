from pydantic import BaseModel, model_validator

from models.input.input_data_elements import CustomConstraints
from models.input.input_data_elements.information import Information
from models.input.input_data_elements import StudentPreferences
from models.errors.errors import InvalidInputError


class InputData(BaseModel):

    information: Information
    preferences: StudentPreferences
    custom_constraints: CustomConstraints | None

    @model_validator(mode="after")
    def check_length_preferences(self):

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
    def check_length_friends(self):

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
