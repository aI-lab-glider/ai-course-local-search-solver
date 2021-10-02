import os
import json
from dataclasses import fields
from enum import Enum
from inspect import signature
from typing import Type, Union

import click
from genetic_algorithms.algorithm_wrappers import (AlgorithmWrapper,
                                                   VisualizationWrapper)
from genetic_algorithms.algorithm_wrappers.algorithm_monitor import \
    AlgorithmMonitor
from genetic_algorithms.algorithms import Algorithm
from genetic_algorithms.algorithms.algorithm import AlgorithmConfig
from genetic_algorithms.helpers.camel_to_snake import camel_to_snake
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.solvers import LocalSearchSolver
from genetic_algorithms.solvers.solver import SolverConfig
from rich import pretty
from rich.console import Console

# TODO
# [x] Add reference config.
# [] Make perfect TSP:
# [] Add new move generators
# [] Add algorithms logic
# [] Add tests

console = Console()
pretty.install()


@click.command('solve')
@click.option('-c', '--config_file', type=click.Path(readable=True, exists=True), help='File that provides configuration for run')
@click.option('-v', '--visualization', is_flag=True)
@click.option('-s', '--solution_monitor', is_flag=True)
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


def prompt_if_not_exists(options, option_key: str, option_config=None) -> str:
    """
    Prompts for :param option_key: if it doesn't exists in options.
    """
    if options.setdefault(option_key, None) is None:
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
        field_metadata = {
            'default': field.default if not issubclass(field.type, Enum) else field.default.value
        }
        field_value = prompt_if_not_exists(options, field.name, field_metadata)
        dataclass_config[field.name] = field_value
    return dataclass(**dataclass_config)


def create_problem_model(options):
    config = options.setdefault('problem', {})
    console.print("Configuring problem", style="bold blue")
    problem_name = prompt_if_not_exists(config, 'name', {
        'type': click.Choice(list(Model.problems.keys()), case_sensitive=True),
    })
    model = Model.problems[problem_name]

    benchmark_file = prompt_if_not_exists(config, 'benchmark', {
        'type': click.Choice(get_benchmark_names_for_model(model), case_sensitive=True),
    })

    move_generator_name = prompt_if_not_exists(config, 'move_generator', {
        'type': click.Choice(list(model.get_available_move_generation_strategies()), case_sensitive=True)
    })
    return model.from_benchmark(
        benchmark_name=benchmark_file,
        move_generator_name=move_generator_name)


def get_benchmark_names_for_model(model_type: Type[Model]):
    return os.listdir(model_type.get_path_to_benchmarks())


def create_algorithm(problem_model: Model, options) -> Union[Algorithm, AlgorithmWrapper]:
    config = options['algorithm']
    console.print("Configuring algorithm", style="bold blue")

    algo_name = prompt_if_not_exists(config, 'name', {
        'type': click.Choice(list(Algorithm.algorithms.keys()), case_sensitive=True)
    })
    algorithm_type = Algorithm.algorithms[algo_name]

    config_type = signature(algorithm_type).parameters['config'].annotation
    config = create_dataclass(config, config_type)

    algorithm = algorithm_type(config)
    algorithm_with_wrappers = wrap_algorithm_with_wrappers(
        options, problem_model, algorithm)
    return algorithm_with_wrappers


def wrap_algorithm_with_wrappers(options, problem_model: Model, algorithm: Algorithm) -> Union[Algorithm, AlgorithmWrapper]:
    if options.setdefault('visualization', False):
        algorithm = create_visualization_wrapper(
            options, problem_model, algorithm)
    if options.setdefault('algorithm_monitor', False):
        algorithm = create_solution_monitor_wrapper(options,
                                                    algorithm)
    return algorithm


def create_visualization_wrapper(options, problem_model: Model, algorithm: Algorithm) -> Union[Algorithm, AlgorithmWrapper]:
    visualization_wrapper = VisualizationWrapper.visualizations.setdefault(type(
        problem_model), None)
    if visualization_wrapper:
        solver_config = SolverConfig(**options['solver_config'])
        algorithm = visualization_wrapper(
            algorithm=algorithm, config=solver_config)
    return algorithm


def create_solution_monitor_wrapper(options, algorithm: Algorithm):
    config = options['algorithm']
    algorithm_config = create_dataclass(config, AlgorithmConfig)
    return AlgorithmMonitor(config=algorithm_config, algorithm=algorithm)
