from abc import abstractmethod
from re import M
from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import AlgorithmNextNeingbourSubscriber, AlgorithmNextStateSubscriber
from genetic_algorithms.algorithm_wrappers.visualizations.visualization_wrapper import VisualizationSubscriber
from genetic_algorithms.helpers.camel_to_snake import camel_to_snake
from typing import Dict, Generator, List, Type, Union
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.models.next_state_provider import Algorithm
from dataclasses import dataclass, field
from enum import Enum
import operator as op
from abc import ABC
from collections import defaultdict

class OptimizationStrategy(Enum):
    Min = 'min'
    Max = 'max'

class AlgorithmHook(Enum):
    OnNeighbour = 'on_neighbour'
    OnNextState = 'on_next_state'

@dataclass
class AlgorithmConfig:
    max_steps_without_improvement: int = 10
    optimization_stategy: OptimizationStrategy = OptimizationStrategy.Min


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
        self._steps_from_last_state_update = 0
        self.best_cost, self.best_state = float('inf') if config.optimization_stategy == OptimizationStrategy.Min else float('-inf'), None
        self._next_state_subscribers: List[AlgorithmNextStateSubscriber] = []
        self._next_neighbour_subsribers: List[AlgorithmNextNeingbourSubscriber] = []

    def __init_subclass__(cls) -> None:
        SubscribableAlgorithm.algorithms[camel_to_snake(cls.__name__)] = cls

    @abstractmethod
    def _find_next_state(self, model: Model, state: State) -> Union[State, None]:
        """
        Finds next state for model. Returns None in case if state is optimal.
        """

    def next_state(self, model: Model, state: State) -> Union[State, None]:
        next_state = self._find_next_state(model, state)
        if next_state:
            self._update_algorithm_state(model, next_state)
            self._on_next_state(model, next_state)
        return next_state

    def _is_cost_better(self, is_better_cost, is_better_than_cost) -> bool:
        return {
            OptimizationStrategy.Min: op.lt,
            OptimizationStrategy.Max: op.gt,
        }[self.config.optimization_stategy](is_better_cost, is_better_than_cost) or is_better_cost == is_better_than_cost 

    def _update_algorithm_state(self, model: Model, new_state: State):
        next_state_cost = model.cost_for(new_state)
        if self._is_cost_better(next_state_cost, self.best_cost) and self.best_state != new_state:
            self.best_cost, self.best_state = next_state_cost, new_state
            self._steps_from_last_state_update = 0
        else:
            self._steps_from_last_state_update += 1


    def _is_in_optimal_state(self):
        return self._steps_from_last_state_update >= self.config.max_steps_without_improvement

    def _on_next_state(self, model: Model, next_state: State):
        """Called when algorithm find new best state"""
        for subsriber in self._next_state_subscribers:
            subsriber.notify(model, next_state)

    def _on_next_neighbour(self, model: Model, from_state: State, next_neighbour: State):
        """Called when algorithm explores next neighbour"""
        for subsriber in self._next_neighbour_subsribers:
            subsriber.notify(model, from_state, next_neighbour)

    
    def subsribe_to_state_update(self, subsriber: AlgorithmNextStateSubscriber):
        self._next_state_subscribers.append(subsriber)
    
    def subscribe_to_neinghbour_enter(self, subsriber: AlgorithmNextNeingbourSubscriber):
        self._next_neighbour_subsribers.append(subsriber)

    
    def _get_neighbours(self, model: Model, state: State) -> Generator[State, None, None]:
        for move in model.move_generator.available_moves(state):
            neighbour = move.make() 
            self._on_next_neighbour(model, state, neighbour)
            yield neighbour

