from abc import ABC

from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.limited_avatar_problem.goal import ApproximateLimitedAvatar
from local_search.problems.limited_avatar_problem.moves.move_generator import LimitedAvatarMoveGenerator
from local_search.problems.base.problem import Problem
from local_search.problems.limited_avatar_problem.state import LimitedAvatarState
import local_search
from local_search.problems.limited_avatar_problem.models.color import Color
from local_search.problems.limited_avatar_problem.models.vertex import Vertex
from local_search.problems.limited_avatar_problem.models.polygon import Polygon
from typing import Union
from pathlib import Path
from PIL import Image
from io import BytesIO
import base64
import random
from dataclasses import dataclass, asdict


@dataclass
class LimitedAvatarProblemConfig:
    n_polygons: int = 50
    n_polygon_vertices: int = 3


DEFAULT_CONFIG = LimitedAvatarProblemConfig()


class LimitedAvatarProblem(Problem):
    def __init__(self,
                 reference_image: Image.Image,
                 move_generator_name: Union[str, None] = None,
                 config: LimitedAvatarProblemConfig = None,
                 goal_name: str = 'approximate_limited_avatar',
                 ):
        self.config = config or DEFAULT_CONFIG
        self.reference_image = reference_image
        self._image_size = reference_image.size
        move_generator_name = move_generator_name or list(
            self.get_available_move_generation_strategies())[0]
        move_generator = LimitedAvatarMoveGenerator.generators[move_generator_name](
            self._image_size)
        initial_solution = self._find_initial_solution()
        super().__init__(initial_solution,
                         move_generator,
                         goal=self.get_available_goals()[goal_name](reference_image))

    def random_state(self) -> LimitedAvatarState:
        """
        Generates a random state
        """
        def _generate_color() -> Color:
            return Color(R=random.randint(0, 255),
                         G=random.randint(0, 255),
                         B=random.randint(0, 255),
                         A=random.randint(0, 255))

        def _generate_vertex() -> Vertex:
            offset = self._image_size[0]//5
            return Vertex(x=random.randint(0 - offset, self._image_size[0] + offset),
                          y=random.randint(0 - offset, self._image_size[1] + offset))

        polygons = [Polygon(vertices=[_generate_vertex() for _ in range(self.config.n_polygon_vertices)],
                            color=_generate_color()) for _ in range(self.config.n_polygons)]
        return LimitedAvatarState(polygons=polygons, image_size=self._image_size)

    def _find_initial_solution(self) -> LimitedAvatarState:
        return self.random_state()

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
            'config': asdict(self.config),
            **base
        }

    @staticmethod
    def get_available_move_generation_strategies():
        return LimitedAvatarMoveGenerator.generators.keys()

    @staticmethod
    def get_available_goals():
        return {
            camel_to_snake(ApproximateLimitedAvatar.__name__): ApproximateLimitedAvatar
        }

    @classmethod
    def from_dict(cls, data):
        cls.validate_data(data)
        data['reference_image'] = Image.open(
            BytesIO(base64.b64decode(data['reference_image'])))
        data['config'] = LimitedAvatarProblemConfig(**data['config'])
        return cls(**data)

    @staticmethod
    def from_benchmark(benchmark_name: str, move_generator_name: str, goal_name: str = 'approximate_limited_avatar', config: LimitedAvatarProblemConfig = None):
        img = Image.open(Path(
            local_search.__file__).parent / "problems" / "limited_avatar_problem" / "benchmarks" / benchmark_name)
        return LimitedAvatarProblem(
            img,
            move_generator_name,
            config
        )
