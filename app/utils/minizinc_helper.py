from datetime import timedelta
from minizinc import MiniZincError, Instance, Result, Status

from dependecies.logger import logger
from models.errors.errors import MinizincSolverError, UnsatisfiableError, InvalidInputError


def solve_using_minizinc(instance: Instance, seconds) -> Result:

    try:
        result = instance.solve(processes=8, timeout=timedelta(seconds=seconds))

        if result.status == Status.UNSATISFIABLE:

            logger.warning("Solution unsatisfiable. Status: UNSATISFIABLE.")

            raise UnsatisfiableError(
                detail="It's impossible to create groups from the provided data. " +
                       "Please reconsider your model and make changes."
            )

        if result.status == Status.UNKNOWN:
            logger.warning("Solution not found. Status: UNKNOWN.")
            raise MinizincSolverError(detail="Solution not found. Consider increasing the time limit.")

        return result

    except MiniZincError as e:
        logger.exception("An unexpected MiniZincError occurred: %s", e.message)
        raise MinizincSolverError(detail="Some unexpected error occurred. Contact your administrator.")

