import os
from typing import Type
from local_search.cli.utils.console import print_section_name
import click
import inspect
from local_search.cli.utils.create_dataclass import create_dataclass

from local_search.cli.utils.prompt import get_or_prompt_if_not_exists_or_invalid
from local_search.problems.base.problem import Problem


def create_problem_model(options):
    config = options.setdefault('problem', {})

    print_section_name("Configuring problem")
    problem_name = get_or_prompt_if_not_exists_or_invalid(config, 'name', {
        'type': click.Choice(list(Problem.problems.keys()), case_sensitive=True),
    })
    model = Problem.problems[problem_name]
    params = inspect.signature(model.from_benchmark).parameters

    available_benchmarks = get_benchmark_names_for_model(model)
    default_benchmark_file = params['benchmark_name'].default
    benchmark_file = get_or_prompt_if_not_exists_or_invalid(config, 'benchmark', {
        'type': click.Choice(available_benchmarks, case_sensitive=True),
        'default': default_benchmark_file
    })

    available_move_generators = list(
        model.get_available_move_generation_strategies())
    default_move_generator_name = params['move_generator_name'].default
    default_move_generator_name = get_or_prompt_if_not_exists_or_invalid(config, 'move_generator', {
        'type': click.Choice(available_move_generators, case_sensitive=True),
        'default': default_move_generator_name
    })

    available_goals = list(model.get_available_goals())
    default_goal_name = params['goal_name'].default
    default_goal_name = get_or_prompt_if_not_exists_or_invalid(config, 'goal', {
        'type': click.Choice(available_goals, case_sensitive=True),
        'default': default_goal_name
    })

    kwargs = {
        'benchmark_name': benchmark_file,
        'move_generator_name': default_move_generator_name,
        'goal_name': default_goal_name
    }

    from_benchmark_params = inspect.signature(model.from_benchmark).parameters
    if 'config' in from_benchmark_params:
        problem_config = config.setdefault('config', {})
        kwargs['config'] = create_dataclass(
            problem_config, from_benchmark_params['config'].annotation)
    return model.from_benchmark(**kwargs)


def get_benchmark_names_for_model(model_type: Type[Problem]):
    return os.listdir(model_type.get_path_to_benchmarks())
