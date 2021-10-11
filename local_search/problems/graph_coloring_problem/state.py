
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

    def asdict(self):
        base = super().asdict()
        return {
            'coloring': [(vertex.idx, vertex.color) for vertex in self.coloring],
            **base
        }

    @classmethod
    def from_dict(cls, data):
        cls.validate_data(data)
        coloring = [Vertex(idx=vertex_tuple[0], color=vertex_tuple[1])
                    for vertex_tuple in data['coloring']]
        return cls(coloring)
