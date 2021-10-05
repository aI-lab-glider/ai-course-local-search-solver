import sys
import time
from math import inf
from pathlib import Path
from typing import Literal, Union

import genetic_algorithms
from genetic_algorithms.algorithms.algorithm import SubscribableAlgorithm
import pygame
from genetic_algorithms.algorithm_wrappers.visualizations.visualization_wrapper import \
    VisualizationSubscriber
from genetic_algorithms.models.next_state_provider import Algorithm
from genetic_algorithms.problems.traveling_salesman_problem.problem_model import \
    TravelingSalesmanProblem
from genetic_algorithms.problems.traveling_salesman_problem.state import \
    TravelingSalesmanState
from genetic_algorithms.solvers.solver import SolverConfig
import time


ROAD_COLOR = (0, 150, 0)


class TravelingSalesmanVisualization(VisualizationSubscriber):

    @staticmethod
    def get_corresponding_problem():
        return TravelingSalesmanProblem

    def _draw_state(self, screen, model: TravelingSalesmanProblem, state: TravelingSalesmanState):
        self._draw_buildings(model, state, screen)
        route = [(self._scale(model.points[idx], model, screen))
                 for idx in state.route]
        pygame.draw.lines(screen, ROAD_COLOR,
                          True, route, 3)

    def _scale(self, point, model: TravelingSalesmanProblem, screen):
        min_x, max_x, min_y, max_y = self._find_extreme(model)
        x, y = point.x, point.y
        x -= min_x
        y -= min_y
        x = x * (screen.get_width() / (max_x - min_x))
        y = y * (screen.get_height() / (max_y - min_y))
        if x == 0:
            x += 10
        if y == 0:
            y += 10
        if x == screen.get_width():
            x -= 10
        if y == screen.get_height():
            y -= 10
        return x, y

    def _find_extreme(self, model: TravelingSalesmanProblem):
        min_x = min(point.x for point in model.points)
        max_x = max(point.x for point in model.points)
        min_y = min(point.y for point in model.points)
        max_y = max(point.y for point in model.points)

        return min_x, max_x, min_y, max_y

    def _draw_buildings(self, model: TravelingSalesmanProblem, state: TravelingSalesmanState, screen):
        if not state:
            return
        for idx in state.route:
            x, y = self._scale(model.points[idx], model, screen)
            building, pic_size = self._get_picture(
                'building' if idx != model.depot_idx else 'depot')
            screen.blit(
                building, (x - pic_size/2, y - pic_size/2))

    def _get_picture(self, pic_name: Union[Literal['depot'], Literal['building']]):
        pic_size = 30
        picture = pygame.image.load(Path(
            genetic_algorithms.__file__).parent / "algorithm_wrappers" / "visualizations" / "pictures" / f"{pic_name}.png")
        picture = pygame.transform.scale(picture, (pic_size, pic_size))
        return picture, pic_size
