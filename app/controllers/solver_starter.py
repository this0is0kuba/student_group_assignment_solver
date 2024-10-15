from app.models import InputData
from app.solver.solver import StudentAssignmentSolver
from models.solution import Solution
from solver.preprocessor import prepare_input_for_student_preferences, prepare_input_for_parallel_groups


def start_process(input_data: InputData) -> None:

    input_student_preferences = prepare_input_for_student_preferences(input_data)
    input_parallel_groups = prepare_input_for_parallel_groups(input_data)

    solver: StudentAssignmentSolver = StudentAssignmentSolver(input_student_preferences, input_parallel_groups)
    solution: Solution = solver.solve()

    print(solution)
    # TODO - save solution
