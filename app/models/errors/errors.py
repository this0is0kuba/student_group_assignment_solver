from fastapi import HTTPException


class MinizincSolverError(HTTPException):
    def __init__(self, detail: str = "An error occurred while solving with Minizinc."):
        super().__init__(status_code=500, detail=detail)


class UnsatisfiableError(HTTPException):
    def __init__(self, detail: str = "There is no solution for the provided data."):
        super().__init__(status_code=400, detail=detail)


class InvalidInputError(HTTPException):
    def __init__(self, detail: str = "Invalid input provided."):
        super().__init__(status_code=400, detail=detail)
