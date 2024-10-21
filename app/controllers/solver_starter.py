from app.models import InputData
from app.solver.solver import StudentAssignmentSolver
from models.minizinc_solution import MinizincSolution
from tools.preprocessor import Preprocessor


def start_process(input_data: InputData) -> None:

    # Prepare input for minizinc solvers
    minizinc_student_preferences = Preprocessor.prepare_student_preferences(input_data)
    minizinc_parallel_groups = Preprocessor.prepare_parallel_groups(input_data)

    # Run minizinc solver
    solver: StudentAssignmentSolver = StudentAssignmentSolver(minizinc_student_preferences, minizinc_parallel_groups)
    minizincSolution: MinizincSolution = solver.solve()

    # TODO - Verify the solution
    # Verify the solution

    # TODO - Covert minizinc solution
    # Covert minizinc solution

    # TODO - Save solution
    # Save solution

    print(minizincSolution)
