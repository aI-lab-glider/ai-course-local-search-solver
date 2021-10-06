import click
from local_search.cli.solve import solve
from local_search.cli.describe_algorithm import describe_algorithm


@click.group()
def entry_point():
    """
    Entry point for genetic algorithms cli
    """


entry_point.add_command(solve)
entry_point.add_command(describe_algorithm)
