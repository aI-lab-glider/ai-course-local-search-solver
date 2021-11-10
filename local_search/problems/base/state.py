from abc import ABC, abstractmethod
from dataclasses import dataclass
from inspect import signature, getmro
from itertools import chain
from typing import Dict, Type

from local_search.helpers.camel_to_snake import camel_to_snake


@dataclass
class State(ABC):
    states = {}

    def __init_subclass__(cls):
        cls.states[camel_to_snake(cls.__name__)] = cls

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns a string representing a problem.
        """

    @abstractmethod
    def __eq__(self, other):
        """
        Compares current states to another state.
        """

    def asdict(self):
        """
        Creates dictionary with keys same as parameters from __init__ method.
        """
        return {
            'name': camel_to_snake(type(self).__name__)
        }

    @classmethod
    def validate_data(cls, data) -> None:
        """
        Validates if data contains all params required by class.
        """
        params = set(signature(cls).parameters.keys())
        missing_params = params - set(data.keys())
        if missing_params:
            raise ValueError(
                f'Cannot create {cls.__name__} from passed dict. Missing params are: {",".join(missing_params)}')

    @classmethod
    def from_dict(cls, data) -> 'State':
        """
        Creates state from dictionary
        """
        name = data['name']
        state_type = cls.states[name]
        state_type.validate_data(data)
        del data['name']
        return state_type.from_dict(data)
