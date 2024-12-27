import json
import os

import pytest

from models import InputData, InputSubjects1, InputMinizincBase, InputSubjects2, InputSubjectsWithAverage, InputGroups, \
    InputGroupsWithFriends
from utils.input_processing import prepare_for_subjects_1, prepare_for_subjects_2, prepare_for_subjects_with_average, \
    prepare_for_groups, prepare_for_groups_with_friends

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

inputMinizincBaseBasic = InputMinizincBase(
    number_students=4,
    number_instructors=3,
    number_subjects=2,
    number_class_types=1,
    number_classes=5,
    class_type=[1, 1, 1, 1, 1],
    class_subject=[1, 1, 1, 2, 2],
    class_instructor=[1, 2, 2, 1, 3],
    class_time_h=[28, 14, 14, 28, 28],
    instructor_max_h=[100, 100, 100],
    class_type_min_students=[2],
    class_type_max_students=[4],
    number_conditional_students=0,
    conditional_students=[]
)

inputSubjects1Basic = InputSubjects1(
    **inputMinizincBaseBasic.__dict__,
    number_section=1,
    subject_section=[1, 1],
    student_subjects_in_section=[[1], [1], [1], [1]],
    student_preferences=[[2, 1], [2, 1], [2, 1], [1, 2]],
    number_predetermined_subjects=0,
    predetermined_subjects=[],
    number_predetermined_students=0,
    predetermined_students=[],
    predetermined_subjects_for_students=[]
)

inputSubjects2Basic = InputSubjects2(
    **inputSubjects1Basic.__dict__,
    the_saddest_student_happiness=None
)

inputSubjectsWithAverageBasic = InputSubjectsWithAverage(
    **inputSubjects2Basic.__dict__,
    student_average=[300, 350, 500, 450],
    students_happiness=None
)

inputGroupsBasic = InputGroups(
    **inputMinizincBaseBasic.__dict__,
    number_predetermined_students=0,
    predetermined_students=[],
    predetermined_classes_for_students=[],
    predetermined_groups_for_students=[],
    student_subject=None,
    max_number_of_groups=None,
    min_number_of_groups_in_class=None,
)


inputMinizincBaseReal = InputMinizincBase(
    number_students=92,
    number_instructors=11,
    number_subjects=11,
    number_class_types=4,
    number_classes=22,
    class_type=[1, 2, 1, 2, 1, 2, 3, 4, 1, 2, 1, 2, 3, 1, 2, 1, 3, 2, 1, 3, 1, 2],
    class_subject=[1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6, 7, 7, 8, 8, 9, 10, 10, 11, 11],
    class_instructor=[1, 2, 2, 2, 4, 4, 5, 5, 6, 6, 1, 2, 7, 8, 8, 9, 9, 10, 4, 4, 11, 11],
    class_time_h=[14, 28, 28, 20, 14, 14, 10, 20, 14, 28, 10, 20, 10, 14, 28, 28, 14, 42, 14, 14, 14, 28],
    instructor_max_h=[140, 280, 140, 280, 140, 140, 140, 140, 140, 140, 140],
    class_type_min_students=[1, 8, 15, 15],
    class_type_max_students=[100, 15, 30, 30],
    number_conditional_students=0,
    conditional_students=[]
)

