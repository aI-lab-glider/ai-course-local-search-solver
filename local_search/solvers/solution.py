from dataclasses import dataclass
from inspect import signature
from local_search.algorithms.algorithm_config import AlgorithmConfig
from local_search.algorithms.subscribable_algorithm import SubscribableAlgorithm
from local_search.helpers.get_type_for_param import get_type_for_param
from local_search.problems.base import State, Problem
from local_search.algorithm_subscribers.algorithm_monitor import AlgorithmStatistics
from pathlib import Path
import json


@dataclass
class Solution:
    state: State
    problem: Problem
    statistics: AlgorithmStatistics
    algorithm_config: AlgorithmConfig

    def to_dict(self):
        return {
            "state": self.state.asdict(),
            "problem": self.problem.asdict(),
            "statistics": self.statistics.asdict(),
            "algorithm_config": self.algorithm_config.asdict(),
        }

    def to_json(self, path: Path):
        with open(path, 'w+') as target:
            json.dump(self.to_dict(), target, indent=4)

    @staticmethod
    def from_json(path: Path):
        with open(path) as source:
            data = json.load(source)
            problem = Problem.from_dict(data["problem"])
            state = State.from_dict(data["state"])
            statistics = AlgorithmStatistics.from_dict(data["statistics"])
            config_type = get_type_for_param(
                SubscribableAlgorithm.algorithms[statistics.algorithm_name], 'config')
            algorithm_config = config_type(**data['algorithm_config'])
        return Solution(
            state=state,
            problem=problem,
            statistics=statistics,
            algorithm_config=algorithm_config
        )
