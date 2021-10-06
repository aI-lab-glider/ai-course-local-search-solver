import os
import json
from dataclasses import fields
from enum import Enum
from inspect import signature
from typing import Type, Union

import click
from local_search.algorithm_subscribers import (AlgorithmSubscriber,
                                                VisualizationSubscriber)
from local_search.algorithm_subscribers.algorithm_monitor import \
    AlgorithmMonitor
from local_search.algorithms import SubscribableAlgorithm
from local_search.algorithms.subscribable_algorithm import AlgorithmConfig
from local_search.algorithms.hill_climbing import HillClimbing
from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.avatar_problem.problem import AvatarProblem
from local_search.problems.base.problem import Problem
from local_search.solvers import LocalSearchSolver
from local_search.solvers.solver import SolverConfig
from rich import pretty
from rich.console import Console

# TODO
# [x] Make Avatars compatible
# [x] Change subscription logic
# [x] Rename things
# [x] Remove useless methods and fields
# [x] Add visualization from GC
# [x] Add pause button
# [] Move visualization params to config
# [] Add documentation
# [] Add tests

console = Console()
pretty.install()


@click.command('solve')
@click.option('-c', '--config_file', type=click.Path(readable=True, exists=True), help='File that provides configuration for run')
@click.option('-v', '--visualization', is_flag=True)
@click.option('-m', '--algorithm_monitor', is_flag=True)
def solve(config_file, **cli_options):
    """
    Solves a problem based on config file or cli options.
    Config file should contain same keys as defined in click.option decorator above.
    """
    options = merge_options(config_file, cli_options)
    solver = create_solver(options)
    problem_model = create_problem_model(options)
    algorithm = create_algorithm(problem_model, options)
    solution = solver.solve(problem_model, algorithm)
    console.print("Solution: ", str(solution))


def merge_options(config_file_path: str, cli_options):
    options = cli_options
    if config_file_path:
        with open(config_file_path, 'r') as config:
            config = json.load(config)
            options = {
                k: cli_options.setdefault(
                    k, None) or config.setdefault(k, None)
                for k in set([*cli_options.keys(), *config.keys()])}
    console.log("Initialized with options: ", options)
    return options


def get_or_prompt_if_not_exists_or_invalid(options, option_key: str, option_config=None) -> str:
    """
    Prompts for :param option_key: if it doesn't exists in options or if it is invalid.
    """
    option_config = option_config or {}
    if options.setdefault(option_key, None) is None:
        get_or_prompt(options, option_key, option_config)
    if option_config.setdefault('type', False):
        if isinstance(option_config['type'], click.Choice) and options[option_key] not in option_config['type'].choices:
            console.print(
                f"Value {options[option_key]} is invalid for for option {option_key} in this context.")
            get_or_prompt(options, option_key, option_config)
    return options[option_key]


def get_or_prompt(options, option_key: str, option_config=None):
    prompt = f'Select {option_key.replace("_", " ")}'
    option_config = option_config or {}
    options[option_key] = click.prompt(prompt,
                                       type=option_config.setdefault(
                                           'type', None),
                                       default=option_config.setdefault(
                                           'default', None)
                                       )
    return options[option_key]


def create_solver(options):
    config = options.setdefault('solver_config', {})
    console.print("Configuring solver", style="bold blue")
    config = create_dataclass(config, SolverConfig)
    return LocalSearchSolver(config)


def create_dataclass(options, dataclass: Type):
    dataclass_config = {}
    for field in fields(dataclass):
        if issubclass(field.type, Enum):
            value = get_or_prompt_if_not_exists_or_invalid(options, field.name, {
                'default': field.default.value
            })
            field_value = field.type(value)
        else:
            field_value = get_or_prompt_if_not_exists_or_invalid(options, field.name, {
                'default': field.default
            })

        dataclass_config[field.name] = field_value
    return dataclass(**dataclass_config)


def create_problem_model(options):
    config = options.setdefault('problem', {})
    console.print("Configuring problem", style="bold blue")
    problem_name = get_or_prompt_if_not_exists_or_invalid(config, 'name', {
        'type': click.Choice(list(Problem.problems.keys()), case_sensitive=True),
    })
    model = Problem.problems[problem_name]

    benchmark_file = get_or_prompt_if_not_exists_or_invalid(config, 'benchmark', {
        'type': click.Choice(get_benchmark_names_for_model(model), case_sensitive=True),
    })
    move_generator_name = get_or_prompt_if_not_exists_or_invalid(config, 'move_generator', {
        'type': click.Choice(list(model.get_available_move_generation_strategies()), case_sensitive=True)
    })
    return model.from_benchmark(
        benchmark_name=benchmark_file,
        move_generator_name=move_generator_name)


def get_benchmark_names_for_model(model_type: Type[Problem]):
    return os.listdir(model_type.get_path_to_benchmarks())


def create_algorithm(problem_model: Problem, options) -> SubscribableAlgorithm:
    config = options['algorithm']

    console.print("Configuring algorithm", style="bold blue")

    algo_name = assure_problem_is_solvable_by_algo(
        config, 'name', problem_model)

    get_or_prompt_if_not_exists_or_invalid(config, 'name', {
        'type': click.Choice(list(SubscribableAlgorithm.algorithms.keys()), case_sensitive=True)
    })

    algorithm_type = SubscribableAlgorithm.algorithms[algo_name]
    config_type = signature(algorithm_type).parameters['config'].annotation
    config = create_dataclass(config, config_type)

    algorithm = algorithm_type(config)
    add_alrogithm_subscribers(
        options, problem_model, algorithm)
    return algorithm


def assure_problem_is_solvable_by_algo(config, key: str, problem_model: Problem):
    available_algorithms = set(SubscribableAlgorithm.algorithms.keys())
    if isinstance(problem_model, AvatarProblem):
        available_algorithms = available_algorithms - \
            {camel_to_snake(HillClimbing.__name__)}
    algo_name = get_or_prompt_if_not_exists_or_invalid(config, key, {
        'type': click.Choice(list(available_algorithms), case_sensitive=True)
    })
    return algo_name


def add_alrogithm_subscribers(options, problem_model: Problem, algorithm: SubscribableAlgorithm):
    if options.setdefault('visualization', False):
        add_visualization_subscriber(
            problem_model, algorithm)
    if options.setdefault('algorithm_monitor', False):
        add_algorithm_monitor_subsriber(options, algorithm)


def add_visualization_subscriber(problem_model: Problem, algorithm: SubscribableAlgorithm) -> Union[SubscribableAlgorithm, AlgorithmSubscriber]:
    visualization = VisualizationSubscriber.visualizations.setdefault(type(
        problem_model), None)
    if visualization:
        visualization = visualization(algorithm=algorithm, model=problem_model)


def add_algorithm_monitor_subsriber(options, algorithm: SubscribableAlgorithm):
    config = options['algorithm']
    algorithm_config = create_dataclass(config, AlgorithmConfig)
    AlgorithmMonitor(config=algorithm_config, algorithm=algorithm)
