import json
import os
from pathlib import Path
from typing import List
import click
from local_search.cli.utils.console import console
from local_search.cli.utils.create_algorithm import create_algorithm
from local_search.cli.utils.create_problem_model import create_problem_model
from local_search.cli.utils.create_solver import create_solver
from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.solvers.solution import Solution
from rich.table import Table
from rich import box


@click.group('compare')
def compare():
    """
    Compares few algorithms based on their file
    """


@compare.command('solutions', help='Compares solutions')
@click.option('-p', '--path', type=click.Path(exists=True, readable=True), help='Path to directory with solutions that should be compared')
def comapre_solutions(path):
    solutions_dir = Path(path)
    solutions = [Solution.from_json(solutions_dir/file)
                 for file in os.listdir(solutions_dir)]
    comparison = create_comparison_for_solutions(solutions)
    console.print(comparison)


@compare.command('configurations', help='Runs different configurations on preconfigured solver and problem and compares returned solutions')
@click.option('-c', '--config', type=click.Path(exists=True, readable=True), help='Path to directory with compare config')
def compare_configurations(config):
    with open(config, 'r') as config:
        config = json.load(config)
    console.log("Compares configurations with config: ", config)
    common_config = config["common"]
    solver = create_solver(common_config)
    solutions = []
    changeable_config = {
        'problem': common_config.setdefault('problem', {}),
        'algorithm': common_config.setdefault('algorithm', {})
    }
    # Adding empty dict to solve for base configuration (i.e configuration without overwrites).
    for idx, overwrite in enumerate([{}, *config["overwrites"]]):
        console.print(f"Started solving for {idx} overwrite ...")
        overwrited_config = {
            'problem': {
                **changeable_config['problem'],
                **overwrite.setdefault('problem', {})
            },
            'algorithm': {
                **changeable_config['algorithm'],
                **overwrite.setdefault('algorithm', {})
            }
        }
        problem = create_problem_model(overwrited_config)
        algorithm = create_algorithm(problem, overwrited_config)
        solution = solver.solve(problem, algorithm)
        solutions.append(solution)
        console.print(f"End solving for {idx} overwrite ...")

    table = create_comparison_for_solutions(solutions)
    console.print(table)


def create_comparison_for_solutions(solutions: List[Solution]):
    table = Table(title='Solutions comparison', box=box.ASCII)
    columns = ['Algorithm name',
               'Problem name',
               'Move generator name',
               'Goal name',
               'Objective value',
               'Time until optimum found',
               'Local optimum escapes count',
               'Explored states count']
    for column in columns:
        table.add_column(column, justify="right")

    for solution in solutions:
        table.add_row(
            str(solution.statistics.algorithm_name),
            str(camel_to_snake(type(solution.problem).__name__)),
            str(camel_to_snake(type(solution.problem.move_generator).__name__)),
            str(camel_to_snake(type(solution.problem.goal).__name__)),
            str(solution.problem.human_readable_objective_for(solution.state)),
            str(solution.statistics.time_untill_optimum_found),
            str(solution.statistics.local_optimum_escapes_count),
            str(solution.statistics.explored_states_count)
        )
    return table
