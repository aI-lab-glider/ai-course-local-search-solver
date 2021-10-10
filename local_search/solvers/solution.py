from dataclasses import dataclass
from local_search.problems.base import State, Problem
from local_search.algorithm_subscribers.algorithm_monitor import AlgorithmStatistics
from pathlib import Path
import json
from typing import Type


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
        with open(path, 'w+') as target:
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
