
from abc import abstractmethod
from math import inf
import sys
import time
from typing import Type
from local_search.algorithm_subscribers.algorithm_subscriber import AlgorithmSubscriber
from local_search.problems import Problem
from local_search.problems.base.state import State
import pygame
from local_search.algorithms.subscribable_algorithm import SubscribableAlgorithm


BEST_STATE = 'best_state'
CURR_NEINGHBOR = 'curr_neinghbour'
FROM_STATE = 'from_state'
STATS = 'stats_info'


RED = (255, 0, 0)
GREEN = (0, 255, 0)


class VisualizationSubscriber(AlgorithmSubscriber):
    """
    Provides visualization to algorithm solutions.
    """
    visualizations = {}
    _BG_COLOR = (255, 255, 255)
    _FONT_COLOR = (0, 0, 0)
    _BUTTON_SIZE = (150, 75)
    _SCREEN_SIZE = (800, 800)

    def __init__(self, algorithm: SubscribableAlgorithm, **kwargs):
        self._init_pygame()
        self._init_state()
        super().__init__(algorithm, **kwargs)

    def __init_subclass__(cls):
        VisualizationSubscriber.visualizations[cls.get_corresponding_problem(
        )] = cls

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
            CURR_NEINGHBOR: (self._SCREEN_SIZE[0]/2, 0),
            BEST_STATE: (0, self._SCREEN_SIZE[1]/2),
            STATS: (self._SCREEN_SIZE[0]/2, self._SCREEN_SIZE[1]/2)
        }
        self.state_screens = {
            BEST_STATE: self.canvas.subsurface(pygame.Rect(*self.screen_coords[BEST_STATE], self._SCREEN_SIZE[0]/2, self._SCREEN_SIZE[1]/2)),
            CURR_NEINGHBOR: self.canvas.subsurface(pygame.Rect(*self.screen_coords[CURR_NEINGHBOR], self._SCREEN_SIZE[0]/2, self._SCREEN_SIZE[1]/2)),
            FROM_STATE: self.canvas.subsurface(pygame.Rect(*self.screen_coords[FROM_STATE], self._SCREEN_SIZE[0]/2, self._SCREEN_SIZE[1]/2)),
            STATS: self.canvas.subsurface(pygame.Rect(*self.screen_coords[STATS], self._SCREEN_SIZE[0]/2, self._SCREEN_SIZE[1]/2)),
        }
        self._is_freezed = False

    def _init_state(self):
        self.explored_states_count = 0
        self.start_time = time.time()
        self.best_state_cost = inf
        self.states = {
            BEST_STATE: None,
            CURR_NEINGHBOR: None,
            FROM_STATE: None
        }

    def on_next_neighbour(self, model: Problem, from_state: State, next_neighbour: State):
        self._update_states(next_neighbour, from_state)
        self._update_statistics()
        self._handle_pygame_events()
        self._draw(model)
        # TODO move to config
        time.sleep(.01)

    def _update_states(self, new_state: State, from_state: State):
        self.states = {
            BEST_STATE: self.algorithm.best_state or from_state,
            FROM_STATE: from_state,
            CURR_NEINGHBOR: new_state
        }

    def _update_statistics(self):
        self.explored_states_count += 1
        self.current_time = time.time()

    def _handle_pygame_events(self):
        exit_on = [pygame.QUIT, pygame.K_ESCAPE]
        for event in pygame.event.get():
            if event.type in exit_on:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._is_button_clicked((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self._on_button_clicked()

    def _draw(self, model):
        self._draw_states(model)
        self._draw_information(model)
        self._draw_button()
        pygame.display.flip()

    def _draw_states(self, model: Problem):
        caption_font_size = 20
        for state_name in self.states:
            state, screen, screen_coords = self.states[state_name], self.state_screens[
                state_name], self.screen_coords[state_name]
            if not state:
                continue
            screen.fill(self._BG_COLOR)
            self._draw_state(screen, model, state)
            self._draw_text(screen, state_name.capitalize().replace(
                '_', ' '), (caption_font_size, caption_font_size), caption_font_size)
            self.main_screen.blit(screen, screen_coords)

    @abstractmethod
    def _draw_state(self, screen, model: Problem, state: State):
        """
        Draws state
        """

    def _draw_text(self, screen, text, position, font_size):
        font = pygame.font.SysFont('arial', font_size)
        renderer = font.render(text, False, self._FONT_COLOR)
        screen.blit(renderer, position)

    def _draw_information(self, model: Problem):
        screen, screen_coords = self.state_screens[STATS], self.screen_coords[STATS]

        screen.fill(self._BG_COLOR)

        def get_cost_or_unknown(state_name):
            state = self.states[state_name]
            if not state:
                return 'Unknown'
            return str(model.cost_for(state))

        font_size = 20
        padding = 5
        stats = {
            'time': f'{round(self.current_time - self.start_time, 2)}',
            'checked_states': self.explored_states_count,
            'current_state': get_cost_or_unknown(CURR_NEINGHBOR),
            'best_state': get_cost_or_unknown(BEST_STATE),
        }

        for idx, item in enumerate(stats.items()):
            stat_name, stat_value = item
            self._draw_text(screen, f'{stat_name.replace("_", " ")}: {stat_value}'.capitalize(),
                                    ((screen.get_width()/2) - 4 * font_size,
                                     idx * (font_size + padding) + font_size),
                                    font_size)

        self.main_screen.blit(screen, screen_coords)

    def _draw_button(self):
        screen = self.state_screens[STATS]
        rect = pygame.Rect(screen.get_width() / 3, screen.get_height() /
                           2, self._BUTTON_SIZE[0], self._BUTTON_SIZE[1])
        if self._is_freezed:
            pygame.draw.rect(screen, RED, rect)
        else:
            pygame.draw.rect(screen, GREEN, rect)

        pygame.draw.rect(screen, self._FONT_COLOR, rect, 3)
        self.main_screen.blit(screen, self.screen_coords[STATS])
        pygame.display.flip()

    def _is_button_clicked(self, position):
        screen = self.state_screens[STATS]
        return screen.get_width() / 3 <= position[0] - self._SCREEN_SIZE[0]/2 <= screen.get_width() / 3 + self._BUTTON_SIZE[0] and \
            screen.get_height()/2 <= position[1] - self._SCREEN_SIZE[1] / \
            2 <= screen.get_height()/2 + self._BUTTON_SIZE[1]

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

    def on_solution(self, **kwargs):
        self._freeze_screen()
