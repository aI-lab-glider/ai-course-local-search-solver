from dataclasses import dataclass
import operator as op
import time
from typing import Union
from local_search.solvers.solver_config import SolverConfig

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
BEST_STATE_HUMAN = 'best_result'

ACTIVE_TIME = 'active_time'
BEST_STATES_UPDATE_COUNT = 'best_state_updates_count'
LOCAL_OPTIMUM_ESCAPES_COUNT = 'local_optimum_escapes_count'
ITERS_FROM_LAST_IMPROVEMENT = 'iters_from_last_impr'


@dataclass
class Event:
    name: str
    message: str


class AlgorithmMonitor(AlgorithmSubscriber):
    delay_time = .001

    def __init__(self, solver_config: SolverConfig, **kwargs):
        super().__init__(**kwargs)
        self._solver_config = solver_config
        self._live = Live(auto_refresh=False)
        if self._solver_config.show_statistics:
            self._live.start()

        self._stats = {
            ACTIVE_TIME: 0.0,
            BEST_STATES_UPDATE_COUNT: 0,
            LOCAL_OPTIMUM_ESCAPES_COUNT: 0,
            BEST_STATE_HUMAN: None
        }
        self._states = {
            BEST_STATE: None,
            BEST_STATE_HUMAN: None,
            CURR_STATE: None,
            PREV_STATE: None
        }
        self._start_time = time.monotonic()
        self._last_event = None

    def on_next_state(self, model: Problem, state: State):
        self._update_info(model, state)
        self._update_live_display(self._create_layout(model))
        time.sleep(self.delay_time)

    def _update_info(self, model: Problem, state: State):
        self._update_states(model, state)
        self._update_stats({
            ACTIVE_TIME: round(time.monotonic() - self._start_time, 2),
            ITERS_FROM_LAST_IMPROVEMENT: self.algorithm.steps_from_last_state_update
        })

    def _update_states(self, model, state):
        self._states[PREV_STATE] = self._states[CURR_STATE]
        self._states[CURR_STATE] = state
        if self._states[BEST_STATE] != self.algorithm.best_state:
            self._states[BEST_STATE] = self.algorithm.best_state
            self._stats[BEST_STATES_UPDATE_COUNT] += 1
            self._stats[BEST_STATE_HUMAN] = model.goal.human_readable_objective_for(
                self.algorithm.best_state)

    def _update_stats(self, new_stats):
        self._stats = {**self._stats, **new_stats}

    def _update_live_display(self, layout: Layout):
        self._live.update(layout, refresh=True)

    def _create_layout(self, model: Problem) -> Layout:
        layout = Layout()
        layout.split_row(
            Layout(name="stats"),
            Layout(name="state", renderable=self._create_state_column())
        )
        layout["stats"].split_column(
            self._create_stats_table(model),
            self._create_event_description()
        )
        return layout

    def _create_stats_table(self, model: Problem):
        rows = {}

        def format_stat_name(stat_name):
            stat_name = stat_name.capitalize().replace('_', ' ')
            return f'[cyan]{stat_name}[/cyan]'

        for stat_name, value in self._stats.items():
            rows[format_stat_name(stat_name)] = value

        pad_time = len(str(self._solver_config.time_limit))
        rows[format_stat_name(
            ACTIVE_TIME)] = f'{rows[format_stat_name(ACTIVE_TIME)]:>{pad_time}} | {self._solver_config.time_limit} s'

        def format_state_name(state_name):
            state_name = f'{state_name.capitalize().replace("_", " ")} objective: '
            return f'[blue_violet]{state_name}[/blue_violet]'

        for state_name, state in self._states.items():
            if state is None:
                continue
            value = model.objective_for(state)
            rows[format_state_name(state_name)] = value

        progress_bar = self._create_progress_bar()

        rows = list(map(lambda item: f'{item[0]}: {item[1]}', rows.items()))
        panel = Panel(
            "\n".join([*rows, progress_bar]),
            title="Algorithm stats",
            box=box.ASCII,
            height=20)
        return panel

    def _create_event_description(self):
        if self._last_event is None:
            return Panel(
                '',
                title='Last events',
                box=box.ASCII,
            )
        return Panel(
            self._last_event.message,
            title=self._last_event.name,
            box=box.ASCII,
        )

    def _create_progress_bar(self):
        completed = self._stats[ITERS_FROM_LAST_IMPROVEMENT] - 1
        left = self.algorithm.config.local_optimum_moves_threshold - completed
        completed_bar = f'[cyan]{"#" * completed}[/cyan]'
        arrow = '[cyan3]>[/cyan3]'
        left_bar = "-" * left
        return f'Steps without improvement: [{completed_bar}{arrow}{left_bar}]'

    def _create_state_column(self) -> Layout:
        layout = Layout()
        layout.split_column(
            *[Panel(str(state), title=name.capitalize().replace("_", " "), box=box.ASCII, height=5)
              for name, state in self._states.items()
              if state is not None]
        )
        return layout

    def on_local_optimum_escape(self, model: Problem, from_state: State, to_state: Union[State, None]) -> None:
        self._update_stats({
            LOCAL_OPTIMUM_ESCAPES_COUNT: self._stats[LOCAL_OPTIMUM_ESCAPES_COUNT] + 1
        })
        self._update_last_event(Event(
            name='Algorithm escaped local optimum',
            message=f'Escaped from state {from_state} to state {to_state}'
        ))
        self._update_live_display(self._create_layout(model))

    def _update_last_event(self, event: Event):
        self._last_event = event

    def on_solution(self, model: Problem, solution: State):
        self._update_last_event(Event(
            name='Solution found',
            message=f'Found solution for problem: {solution}'
        ))
        self._update_live_display(self._create_layout(model))
        self._live.stop()

    def __del__(self):
        self._live.stop()
