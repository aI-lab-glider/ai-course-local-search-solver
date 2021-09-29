import click
from genetic_algorithms.cli.solve import solve
from genetic_algorithms.cli.describe_algorithm import describe_algorithm


@click.group()
def entry_point():
    """
    Entry point for genetic algorithms cli
    """


entry_point.add_command(solve)
entry_point.add_command(describe_algorithm)
