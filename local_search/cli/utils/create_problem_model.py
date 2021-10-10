import os
from typing import Type
from local_search.cli.utils.console import print_section_name
import click

from local_search.cli.utils.prompt import get_or_prompt_if_not_exists_or_invalid
from local_search.problems.base.problem import Problem


def create_problem_model(options):
    config = options.setdefault('problem', {})
    print_section_name("Configuring problem")
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

    goal_name = get_or_prompt_if_not_exists_or_invalid(config, 'goal', {
        'type': click.Choice(list(model.get_available_goals()), case_sensitive=True)
    })

    return model.from_benchmark(
        benchmark_name=benchmark_file,
        move_generator_name=move_generator_name,
        goal_name=goal_name)


def get_benchmark_names_for_model(model_type: Type[Problem]):
    return os.listdir(model_type.get_path_to_benchmarks())
