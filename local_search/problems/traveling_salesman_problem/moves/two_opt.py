from copy import copy
from typing import Generator

from local_search.problems.base import Move
from local_search.problems.traveling_salesman_problem.moves.move_generator import TravelingSalesmanMoveGenerator
from local_search.problems.traveling_salesman_problem.state import TravelingSalesmanState
import random

class TwoOptMove(Move[TravelingSalesmanState]):

    def __init__(self, from_state: TravelingSalesmanState, i1: int, i2: int):
        super().__init__(from_state)
        (self.i1, self.i2) = i1, i2

    def make(self) -> TravelingSalesmanState:
        new_route = self.state.route[0:self.i1] + list(reversed(self.state.route[self.i1:self.i2])) + self.state.route[self.i2:]
        return TravelingSalesmanState(new_route, self.state.points)

class TwoOpt(TravelingSalesmanMoveGenerator):

    def available_moves(self, state: TravelingSalesmanState) -> Generator[Move[TravelingSalesmanState], None, None]:
        for i1 in range(1, len(state.route) - 2):
            for i2 in range(i1 + 1, len(state.route) - 1):
                yield TwoOptMove(state, i1, i2)

    def random_moves(self, state: TravelingSalesmanState) -> Generator[Move[TravelingSalesmanState], None, None]:
        while True:
            i1 = random.randrange(1, len(state.route) - 2)
            i2 = random.randrange(i1 + 1, len(state.route) - 1)
            yield TwoOptMove(state, i1, i2)



