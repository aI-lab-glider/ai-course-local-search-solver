import os
from pathlib import Path
from typing import List
import click
from local_search.cli.utils.console import console
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
def comapre_solutions():
    solutions_dir = Path('solutions')
    solutions = [Solution.from_json(solutions_dir/file)
                 for file in os.listdir(solutions_dir)]
    comparison = create_comparison_for_solutions(solutions)
    console.print(comparison)


@compare.command('configurations', help='Runs solver on configuration files and compares returned solutions')
def compare_configurations():
    console.print("Compares configurations")


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
