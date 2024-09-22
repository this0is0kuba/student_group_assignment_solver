from fastapi import FastAPI

app = FastAPI()


@app.get("/student-groups")
async def root():
    return {"message": "student groups"}
