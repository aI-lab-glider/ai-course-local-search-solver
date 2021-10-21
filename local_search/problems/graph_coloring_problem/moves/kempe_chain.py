import random
from typing import Generator, Set, Dict, List

from local_search.problems.base.moves import Move
from local_search.problems.graph_coloring_problem.models.vertex import Vertex
from local_search.problems.graph_coloring_problem.moves.move_generator import GraphColoringMoveGenerator
from local_search.problems.graph_coloring_problem.state import GraphColoringState
import copy


class KempeChainMove(Move[GraphColoringState]):
    def __init__(self, graph: Dict[int, Set[int]], from_state: GraphColoringState, idx: int, color: int):
        super().__init__(from_state)
        self.idx = idx
        self.color = color
        self.graph = graph
        self.old_color = self.state.coloring[idx].color

    def _kempe_chain(self, coloring: List[Vertex]):
        # TODO: to the kempe chain thing
        # tip 1. it's just a BFS walk over the graph
        # tip 2. self.graph[c] are the neighbors of node c
        old_color = self.old_color
        new_color = self.color
        chain = [self.idx]
        while len(chain) > 0:
            new_chain_links = []
            for c in chain:
                for n in self.graph[c]:
                    if coloring[n].color == new_color:
                        coloring[n].color = old_color
                        new_chain_links.append(n)
            chain = list(set(new_chain_links))
            new_color, old_color = old_color, new_color

    def make(self) -> GraphColoringState:
        new_coloring = copy.deepcopy(self.state.coloring)
        new_coloring[self.idx].color = self.color
        self._kempe_chain(new_coloring)
        return GraphColoringState(coloring=new_coloring)


class KempeChain(GraphColoringMoveGenerator):

    def random_moves(self, state: GraphColoringState) -> Generator[KempeChainMove, None, None]:
        while True:
            idx = random.randrange(self.n_vertices)
            available_colors = self.get_available_colors(idx, state)
            yield KempeChainMove(self.graph,
                                 state,
                                 idx=random.randrange(self.n_vertices),
                                 color=random.choice(available_colors))

    def available_moves(self, state: GraphColoringState) -> Generator[KempeChainMove, None, None]:
        for idx in range(self.n_vertices):
            for color in self.get_available_colors(idx, state):
                if state.coloring[idx].color == color:
                    continue
                yield KempeChainMove(self.graph, state, idx, color)
