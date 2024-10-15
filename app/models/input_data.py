from pydantic import BaseModel
from .input_data_elements.information import Information
from .input_data_elements.preferences import StudentPreferences


class InputData(BaseModel):

    information: Information
    preferences: StudentPreferences
