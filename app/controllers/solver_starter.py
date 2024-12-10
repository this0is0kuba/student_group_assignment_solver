from app.solver.solver import StudentAssignmentSolver
from models import InputGroupsWithFriends, Solution, InputData
from tools.data_processing import prepare_for_subjects_1, prepare_for_subjects_2, prepare_for_subjects_with_average, \
    prepare_for_groups, prepare_for_groups_with_friends


def start_process(input_data: InputData) -> Solution:

    # Prepare input for minizinc solvers
    input_subjects_1 = prepare_for_subjects_1(input_data)
    input_subjects_2 = prepare_for_subjects_2(input_data)
    input_subjects_with_average = prepare_for_subjects_with_average(input_data)

    input_groups = prepare_for_groups(input_data)
    input_groups_with_friends: InputGroupsWithFriends | None = None

    if input_data.preferences.friends_info is not None:
        input_groups_with_friends = prepare_for_groups_with_friends(input_data)

    # Run minizinc solvers
    solver = StudentAssignmentSolver(
        input_subjects_1,
        input_subjects_2,
        input_subjects_with_average,
        input_groups,
        input_groups_with_friends
    )

    minizinc_solution = solver.solve()

    # TODO - Verify the solution
    # Verify the solution

    print(minizinc_solution)

    return minizinc_solution
