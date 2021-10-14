from typing import List, Dict, Set

from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.base.move_generator import MoveGenerator
from local_search.problems.graph_coloring_problem.state import GraphColoringState


class GraphColoringMoveGenerator(MoveGenerator):
    move_generators = {}

    def __init_subclass__(cls) -> None:
        GraphColoringMoveGenerator.move_generators[camel_to_snake(
            cls.__name__)] = cls

    def __init__(self, graph: Dict[int, Set[int]], n_vertices: int):
        self.n_vertices = n_vertices
        self.graph = graph

    def get_available_colors(self, idx: int, state: GraphColoringState):
        used_colors = set([v.color for v in state.coloring])
        return tuple(
            used_colors.difference({state.coloring[idx].color}))
