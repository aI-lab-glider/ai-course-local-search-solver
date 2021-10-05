
from abc import abstractmethod
from math import inf
import sys
import time
from typing import Type
from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import AlgorithmNextNeingbourSubscriber, AlgorithmNextStateSubscriber
from genetic_algorithms.problems import Model
from genetic_algorithms.problems.base.state import State
import pygame
from genetic_algorithms.algorithms.algorithm import SubscribableAlgorithm


BEST_STATE = 'best_state'
CURR_NEINGHBOR = 'curr_neinghbour'
FROM_STATE = 'from_state'
STATS = 'stats_info'


class VisualizationSubscriber(AlgorithmNextNeingbourSubscriber):
    """
    Provides visualization to algorithm solutions.
    """
    visualizations = {}
    _BG_COLOR = (255, 255, 255)
    _FONT_COLOR = (0, 0, 0)

    def __init__(self, algorithm: SubscribableAlgorithm, **kwargs):
        self._init_pygame()
        self._init_state()
        super().__init__(algorithm, **kwargs)

    def __init_subclass__(cls):
        VisualizationSubscriber.visualizations[cls.get_corresponding_problem(
        )] = cls

    @staticmethod
    @abstractmethod
    def get_corresponding_problem() -> Type[Model]:
        """
        Returns model type for which this visualization was done
        """

    def _init_pygame(self):
        pygame.init()
        pygame.font.init()
        self.main_screen = pygame.display.set_mode((800, 800))
        self.canvas = pygame.Surface((800, 800))
        self.screen_coords = {
            FROM_STATE: (0, 0),
            CURR_NEINGHBOR: (400, 0),
            BEST_STATE: (0, 400),
            STATS: (400, 400)
        }
        self.state_screens = {
            BEST_STATE: self.canvas.subsurface(pygame.Rect(*self.screen_coords[BEST_STATE], 400, 400)),
            CURR_NEINGHBOR: self.canvas.subsurface(pygame.Rect(*self.screen_coords[CURR_NEINGHBOR], 400, 400)),
            FROM_STATE: self.canvas.subsurface(pygame.Rect(*self.screen_coords[FROM_STATE], 400, 400)),
            STATS: self.canvas.subsurface(pygame.Rect(*self.screen_coords[STATS], 400, 400)),
        }

    def _init_state(self):
        self.explored_states_count = 0
        self.start_time = time.time()
        self.best_state_cost = inf
        self.states = {
            BEST_STATE: None,
            CURR_NEINGHBOR: None,
            FROM_STATE: None
        }

    def _perform_side_effects(self, model: Model, from_state: State, next_neighbour: State):
        self._update_states(next_neighbour, from_state)
        self._update_statistics()
        self._handle_pygame_events()
        self._draw(model)
        # TODO move to config
        time.sleep(.1)

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

    def _draw(self, model):
        self._draw_states(model)
        self._draw_information(model)
        pygame.display.flip()

    def _draw_states(self, model: Model):
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
    def _draw_state(self, screen, model: Model, state: State):
        """
        Draws state
        """

    def _draw_text(self, screen, text, position, font_size):
        font = pygame.font.SysFont('arial', font_size)
        renderer = font.render(text, False, self._FONT_COLOR)
        screen.blit(renderer, position)

    def _draw_information(self, model: Model):
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
                                    ((screen.get_width() - screen.get_width()/2),
                                     idx * (font_size + padding)),
                                    font_size)
        self.main_screen.blit(screen, screen_coords)
