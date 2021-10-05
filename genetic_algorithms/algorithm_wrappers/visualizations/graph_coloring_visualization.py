from typing import Tuple
from genetic_algorithms.algorithm_wrappers.visualizations.visualization_wrapper import VisualizationSubscriber
from genetic_algorithms.problems.graph_coloring_problem.problem_model import GraphColoringProblem
from genetic_algorithms.problems.graph_coloring_problem.state import GraphColoringState
from random import randint
import pygame

EDGE_COLOR = (0, 0, 0)


class GraphColoringVisualization(VisualizationSubscriber):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._available_colors = None

    @staticmethod
    def get_corresponding_problem():
        return GraphColoringProblem

    def _draw_state(self, screen, model: GraphColoringProblem, state: GraphColoringState):
        """
        Draws state
        """
        self._draw_lines(screen, model)
        self._draw_vertices(screen, model, state)

    def _draw_lines(self, screen, model: GraphColoringProblem):
        graph = [list(model.graph[i]) for i in range(model.n_vertices)]
        coords = self._generate_coords(model)
        extremes = self._find_extremes(coords)

        for i in range(len(graph)):
            for j in range(len(graph[i])):
                pygame.draw.line(screen, EDGE_COLOR,
                                 self._scale(coords[i], screen, extremes),
                                 self._scale(
                                     coords[graph[i][j]], screen, extremes),
                                 3)

    def _find_extremes(self, coords):
        min_x = min(vertex[0] for vertex in coords)
        max_x = max(vertex[0] for vertex in coords)
        min_y = min(vertex[1] for vertex in coords)
        max_y = max(vertex[1] for vertex in coords)
        return min_x, max_x, min_y, max_y

    def _draw_vertices(self, screen, model: GraphColoringProblem, state: GraphColoringState):
        coords = self._generate_coords(model)
        extremes = self._find_extremes(coords)
        colors = self._get_colors(model)
        for i in range(len(coords)):
            x, y = self._scale(coords[i], screen, extremes)
            pygame.draw.circle(
                screen, colors[state.coloring[i].color], (x, y), 10)
            pygame.draw.circle(screen, (0, 0, 0), (x, y), 10, 2)

    def _generate_coords(self, model: GraphColoringProblem):
        coord = []
        x, y = 1, 1
        for _ in range(model.n_vertices):
            while (x, y) in coord:
                x, y = randint(0, model.n_vertices), randint(
                    0, model.n_vertices)
            coord.append((x, y))

        return coord

    def _get_colors(self, model: GraphColoringProblem):
        if not self._available_colors:
            self._available_colors = self._generate_random_colors(
                model.n_vertices)
        return self._available_colors

    def _generate_random_colors(self, n, except_colors=None):
        colors = []

        def random_color():
            return (randint(0, 255), randint(0, 255), randint(0, 255))
        color = random_color()
        except_colors = except_colors or []
        for _ in range(n):
            while color in colors or color in except_colors:
                color = random_color()
            colors.append(color)
        return colors

    def _scale(self, point: Tuple[int, int], screen, extremes: Tuple[int, int, int, int]):
        min_x, max_x, min_y, max_y = extremes
        x, y = point
        x -= min_x
        y -= min_y
        x = x * (screen.get_width() / max((max_x - min_x), 1))
        y = y * (screen.get_height() / max((max_y - min_y), 1))
        if x == 0:
            x += 40
        if y == 0:
            y += 40
        if x == screen.get_width():
            x -= 40
        if y == screen.get_height():
            y -= 40
        return x, y
