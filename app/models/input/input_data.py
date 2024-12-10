from pydantic import BaseModel

from models.input.input_data_elements import CustomConstraints
from models.input.input_data_elements.information import Information
from models.input.input_data_elements import StudentPreferences


class InputData(BaseModel):

    information: Information
    preferences: StudentPreferences
    custom_constraints: CustomConstraints | None
