import pygame, sys
from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import AlgorithmWrapper
from genetic_algorithms.problems.traveling_salesman_problem.problem_model import TravelingSalesmanModel
from genetic_algorithms.problems.traveling_salesman_problem.state import TravelingSalesmanState

class Visualization(AlgorithmWrapper):
    def _perform_side_effects(self, model: TravelingSalesmanModel, state: TravelingSalesmanState):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 900))
        _points = model.points
        _route = state.route
        self.find_extreme(_points)
        _route_points = [(self.scale(_points[idx])) for idx in _route]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        self.screen.fill((0, 0, 0))
        self.draw_points(_route, _points)
        pygame.draw.lines(self.screen,(0, 150, 0),True,_route_points)
        pygame.display.flip()
        pygame.time.delay(500)
        pygame.display.flip()


    def draw_points(self, _route, _points):
        for idx in _route:
            pygame.draw.circle(self.screen, (150, 0, 0),(self.scale(_points[idx])), 3)

    def find_extreme(self,_points):
        self._min_x = min(point.x for point in _points)
        self._max_x = max(point.x for point in _points)
        self._min_y = min(point.y for point in _points)
        self._max_y = max(point.y for point in _points)

    def scale(self,point):
        x,y = point.x, point.y
        x -= self._min_x
        y -= self._min_y

        return x*(900/(self._max_x-self._min_x)), y*(900/(self._max_y - self._min_y))
