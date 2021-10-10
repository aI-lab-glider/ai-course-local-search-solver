import click
from local_search.cli.utils.console import console


@click.group('compare')
def compare():
    """
    Compares few algorithms based on their file
    """


@compare.command('solutions', help='Compares solutions')
def comapre_solutions():
    console.print('Compares few solutions')


@compare.command('configurations', help='Runs solver on configuration files and compares returned solutions')
def compare_configurations():
    console.print("Compares configurations")
