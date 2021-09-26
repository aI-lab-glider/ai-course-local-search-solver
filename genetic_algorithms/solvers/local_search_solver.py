from genetic_algorithms.models.next_state_provider import NextStateProvider
from genetic_algorithms.problems.base import Model, State
from genetic_algorithms.solvers.solver import Solver


class LocalSearchSolver(Solver):
    """
    Wrapper that contains all logic except algorithm
    """

    def solve(self, model: Model, algorithm: NextStateProvider) -> State:
        self.start_timer()
        solution = model.initial_solution
        while not self._is_optimal_solution_found():
            solution = algorithm.next_state(model, solution)
            self._update_best_state(model, solution)
        self.stop_timer()
        return solution

    def _is_optimal_solution_found(self) -> bool:
        return self.cost_history.is_full() and len(set(self.cost_history)) == 1

    def _update_best_state(self, model: Model, solution: State) -> None:
        if model.cost_for(model.best_state) >= model.cost_for(solution):
            model.best_state = solution
            self.cost_history.append(model.cost_for(model.best_state))
