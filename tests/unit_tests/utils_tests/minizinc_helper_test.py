import unittest
from unittest.mock import MagicMock, patch

from minizinc import MiniZincError, Status

from models.errors.errors import UnsatisfiableError, MinizincSolverError, MinizincTimeoutError
from utils.minizinc_helper import solve_using_minizinc


class TestSolveUsingMinizinc(unittest.TestCase):

    @patch('utils.minizinc_helper.logger')
    @patch('minizinc.Instance')
    def test_unsatisfiable(self, mock_instance, mock_logger):

        mock_result = MagicMock()
        mock_result.status = Status.UNSATISFIABLE
        mock_instance.solve.return_value = mock_result

        with self.assertRaises(UnsatisfiableError) as _:
            solve_using_minizinc(mock_instance, 1)

        mock_logger.info.assert_called()

    @patch('utils.minizinc_helper.logger')
    @patch('minizinc.Instance')
    def test_unknown_status(self, mock_instance, mock_logger):

        mock_result = MagicMock()
        mock_result.status = Status.UNKNOWN
        mock_instance.solve.return_value = mock_result

        with self.assertRaises(MinizincTimeoutError) as _:
            solve_using_minizinc(mock_instance, 1)

        mock_logger.info.assert_called()

    @patch('minizinc.Instance')
    def test_successful_result(self, mock_instance):

        mock_result = MagicMock()
        mock_result.status = Status.SATISFIED
        mock_instance.solve.return_value = mock_result

        result = solve_using_minizinc(mock_instance, 1)
        self.assertEqual(result, mock_result)

    @patch('utils.minizinc_helper.logger')
    @patch('minizinc.Instance')
    def test_minizinc_error(self, mock_instance, mock_logger):

        mock_instance.solve.side_effect = MiniZincError()

        with self.assertRaises(MinizincSolverError) as _:
            solve_using_minizinc(mock_instance, 1)

        mock_logger.exception.assert_called()


if __name__ == "__main__":
    unittest.main()
