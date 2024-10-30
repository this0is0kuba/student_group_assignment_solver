from pydantic import BaseModel

from models.input_data_elements.information_elements import BasicInfo, ClassInfo, Constraints


class Information(BaseModel):

    basic_info: BasicInfo
    class_info: ClassInfo
    constraints: Constraints
