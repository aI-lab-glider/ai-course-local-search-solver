import operator as op
import time

from rich import box

from local_search.algorithm_subscribers.algorithm_subscriber import \
    AlgorithmSubscriber
from local_search.algorithms import AlgorithmConfig
from local_search.problems.base.problem import Problem
from local_search.problems.base.state import State
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel

CURR_STATE = 'current_state'
PREV_STATE = 'previous_state'
BEST_STATE = 'best_state'


class AlgorithmMonitor(AlgorithmSubscriber):
    delay_time = .001

    def __init__(self, config: AlgorithmConfig, **kwargs):
        super().__init__(**kwargs)
        self._algorithm_config = config
        self._live = Live(auto_refresh=False)
        self._live.start()

        self._stats = {
            'active_time': 0.0,
            'best_state_updates_count': 0
        }
        self._states = {
            BEST_STATE: None,
            CURR_STATE: None,
            PREV_STATE: None
        }
        self._start_time = time.monotonic()
        self._iters_from_last_impr = 0

    def on_next_state(self, model: Problem, state: State):
        self._update_stats(state)
        self._live.update(self._create_layout(model), refresh=True)
        time.sleep(self.delay_time)

    def _update_stats(self, state):
        self._states[PREV_STATE] = self._states[CURR_STATE]
        self._states[CURR_STATE] = state

        if self._states[BEST_STATE] != self.algorithm.best_state:
            self._states[BEST_STATE] = self.algorithm.best_state
            self._iters_from_last_impr = self.algorithm.steps_from_last_state_update
            self._stats["best_state_updates_count"] += 1

        self._stats["active_time"] = round(
            time.monotonic() - self._start_time, 2)
        self._iters_from_last_impr = self.algorithm.steps_from_last_state_update

    def _create_layout(self, model: Problem) -> Layout:
        layout = Layout()
        layout.split_row(
            Layout(name="stats", renderable=self._create_stats_column(model)),
            Layout(name="state", renderable=self._create_state_column())
        )
        return layout

    def _create_stats_column(self, model: Problem):
        rows = []
        for stat_name, value in self._stats.items():
            stat_name = stat_name.capitalize().replace('_', ' ')
            rows.append(f'[cyan]{stat_name}[/cyan]: {value}')

        for state_name, state in self._states.items():
            if state is None:
                continue
            stat_name = f'{state_name.capitalize().replace("_", " ")} cost: '
            value = model.objective_for(state)
            rows.append(f'[blue_violet]{stat_name}[/blue_violet]: {value}')

        progress_bar = self._create_progress_bar()

        panel = Panel(
            "\n".join([*rows, progress_bar]),
            title="Algorithm stats",
            box=box.ASCII,
            height=20)
        return panel

    def _create_progress_bar(self):
        completed = self._iters_from_last_impr - 1
        left = self._algorithm_config.local_optimum_moves_threshold - completed
        completed_bar = f'[cyan]{"#" * completed}[/cyan]'
        arrow = '[cyan3]>[/cyan3]'
        left_bar = "-" * left
        return f'Steps from last best state change: [{completed_bar}{arrow}{left_bar}]'

    def _create_state_column(self) -> Layout:
        layout = Layout()
        layout.split_column(
            *[Panel(str(state), title=name.capitalize().replace("_", " "), box=box.ASCII, height=5)
              for name, state in self._states.items()
              if state is not None]
        )
        return layout

    def on_solution(self):
        self._live.stop()

    def __del__(self):
        self._live.stop()
