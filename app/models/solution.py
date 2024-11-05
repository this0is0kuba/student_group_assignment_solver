from pydantic import BaseModel


class Solution(BaseModel):

    # 2 dimensional array about students' groups.
    # Example:
    # student_group[1, 2] = 3 means that student with index 1 is assigned to group number 3 for subject with number 2
    student_group: list[list[int]]