inputSubjects1Real = InputSubjects1(
    **inputMinizincBaseReal.__dict__,
    number_section=2,
    subject_section=[1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
    student_subjects_in_section=[
            [3, 2], [3, 2], [3, 2], [3, 2], [2, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2],
            [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [2, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2],
            [3, 2], [3, 2], [3, 2], [2, 2], [3, 2], [3, 2], [2, 2], [3, 2], [3, 2], [3, 2], [2, 2], [3, 2], [3, 2],
            [3, 2], [3, 2], [3, 2], [2, 2], [3, 2], [3, 2], [3, 2], [2, 2], [3, 2], [2, 2], [3, 2], [3, 2], [2, 2],
            [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [2, 2], [3, 2], [2, 2],
            [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [2, 2], [3, 2], [3, 2], [2, 2], [2, 2], [3, 2], [3, 2],
            [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2],
            [3, 2]],
    student_preferences=[
        [4, 7, 6, 5, 1, 3, 2, 7, 4, 5, 2],
        [1, 7, 6, 4, 3, 5, 2, 7, 5, 2, 4],
        [6, 7, 3, 4, 2, 5, 1, 7, 5, 2, 4],
        [4, 7, 6, 5, 1, 2, 3, 7, 5, 4, 2],
        [3, 7, 6, 5, 1, 4, 2, 7, 4, 5, 2],
        [6, 5, 7, 3, 2, 4, 1, 7, 2, 5, 4],
        [3, 7, 5, 6, 1, 2, 4, 5, 4, 7, 2],
        [3, 7, 2, 4, 6, 1, 5, 7, 4, 5, 2],
        [1, 7, 2, 5, 3, 4, 6, 4, 5, 2, 7],
        [4, 7, 5, 6, 2, 3, 1, 4, 7, 2, 5],
        [4, 5, 7, 6, 2, 1, 3, 7, 2, 5, 4],
        [1, 7, 5, 6, 2, 4, 3, 2, 4, 7, 5],
        [5, 7, 6, 3, 2, 4, 1, 7, 2, 5, 4],
        [1, 7, 5, 6, 3, 4, 2, 2, 4, 7, 5],
        [2, 4, 7, 1, 6, 3, 5, 5, 2, 7, 4],
        [1, 7, 5, 6, 3, 4, 2, 7, 4, 5, 2],
        [7, 4, 5, 2, 1, 6, 3, 5, 4, 7, 2],
        [6, 7, 3, 4, 1, 5, 2, 2, 4, 7, 5],
        [3, 7, 5, 6, 2, 4, 1, 2, 5, 7, 4],
        [2, 7, 6, 5, 1, 4, 3, 7, 2, 5, 4],
        [1, 6, 7, 5, 2, 3, 4, 5, 7, 2, 4],
        [3, 7, 5, 6, 1, 2, 4, 5, 7, 4, 2],
        [1, 7, 5, 6, 2, 4, 3, 7, 4, 5, 2],
        [5, 2, 7, 4, 1, 6, 3, 5, 7, 2, 4],
        [3, 6, 7, 5, 1, 4, 2, 7, 5, 2, 4],
        [4, 7, 6, 5, 3, 2, 1, 7, 5, 4, 2],
        [4, 6, 7, 5, 1, 3, 2, 5, 4, 7, 2],
        [3, 7, 6, 5, 1, 4, 2, 7, 2, 5, 4],
        [3, 7, 6, 5, 2, 4, 1, 7, 5, 4, 2],
        [4, 7, 3, 6, 2, 5, 1, 5, 7, 2, 4],
        [5, 7, 6, 3, 2, 4, 1, 7, 2, 5, 4],
        [6, 7, 4, 3, 1, 5, 2, 4, 5, 7, 2],
        [2, 7, 6, 5, 1, 4, 3, 7, 4, 5, 2],
        [5, 3, 7, 4, 1, 6, 2, 7, 2, 5, 4],
        [6, 7, 3, 3, 1, 5, 2, 2, 5, 7, 4],
        [2, 7, 5, 3, 1, 4, 3, 7, 5, 2, 4],
        [4, 7, 3, 6, 2, 5, 1, 5, 7, 2, 4],
        [3, 7, 6, 3, 2, 5, 4, 7, 2, 5, 4],
        [6, 7, 3, 3, 1, 5, 2, 2, 4, 7, 5],
        [2, 7, 5, 3, 1, 3, 4, 7, 5, 4, 2],
        [4, 6, 7, 3, 1, 5, 3, 5, 2, 7, 4],
        [2, 7, 6, 3, 1, 4, 3, 7, 2, 5, 4],
        [1, 2, 6, 5, 4, 7, 3, 2, 7, 5, 4],
        [2, 5, 4, 3, 7, 1, 3, 5, 7, 4, 2],
        [3, 7, 5, 3, 1, 4, 2, 7, 5, 4, 2],
        [5, 7, 6, 3, 1, 4, 2, 5, 4, 7, 2],
        [4, 7, 3, 6, 2, 5, 1, 5, 7, 2, 4],
        [6, 4, 5, 2, 1, 7, 3, 5, 4, 7, 2],
        [5, 1, 6, 4, 3, 7, 2, 2, 7, 5, 4],
        [3, 6, 5, 7, 1, 4, 2, 7, 5, 4, 2],
        [4, 7, 6, 5, 1, 3, 2, 5, 4, 7, 2],
        [3, 7, 6, 5, 2, 4, 1, 7, 4, 5, 2],
        [1, 3, 7, 4, 2, 5, 6, 4, 7, 2, 5],
        [5, 3, 7, 4, 2, 6, 1, 5, 4, 7, 2],
        [6, 7, 5, 3, 2, 4, 1, 7, 2, 5, 4],
        [1, 2, 7, 4, 3, 6, 5, 2, 7, 5, 4],
        [3, 7, 6, 5, 1, 4, 2, 5, 4, 7, 2],
        [6, 4, 7, 5, 2, 1, 3, 2, 7, 5, 4],
        [1, 6, 5, 7, 4, 2, 3, 2, 2, 2, 2],
        [4, 7, 5, 6, 2, 3, 1, 5, 7, 2, 4],
        [2, 7, 5, 6, 3, 4, 1, 5, 4, 7, 2],
        [5, 7, 6, 3, 2, 4, 1, 7, 2, 5, 4],
        [1, 2, 6, 5, 4, 7, 3, 2, 7, 5, 4],
        [3, 5, 7, 6, 2, 1, 4, 7, 2, 5, 4],
        [4, 5, 7, 6, 2, 3, 1, 5, 2, 7, 4],
        [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
        [7, 5, 3, 2, 1, 4, 6, 4, 5, 2, 7],
        [4, 5, 7, 6, 1, 3, 2, 4, 2, 7, 5],
        [4, 7, 6, 5, 2, 3, 1, 7, 4, 5, 2],
        [1, 7, 3, 5, 2, 4, 6, 7, 5, 4, 2],
        [5, 4, 7, 6, 3, 2, 1, 4, 5, 7, 2],
        [7, 3, 5, 4, 1, 6, 2, 2, 4, 7, 5],
        [7, 4, 5, 3, 1, 6, 2, 5, 4, 7, 2],
        [1, 7, 5, 4, 2, 6, 3, 4, 5, 7, 2],
        [4, 1, 7, 6, 2, 3, 5, 5, 7, 2, 4],
        [5, 4, 7, 6, 1, 3, 2, 4, 5, 7, 2],
        [2, 4, 7, 6, 1, 5, 3, 4, 7, 2, 5],
        [3, 5, 7, 6, 2, 1, 4, 7, 2, 5, 4],
        [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
        [5, 4, 7, 3, 1, 6, 2, 7, 4, 5, 2],
        [1, 7, 6, 5, 2, 4, 3, 7, 4, 5, 2],
        [5, 7, 6, 3, 1, 4, 2, 5, 4, 7, 2],
        [3, 7, 6, 5, 1, 2, 4, 7, 4, 5, 2],
        [6, 7, 5, 3, 2, 4, 1, 7, 2, 5, 4],
        [1, 7, 6, 5, 2, 3, 4, 7, 4, 2, 5],
        [3, 7, 6, 5, 1, 4, 2, 7, 5, 4, 2],
        [2, 6, 3, 5, 7, 4, 1, 4, 7, 2, 5],
        [7, 5, 3, 4, 1, 6, 2, 2, 5, 7, 4],
        [2, 5, 3, 4, 7, 1, 6, 7, 4, 2, 5],
        [2, 7, 6, 5, 3, 1, 4, 7, 4, 2, 5],
        [1, 7, 6, 5, 2, 4, 3, 7, 4, 5, 2],
        [5, 4, 7, 3, 2, 6, 1, 4, 5, 7, 2]
    ],
    number_predetermined_subjects=0,
    predetermined_subjects=[],
    number_predetermined_students=0,
    predetermined_students=[],
    predetermined_subjects_for_students=[]
)

inputSubjects2Real = InputSubjects2(
    **inputSubjects1Real.__dict__,
    the_saddest_student_happiness=None
)

inputSubjectsWithAverageReal = InputSubjectsWithAverage(
    **inputSubjects2Real.__dict__,
    student_average=[393, 450, 485, 411, 471, 315, 438, 414, 484, 432, 360, 393, 409, 334, 436, 410, 378, 476, 344, 464,
                     367, 423, 382, 415, 428, 355, 399, 364, 442, 479, 445, 400, 371, 313, 314, 352, 387, 454, 347, 334,
                     439, 417, 338, 424, 491, 403, 452, 367, 438, 364, 409, 441, 468, 478, 338, 425, 302, 459, 401, 415,
                     453, 410, 432, 411, 485, 346, 413, 489, 308, 405, 464, 484, 466, 311, 338, 380, 348, 371, 349, 443,
                     421, 389, 471, 416, 402, 494, 353, 458, 445, 413, 491, 403],
    students_happiness=None
)

inputGroupsReal = InputGroups(
    **inputMinizincBaseReal.__dict__,
    number_predetermined_students=0,
    predetermined_students=[],
    predetermined_classes_for_students=[],
    predetermined_groups_for_students=[],
    student_subject=None,
    max_number_of_groups=None,
    min_number_of_groups_in_class=None
)


inputMinizincBaseFriends = InputMinizincBase(
    number_students=30,
    number_instructors=8,
    number_subjects=6,
    number_class_types=4,
    number_classes=13,
    class_type=[1, 2, 4, 1, 2, 1, 3, 1, 2, 1, 3, 1, 2],
    class_subject=[1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
    class_instructor=[1, 2, 2, 3, 4, 3, 4, 5, 6, 7, 7, 8, 8],
    class_time_h=[28, 14, 14, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28],
    instructor_max_h=[336, 140, 336, 336, 336, 336, 336, 336],
    class_type_min_students=[1, 2, 5, 5],
    class_type_max_students=[30, 5, 10, 10],
    number_conditional_students=0,
    conditional_students=[]
)

inputSubjects1Friends = InputSubjects1(
    **inputMinizincBaseFriends.__dict__,
    number_section=2,
    subject_section=[1, 1, 1, 2, 2, 2],
    student_subjects_in_section=[[0, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [1, 2],
                                 [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [1, 2], [2, 2],
                                 [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 1]],
    student_preferences=[
        [2, 3, 1, 3, 2, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [1, 3, 2, 1, 3, 2],
        [1, 3, 2, 1, 3, 2],
        [2, 3, 1, 1, 3, 2],
        [2, 3, 1, 1, 3, 2],
        [2, 3, 1, 3, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [1, 3, 2, 1, 3, 2],
        [1, 3, 2, 1, 3, 2],
        [2, 3, 1, 1, 3, 2],
        [2, 3, 1, 1, 3, 2],
        [2, 3, 1, 3, 2, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [1, 3, 2, 1, 3, 2],
        [1, 3, 2, 1, 3, 2],
        [2, 3, 1, 1, 3, 2],
        [2, 3, 1, 1, 3, 2]
    ],
    number_predetermined_subjects=0,
    predetermined_subjects=[],
    number_predetermined_students=0,
    predetermined_students=[],
    predetermined_subjects_for_students=[]
)

inputSubjects2Friends = InputSubjects2(
    **inputSubjects1Friends.__dict__,
    the_saddest_student_happiness=None
)

inputSubjectsWithAverageFriends = InputSubjectsWithAverage(
    **inputSubjects2Friends.__dict__,
    student_average=[300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400,
                     500, 500, 500, 500, 500, 500, 500, 500, 500, 500],
    students_happiness=None
)

inputGroupsFriends = InputGroups(
    **inputMinizincBaseFriends.__dict__,
    number_predetermined_students=0,
    predetermined_students=[],
    predetermined_classes_for_students=[],
    predetermined_groups_for_students=[],
    student_subject=None,
    max_number_of_groups=None,
    min_number_of_groups_in_class=None
)

inputGroupsWithFriendsFriends = InputGroupsWithFriends(
    **inputGroupsFriends.__dict__,
    friends_array=[
        [2, 3, 0], [1, 3, 0], [1, 2, 4], [5, 0, 0], [4, 0, 0], [7, 6, 0], [6, 8, 0], [6, 7, 0], [8, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [26, 27, 28], [25, 27, 28], [25, 26, 28], [25, 26, 27], [30, 0, 0],
        [29, 0, 0]
    ],
    friends_max_number=3,
    groups_with_common_students=None,
)


inputMinizincBaseCustomConstraints = InputMinizincBase(
    number_students=30,
    number_instructors=8,
    number_subjects=6,
    number_class_types=4,
    number_classes=13,
    class_type=[1, 2, 4, 1, 2, 1, 3, 1, 2, 1, 3, 1, 2],
    class_subject=[1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
    class_instructor=[1, 2, 2, 3, 4, 3, 4, 5, 6, 7, 7, 8, 8],
    class_time_h=[28, 14, 14, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28],
    instructor_max_h=[336, 140, 336, 336, 336, 336, 336, 336],
    class_type_min_students=[1, 2, 5, 5],
    class_type_max_students=[30, 5, 10, 10],
    number_conditional_students=7,
    conditional_students=[1, 2, 3, 4, 5, 6, 7]
)

inputSubjects1CustomConstraints = InputSubjects1(
    **inputMinizincBaseCustomConstraints.__dict__,
    number_section=2,
    subject_section=[1, 1, 1, 2, 2, 2],
    student_subjects_in_section=[[0, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [1, 2],
                                 [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [1, 2], [2, 2],
                                 [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 1]],
    student_preferences=[
        [2, 3, 1, 3, 2, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [1, 3, 2, 1, 3, 2],
        [1, 3, 2, 1, 3, 2],
        [2, 3, 1, 1, 3, 2],
        [2, 3, 1, 1, 3, 2],
        [2, 3, 1, 3, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [1, 3, 2, 1, 3, 2],
        [1, 3, 2, 1, 3, 2],
        [2, 3, 1, 1, 3, 2],
        [2, 3, 1, 1, 3, 2],
        [2, 3, 1, 3, 2, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [2, 3, 1, 2, 3, 1],
        [1, 3, 2, 1, 3, 2],
        [1, 3, 2, 1, 3, 2],
        [2, 3, 1, 1, 3, 2],
        [2, 3, 1, 1, 3, 2]
    ],
    number_predetermined_subjects=2,
    predetermined_subjects=[3, 6],
    number_predetermined_students=1,
    predetermined_students=[2],
    predetermined_subjects_for_students=[[3, 6, 0, 0, 0, 0]]
)

inputSubjects2CustomConstraints = InputSubjects2(
    **inputSubjects1CustomConstraints.__dict__,
    the_saddest_student_happiness=None
)

inputSubjectsWithAverageCustomConstraints = InputSubjectsWithAverage(
    **inputSubjects2CustomConstraints.__dict__,
    student_average=[300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400,
                     500, 500, 500, 500, 500, 500, 500, 500, 500, 500],
    students_happiness=None
)

inputGroupsCustomConstraints = InputGroups(
    **inputMinizincBaseCustomConstraints.__dict__,
    number_predetermined_students=1,
    predetermined_students=[2],
    predetermined_classes_for_students=[[7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    predetermined_groups_for_students=[[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    student_subject=None,
    max_number_of_groups=None,
    min_number_of_groups_in_class=None
)


def load_json_file(file_path: str):
    with open(file_path, "r") as file:
        return json.load(file)


@pytest.mark.parametrize(
    "path, expected",
    [
        (os.path.join(TEST_DIR, "resources/basic.json"), inputSubjects1Basic),
        (os.path.join(TEST_DIR, "resources/real.json"), inputSubjects1Real),
        (os.path.join(TEST_DIR, "resources/medium_friends.json"), inputSubjects1Friends),
        (os.path.join(TEST_DIR, "resources/medium_custom_constraints.json"), inputSubjects1CustomConstraints)
    ]
)
def test_prepare_for_subjects_1(path, expected):

    json_data = load_json_file(path)
    input_data = InputData(**json_data)

    minizinc_input = prepare_for_subjects_1(input_data)
    print(TEST_DIR)

    assert minizinc_input == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        (os.path.join(TEST_DIR, "resources/basic.json"), inputSubjects2Basic),
        (os.path.join(TEST_DIR, "resources/real.json"), inputSubjects2Real),
        (os.path.join(TEST_DIR, "resources/medium_friends.json"), inputSubjects2Friends),
        (os.path.join(TEST_DIR, "resources/medium_custom_constraints.json"), inputSubjects2CustomConstraints)
    ]
)
def test_prepare_for_subjects_2(path, expected):

    json_data = load_json_file(path)
    input_data = InputData(**json_data)

    minizinc_input = prepare_for_subjects_2(input_data)

    assert minizinc_input == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        (os.path.join(TEST_DIR, "resources/basic.json"), inputSubjectsWithAverageBasic),
        (os.path.join(TEST_DIR, "resources/real.json"), inputSubjectsWithAverageReal),
        (os.path.join(TEST_DIR, "resources/medium_friends.json"), inputSubjectsWithAverageFriends),
        (os.path.join(TEST_DIR, "resources/medium_custom_constraints.json"), inputSubjectsWithAverageCustomConstraints)
    ]
)
def test_prepare_for_subjects_with_average(path, expected):

    json_data = load_json_file(path)
    input_data = InputData(**json_data)

    minizinc_input = prepare_for_subjects_with_average(input_data)

    assert minizinc_input == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        (os.path.join(TEST_DIR, "resources/basic.json"), inputGroupsBasic),
        (os.path.join(TEST_DIR, "resources/real.json"), inputGroupsReal),
        (os.path.join(TEST_DIR, "resources/medium_friends.json"), inputGroupsFriends),
        (os.path.join(TEST_DIR, "resources/medium_custom_constraints.json"), inputGroupsCustomConstraints)
    ]
)
def test_prepare_for_groups(path, expected):

    json_data = load_json_file(path)
    input_data = InputData(**json_data)

    minizinc_input = prepare_for_groups(input_data)

    assert minizinc_input == expected


def test_prepare_for_groups_with_friends():

    json_data = load_json_file(os.path.join(TEST_DIR, "resources/medium_friends.json"))
    input_data = InputData(**json_data)

    minizinc_input = prepare_for_groups_with_friends(input_data)

    assert minizinc_input == inputGroupsWithFriendsFriends
