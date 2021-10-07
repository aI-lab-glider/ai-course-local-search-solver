
from dataclasses import dataclass
from typing import List
import random
from local_search.problems.base.state import State
from local_search.problems.graph_coloring_problem.models.vertex import Vertex
from copy import deepcopy


@dataclass
class GraphColoringState(State):
    coloring: List[Vertex]

    def __str__(self):
        return " ".join([f"({v.idx}: {v.color})" for v in self.coloring])

    def __eq__(self, other: 'GraphColoringState'):
        if other is None:
            return False
        return all(ov.color == sv.color for sv, ov in zip(self.coloring, other.coloring))
