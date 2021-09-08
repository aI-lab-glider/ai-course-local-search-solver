from typing import Generator, List, Set, Dict
from pathlib import Path

import genetic_algorithms
from genetic_algorithms.problems.graph_coloring_problem.state import GraphColoringState
from genetic_algorithms.problems.graph_coloring_problem.moves import ChangeColor

from genetic_algorithms.problems.base.model import Model

from genetic_algorithms.problems.graph_coloring_problem.models.edge import Edge
from genetic_algorithms.problems.graph_coloring_problem.models.vertex import Vertex
from genetic_algorithms.problems.graph_coloring_problem.move_generator import GraphColoringMoveGenerator


class GraphColoringModel(Model):
    def __init__(self, edges: List[Edge]):
        self._edges: List[Edge] = edges
        self.graph: Dict[int, Set[int]] = self._create_graph()
        self.n_vertices = len(self.graph)
        move_generator = GraphColoringMoveGenerator(self.n_vertices)
        initial_solution = self._find_initial_solution()
        super().__init__(initial_solution, move_generator)

    @property
    def edges(self):
        return self._edges

    def _create_graph(self) -> Dict[int, Set[int]]:
        graph = {}
        for edge in self._edges:
            if edge.start in graph.keys():
                graph[edge.start].add(edge.end)
            else:
                graph[edge.start] = {edge.end}
            if edge.end in graph.keys():
                graph[edge.end].add(edge.start)
            else:
                graph[edge.end] = {edge.start}
        return graph

    def _find_initial_solution(self) -> GraphColoringState:
        coloring = [Vertex(idx=i, color=-1) for i in range(self.n_vertices)]
        coloring[0].color = 0
        for vertex in self.graph:
            available_colors = [i for i in range(self.n_vertices)]
            for neighbour in self.graph[vertex]:
                if coloring[neighbour].color in available_colors:
                    available_colors.remove(coloring[neighbour].color)
            coloring[vertex].color = available_colors[0]
        return GraphColoringState(model=self, coloring=coloring)

    def _bad_edges(self, state: GraphColoringState) -> List[int]:
        bad_edges = [0 for _ in range(self.n_vertices)]
        for edge in self._edges:
            if state.coloring[edge.start].color == state.coloring[edge.end].color:
                bad_edges[state.coloring[edge.start].color] += 1
        return bad_edges

    def _color_classes(self, state: GraphColoringState) -> List[int]:
        color_classes = [0 for _ in range(self.n_vertices)]
        for vertex in state.coloring:
            color_classes[vertex.color] += 1
        return color_classes

    def moves_for(self, state: GraphColoringState) -> Generator[ChangeColor, None, None]:
        return (ChangeColor(state, idx, color) for idx in range(self.n_vertices) for color in range(self.n_vertices))

    def cost_for(self, state: GraphColoringState) -> int:
        bad_edges = self._bad_edges(state)
        color_classes = self._color_classes(state)
        return sum([2*bad_edges[i]*color_classes[i]-color_classes[i]**2 for i in range(self.n_vertices)])

    @staticmethod
    def from_benchmark(benchmark_name: str):
        with open(Path(genetic_algorithms.__file__).parent / "problems" / "graph_coloring_problem" / "benchmarks" / benchmark_name) as benchmark_file:

            def line_to_edge(line: str):
                (start, end) = map(int, line.split(sep=' '))
                return Edge(start, end)

            edges = [line_to_edge(line) for line in benchmark_file]
            return GraphColoringModel(edges=edges)

