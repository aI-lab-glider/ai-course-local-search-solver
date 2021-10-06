
from dataclasses import dataclass
from typing import List
import random
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.graph_coloring_problem.models.vertex import Vertex
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

    # TODO
    def shuffle(self):
        available_colors = {vertex.color for vertex in self.coloring}
        new_coloring = deepcopy(self.coloring)
        for vertex in new_coloring:
            vertex.color = random.choice(list(available_colors))
        return GraphColoringState(self.model, new_coloring)
