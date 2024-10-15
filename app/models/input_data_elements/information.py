from pydantic import BaseModel

from models.input_data_elements.information_elements import BasicInfo, ClassInfo, Constraints, ScienceClubAndResearch


class Information(BaseModel):

    basic_info: BasicInfo
    class_info: ClassInfo
    science_club_and_research: ScienceClubAndResearch
    constraints: Constraints
