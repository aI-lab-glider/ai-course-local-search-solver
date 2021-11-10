from io import TextIOWrapper
import random
from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.base.problem import Problem
from typing import Iterable, List, Set, Dict, Union

from local_search.problems.graph_coloring_problem.goals.goal import GraphColoringGoal
from local_search.problems.graph_coloring_problem.state import GraphColoringState

from local_search.problems.graph_coloring_problem.models.edge import Edge
from local_search.problems.graph_coloring_problem.models.vertex import Vertex
from local_search.problems.graph_coloring_problem.moves.move_generator import GraphColoringMoveGenerator


class GraphColoringProblem(Problem):

    def __init__(self, edges: List[Edge], move_generator_name: Union[str, None] = None, goal_name: Union[str, None] = None):
        self._edges: List[Edge] = edges
        self.graph: Dict[int, Set[int]] = self._create_graph()
        self.n_vertices = len(self.graph)
        move_generator_name = move_generator_name or list(
            GraphColoringMoveGenerator.move_generators.keys())[0]
        move_generator = GraphColoringMoveGenerator.move_generators[move_generator_name](
            self.graph, self.n_vertices)
        goal_name = goal_name or list(GraphColoringGoal.goals.keys())[0]
        goal = GraphColoringGoal.goals[goal_name](self.edges, self.n_vertices)
        initial_solution = self._find_random_solution()
        super().__init__(initial_solution, move_generator, goal)

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

    def _find_random_solution(self) -> GraphColoringState:
        coloring = [Vertex(idx=i, color=-1) for i in range(self.n_vertices)]
        coloring[0].color = 0
        for vertex in self.graph:
            available_colors = [i for i in range(self.n_vertices)]
            for neighbour in self.graph[vertex]:
                if coloring[neighbour].color in available_colors:
                    available_colors.remove(coloring[neighbour].color)
            coloring[vertex].color = random.choice(available_colors)
        return GraphColoringState(coloring=coloring)

    def random_state(self) -> GraphColoringState:
        return self._find_random_solution()

    @classmethod
    def from_benchmark(cls, benchmark_name: str, move_generator_name: str = None, goal_name: str = None):
        with open(cls.get_path_to_benchmarks()/benchmark_name) as benchmark_file:
            edges = cls.parse_edges(benchmark_file)
            return GraphColoringProblem(edges=edges, move_generator_name=move_generator_name, goal_name=goal_name)

    @classmethod
    def parse_edges(cls, file_buffer: TextIOWrapper):
        def line_to_edge(line: str):
            (start, end) = map(int, line.split(sep=' '))
            return Edge(start, end)
        edges = [line_to_edge(line) for line in file_buffer]
        return edges

    @staticmethod
    def get_available_move_generation_strategies() -> Iterable[str]:
        return GraphColoringMoveGenerator.move_generators.keys()

    @staticmethod
    def get_available_goals() -> Iterable[str]:
        return GraphColoringGoal.goals.keys()

    def asdict(self):
        base = super().asdict()
        return {
            'edges': [(edge.start, edge.end) for edge in self.edges],
            **base
        }

    @classmethod
    def from_dict(cls, data):
        data['edges'] = [Edge(start=edge_tuple[0], end=edge_tuple[1])
                         for edge_tuple in data['edges']]
        return cls(**data)
