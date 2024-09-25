from pydantic import BaseModel


class StudentPreferences(BaseModel):

    class PreferencesSubjects(BaseModel):
        preferences_subjects: list[list[int]]

    class PreferencesFriends(BaseModel):
        preferences_friends: list[list[int]]
        friends_max_number: int

    preferences_subjects: PreferencesSubjects
    preferences_friends: PreferencesFriends | None = None
