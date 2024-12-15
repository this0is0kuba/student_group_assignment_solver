from datetime import timedelta
from minizinc import MiniZincError, Instance, Result, Status

from models.errors.errors import MinizincSolverError


def solve_using_minizinc(instance: Instance, seconds) -> Result:

    try:
        result = instance.solve(processes=8, timeout=timedelta(seconds=seconds))

        if result.status == Status.UNKNOWN:
            raise MinizincSolverError(detail="Solution not found. Consider increasing the time limit.")

        if result.status == Status.UNSATISFIABLE:
            raise MinizincSolverError(
                detail="There is no solution. It's impossible to create groups from the provided data."
            )

        return result

    except MiniZincError as e:
        print(e.message)
        raise MinizincSolverError(detail="Some unexpected error occurred. Contact your administrator.")

