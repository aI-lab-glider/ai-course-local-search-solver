from local_search.helpers.camel_to_snake import camel_to_snake
import random

from local_search.problems.base.move_generator import MoveGenerator
from local_search.problems.graph_coloring_problem.state import GraphColoringState
from local_search.problems.graph_coloring_problem.moves import ChangeColor
from typing import Generator


class GraphColoringMoveGenerator(MoveGenerator):
    move_generators = {}

    def __init_subclass__(cls) -> None:
        GraphColoringMoveGenerator.move_generators[camel_to_snake(
            cls.__name__)] = cls

    def __init__(self, n_vertices: int):
        self.n_vertices = n_vertices


class ChangeColorMg(GraphColoringMoveGenerator):

    def random_moves(self, state: GraphColoringState) -> Generator[ChangeColor, None, None]:
        while True:
            yield ChangeColor(state,
                              idx=random.randint(0, self.n_vertices-1),
                              color=random.randint(0, self.n_vertices-1))

    def available_moves(self, state: GraphColoringState) -> Generator[ChangeColor, None, None]:
        return (ChangeColor(state, idx, color) for idx in range(self.n_vertices) for color in range(self.n_vertices))

# TODO add Kemp Chain
