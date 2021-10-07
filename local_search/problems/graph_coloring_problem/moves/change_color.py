import random
from typing import Generator

from local_search.problems.base.moves import Move
from local_search.problems.graph_coloring_problem.moves.move_generator import GraphColoringMoveGenerator
from local_search.problems.graph_coloring_problem.state import GraphColoringState
import copy


class ChangeColorMove(Move[GraphColoringState]):
    def __init__(self, from_state: GraphColoringState, idx: int, color: int):
        super().__init__(from_state)
        (self.idx, self.color) = idx, color

    def make(self) -> GraphColoringState:
        new_coloring = copy.deepcopy(self.state.coloring)
        new_coloring[self.idx].color = self.color
        return GraphColoringState(coloring=new_coloring)


class ChangeColor(GraphColoringMoveGenerator):

    def random_moves(self, state: GraphColoringState) -> Generator[ChangeColorMove, None, None]:
        used_colors = set([v.color for v in state.coloring])
        while True:
            idx = random.randrange(self.n_vertices)
            available_colors = used_colors.difference(state.coloring[idx].color)
            yield ChangeColorMove(state,
                              idx=random.randrange(self.n_vertices),
                              color=random.choice(available_colors))

    def available_moves(self, state: GraphColoringState) -> Generator[ChangeColorMove, None, None]:
        used_colors = set([v.color for v in state.coloring])
        for idx in range(self.n_vertices):
            for color in used_colors:
                if state.coloring[idx].color == color:
                    continue
                yield ChangeColorMove(state, idx, color)

