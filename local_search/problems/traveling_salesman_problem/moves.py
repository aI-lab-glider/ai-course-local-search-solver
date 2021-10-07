from local_search.problems.base.moves import Move
from local_search.problems.traveling_salesman_problem.models.edge import \
    Edge
from local_search.problems.traveling_salesman_problem.state import \
    TravelingSalesmanState


class SwapTwoEdges(Move[TravelingSalesmanState]):
    def __init__(self, from_state: TravelingSalesmanState, a: Edge, b: Edge):
        super().__init__(from_state)
        (self.a, self.b) = a, b

    def make(self) -> TravelingSalesmanState:
        indices = [*self.state.route]
        indices[self.a.end], indices[self.b.end] = indices[self.b.end], indices[self.a.end]
        return TravelingSalesmanState(points=self.state.points, route=indices)

class SwapThreeEdges(Move[TravelingSalesmanState]):
    def __init__(self, from_state: TravelingSalesmanState, a: Edge, b: Edge, c: Edge):
        super().__init__(from_state)
        self.edges = [a, b, c]

    def make(self) -> TravelingSalesmanState:
        indices = [*self.state.route]
        starts = [edge.start for edge in self.edges]
        ends = [edge.end for edge in self.edges]

        for _ in range(len(self.edges)):
            loops_count = sum(starts[i] == ends[i] for i in range(len(self.edges)))
            ends =  ends[1:] + [ends[0]]
            if loops_count == 0:
                break
        
        for i in range(len(self.edges)):
            start, end = starts[i], ends[i]
            indices[start+1], indices[end] = indices[end], indices[start+1]

        return TravelingSalesmanState(points=self.state.points, route=indices)

