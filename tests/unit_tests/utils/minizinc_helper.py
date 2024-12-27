import unittest
from unittest.mock import MagicMock, patch

from minizinc import MiniZincError, Status

from models.errors.errors import UnsatisfiableError, MinizincSolverError
from utils.minizinc_helper import solve_using_minizinc


class TestSolveUsingMinizinc(unittest.TestCase):

    @patch('utils.minizinc_helper.logger')
    @patch('minizinc.Instance')
    def test_unsatisfiable(self, MockInstance, MockLogger):

        mock_instance = MockInstance()
        mock_result = MagicMock()
        mock_result.status = Status.UNSATISFIABLE
        mock_instance.solve.return_value = mock_result

        with self.assertRaises(UnsatisfiableError) as _:
            solve_using_minizinc(mock_instance, 1)

        MockLogger.info.assert_called()

    @patch('utils.minizinc_helper.logger')
    @patch('minizinc.Instance')
    def test_unknown_status(self, MockInstance, MockLogger):

        mock_instance = MockInstance()
        mock_result = MagicMock()
        mock_result.status = Status.UNKNOWN
        mock_instance.solve.return_value = mock_result

        with self.assertRaises(MinizincSolverError) as _:
            solve_using_minizinc(mock_instance, 1)

        MockLogger.info.assert_called()

    @patch('minizinc.Instance')
    def test_successful_result(self, MockInstance):

        mock_instance = MockInstance()
        mock_result = MagicMock()
        mock_result.status = Status.SATISFIED
        mock_instance.solve.return_value = mock_result

        result = solve_using_minizinc(mock_instance, 1)
        self.assertEqual(result, mock_result)

    @patch('utils.minizinc_helper.logger')
    @patch('minizinc.Instance')
    def test_minizinc_error(self, MockInstance, MockLogger):

        mock_instance = MockInstance()
        mock_instance.solve.side_effect = MiniZincError()

        with self.assertRaises(MinizincSolverError) as _:
            solve_using_minizinc(mock_instance, 1)

        MockLogger.exception.assert_called()


if __name__ == "__main__":
    unittest.main()
