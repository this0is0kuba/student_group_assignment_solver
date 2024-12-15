from datetime import timedelta
from minizinc import MiniZincError

from models.errors.errors import MinizincSolverError


def solve_using_minizinc(instance, seconds):

    try:
        return instance.solve(processes=8, timeout=timedelta(seconds=seconds))
    except MiniZincError as e:
        raise MinizincSolverError(detail=e.message)
