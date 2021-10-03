import sys
from math import inf
from pathlib import Path

import genetic_algorithms
import pygame
from genetic_algorithms.algorithm_wrappers.visualizations.visualization_wrapper import \
    VisualizationWrapper
from genetic_algorithms.models.next_state_provider import NextStateProvider
from genetic_algorithms.problems.traveling_salesman_problem.problem_model import \
    TravelingSalesmanProblem
from genetic_algorithms.problems.traveling_salesman_problem.state import \
    TravelingSalesmanState
from genetic_algorithms.solvers.solver import SolverConfig
import time

BEST_STATE = 'best_state'
CURR_STATE = 'curr_state'
PREV_STATE = 'prev_state'

STATS = 'stats_info'

ROAD_COLOR = (0, 150, 0)
BG_COLOR = (255, 255, 255)
FONT_COLOR = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SCREEN_SIZE = (800, 800)
PIC_SIZE = 30
CAPTION_FONT_SIZE = 20
FONT_SIZE = 30
PADDING = 5
BUTTON_SIZE = (150, 75)


class TravelingSalesmanVisualization(VisualizationWrapper):

    @staticmethod
    def get_corresponding_problem():
        return TravelingSalesmanProblem

    def __init__(self, config: SolverConfig, algorithm: NextStateProvider, **kwargs):
        super().__init__(algorithm, **kwargs)
        self._init_pygame()
        self._init_state(config)

    def _init_pygame(self):
        pygame.init()
        pygame.font.init()
        self.main_screen = pygame.display.set_mode(SCREEN_SIZE)
        self.canvas = pygame.Surface(SCREEN_SIZE)
        self.is_freezed = False
        self.screen_coords = {
            PREV_STATE: (0, 0),
            CURR_STATE: (SCREEN_SIZE[0] / 2, 0),
            BEST_STATE: (0, SCREEN_SIZE[1] / 2),
            STATS: (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
        }
        self.state_screens = {
            BEST_STATE: self.canvas.subsurface(
                pygame.Rect(*self.screen_coords[BEST_STATE], SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)),
            CURR_STATE: self.canvas.subsurface(
                pygame.Rect(*self.screen_coords[CURR_STATE], SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)),
            PREV_STATE: self.canvas.subsurface(
                pygame.Rect(*self.screen_coords[PREV_STATE], SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)),
            STATS: self.canvas.subsurface(
                pygame.Rect(*self.screen_coords[STATS], SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)),
        }

    def _init_state(self, config: SolverConfig):
        self.explored_states_count = 0
        self.start_time = time.time()
        self.time_limit = config.time_limit
        # TODO best state should depdent on optimization strategy
        self.best_state_cost = inf
        self.states = {
            BEST_STATE: None,
            CURR_STATE: None,
            PREV_STATE: None
        }

    def _perform_side_effects(self, model: TravelingSalesmanProblem, state: TravelingSalesmanState):
        self._update_states(model, state)
        self._update_statistics()
        self._handle_pygame_events(model)
        self._draw(model)

    def _on_solution_found(self, model: TravelingSalesmanProblem, state: TravelingSalesmanState):
        self._freeze_screen(model)

    def _freeze_screen(self, model: TravelingSalesmanProblem):
        while True:
            self._handle_pygame_events(model)
            if not self.is_freezed:
                break


    def _update_states(self, model: TravelingSalesmanProblem, new_state: TravelingSalesmanState):
        self.states = {
            **self.states,
            PREV_STATE: self.states[CURR_STATE],
            CURR_STATE: new_state
        }
        # TODO: should depdent on optimization strategy
        if self.states[BEST_STATE] is None or model.cost_for(new_state) <= model.cost_for(self.states[BEST_STATE]):
            self.states[BEST_STATE] = new_state

    def _update_statistics(self):
        self.explored_states_count += 1
        self.current_time = time.time()

    def _handle_pygame_events(self, model: TravelingSalesmanProblem):
        exit_on = [pygame.QUIT, pygame.KEYDOWN, pygame.K_ESCAPE]
        for event in pygame.event.get():
            if event.type in exit_on:
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._is_button_clicked((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self._on_button_clicked(model)

    def _draw(self, model: TravelingSalesmanProblem):
        self._draw_states(model)
        self._draw_information(model)
        self._draw_button()
        pygame.display.flip()

    def _draw_states(self, model: TravelingSalesmanProblem):
        for state_name in self.states:
            state, screen = self.states[state_name], self.state_screens[state_name]
            if not state:
                continue
            screen.fill(BG_COLOR)
            self._draw_buildings(model, state_name)
            route = [(self._scale(model.points[idx], model, state_name))
                     for idx in state.route]
            pygame.draw.lines(screen, ROAD_COLOR,
                              True, route, 3)
            self._draw_text(screen, state_name.capitalize().replace('_', ' '), (0, 0), CAPTION_FONT_SIZE)
            self.main_screen.blit(screen, self.screen_coords[state_name])

    def _scale(self, point, model: TravelingSalesmanProblem, state_name):
        screen = self.state_screens[state_name]
        min_x, max_x, min_y, max_y = self._find_extreme(model)
        x, y = point.x, point.y
        x -= min_x
        y -= min_y
        x = x * (screen.get_width() / (max_x - min_x))
        y = y * (screen.get_height() / (max_y - min_y))
        if x == 0:
            x += PIC_SIZE / 2
        if y == 0:
            y += PIC_SIZE / 2
        if x == screen.get_width():
            x -= PIC_SIZE / 2
        if y == screen.get_height():
            y -= PIC_SIZE / 2
        return x, y

    def _find_extreme(self, model: TravelingSalesmanProblem):
        min_x = min(point.x for point in model.points)
        max_x = max(point.x for point in model.points)
        min_y = min(point.y for point in model.points)
        max_y = max(point.y for point in model.points)

        return min_x, max_x, min_y, max_y

    def _draw_buildings(self, model: TravelingSalesmanProblem, state_name: 'curr_state | best_state | prev_state'):
        state = self.states[state_name]
        if not state:
            return
        for idx in state.route:
            x, y = self._scale(model.points[idx], model, state_name)
            building = self._get_picture('building' if idx != model.depot_idx else 'depot')
            self.state_screens[state_name].blit(building, (x - PIC_SIZE / 2, y - PIC_SIZE / 2))

    def _get_picture(self, pic_name: 'depot | building'):
        picture = pygame.image.load(Path(
            genetic_algorithms.__file__).parent / "algorithm_wrappers" / "visualizations" / "pictures" / f"{pic_name}.png")
        picture = pygame.transform.scale(picture, (PIC_SIZE, PIC_SIZE))
        return picture

    def _draw_information(self, model: TravelingSalesmanProblem):
        screen = self.state_screens[STATS]
        screen.fill(BG_COLOR)

        def get_cost_or_unknown(state_name):
            state = self.states[state_name]
            if not state:
                return 'Unknown'
            return str(model.cost_for(state))

        stats = {
            'time': f'{round(self.current_time - self.start_time, 2)}/{self.time_limit}',
            'checked_states': self.explored_states_count,
            'current_state': get_cost_or_unknown(CURR_STATE),
            'best_state': get_cost_or_unknown(BEST_STATE),
        }

        for idx, item in enumerate(stats.items()):
            stat_name, stat_value = item
            self._draw_text(screen, f'{stat_name.replace("_", " ")}: {stat_value}'.capitalize(),
                            ((screen.get_width() / 2) - 4 * FONT_SIZE, idx * (FONT_SIZE + PADDING) + FONT_SIZE),
                            FONT_SIZE)

        max_len = len(max(stats.keys(), key=lambda x: len(x)))
        rect = pygame.Rect(screen.get_width() / 2 - 4.5 * FONT_SIZE, FONT_SIZE / 2, max_len * FONT_SIZE * 0.65,
                           (len(stats) + 1.65) * FONT_SIZE)
        pygame.draw.rect(screen, FONT_COLOR, rect, 3)
        self.main_screen.blit(screen, self.screen_coords[STATS])

    def _draw_text(self, screen, text, position, font_size):
        font = pygame.font.SysFont('arial', font_size)
        renderer = font.render(text, False, FONT_COLOR)
        screen.blit(renderer, position)

    def _draw_button(self):
        screen = self.state_screens[STATS]
        rect = pygame.Rect(screen.get_width() / 3, screen.get_height() / 2, BUTTON_SIZE[0], BUTTON_SIZE[1])
        if self.is_freezed:
            pygame.draw.rect(screen, RED, rect)
        else:
            pygame.draw.rect(screen, GREEN, rect)

        pygame.draw.rect(screen, FONT_COLOR, rect, 3)
        self.main_screen.blit(screen, self.screen_coords[STATS])
        pygame.display.flip()

    def _is_button_clicked(self,position):
        screen = self.state_screens[STATS]
        return screen.get_width() / 3 <= position[0] - SCREEN_SIZE[0]/2 <= screen.get_width() / 3 + BUTTON_SIZE[0] and \
                screen.get_height()/2 <= position[1] - SCREEN_SIZE[1]/2 <= screen.get_height()/2 + BUTTON_SIZE[1]

    def _on_button_clicked(self, model: TravelingSalesmanProblem):
        self.is_freezed = not self.is_freezed
        self._draw_button()
        if self.is_freezed:
            self._freeze_screen(model)
