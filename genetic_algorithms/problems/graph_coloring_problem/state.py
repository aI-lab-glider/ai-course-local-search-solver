
from dataclasses import dataclass
from typing import List

from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.graph_coloring_problem.models.vertex import Vertex


@dataclass
class GraphColoringState(State):
    coloring: List[Vertex]

    def __str__(self):
        return " ".join([f"({v.idx}: {v.color})" for v in self.coloring])
