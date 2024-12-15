from pydantic import BaseModel, Field


class StudentPreferences(BaseModel):

    class FriendsInfo(BaseModel):
        friends_array: list[list[int]]
        max_number_friends: int = Field(ge=1)

    preferences_subjects: list[list[int]]
    friends_info: FriendsInfo | None = None
