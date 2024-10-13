from pydantic import BaseModel
from .input_data.information import Information
from .input_data.preferences import StudentPreferences


class Input(BaseModel):

    information: Information
    preferences: StudentPreferences
