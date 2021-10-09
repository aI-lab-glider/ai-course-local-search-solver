from typing import Any, Callable, Dict, Generic, List, Type, TypeVar
from local_search.algorithm_subscribers.algorithm_monitor import AlgorithmStatistics
from local_search.algorithms.algorithm import Algorithm
from local_search.algorithms.subscribable_algorithm import MIN_NICENCESS, SubscribableAlgorithm
from local_search.problems.base import State, Problem
from local_search.solvers.solver import Solver
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class Solution:
    state: State
    problem: Problem
    statistics: AlgorithmStatistics

    def to_dict(self):
        return {
            "state": self.state.asdict(),
            "problem": self.problem.asdict(),
            "statistics": self.statistics.asdict()
        }

    def to_json(self, path: Path):
        with open(path) as target:
            json.dump(self.to_dict(), target)

    @staticmethod
    def from_json(path: Path, problem_type: Type[Problem], state_type: Type[State]):
        with open(path) as source:
            data = json.load(source)
            problem = problem_type.from_dict(data["problem"])
            state = state_type.from_dict(data["state"])
            statistics = AlgorithmStatistics.from_dict(data["statistics"])
        return Solution(
            state=state,
            problem=problem,
            statistics=statistics
        )


class LocalSearchSolver(Solver):
    """
    Wrapper that contains all logic except algorithm
    """

    def solve(self, model: Problem, algorithm: SubscribableAlgorithm) -> Solution:
        statistics_subscription = algorithm.subscribe(
            self.algorithm_monitor, niceness=MIN_NICENCESS)
        # TODO delegate to algorithm monitor
        self.start_timer()
        solution_state = model.initial_state
        while not self.is_timeout():
            next_state = algorithm.next_state(model, solution_state)
            if next_state:
                solution_state = next_state
            else:
                break
        self.stop_timer()
        statistics = statistics_subscription.subscriber.statistics
        statistics_subscription.close()
        return Solution(
            state=solution_state,
            problem=model,
            statistics=statistics)
