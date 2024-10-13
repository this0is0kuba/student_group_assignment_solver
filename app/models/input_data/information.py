from pydantic import BaseModel

from models.input_data.information_elements import BasicInfo, ClassInfo, Constraints, ScienceClubAndResearch


class Information(BaseModel):

    basic_info: BasicInfo
    class_info: ClassInfo
    constraints: Constraints
    science_club_and_research: ScienceClubAndResearch
