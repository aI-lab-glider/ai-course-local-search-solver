from local_search.algorithm_subscribers.visualization_subscribers.visualization_subscriber import \
    VisualizationSubscriber, StateDrawer
from local_search.problems import Problem, State
from local_search.problems.limited_avatar_problem.problem import LimitedAvatarProblem
from local_search.problems.limited_avatar_problem.state import LimitedAvatarState
import pygame


class LimitedAvatarProblemVisualization(VisualizationSubscriber):

    @staticmethod
    def get_corresponding_problem():
        return LimitedAvatarProblem

    @classmethod
    def create_state_drawer(cls, *_, **kwargs):
        return LimitedAvatarStateDrawer()


class LimitedAvatarStateDrawer(StateDrawer):

    def draw_state(self, screen, model: LimitedAvatarProblem, state: LimitedAvatarState):
        mode, im_size, data = state.image.mode, state.image.size, state.image.tobytes()
        py_image = pygame.image.fromstring(data, im_size, mode)
        screen_size = screen.get_width(), screen.get_height()
        scaled_im_size = self._get_new_im_size(screen_size, im_size)
        scaled_image = self._scale_image(py_image, scaled_im_size)
        screen.blit(scaled_image, self.image_coords(
            screen_size, scaled_im_size))

    def _get_new_im_size(self, screen_size, im_size):
        y = screen_size[0] * im_size[1] / im_size[0]
        x = screen_size[0]
        if y > screen_size[1]:
            x = screen_size[1] * x / y
            y = screen_size[1]
        return int(x), int(y)

    def image_coords(self, screen_size, scaled_im_size):
        return (screen_size[0]-scaled_im_size[0])//2, (screen_size[1]-scaled_im_size[1])//2

    def _scale_image(self, py_image, scaled_im_size):
        return pygame.transform.scale(py_image, scaled_im_size)
