from app.solver.models.input import Input


class Solver:

    def __int__(self, solver_input: Input):
        self.solver_input = solver_input
        self._preprocess_data()

    def solve(self):
        pass

    def _preprocess_data(self):
        pass
