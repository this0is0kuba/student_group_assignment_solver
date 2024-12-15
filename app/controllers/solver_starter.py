from app.models import InputData
from app.solver.solver import StudentAssignmentSolver
from models import InputStudentGroupsWithFriends, Solution

from utils.data_processing import prepare_input_student_groups, \
    prepare_input_student_subjects_with_average, prepare_input_student_subjects_1, prepare_input_student_subjects_2, \
    prepare_input_student_groups_with_friends


def start_process(input_data: InputData) -> Solution:

    # Prepare input for minizinc solvers
    input_student_subjects_1 = prepare_input_student_subjects_1(input_data)
    input_student_subjects_2 = prepare_input_student_subjects_2(input_data)
    input_student_subjects_with_average = prepare_input_student_subjects_with_average(input_data)

    input_student_groups = prepare_input_student_groups(input_data)
    input_student_groups_with_friends: InputStudentGroupsWithFriends | None = None

    if input_data.preferences.friends_info is not None:
        input_student_groups_with_friends = prepare_input_student_groups_with_friends(input_data)

    # Run minizinc solvers
    solver = StudentAssignmentSolver(
        input_student_subjects_1,
        input_student_subjects_2,
        input_student_subjects_with_average,
        input_student_groups,
        input_student_groups_with_friends
    )

    minizinc_solution = solver.solve()

    # TODO - Verify the solution
    # Verify the solution

    print(minizinc_solution)

    return minizinc_solution
