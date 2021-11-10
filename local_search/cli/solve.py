import os
from pathlib import Path

import click
from local_search.cli.utils.console import console
from local_search.cli.utils.create_algorithm import create_algorithm
from local_search.cli.utils.create_problem_model import create_problem_model
from local_search.cli.utils.create_solver import create_solver
from local_search.cli.utils.markdown_command import MarkdownCommand
from local_search.cli.utils.merge_options import merge_options
from local_search.cli.utils.prompt import \
    get_or_prompt_if_not_exists_or_invalid

import random
random.seed(42)


@click.command('solve', cls=MarkdownCommand)
@click.option('-c', '--config_file', type=click.Path(readable=True, exists=True), help='File that provides configuration for run')
@click.option('-v', '--visualization', is_flag=True)
@click.option('-m', '--algorithm_monitor', is_flag=True)
def solve(config_file, **cli_options):
    """
    # Solve

    Solves a problem based on configuration provided in a _configuration file_.
    **Each** configuration file should have a following sections (headers have the same name as key in the configuration file).
    In case, if some param will be missing or invalid, user will be prompt for it.

    ## problem
    Describes for problem that should be solved. 
    Common params:

        - name: name problem in snake case. All available problems could be found in :see local_search.problems:
        - benchmark: text file that describes problem
        - move_generator: name of move generator responsible for generation of moves to generate neighbourhood
        - goal: goal that should be optimized

    There also could be additional parameters in case if problem requires it (e.g. :see `LimitedAvatarProblem`:).

    ## algorithm
    Describes algorithm that will be used to solve a problem.
    Common params:

        - name: name of algorirthm in snake case. All available algorithms could be found in :see local_search.algorithms:
        - local_optimum_moves_threshold: if reached, algorithm considers itself as it is in optimum.
        - local_optimum_escape_max: max amount of escapes from local optimum. If exceed, algorithm stops it work and returns a solution.

    Additional params: if exists, they should be provided in dataclass, that derives from :see `AlgorithmConfig`:

    ## solver_config
    Describes how solver should behave.
    Params: 

        - time_limit: maximum amount of time solver can run.
        - show_statistics: if solver should show current statistics of algorithm.

    ## visualization
    Describes how visualization should behave (if exists).
    Params: 

        - enabled: is enabled
        - min_time_between_steps: min time, current state should be on screen, untill next state vizualization will be shown
        - show_only_soution: if visualization is enabled, configures if it should be visible during solving or only in the end.

    ## save_solution
    If solution should be saved.


    # Example
    See example config in reference config.
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
            should_save = click.confirm(
                f"There is already a solution with to problem with this name, benchmark, move generator and goal. Do you want to save this solution?", default=True)
            if not should_save:
                return
            should_overwrite = click.confirm("Do you want to overwrite it?")
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
