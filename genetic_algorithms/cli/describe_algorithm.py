import click
from genetic_algorithms.algorithms import Algorithm
from rich import inspect


@click.command('describe_algo')
@click.argument('algorithm', required=True, type=click.Choice(list(Algorithm._algorithms.keys())))
def describe_algorithm(algorithm):
    """
    Desribes an algorithm passed as an argument
    """
    algo = Algorithm._algorithms[algorithm]
    inspect(algo, methods=True)
