from pathlib import Path
from math import inf

import pygame
import sys
import time
import random

from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import AlgorithmWrapper
from genetic_algorithms.models.next_state_provider import NextStateProvider
from genetic_algorithms.problems.graph_coloring_problem.problem_model import GraphColoringModel
from genetic_algorithms.problems.graph_coloring_problem.state import GraphColoringState
from genetic_algorithms.solvers.solver import SolverConfig

class GraphColoringVisualization(AlgorithmWrapper):
    def __init__(self, config: SolverConfig, algorithm: NextStateProvider, model: GraphColoringModel, **kwargs):
        pygame.init()
        pygame.font.init()
        self.time_limit = config.time_limit
        self.coord = self._generate_coord(model)
        self.start_time = time.time()
        self.time_limit = config.time_limit
        self.colors = self._generate_colors(model)
        self.states = 0
        self.cost_best_state = inf
        super().__init__(algorithm, **kwargs)

    def _perform_side_effects(self, model: GraphColoringModel, state: GraphColoringState):
        self.screen = pygame.display.set_mode((800, 800))
        self.current_time = time.time()
        self.states += 1
        self.cost_current_state = model.cost_for(state)
        self._check_states()

        while True:
            self._handle_pygame_events()
            self._draw(state, model)

    def _draw_vertices(self, state: GraphColoringState):
        for i in range(len(self.coord)):
            x, y = self._scale(self.coord[i])
            pygame.draw.circle(self.screen, self.colors[state.coloring[i].color], (x, y), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 10, 2)

    def _draw(self, state: GraphColoringState, model: GraphColoringModel):
        self.screen.fill((255, 255, 255))
        self._draw_lines(model)
        self._draw_vertices(state)
        self._draw_information()
        pygame.display.flip()

        if self._check_time():
            while True:
                self.screen = pygame.display.set_mode((900, 900))
                self._handle_pygame_events()

    def _generate_coord(self, model: GraphColoringModel):
        coord = []
        x, y = 1, 1
        for i in range(model.n_vertices):
            while (x, y) in coord:
                x, y = random.randint(0, model.n_vertices), random.randint(0, model.n_vertices)
            coord.append((x, y))

        return coord

    def _generate_colors(self, model: GraphColoringModel):
        colors = []
        color = (0, 150, 0)
        for i in range(model.n_vertices):
            while color in colors:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            colors.append(color)
        return colors

    def _find_extreme(self):
        min_x = min(vertex[0] for vertex in self.coord)
        max_x = max(vertex[0] for vertex in self.coord)
        min_y = min(vertex[1] for vertex in self.coord)
        max_y = max(vertex[1] for vertex in self.coord)

        return min_x, max_x, min_y, max_y

    def _scale(self, point):
        min_x, max_x, min_y, max_y = self._find_extreme()
        x, y = point[0], point[1]
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

    def _check_time(self):
        if self.current_time - self.start_time >= self.time_limit:
            return True

    def _scaled_coord(self):
        scaled_coord = []
        for coord in self.coord:
            scaled_coord.append(self._scale(coord))
        return scaled_coord

    def _draw_lines(self, model: GraphColoringModel):
        graph = [list(model.graph[i]) for i in range(model.n_vertices)]
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                pygame.draw.line(self.screen, (0, 0, 0), self._scale(self.coord[i]),
                                 self._scale(self.coord[graph[i][j]]), 3)

    def _draw_information(self):
        font = pygame.font.SysFont('arial', 20)
        text_1 = font.render('Time: ' + str(round(self.current_time - self.start_time, 2)) + '/' + str(self.time_limit),
                             False, (0, 0, 0))
        text_2 = font.render('Checked states: ' + str(self.states), False, (0, 0, 0))
        text_3 = font.render('Current state: ' + str(self.cost_current_state), False, (0, 0, 0))
        text_4 = font.render('Best state: ' + str(self.cost_best_state), False, (0, 0, 0))
        self.screen.blit(text_1, (self.screen.get_width() - 215, 25))
        self.screen.blit(text_2, (self.screen.get_width() - 215, 50))
        self.screen.blit(text_3, (self.screen.get_width() - 215, 75))
        self.screen.blit(text_4, (self.screen.get_width() - 215, 100))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.screen.get_width() - 220, 20, 215, 105), 2)

        if self._check_time():
            text_5 = font.render('TIME EXCEEDED', False, (150, 0, 0))
            self.screen.blit(text_5, (self.screen.get_width() - 215, 127))

    def _check_states(self):
        if self.cost_best_state > self.cost_current_state:
            self.cost_best_state = self.cost_current_state
