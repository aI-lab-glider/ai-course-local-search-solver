import click
from local_search.cli.compare import compare
from local_search.cli.solve import solve
from local_search.cli.describe_algorithm import describe_algorithm
from local_search.cli.show import show


@click.group()
def entry_point():
    """
    Entry point for genetic algorithms cli
    """


entry_point.add_command(solve)
entry_point.add_command(describe_algorithm)
entry_point.add_command(show)
entry_point.add_command(compare)
