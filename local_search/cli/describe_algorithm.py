import click
from local_search.algorithms import SubscribableAlgorithm
from rich import inspect


@click.command('describe_algo')
@click.argument('algorithm', required=True, type=click.Choice(list(SubscribableAlgorithm.algorithms.keys())))
def describe_algorithm(algorithm):
    """
    Desribes an algorithm passed as an argument
    """
    algo = SubscribableAlgorithm.algorithms[algorithm]
    inspect(algo, methods=True)
