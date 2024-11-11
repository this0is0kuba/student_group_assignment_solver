from app.models import InputData
from app.solver.solver import StudentAssignmentSolver
from models import InputStudentGroups, InputStudentSubjectsWithAverage, InputStudentSubjects1, InputStudentSubjects2, \
    InputStudentGroupsWithFriends
from models.minizinc_solutions import Solution
from tools.data_processing import prepare_input_student_groups, \
    prepare_input_student_subjects_with_average, prepare_input_student_subjects_1, prepare_input_student_subjects_2, \
    prepare_input_student_groups_with_friends


def start_process(input_data: InputData) -> None:
    # Prepare input for minizinc solvers
    input_student_subjects_1: InputStudentSubjects1 = prepare_input_student_subjects_1(input_data)
    input_student_subjects_2: InputStudentSubjects2 = prepare_input_student_subjects_2(input_data)
    input_student_subjects_with_average: InputStudentSubjectsWithAverage = \
        prepare_input_student_subjects_with_average(input_data)

    input_student_groups: InputStudentGroups = prepare_input_student_groups(input_data)
    input_student_groups_with_friends: InputStudentGroupsWithFriends | None = None

    if input_data.preferences.friends_info is not None:
        input_student_groups_with_friends = prepare_input_student_groups_with_friends(input_data)

    # Run minizinc solver
    solver: StudentAssignmentSolver = StudentAssignmentSolver(
        input_student_subjects_1,
        input_student_subjects_2,
        input_student_subjects_with_average,
        input_student_groups,
        input_student_groups_with_friends
    )

    minizinc_solution: Solution = solver.solve()

    # TODO - Verify the solution
    # Verify the solution

    # TODO - Save solution
    # Save solution

    print(minizinc_solution)
