from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.avatar_problem.goal import ApproximateAvatar
from local_search.problems.avatar_problem.moves.move_generator import AvatarMoveGenerator
from local_search.problems.base.problem import Problem
from local_search.problems.avatar_problem.state import AvatarState
import local_search
from typing import Tuple
from pathlib import Path
from PIL import Image
import numpy as np


class AvatarProblem(Problem):
    def __init__(self,
                 reference_image: Image.Image,
                 move_generator_name: str
                 ):
        self.reference_image = reference_image
        self._reference_image_data = reference_image.getdata()
        self._image_size = reference_image.size
        move_generator = AvatarMoveGenerator.generators[move_generator_name](
            self._image_size)
        initial_solution = self._find_initial_solution()
        super().__init__(
            initial_solution,
            move_generator,
            ApproximateAvatar(reference_image))

    def random_state(self) -> AvatarState:
        """
        Generates a random state
        """
        imarray = np.random.rand(*self.reference_image.size, 3) * 255
        img = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
        return AvatarState(img)

    @staticmethod
    def get_available_move_generation_strategies():
        return AvatarMoveGenerator.generators.keys()

    @staticmethod
    def get_available_goals():
        return [camel_to_snake(ApproximateAvatar.__name__)]

    def _find_initial_solution(self) -> AvatarState:
        return AvatarState(image=Image.new("RGB", self._image_size, "white"))

    @staticmethod
    def from_benchmark(benchmark_name: str, move_generator_name: str, **kwargs):
        img = Image.open(Path(
            local_search.__file__).parent / "problems" / "avatar_problem" / "benchmarks" / benchmark_name)
        return AvatarProblem(
            img,
            move_generator_name
        )
