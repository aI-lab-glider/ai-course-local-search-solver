from genetic_algorithms.problems.base.moves import Move
from genetic_algorithms.problems.graph_coloring_problem.state import GraphColoringState
import copy


class ChangeColor(Move[GraphColoringState]):
    def __init__(self, from_state: GraphColoringState, idx: int, color: int):
        super().__init__(from_state)
        (self.idx, self.color) = idx, color

    def make(self) -> GraphColoringState:
        new_coloring = copy.deepcopy(self.state.coloring)
        new_coloring[self.idx].color = self.color
        return GraphColoringState(model=self.state.model, coloring=new_coloring)
