from dataclasses import dataclass
from local_search.problems.base.state import State
from local_search.problems.base.problem import Problem


@dataclass
class Solution:
    final_state: State
    problem_model: Problem
