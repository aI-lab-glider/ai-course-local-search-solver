from pathlib import Path
from math import inf

import pygame
import sys
import time

import genetic_algorithms
from genetic_algorithms.algorithm_wrappers import VisualizationWrapper
from genetic_algorithms.models.next_state_provider import NextStateProvider
from genetic_algorithms.problems.traveling_salesman_problem.problem_model import TravelingSalesmanProblem
from genetic_algorithms.problems.traveling_salesman_problem.state import TravelingSalesmanState
from genetic_algorithms.solvers.solver import SolverConfig


class TravelingSalesmanVisualization(VisualizationWrapper):

    @staticmethod
    def get_corresponding_problem():
        return TravelingSalesmanVisualization

    def __init__(self, config: SolverConfig, algorithm: NextStateProvider, **kwargs):
        pygame.init()
        pygame.font.init()
        self.states = 0
        self.start_time = time.time()
        self.time_limit = config.time_limit
        self.cost_best_state = inf
        super().__init__(algorithm, **kwargs)

    def _perform_side_effects(self, model: TravelingSalesmanProblem, state: TravelingSalesmanState):
        self.screen = pygame.display.set_mode((900, 900))
        self.current_route = [(self._scale(model.points[idx], model))
                              for idx in state.route]
        self.states += 1
        self.current_time = time.time()
        self.cost_current_state = model.cost_for(state)

        self._check_states()
        self._handle_pygame_events()
        self._draw(model, state)

    def _draw_buildings(self, model: TravelingSalesmanProblem, state: TravelingSalesmanState):
        building = pygame.image.load(Path(
            genetic_algorithms.__file__).parent / "problems" / "traveling_salesman_problem" / "pictures" / "building.png")
        building = pygame.transform.scale(building, (80, 80))
        for idx in state.route:
            x, y = self._scale(model.points[idx], model)
            self.screen.blit(building, (x - 40, y - 40))

    def _find_extreme(self, model: TravelingSalesmanProblem):
        min_x = min(point.x for point in model.points)
        max_x = max(point.x for point in model.points)
        min_y = min(point.y for point in model.points)
        max_y = max(point.y for point in model.points)

        return min_x, max_x, min_y, max_y

    def _scale(self, point, model: TravelingSalesmanProblem):
        min_x, max_x, min_y, max_y = self._find_extreme(model)
        x, y = point.x, point.y
        x -= min_x
        y -= min_y
        x = x * (self.screen.get_width() / (max_x - min_x))
        y = y * (self.screen.get_height() / (max_y - min_y))
        if x == 0:
            x += 40
        if y == 0:
            y += 40
        if x == self.screen.get_width():
            x -= 40
        if y == self.screen.get_height():
            y -= 40
        return x, y

    def _handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

    def _draw(self, model: TravelingSalesmanProblem, state: TravelingSalesmanState):
        self.screen.fill((255, 255, 255))
        self._draw_buildings(model, state)
        self._draw_information()
        pygame.draw.lines(self.screen, (0, 150, 0),
                          True, self.current_route, 3)
        pygame.display.flip()

        if self._check_time():
            while True:
                self.screen = pygame.display.set_mode((900, 900))
                self._handle_pygame_events()

    def _draw_information(self):
        font = pygame.font.SysFont('arial', 20)
        text_1 = font.render('Time: ' + str(round(self.current_time - self.start_time, 2)) + '/' + str(self.time_limit),
                             False, (0, 0, 0))
        text_2 = font.render('Checked states: ' +
                             str(self.states), False, (0, 0, 0))
        text_3 = font.render('Current state: ' +
                             str(self.cost_current_state), False, (0, 0, 0))
        text_4 = font.render(
            'Best state: ' + str(self.cost_best_state), False, (0, 0, 0))
        self.screen.blit(text_1, (self.screen.get_width() - 215, 25))
        self.screen.blit(text_2, (self.screen.get_width() - 215, 50))
        self.screen.blit(text_3, (self.screen.get_width() - 215, 75))
        self.screen.blit(text_4, (self.screen.get_width() - 215, 100))
        pygame.draw.rect(self.screen, (0, 0, 0), (680, 20, 215, 105), 2)

        if self._check_time():
            text_5 = font.render('TIME EXCEEDED', False, (150, 0, 0))
            self.screen.blit(text_5, (self.screen.get_width() - 215, 127))

    def _check_states(self):
        if self.cost_best_state > self.cost_current_state:
            self.cost_best_state = self.cost_current_state

    def _check_time(self):
        if self.current_time - self.start_time >= self.time_limit:
            return True
