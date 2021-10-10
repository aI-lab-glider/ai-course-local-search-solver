from abc import ABC, abstractmethod
from dataclasses import dataclass
from inspect import signature, getmro
from itertools import chain


@dataclass
class State(ABC):

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

    @abstractmethod
    def asdict(self):
        """
        Creates dictionary with keys same as parameters from __init__ method.
        """

    @classmethod
    def validate_data(cls, data) -> None:
        """
        Validates if data contains all params required by class.
        """
        params = set(chain(signature(method).parameters.keys()
                     for method in getmro(cls)))
        missing_params = set(data.keys()) - params
        if missing_params:
            raise ValueError(
                f'Cannot create {cls.__name__} from passed dict. Missing params are: {",".join(missing_params)}')

    @classmethod
    @abstractmethod
    def from_dict(cls, data) -> 'State':
        """
        Creates state from dictionary
        """
