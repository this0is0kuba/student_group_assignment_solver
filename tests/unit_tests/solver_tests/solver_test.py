import unittest
from unittest.mock import MagicMock, patch

from models import InputSubjects1, InputSubjects2, InputSubjectsWithAverage, InputGroups, InputGroupsWithFriends
from solver.solver import StudentAssignmentSolver


class TestStudentAssignmentSolver(unittest.TestCase):

    @patch('utils.minizinc_helper.solve_using_minizinc')
    @patch('minizinc.Solver.lookup')
    def test_solve_method_calls(self, MockSolverLookup, MockSolveUsingMinizinc):

        # Mock inputs for the StudentAssignmentSolver
        input_subjects_1 = MagicMock(spec=InputSubjects1)
        input_subjects_2 = MagicMock(spec=InputSubjects2)
        input_subjects_with_average = MagicMock(spec=InputSubjectsWithAverage)
        input_groups = MagicMock(spec=InputGroups)
        input_groups_with_friends = MagicMock(spec=InputGroupsWithFriends)

        # Mock the solver object
        mock_solver = MagicMock()
        MockSolverLookup.return_value = mock_solver

        # Mock the return value of solve_using_minizinc
        MockSolveUsingMinizinc.return_value = {
            "key": "value"
        }

        # Instantiate the solver
        solver = StudentAssignmentSolver(
            input_subjects_1=input_subjects_1,
            input_subjects_2=input_subjects_2,
            input_subjects_with_average=input_subjects_with_average,
            input_groups=input_groups,
            input_groups_with_friends=input_groups_with_friends
        )

        # Mock the internal methods of StudentAssignmentSolver
        solver._solve_subjects_1 = MagicMock()
        solver._solve_subjects_2 = MagicMock()
        solver._solve_subjects_with_average = MagicMock()
        solver._solve_groups = MagicMock()
        solver._solve_groups_with_friends = MagicMock()

        solver._create_instance_subjects_1 = MagicMock()
        solver._create_instance_subjects_2 = MagicMock()
        solver._create_instance_subjects_with_average = MagicMock()
        solver._create_instance_groups = MagicMock()
        solver._create_instance_groups_with_friends = MagicMock()

        # Call the solve method
        solver.solve()

        # Assert that _solve_ methods were called once
        solver._solve_subjects_1.assert_called_once_with(mock_solver)
        solver._solve_subjects_2.assert_called_once_with(mock_solver, solver._solve_subjects_1.return_value)
        solver._solve_subjects_with_average.assert_called_once_with(mock_solver, solver._solve_subjects_2.return_value)
        solver._solve_groups.assert_called_once_with(mock_solver, solver._solve_subjects_with_average.return_value)
        solver._solve_groups_with_friends.assert_called_once_with(
            mock_solver,
            solver._solve_subjects_with_average.return_value,
            solver._solve_groups.return_value
        )


if __name__ == "__main__":
    unittest.main()