from dataclasses import dataclass
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model


@dataclass
class Solution:
    final_state: State
    problem_model: Model
