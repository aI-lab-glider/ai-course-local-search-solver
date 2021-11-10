from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.avatar_problem.goal import ApproximateAvatar
from local_search.problems.avatar_problem.moves.move_generator import AvatarMoveGenerator
from local_search.problems.base.problem import Problem
from local_search.problems.avatar_problem.state import AvatarState
import local_search
from typing import Tuple, Union
from pathlib import Path
from PIL import Image
from io import BytesIO, TextIOWrapper
import base64
import numpy as np


class AvatarProblem(Problem):
    def __init__(self,
                 reference_image: Image.Image,
                 move_generator_name: Union[str, None] = None,
                 goal_name: str = "approximate_avatar"
                 ):
        self.reference_image = reference_image
        self._reference_image_data = reference_image.getdata()
        self._image_size = reference_image.size
        move_generator_name = move_generator_name or list(
            self.get_available_move_generation_strategies())[0]
        move_generator = AvatarMoveGenerator.generators[move_generator_name](
            self._image_size)
        goal = AvatarProblem.get_available_goals()[goal_name](reference_image)
        initial_solution = self._find_initial_solution()
        super().__init__(
            initial_solution,
            move_generator,
            goal)

    def random_state(self) -> AvatarState:
        """
        Generates a random state
        """
        imarray = np.random.rand(*self.reference_image.size, 3) * 255
        img = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
        return AvatarState(img)

    @staticmethod
    def to_b64(image: Image.Image):
        im_file = BytesIO()
        image.save(im_file, format="JPEG")
        im_bytes = im_file.getvalue()
        return base64.b64encode(im_bytes)

    def asdict(self):
        base = super().asdict()
        return {
            'reference_image': f"{self.to_b64(self.reference_image)}".replace("b'", ""),
            **base
        }

    @classmethod
    def from_dict(cls, data):
        cls.validate_data(data)
        data['reference_image'] = Image.open(
            BytesIO(base64.b64decode(data['reference_image'])))
        return cls(**data)

    @staticmethod
    def get_available_move_generation_strategies():
        return AvatarMoveGenerator.generators.keys()

    @staticmethod
    def get_available_goals():
        return {
            camel_to_snake(ApproximateAvatar.__name__): ApproximateAvatar
        }

    def _find_initial_solution(self) -> AvatarState:
        return AvatarState(image=Image.new("RGB", self._image_size, "white"))

    @staticmethod
    def from_benchmark(benchmark_name: str, move_generator_name: str, goal_name: str = 'approximate_avatar', **kwargs):
        img = Image.open(Path(
            local_search.__file__).parent / "problems" / "avatar_problem" / "benchmarks" / benchmark_name)
        return AvatarProblem(
            img,
            move_generator_name,
            goal_name
        )
