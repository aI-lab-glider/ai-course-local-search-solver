import operator as op
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Generator, List, Union

from local_search.algorithm_subscribers.algorithm_subscriber import AlgorithmSubscriber
from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.algorithms.algorithm import Algorithm
from local_search.problems.base.problem import Problem
from local_search.problems.base.state import State


class OptimizationStrategy(Enum):
    Min = 'min'
    Max = 'max'


@dataclass
class AlgorithmConfig:
    max_steps_without_improvement: int = 10
    optimization_strategy: OptimizationStrategy = OptimizationStrategy.Min


DEFAULT_CONFIG = AlgorithmConfig()


class SubscribableAlgorithm(Algorithm):
    """
    Generates next states for the problem based on some logic.
    """
    algorithms = {}

    def __init__(self, config: AlgorithmConfig = None):
        super().__init__()
        config = config or DEFAULT_CONFIG
        self.config = config
        self.steps_from_last_state_update = 0
        self.best_cost, self.best_state = float(
            'inf') if config.optimization_strategy == OptimizationStrategy.Min else float('-inf'), None
        self._subscribers: List[AlgorithmSubscriber] = []

    def __init_subclass__(cls) -> None:
        SubscribableAlgorithm.algorithms[camel_to_snake(cls.__name__)] = cls

    @abstractmethod
    def _find_next_state(self, model: Problem, state: State) -> Union[State, None]:
        """
        Finds next state for model. Returns None in case if state is optimal.
        """

    def next_state(self, model: Problem, state: State) -> Union[State, None]:
        if self.best_state is None:
            self.best_state = state
            self._on_next_state(model, state)
        next_state = self._find_next_state(model, state)
        if next_state:
            self._update_algorithm_state(model, next_state)
            self._on_next_state(model, next_state)
        return next_state

    def _is_cost_strictly_better(self, better_cost, better_than_cost) -> bool:
        return {
            OptimizationStrategy.Min: op.lt,
            OptimizationStrategy.Max: op.gt,
        }[self.config.optimization_strategy](better_cost, better_than_cost)

    def _is_cost_better_or_same(self, better_cost, better_than_cost) -> bool:
        return self._is_cost_strictly_better(better_cost, better_than_cost) or better_cost == better_than_cost

    def _update_algorithm_state(self, model: Problem, new_state: State):
        if self.best_state is None:
            self.best_state = new_state
        next_state_cost = model.cost_for(new_state)
        if self._is_cost_better_or_same(next_state_cost, self.best_cost) and self.best_state != new_state:
            self.best_cost, self.best_state = next_state_cost, new_state
            self.steps_from_last_state_update = 0
        else:
            self.steps_from_last_state_update += 1

    def _is_in_optimal_state(self):
        return self.steps_from_last_state_update >= self.config.max_steps_without_improvement

    def _on_next_state(self, model: Problem, next_state: State):
        """Called when algorithm find new best state"""
        for subscriber in self._subscribers:
            subscriber.on_next_state(model, next_state)

    def _on_next_neighbour(self, model: Problem, from_state: State, next_neighbour: State):
        """Called when algorithm explores next neighbour"""
        for subsriber in self._subscribers:
            subsriber.on_next_neighbour(model, from_state, next_neighbour)

    def subscribe(self, subsriber: AlgorithmSubscriber):
        self._subscribers.append(subsriber)

    def _get_neighbours(self, model: Problem, state: State, is_stochastic=False) -> Generator[State, None, None]:
        move_gen = model.move_generator.available_moves if not is_stochastic else model.move_generator.random_moves
        while True:
            for move in move_gen(state):
                neighbour = move.make()
                self._on_next_neighbour(model, state, neighbour)
                yield neighbour
