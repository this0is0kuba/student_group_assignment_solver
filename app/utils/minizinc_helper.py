from datetime import timedelta
from minizinc import MiniZincError, Instance, Result, Status

from dependecies.logger import logger
from models.errors.errors import MinizincSolverError, UnsatisfiableError, MinizincTimeoutError


def solve_using_minizinc(instance: Instance, seconds) -> Result:

    try:
        result = instance.solve(processes=8, timeout=timedelta(seconds=seconds))

        if result.status == Status.UNSATISFIABLE:

            logger.info("Solution unsatisfiable. Status: UNSATISFIABLE.")

            raise UnsatisfiableError(
                detail="It's impossible to create groups from the provided data. " +
                       "Please reconsider your model and make changes."
            )

        if result.status == Status.UNKNOWN:

            logger.info("Solution not found. Status: UNKNOWN.")
            raise MinizincTimeoutError(detail="Solution not found. Too much data for the server to find a solution " +
                                              " in a timely manner.")

        return result

    except MiniZincError as e:
        logger.exception("An unexpected MiniZincError occurred: %s", str(e))
        raise MinizincSolverError(detail="Some unexpected error occurred. Contact your administrator.")

