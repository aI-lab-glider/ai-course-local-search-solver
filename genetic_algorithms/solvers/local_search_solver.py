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
        while not self.timeout():
            next_state = algorithm.next_state(model, solution)
            if next_state:
                solution = next_state
            else:
                break
        self.stop_timer()
        return solution
