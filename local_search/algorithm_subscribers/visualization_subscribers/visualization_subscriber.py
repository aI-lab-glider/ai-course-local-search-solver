import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import inf
from typing import Dict, Type

import pygame
from local_search.algorithm_subscribers.algorithm_subscriber import \
    AlgorithmSubscriber
from local_search.problems import Problem
from local_search.problems.base.state import State

BEST_STATE = 'best_state'
CURR_NEIGHBOUR = 'current_neinghbour'
FROM_STATE = 'from_state'
STATS = 'stats_info'

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (61, 46, 158)
BLACK = (0, 0, 0)
DIRTY_WHITE = (242, 248, 243)


@dataclass
class VisualizationSubcriberConfig:
    min_time_between_steps: float = 0.01
    show_only_solution: bool = False


DEFAULT_CONFIG = VisualizationSubcriberConfig()


class StateDrawer(ABC):
    @abstractmethod
    def draw_state(self, screen, model: Problem, state: State):
        """
        Draws state on provided screen.
        """


class VisualizationSubscriber(AlgorithmSubscriber):
    """
    Provides visualization to algorithm solutions.
    """
    visualizations: Dict[Type[Problem], Type['VisualizationSubscriber']] = {}
    _BG_COLOR = (255, 255, 255)
    _FONT_COLOR = (0, 0, 0)
    _BUTTON_SIZE = (150, 75)
    _SCREEN_SIZE = (800, 800)
    _FONT_SIZE = 25
    _PADDING = 5

    def __init__(self, model: Problem, config: VisualizationSubcriberConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.state_drawer = self.create_state_drawer(model)
        if not self.config.show_only_solution:
            self._init_pygame()
        self._init_state()
        super().__init__()

    def __init_subclass__(cls):
        VisualizationSubscriber.visualizations[cls.get_corresponding_problem(
        )] = cls

    @classmethod
    @abstractmethod
    def create_state_drawer(cls, model: Problem) -> StateDrawer:
        """
        Returns state drawer for problem
        """

    @staticmethod
    @abstractmethod
    def get_corresponding_problem() -> Type[Problem]:
        """
        Returns model type for which this visualization was done
        """

    def _init_pygame(self):
        pygame.init()
        pygame.font.init()
        self.main_screen = pygame.display.set_mode(self._SCREEN_SIZE)
        self.canvas = pygame.Surface(self._SCREEN_SIZE)
        self.screen_coords = {
            FROM_STATE: (0, 0),
            CURR_NEIGHBOUR: (self._SCREEN_SIZE[0] / 2, 0),
            BEST_STATE: (0, self._SCREEN_SIZE[1] / 2),
            STATS: (self._SCREEN_SIZE[0] / 2, self._SCREEN_SIZE[1] / 2)
        }
        self.state_screens = {
            BEST_STATE: self.canvas.subsurface(
                pygame.Rect(*self.screen_coords[BEST_STATE], self._SCREEN_SIZE[0] / 2, self._SCREEN_SIZE[1] / 2)),
            CURR_NEIGHBOUR: self.canvas.subsurface(
                pygame.Rect(*self.screen_coords[CURR_NEIGHBOUR], self._SCREEN_SIZE[0] / 2, self._SCREEN_SIZE[1] / 2)),
            FROM_STATE: self.canvas.subsurface(
                pygame.Rect(*self.screen_coords[FROM_STATE], self._SCREEN_SIZE[0] / 2, self._SCREEN_SIZE[1] / 2)),
            STATS: self.canvas.subsurface(
                pygame.Rect(*self.screen_coords[STATS], self._SCREEN_SIZE[0] / 2, self._SCREEN_SIZE[1] / 2)),
        }
        self._is_freezed = False

    def _init_state(self):
        self.explored_states_count = 0
        self.start_time = time.time()
        self.best_state_cost = inf
        self.states = {
            BEST_STATE: None,
            CURR_NEIGHBOUR: None,
            FROM_STATE: None
        }

    def on_next_neighbour(self, model: Problem, from_state: State, next_neighbour: State):
        self._update_states(next_neighbour, from_state)
        self._update_statistics()
        if self.config.show_only_solution:
            return
        self._handle_pygame_events()
        self._draw(model)
        time.sleep(self.config.min_time_between_steps)

    def _update_states(self, new_state: State, from_state: State):
        self.states = {
            BEST_STATE: self.algorithm.best_state or from_state,
            FROM_STATE: from_state,
            CURR_NEIGHBOUR: new_state
        }

    def _update_statistics(self):
        self.explored_states_count += 1
        self.current_time = time.time()

    def _handle_pygame_events(self):
        exit_on = [pygame.QUIT, pygame.K_ESCAPE]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

            if event.type in exit_on:
                self._is_freezed = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._is_button_clicked((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self._on_button_clicked()

    def _draw(self, model):
        self._draw_information(model)
        self._draw_states(model)
        self._draw_button()
        self._draw_border()
        pygame.display.flip()

    def _draw_border(self):
        rect = pygame.Rect(0, 0, self.main_screen.get_width() -
                           1, self.main_screen.get_height() - 1)
        pygame.draw.rect(self.main_screen, BLACK, rect, 4)
        pygame.draw.line(self.main_screen, BLACK, (self.main_screen.get_width() / 2, 0),
                         (self.main_screen.get_width() / 2, self.main_screen.get_height()), 3)
        pygame.draw.line(self.main_screen, BLACK, (0, self.main_screen.get_height() / 2),
                         (self.main_screen.get_width(), self.main_screen.get_height() / 2), 3)

    def _draw_states(self, model: Problem):
        caption_font_size = 25
        bold = 3
        for state_name in self.states:
            state, screen, screen_coords = self.states[state_name], self.state_screens[
                state_name], self.screen_coords[state_name]
            if not state:
                continue
            screen.fill(self._BG_COLOR)
            self.state_drawer.draw_state(screen, model, state)
            self._draw_text_with_background(screen, state_name.capitalize().replace(
                '_', ' '), (caption_font_size, caption_font_size), caption_font_size, bold, state_name)
            self.main_screen.blit(screen, screen_coords)

    def _draw_text_with_background(self, screen, text, position, font_size, bold, state_name):
        length = len(state_name)
        rect = pygame.Rect(font_size - 5, font_size + 3,
                           font_size * length / 2, font_size)
        pygame.draw.rect(screen, BLUE, rect)

        rect = pygame.Rect(font_size - 5, font_size + 3,
                           font_size * length / 2, font_size)
        pygame.draw.rect(screen, BLACK, rect, 2)

        font = pygame.font.SysFont('arial', font_size, bold)
        renderer = font.render(text, False, DIRTY_WHITE)
        screen.blit(renderer, position)

    def _draw_text(self, screen, text, position, font_size, bold):
        font = pygame.font.SysFont('arial', font_size, bold)
        renderer = font.render(text, False, self._FONT_COLOR)
        screen.blit(renderer, position)

    def _draw_information(self, model: Problem):
        screen = self.state_screens[STATS]
        screen.fill(self._BG_COLOR)

        def get_cost_or_unknown(state_name):
            state = self.states[state_name]
            if not state:
                return 'Unknown'
            return str(model.objective_for(state))

        stats = {
            'time': f'{round(self.current_time - self.start_time, 2)}',
            'checked_states': self.explored_states_count,
            'current_state': get_cost_or_unknown(FROM_STATE),
            'current neighbour': get_cost_or_unknown(CURR_NEIGHBOUR),
            'best_state': get_cost_or_unknown(BEST_STATE),
        }

        for idx, item in enumerate(stats.items()):
            stat_name, stat_value = item
            self._draw_text(screen, f'{stat_name.replace("_", " ")}: {stat_value}'.capitalize(),
                            ((screen.get_width() / 2) - 4 * self._FONT_SIZE,
                             idx * (self._FONT_SIZE + self._PADDING) + self._FONT_SIZE),
                            self._FONT_SIZE, 0)

        max_len = len(max(stats.keys(), key=lambda x: len(x)))
        rect = pygame.Rect(screen.get_width() / 2 - 4.5 * self._FONT_SIZE, self._FONT_SIZE / 2,
                           max_len * self._FONT_SIZE * 0.65,
                           (len(stats) + 1.65) * self._FONT_SIZE)
        pygame.draw.rect(screen, self._FONT_COLOR, rect, 3)
        self.main_screen.blit(screen, self.screen_coords[STATS])

    def _draw_button(self):
        screen = self.state_screens[STATS]
        rect = pygame.Rect(screen.get_width() / 3, screen.get_height() /
                           2, *self._BUTTON_SIZE)
        if self._is_freezed:
            pygame.draw.rect(screen, RED, rect)
        else:
            pygame.draw.rect(screen, GREEN, rect)

        pygame.draw.rect(screen, self._FONT_COLOR, rect, 3)
        self.main_screen.blit(screen, self.screen_coords[STATS])
        self._draw_border()
        pygame.display.flip()

    def _is_button_clicked(self, position):
        screen = self.state_screens[STATS]
        return screen.get_width() / 3 <= position[0] - self._SCREEN_SIZE[0] / 2 <= screen.get_width() / 3 + \
            self._BUTTON_SIZE[0] and \
            screen.get_height() / 2 <= position[1] - self._SCREEN_SIZE[1] / \
            2 <= screen.get_height() / 2 + self._BUTTON_SIZE[1]

    def _on_button_clicked(self):
        self._is_freezed = not self._is_freezed
        self._draw_button()
        if self._is_freezed:
            self._freeze_screen()

    def _freeze_screen(self):
        while True:
            self._handle_pygame_events()
            if not self._is_freezed:
                break

    def on_solution(self, model: Problem, **kwargs):
        if self.config.show_only_solution:
            self._init_pygame()
        self._draw(model)
        self._is_freezed = True
        self._freeze_screen()
