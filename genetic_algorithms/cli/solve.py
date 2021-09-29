from genetic_algorithms.algorithms.algorithm import AlgorithmConfig
from genetic_algorithms.algorithm_wrappers.algorithm_monitor import AlgorithmMonitor
from genetic_algorithms.helpers.camel_to_snake import camel_to_snake
import json
from dataclasses import fields
from typing import Dict, Type, Union
import typing

import click
from genetic_algorithms.algorithm_wrappers import (
    AlgorithmWrapper, VisualizationWrapper)
from genetic_algorithms.algorithms import Algorithm
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.solvers import LocalSearchSolver
from genetic_algorithms.solvers.solver import SolverConfig
from rich.console import Console
from rich import pretty
from inspect import signature

console = Console()
pretty.install()

required_options = {
    'problem_model': {
        'type': click.Choice(list(Model.problems.keys()), case_sensitive=True),
    },
    'algorithm': {
        'type': click.Choice(list(Algorithm._algorithms.keys()), case_sensitive=True)
    },
    'benchmark_file': {
        'type': click.Path(readable=True, exists=True)
    }
}

config_metadata = {
    **required_options,
    'config_file': {
        'type': click.Path(readable=True, exists=True),
    },

}


@click.command('solve')
@click.option('-c', '--config_file', type=config_metadata['config_file']['type'], help='File that provides configuration for run')
@click.option('-p', '--problem_model', type=config_metadata['problem_model']['type'], help='Problem to be solved')
@click.option('-b', '--benchmark_file', help='Benchmark file on which problem will be run')
@click.option('-a', '--algorithm', type=config_metadata['algorithm']['type'], help='Algorithm with which problem will be solved')
@click.option('-v', '--visualization', is_flag=True)
def solve(config_file, **cli_options):
    """
    Solves a problem based on config file or cli options. 
    Config file should contain same keys as defined in click.option decorator above.
    """
    options = read_options(config_file, cli_options)
    solver = create_solver(options)
    problem_model = create_problem_model(options)
    algorithm = create_algorithm(problem_model, options)
    solution = solver.solve(problem_model, algorithm)
    click.echo(solution)


def read_options(config_file_path: str, cli_options):
    options = cli_options
    if config_file_path:
        with open(config_file_path, 'r') as config:
            config = json.load(config)
            options = {k: cli_options[k] or config.setdefault(
                k, None) for k in cli_options}
    for key in required_options.keys():
        prompt_if_not_exists(options, key, required_options)
    console.log("Initialized with options: ", options)
    return options


def prompt_if_not_exists(options, key: str, metadata=None):
    if options.setdefault(key, None) is None:
        prompt = f'Select {key.replace("_", " ")}'
        option_metadata = metadata.setdefault(key, {})
        options[key] = click.prompt(prompt,
                                    type=option_metadata.setdefault(
                                        'type', None),
                                    default=option_metadata.setdefault(
                                        'default', None)
                                    )


def create_solver(options):
    options = options.setdefault('solver_config', {})
    console.print("Configuring solver", style="bold blue")
    config = populate_options_for_dataclass(options, SolverConfig)
    return LocalSearchSolver(config)


def populate_options_for_dataclass(options, dataclass: Type):
    for field in fields(dataclass):
        field_metadata = {field.name: {
            'default': field.default
        }}
        prompt_if_not_exists(options, field.name, field_metadata)
    return dataclass(**options)


def create_problem_model(options):
    return Model.problems[options['problem_model']].from_benchmark(
        options['benchmark_file'])


def create_algorithm(problem_model: Model, options) -> Union[Algorithm, AlgorithmWrapper]:
    algorithm_type = Algorithm._algorithms[options['algorithm']]

    console.print(
        f"Configuring {camel_to_snake(algorithm_type.__name__).replace('_', ' ')}", style="bold blue")

    config_type = signature(algorithm_type).parameters['config'].annotation
    config = options.setdefault('algorithm_config', {})
    config = populate_options_for_dataclass(config, config_type)
    algorithm = algorithm_type(config)
    algorithm_with_wrappers = wrap_algorithm_with_wrappers(
        options, problem_model, algorithm)
    return algorithm_with_wrappers


def wrap_algorithm_with_wrappers(options, problem_model: Model, algorithm: Algorithm) -> Union[Algorithm, AlgorithmWrapper]:
    if options['visualization']:
        algorithm = create_visualization_wrapper(
            options, problem_model, algorithm)

    return create_solution_monitor_wrapper(options, algorithm)


def create_visualization_wrapper(options, problem_model: Model, algorithm: Algorithm) -> Union[Algorithm, AlgorithmWrapper]:
    visualization_wrapper = VisualizationWrapper.visualizations.setdefault(type(
        problem_model), None)
    if visualization_wrapper:
        solver_config = SolverConfig(**options['solver_config'])
        algorithm = visualization_wrapper(
            algorithm=algorithm, config=solver_config)
    return algorithm


def create_solution_monitor_wrapper(options, algorithm: Algorithm):
    algorithm_config = AlgorithmConfig(**options['algorithm_config'])
    return AlgorithmMonitor(config=algorithm_config, algorithm=algorithm)
