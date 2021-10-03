import sys
import time
from math import inf
from pathlib import Path

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


BEST_STATE = 'best_state'
CURR_NEINGHBOR = 'curr_neinghbor'
FROM_STATE = 'from_state'

STATS = 'stats_info'

ROAD_COLOR = (0, 150, 0)
BG_COLOR = (255,255,255)
FONT_COLOR = (0, 0, 0)

class TravelingSalesmanVisualization(VisualizationSubscriber):

    @staticmethod
    def get_corresponding_problem():
        return TravelingSalesmanProblem


    def __init__(self, config: SolverConfig, algorithm: SubscribableAlgorithm, **kwargs):
        super().__init__(algorithm, **kwargs)
        self._init_pygame()
        self._init_state(config)

    def _init_pygame(self):
        pygame.init()
        pygame.font.init()
        self.main_screen = pygame.display.set_mode((800, 800))
        self.canvas = pygame.Surface((800, 800))
        self.screen_coords = {
            FROM_STATE: (0, 0),
            CURR_NEINGHBOR: (400, 0),
            BEST_STATE: (0, 400),
            STATS: (400,400)
        }
        self.state_screens = {
            BEST_STATE: self.canvas.subsurface(pygame.Rect(*self.screen_coords[BEST_STATE], 400, 400)),
            CURR_NEINGHBOR: self.canvas.subsurface(pygame.Rect(*self.screen_coords[CURR_NEINGHBOR], 400, 400)), 
            FROM_STATE: self.canvas.subsurface(pygame.Rect(*self.screen_coords[FROM_STATE], 400, 400)),
            STATS: self.canvas.subsurface(pygame.Rect(*self.screen_coords[STATS], 400, 400)),
        }



    def _init_state(self, config: SolverConfig):
        self.explored_states_count = 0
        self.start_time = time.time()
        self.time_limit = config.time_limit
        # TODO best state should depdent on optimization strategy
        self.best_state_cost = inf
        self.states = {
            BEST_STATE: None,
            CURR_NEINGHBOR: None, 
            FROM_STATE: None
        }


    def _perform_side_effects(self, model: TravelingSalesmanProblem, from_state: TravelingSalesmanState, next_neighbour: TravelingSalesmanState):
        self._update_states(next_neighbour, from_state)
        self._update_statistics()
        self._handle_pygame_events()
        self._draw(model)
        time.sleep(.01)

    def _update_states(self, new_state: TravelingSalesmanState, from_state: TravelingSalesmanState):
        self.states = {
            BEST_STATE: self.algorithm.best_state,
            FROM_STATE: from_state,
            CURR_NEINGHBOR: new_state
        }
    
    def _update_statistics(self):
        self.explored_states_count += 1
        self.current_time = time.time()

    def _handle_pygame_events(self):
        exit_on = [pygame.QUIT, pygame.KEYDOWN, pygame.K_ESCAPE]
        for event in pygame.event.get():
            if event.type in exit_on:
                sys.exit(0)

    def _draw(self, model: TravelingSalesmanProblem):
        self._draw_states(model)
        self._draw_information(model)
        pygame.display.flip()

    def _draw_states(self, model: TravelingSalesmanProblem):
        caption_font_size = 20
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
            self._draw_text(screen, state_name.capitalize().replace('_', ' '), ( caption_font_size, caption_font_size), caption_font_size)
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

    def _draw_buildings(self, model: TravelingSalesmanProblem, state_name: 'curr_state | best_state | prev_state'):
        state = self.states[state_name]
        if not state: 
            return
        for idx in state.route:
            x, y = self._scale(model.points[idx], model, state_name)
            building, pic_size = self._get_picture('building' if idx != model.depot_idx else 'depot')
            self.state_screens[state_name].blit(building, (x - pic_size/2, y - pic_size/2))

    def _get_picture(self, pic_name: 'depot | building'):
        pic_size = 30
        picture = pygame.image.load(Path(
            genetic_algorithms.__file__).parent / "algorithm_wrappers" / "visualizations" / "pictures" / f"{pic_name}.png")
        picture = pygame.transform.scale(picture, (pic_size, pic_size))
        return picture, pic_size


    def _draw_information(self, model: TravelingSalesmanProblem):
        screen = self.state_screens[STATS]
        screen.fill(BG_COLOR)
        def get_cost_or_unknown(state_name):
            state = self.states[state_name]
            if not state:
                return 'Unknown'
            return str(model.cost_for(state))

        font_size = 20
        padding = 5
        stats = {
            'time': f'{round(self.current_time - self.start_time, 2)}/{self.time_limit}',
            'checked_states': self.explored_states_count,
            'current_state': get_cost_or_unknown(CURR_NEINGHBOR),
            'best_state': get_cost_or_unknown(BEST_STATE),
        }

        for idx, item in enumerate(stats.items()):
            stat_name, stat_value = item
            self._draw_text(screen, f'{stat_name.replace("_", " ")}: {stat_value}'.capitalize(), 
                                    ((screen.get_width() - screen.get_width()/2), idx * (font_size+padding)), 
                                    font_size)
        self.main_screen.blit(screen, self.screen_coords[STATS])

    
    def _draw_text(self, screen, text, position, font_size):
        font = pygame.font.SysFont('arial', font_size)
        renderer = font.render(text, False, FONT_COLOR)
        screen.blit(renderer, position)



