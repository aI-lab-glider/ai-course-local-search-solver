import os
from pathlib import Path

import click
from local_search.cli.utils.console import console
from local_search.cli.utils.create_algorithm import create_algorithm
from local_search.cli.utils.create_problem_model import create_problem_model
from local_search.cli.utils.create_solver import create_solver
from local_search.cli.utils.merge_options import merge_options
from local_search.cli.utils.prompt import \
    get_or_prompt_if_not_exists_or_invalid

import random
random.seed(42)


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
    if get_or_prompt_if_not_exists_or_invalid(options, 'save_solution', {
        'type': bool,
        'default': True
    }):
        path = create_path_to_save_solution(options)
        while path.exists():
            should_overwrite = click.confirm(
                f"There is already a solution saved to {path}. Do you want to overwrite it?", default=True)
            if not should_overwrite:
                new_name = click.prompt(
                    f'New name to save in folder {path.parent} (without extension)', type=str)
                path = path.parent/f'{new_name}.json'
            else:
                break
        solution.to_json(path)
        console.print(f'Solution is saved to file {path}')


def create_path_to_save_solution(config):
    solution_dir = Path("student_solutions")
    if not solution_dir.exists():
        os.mkdir(solution_dir)
    file_name = 'solution'

    name_fragments = {
        'problem': ['name', 'benchmark', 'move_generator', 'goal'],
        'algorithm': ['name']
    }
    for section in name_fragments:
        for key in name_fragments[section]:
            file_name += f'_{config[section][key]}'
    return solution_dir/f'{file_name}.json'
