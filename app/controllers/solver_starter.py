from app.models import Input
from app.solver.solver import StudentAssignmentSolver
from models.solution import Solution
from solver.preprocessor import prepare_input_for_student_preferences, prepare_input_for_parallel_groups


async def start_process(solver_input: Input) -> None:

    input_student_preferences = prepare_input_for_student_preferences(solver_input)
    input_parallel_groups = prepare_input_for_parallel_groups(solver_input)

    solver: StudentAssignmentSolver = StudentAssignmentSolver(input_student_preferences, input_parallel_groups)
    solution: Solution = solver.solve()

    print(solution)
    # TODO - save solution
