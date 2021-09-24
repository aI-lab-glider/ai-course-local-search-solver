from pathlib import Path

import pygame
import sys

import genetic_algorithms
from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import AlgorithmWrapper
from genetic_algorithms.models.next_state_provider import NextStateProvider
from genetic_algorithms.problems.traveling_salesman_problem.problem_model import TravelingSalesmanModel
from genetic_algorithms.problems.traveling_salesman_problem.state import TravelingSalesmanState


class Visualization(AlgorithmWrapper):
    def __init__(self, algorithm: NextStateProvider):
        pygame.init()
        super().__init__(algorithm)

    def _perform_side_effects(self, model: TravelingSalesmanModel, state: TravelingSalesmanState):
        self.screen = pygame.display.set_mode((900, 900))
        self.current_route = [(self._scale(model.points[idx], model)) for idx in state.route]

        self._handle_pygame_events()
        self._draw(model,state)

    def _draw_buildings(self, model: TravelingSalesmanModel, state: TravelingSalesmanState):
        building = pygame.image.load(Path(genetic_algorithms.__file__).parent/"problems"/"traveling_salesman_problem"/"pictures"/"building.png")
        building = pygame.transform.scale(building,(80,80))
        for idx in state.route:
            x, y = self._scale(model.points[idx],model)
            self.screen.blit(building,(x - 40, y - 40))

    def _find_extreme(self, model: TravelingSalesmanModel):
        min_x = min(point.x for point in model.points)
        max_x = max(point.x for point in model.points)
        min_y = min(point.y for point in model.points)
        max_y = max(point.y for point in model.points)

        return min_x, max_x, min_y, max_y

    def _scale(self, point, model: TravelingSalesmanModel):
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

    def _draw(self, model: TravelingSalesmanModel, state: TravelingSalesmanState):
        self.screen.fill((255, 255, 255))
        self._draw_buildings(model, state)
        pygame.draw.lines(self.screen, (0, 150, 0), True, self.current_route,3)
        pygame.display.flip()
        pygame.time.delay(500)
