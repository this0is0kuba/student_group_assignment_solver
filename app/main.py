from threading import Lock

from fastapi import FastAPI, HTTPException
from app.models import InputData
from controllers.solver_starter import start_process
from models import Solution

app = FastAPI()
solver_lock = Lock()


@app.post("/run-solver")
def run_solver(input_data: InputData) -> Solution:

    if not solver_lock.acquire(blocking=False):
        raise HTTPException(status_code=429, detail="Server is busy. Try again later.")

    try:
        return start_process(input_data)
    finally:
        solver_lock.release()
