from abc import abstractmethod, ABC
from typing import Generator, List, Union

from local_search.algorithm_subscribers.algorithm_subscriber import AlgorithmSubscriber
from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.algorithms.algorithm import Algorithm
from local_search.algorithms.algorithm_config import DEFAULT_CONFIG, AlgorithmConfig
from local_search.problems.base.problem import Problem
from local_search.problems.base.state import State


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
        self.best_obj, self.best_state = None, None
        self._subscribers: List[AlgorithmSubscriber] = []

    def __init_subclass__(cls) -> None:
        if ABC not in cls.__bases__:
            SubscribableAlgorithm.algorithms[camel_to_snake(
                cls.__name__)] = cls

    @abstractmethod
    def _find_next_state(self, model: Problem, state: State) -> Union[State, None]:
        """
        Finds next state for model. Returns None in case if state is optimal.
        """

    def _random_restart(self, model: Problem):
        return model.random_state()

    def _perturb(self, model: Problem, how_much: int):
        perturbed_state = self.best_state
        for i in range(how_much):
            perturbed_state = next(
                model.move_generator.random_moves(perturbed_state)).make()
        return perturbed_state

    def _get_neighbours(self, model: Problem, state: State) -> Generator[State, None, None]:
        for move in model.move_generator.available_moves(state):
            neighbour = move.make()
            self._on_next_neighbour(model, state, neighbour)
            yield neighbour

    def _get_random_neighbours(self, model: Problem, state: State) -> Generator[State, None, None]:
        for move in model.move_generator.random_moves(state):
            neighbour = move.make()
            self._on_next_neighbour(model, state, neighbour)
            yield neighbour

    def _is_stuck_in_local_optimum(self):
        return self.steps_from_last_state_update >= self.config.local_optimum_moves_threshold

    def next_state(self, model: Problem, state: State) -> Union[State, None]:
        if self.best_state is None:
            self.best_state = state
            self._on_next_state(model, state)

        if self._is_stuck_in_local_optimum():
            next_state = self.escape_local_optimum(
                model, state, self.best_state)
        else:
            next_state = self._find_next_state(model, state)

        if next_state is not None:
            self._update_algorithm_state(model, next_state)
            self._on_next_state(model, next_state)
        else:
            self._on_solution(model, state)

        return next_state

    def _update_algorithm_state(self, model: Problem, new_state: State):
        if self.best_state is None:
            self.best_state = new_state

        if model.improvement(new_state, self.best_state) > 0:
            self.best_obj, self.best_state = model.objective_for(
                new_state), new_state
            self.steps_from_last_state_update = 0
        else:
            self.steps_from_last_state_update += 1

    def _on_next_state(self, model: Problem, next_state: State):
        """Called when algorithm find new best state"""
        for subscriber in self._subscribers:
            subscriber.on_next_state(model, next_state)

    def _on_next_neighbour(self, model: Problem, from_state: State, next_neighbour: State):
        """Called when algorithm explores next neighbour"""
        for subscriber in self._subscribers:
            subscriber.on_next_neighbour(model, from_state, next_neighbour)

    def _on_solution(self, model: Problem, solution: State):
        for subscriber in self._subscribers:
            subscriber.on_solution(model=model, solution=solution)

    def subscribe(self, subsriber: AlgorithmSubscriber):
        self._subscribers.append(subsriber)
