from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.base.problem import Problem
from local_search.problems.avatar_problem.move_generator import AvatarMoveGenerator
from local_search.problems.avatar_problem.state import AvatarState
import local_search
from typing import Tuple
from pathlib import Path
from PIL import Image


class AvatarProblem(Problem):
    def __init__(self, reference_image: Image.Image):
        self.reference_image = reference_image
        self._reference_image_data = reference_image.getdata()
        self._image_size = reference_image.size
        move_generator = AvatarMoveGenerator(self._image_size)
        initial_solution = self._find_initial_solution()
        super().__init__(initial_solution, move_generator)

    @staticmethod
    def get_available_move_generation_strategies():
        return [camel_to_snake(AvatarMoveGenerator.__name__)]

    def _find_initial_solution(self) -> AvatarState:
        return AvatarState(image=Image.new("RGB", self._image_size, "white"))

    def _pix_comp(self, ref_pix: Tuple[int, int, int], pix_to_comp: Tuple[int, int, int]) -> int:
        d_r = ref_pix[0] - pix_to_comp[0]
        d_g = ref_pix[1] - pix_to_comp[1]
        d_b = ref_pix[2] - pix_to_comp[2]
        return d_r * d_r + d_g * d_g + d_b * d_b

    def cost_for(self, state: AvatarState) -> int:
        return sum(self._pix_comp(self.reference_image.getpixel((x, y)), state.image.getpixel((x, y)))
                   for y in range(self._image_size[1]) for x in range(self._image_size[0]))

    @staticmethod
    def from_benchmark(benchmark_name: str, move_generator_name: str):
        img = Image.open(Path(
            local_search.__file__).parent / "problems" / "avatar_problem" / "benchmarks" / benchmark_name)
        return AvatarProblem(img)
