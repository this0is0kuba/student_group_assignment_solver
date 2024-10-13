from fastapi import FastAPI
from app.models import Input

app = FastAPI()


@app.post("/run-solver")
async def run_solver(solver_input: Input):

    

    return {"message": "started solving"}


@app.get("/results")
async def get_results():
    return {"message": "results"}
