from datetime import timedelta
from minizinc import MiniZincError, Instance, Result, Status

from models.errors.errors import MinizincSolverError, UnsatisfiableError


def solve_using_minizinc(instance: Instance, seconds) -> Result:

    try:
        result = instance.solve(processes=8, timeout=timedelta(seconds=seconds))

        if result.status == Status.UNKNOWN:
            raise MinizincSolverError(detail="Solution not found. Consider increasing the time limit.")

        if result.status == Status.UNSATISFIABLE:
            raise UnsatisfiableError(
                detail="""It's impossible to create groups from the provided data. 
                          Please reconsider your model and make changes."""
            )

        return result

    except MiniZincError as e:
        print(e.message)
        raise MinizincSolverError(detail="Some unexpected error occurred. Contact your administrator.")

