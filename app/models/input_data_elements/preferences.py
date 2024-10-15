from pydantic import BaseModel


class StudentPreferences(BaseModel):

    class FriendsInfo(BaseModel):
        preferences_friends: list[list[int]]
        friends_max_number: int
        weight: int = 100

    preferences_subjects: list[list[int]]
    friends_info: FriendsInfo | None = None
