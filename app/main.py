from fastapi import FastAPI, BackgroundTasks
from app.models import InputData
from controllers.solver_starter import start_process

app = FastAPI()


@app.post("/run-solver")
async def run_solver(input_data: InputData, background_tasks: BackgroundTasks):

    background_tasks.add_task(start_process, input_data)

    return {"message": "started solving"}


@app.get("/results")
async def get_results():
    return {"message": "results"}
