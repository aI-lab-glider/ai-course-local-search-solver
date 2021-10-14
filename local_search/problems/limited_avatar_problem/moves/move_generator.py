from typing import Tuple

from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.base.move_generator import MoveGenerator


class LimitedAvatarMoveGenerator(MoveGenerator):
    generators = {}

    def __init_subclass__(cls):
        cls.generators[camel_to_snake(cls.__name__)] = cls

    def __init__(self, im_size: Tuple[int, int]):
        self.im_size = im_size
