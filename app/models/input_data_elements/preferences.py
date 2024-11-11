from pydantic import BaseModel


class StudentPreferences(BaseModel):

    class FriendsInfo(BaseModel):
        friends_array: list[list[int]]
        max_number_friends: int

    preferences_subjects: list[list[int]]
    friends_info: FriendsInfo | None = None
