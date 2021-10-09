from local_search.algorithms.algorithm import Algorithm
from local_search.algorithms.subscribable_algorithm import SubscribableAlgorithm
from local_search.problems.base import Problem, State
from local_search.solvers.solver import Solver


class LocalSearchSolver(Solver):
    """
    Wrapper that contains all logic except algorithm
    """

    def solve(self, model: Problem, algorithm: SubscribableAlgorithm) -> State:
        statistics_subscription = algorithm.subscribe(self.algorithm_monitor)
        self.start_timer()
        solution = model.initial_solution
        while not self.timeout():
            next_state = algorithm.next_state(model, solution)
            if next_state:
                solution = next_state
            else:
                break
        self.stop_timer()
        statistics_subscription.close()
        return solution
