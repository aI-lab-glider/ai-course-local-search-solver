from abc import ABC

from local_search.helpers.camel_to_snake import camel_to_snake

from local_search.problems.base.move_generator import MoveGenerator


class TravelingSalesmanMoveGenerator(MoveGenerator, ABC):
    """
    Base class for move generators for traveling salesman problem
    """
    move_generators = {}

    def __init_subclass__(cls):
        TravelingSalesmanMoveGenerator.move_generators[camel_to_snake(cls.__name__)] = cls