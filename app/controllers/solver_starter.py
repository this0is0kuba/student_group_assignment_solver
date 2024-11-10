from app.models import InputData
from app.solver.solver import StudentAssignmentSolver
from models import InputStudentSubjects, InputStudentGroups
from models.solution import Solution
from tools.preprocessor import Preprocessor


def start_process(input_data: InputData) -> None:

    # Prepare input for minizinc solvers
    input_student_subjects: InputStudentSubjects = Preprocessor.prepare_input_student_subjects(input_data)
    input_student_groups: InputStudentGroups = Preprocessor.prepare_input_student_groups(input_data)

    # Run minizinc solver
    solver: StudentAssignmentSolver = StudentAssignmentSolver(input_student_subjects, input_student_groups)
    minizinc_solution: Solution = solver.solve()

    # TODO - Verify the solution
    # Verify the solution

    # TODO - Save solution
    # Save solution

    print(minizinc_solution)
