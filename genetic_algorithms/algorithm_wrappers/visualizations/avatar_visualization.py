from genetic_algorithms.algorithm_wrappers.visualizations.visualization_wrapper import VisualizationSubscriber
from genetic_algorithms.problems.avatar_problem.problem_model import AvatarModel
from genetic_algorithms.problems.avatar_problem.state import AvatarState
import pygame


class AvatarVisualization(VisualizationSubscriber):
    @staticmethod
    def get_corresponding_problem():
        return AvatarModel

    def _draw_state(self, screen, model: AvatarModel, state: AvatarState):
        mode, im_size, data = state.image.mode, state.image.size, state.image.tobytes()
        py_image = pygame.image.fromstring(data, im_size, mode)
        screen_size = screen.get_width(), screen.get_height()
        scaled_im_size = self._get_new_im_size(screen_size, im_size)
        scaled_image = self._scale_image(py_image, scaled_im_size)
        screen.blit(scaled_image, self.image_coords(screen_size, scaled_im_size))

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