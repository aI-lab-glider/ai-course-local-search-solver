import random

from genetic_algorithms.models.move_generator import MoveGenerator
from genetic_algorithms.problems.graph_coloring_problem.state import GraphColoringState
from genetic_algorithms.problems.graph_coloring_problem.moves import ChangeColor
from typing import Generator


class GraphColoringMoveGenerator(MoveGenerator):
    def __init__(self, n_vertices: int):
        self.n_vertices = n_vertices

    def random_move(self, state: GraphColoringState) -> ChangeColor:
        return ChangeColor(state,
                           idx=random.randint(0, self.n_vertices-1),
                           color=random.randint(0, self.n_vertices-1))

    def available_moves(self, state: GraphColoringState) -> Generator[ChangeColor, None, None]:
        return (ChangeColor(state, idx, color) for idx in range(self.n_vertices) for color in range(self.n_vertices))
