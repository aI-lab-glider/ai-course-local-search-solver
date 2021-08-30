from genetic_algorithms.problems.base.moves import Move
from genetic_algorithms.problems.traveling_salesman_problem.models.edge import \
    Edge
from genetic_algorithms.problems.traveling_salesman_problem.state import \
    TravelingSalesmanState


class SwapEdges(Move[TravelingSalesmanState]):
    def __init__(self, from_state: TravelingSalesmanState, a: Edge, b: Edge):
        super().__init__(from_state)
        (self.a, self.b) = a, b

    def make(self) -> TravelingSalesmanState:
        indicies = [*self.state.route]
        indicies[self.a.end], indicies[self.b.end] = indicies[self.b.end], indicies[self.a.end]
        return TravelingSalesmanState(model=self.state.model, route=indicies)
