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
        goal = AvatarProblem.get_available_goals()[goal_name]
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
    def to_string(image: Image.Image):
        byte_io = BytesIO()
        image.save(byte_io, 'PNG')
        return byte_io.getvalue().decode('ISO-8859-1')

    def asdict(self):
        return {
            'reference_image': self.to_string(self.reference_image),
            'move_generator_name': camel_to_snake(type(self.move_generator).__name__),
            'goal_name': camel_to_snake(type(self.goal).__name__),
        }

    @classmethod
    def from_dict(cls, data):
        cls.validate_data(data)
        data['reference_image'] = Image.open(BytesIO(data['reference_image'].encode('ISO-8859-1')))
        return cls(**data)

    @classmethod
    def parse_image(cls, file_buffer: TextIOWrapper):
        line = file_buffer.readline()
        return Image.open(BytesIO(line.encode('ISO-8859-1')))

    @classmethod
    def from_solution(cls, solution_name: str):
        with open(cls.get_path_to_solutions() / solution_name, 'r') as solution_file:
            image = cls.parse_image(solution_file)
            _ = solution_file.readline()
            reference_image = cls.parse_image(solution_file)
        model = cls(reference_image=reference_image)
        model.initial_state = AvatarState(image=image)
        return model

    @staticmethod
    def get_available_move_generation_strategies():
        return AvatarMoveGenerator.generators.keys()

    @staticmethod
    def get_available_goals():
        return [camel_to_snake(ApproximateAvatar.__name__)]

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
