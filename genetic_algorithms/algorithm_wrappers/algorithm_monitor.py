import operator as op
from genetic_algorithms.algorithms.algorithm import AlgorithmConfig, OptimizationStrategy
from re import S
from genetic_algorithms.solvers.solver import SolverConfig
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import AlgorithmWrapper
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from time import sleep

console = Console()


class AlgorithmMonitor(AlgorithmWrapper):
    def __init__(self, config: AlgorithmConfig, **kwargs):
        super().__init__(**kwargs)
        self._algorithm_config = config
        self._best_algo_cost, self._iters_from_last_impr = float('inf'), 0
        self._progress_bar = self._create_progress_bar()

    def _create_step_table(self, new_cost):
        table = Table(show_header=True, header_style="bold magenta")
        columns = ["Title", "Value"]
        for column in columns:
            table.add_column(column)
        table.add_row(
            "Best found cost",
            str(self._best_algo_cost)
        )
        table.add_row(
            "Current cost",
            str(new_cost)
        )
        return table

    def _create_progress_bar(self):
        completed = self._iters_from_last_impr
        left = self._algorithm_config.max_steps_without_improvement - completed
        return f'Steps from last impr: [[cyan]{"#" * completed}[/cyan]{"-" * (left)}]'

    def _perform_side_effects(self, model: Model, state: State):
        new_cost = model.cost_for(state)
        if new_cost < self._best_algo_cost:
            self._best_algo_cost = new_cost
            self._iters_from_last_impr = 0
        progess_bar = self._create_progress_bar()
        table = self._create_step_table(new_cost)
        console.print(table)
        console.print(progess_bar)
        self._iters_from_last_impr += 1
        sleep(0.1)

    def _is_cost_strictly_better(self, is_better_cost, is_better_than_cost) -> bool:
        return {
            OptimizationStrategy.Min.value: op.lt,
            OptimizationStrategy.Max.value: op.gt,
        }[self._algorithm_config.optimization_stategy](is_better_cost, is_better_than_cost)
