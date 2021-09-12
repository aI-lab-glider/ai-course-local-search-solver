from genetic_algorithms.problems.base import Model, State
from genetic_algorithms.helpers import History
from genetic_algorithms.solvers.solver import Solver
from genetic_algorithms.models.algorithm import Algorithm


class LocalSearchSolver(Solver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def solve(self, model: Model, algorithm: Algorithm) -> State:
        self.start_timer()
        solution = model.initial_solution
        while not algorithm.is_terminated and not self.timeout():
            solution = algorithm.next_state(model, solution)
            self._update_best_state(model, solution)
        self.stop_timer()
        return solution

    def _update_best_state(self, model: Model, solution: State) -> None:
        if model.cost_for(model.best_state) > model.cost_for(solution):
            model.best_state = solution
