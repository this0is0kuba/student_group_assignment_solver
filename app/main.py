from threading import Lock
from fastapi import FastAPI, HTTPException

from dependecies.logger import logger
from models import InputData, Solution
from controllers.solver_starter import start_process

app = FastAPI()
solver_lock = Lock()


@app.post("/run-solver")
def run_solver(input_data: InputData) -> Solution:

    if not solver_lock.acquire(blocking=False):
        raise HTTPException(status_code=503, detail="Server is busy. Try again later.")

    try:
        return start_process(input_data)

    except Exception as e:
        logger.exception("An error occurred while running the solver process: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error.")

    finally:
        solver_lock.release()
