
from dataclasses import dataclass
from typing import Iterable, List

from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.traveling_salesman_problem.models.edge import \
    Edge
from random import sample

@dataclass
class TravelingSalesmanState(State):
    route: List[int]

    def __str__(self):
        return str.join(" -> ", map(lambda idx: f'({self.model.points[idx].x}, {self.model.points[idx].y})', self.route))

    @property
    def edges(self) -> Iterable[Edge]:
        not_connected_edges = zip(
            self.route,
            self.route[1:] + [self.route[0]]
        )
        return map(lambda edge: Edge(edge[0], edge[1]), not_connected_edges)
    
    def __eq__(self, other):
        if other is None:
            return False
        is_any_idx_differs = any(self.route[i] != other.route[i] for i in range(len(self.route)))
        return not is_any_idx_differs

    def shuffle(self):
        new_route = [self.route[0]] + sample(self.route[1:-1], len(self.route) - 2) + [self.route[-1]]
        return TravelingSalesmanState(model=self.model, route=new_route)