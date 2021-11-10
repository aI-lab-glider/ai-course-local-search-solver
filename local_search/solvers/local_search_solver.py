from typing import Any, Callable, Dict, Generic, List, Type, TypeVar
from local_search.algorithms.subscribable_algorithm import MIN_NICENCESS, SubscribableAlgorithm
from local_search.problems.base import Problem
from local_search.solvers.solution import Solution
from local_search.solvers.solver import Solver


class LocalSearchSolver(Solver):
    """
    Wrapper that contains all logic except algorithm
    """

    def solve(self, model: Problem, algorithm: SubscribableAlgorithm) -> Solution:
        statistics_subscription = algorithm.subscribe(
            self.algorithm_monitor, niceness=MIN_NICENCESS)
        self.start_timer()
        solution_state = model.initial_state
        while not self.is_timeout():
            try:
                next_state = algorithm.next_state(model, solution_state)
            except (SystemExit, KeyboardInterrupt):
                solution_state = algorithm.best_state
                break
            if next_state:
                solution_state = next_state
            else:
                solution_state = algorithm.best_state
                break

        self.stop_timer()
        statistics = statistics_subscription.subscriber.statistics
        statistics_subscription.close()
        return Solution(
            state=solution_state,
            problem=model,
            statistics=statistics,
            algorithm_config=algorithm.config)
