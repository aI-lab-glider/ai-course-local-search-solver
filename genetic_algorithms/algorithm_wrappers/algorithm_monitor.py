import operator as op
import time

from rich import box

from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import \
    AlgorithmWrapper
from genetic_algorithms.algorithms.algorithm import (AlgorithmConfig,
                                                     OptimizationStrategy)
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.problems.base.state import State
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table


class AlgorithmMonitor(AlgorithmWrapper):
    delay_time = 0.01

    def __init__(self, config: AlgorithmConfig, **kwargs):
        super().__init__(**kwargs)
        self._algorithm_config = config
        self._live = Live(auto_refresh=False)
        self._live.start()

        self._stats = {
            'best_cost': float('inf') if config.optimization_stategy == OptimizationStrategy.Min else float('-inf'),
            'last_cost': 0,
            'active_time': 0,
            'explored_states_count': 0
        }

        self._start_time = time.monotonic()
        self._iters_from_last_impr = 0

    def _create_layout(self, state: State) -> Layout:
        layout = Layout()
        layout.split_row(
            Layout(name="stats", renderable=self._create_stats_column()),
            Layout(name="state", renderable=self._create_state_column(state))
        )
        return layout

    def _create_stats_column(self):
        rows = []
        for stat_name, value in self._stats.items():
            stat_name = stat_name.capitalize().replace('_', ' ')
            rows.append(f'[cyan]{stat_name}[/cyan]: {value}')

        progress_bar = self._create_progress_bar()

        panel = Panel(
            "\n".join([*rows, progress_bar]),
            title="Algorithm stats",
            box=box.ASCII,
            height=20)
        return panel

    def _create_state_column(self, state: State):
        return Panel(str(state), title="Current state", box=box.ASCII, height=20)

    def _perform_side_effects(self, model: Model, state: State):

        self._update_stats(model, state)
        self._live.update(self._create_layout(state), refresh=True)
        time.sleep(self.delay_time)

    def _update_stats(self, model, state):
        new_state_cost = model.cost_for(state)
        if self._is_cost_strictly_better(new_state_cost, self._stats["best_cost"]):
            self._stats["best_cost"] = new_state_cost
            self._iters_from_last_impr = 0
        self._stats["last_cost"] = new_state_cost
        self._stats["explored_states_count"] += 1

        self._stats["active_time"] = round(
            time.monotonic() - self._start_time, 2)
        self._iters_from_last_impr += 1

    def _is_cost_strictly_better(self, is_better_cost, is_better_than_cost) -> bool:
        return {
            OptimizationStrategy.Min: op.lt,
            OptimizationStrategy.Max: op.gt,
        }[self._algorithm_config.optimization_stategy](is_better_cost, is_better_than_cost)

    def _create_progress_bar(self):
        completed = self._iters_from_last_impr - 1
        left = self._algorithm_config.max_steps_without_improvement - completed
        completed_bar = f'[cyan]{"#" * completed}[/cyan]'
        arrow = '[cyan3]>[/cyan3]'
        left_bar = "-" * (left)
        return f'Steps from last impr: [{completed_bar}{arrow}{left_bar}]'

    def _on_solution_found(self, **kwargs):
        self._live.stop()

    def __del__(self):
        self._live.stop()
