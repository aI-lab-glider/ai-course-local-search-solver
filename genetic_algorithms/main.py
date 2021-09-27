from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import VisualizationWrapper
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.algorithms import Algorithm

from genetic_algorithms.algorithm_wrappers.plot_cost_function_wrapper import CostPrinterWrapper
from genetic_algorithms.problems.traveling_salesman_problem.visualization import TravalingSalesmanVisualisation
from genetic_algorithms.solvers.solver import SolverConfig
from genetic_algorithms.problems.graph_coloring_problem.problem_model import GraphColoringModel
from genetic_algorithms.problems.traveling_salesman_problem import TravelingSalesmanModel
from genetic_algorithms.solvers import LocalSearchSolver
from genetic_algorithms.algorithms.hill_climbing import HillClimbing
from functools import reduce
import click
from dataclasses import dataclass


@click.command()
@click.option('-p', '--problem_model', prompt='Select a problem model: ',
              type=click.Choice(list(Model.problems.keys()),
                                case_sensitive=True),
              autocompletion=list(Model.problems.keys()),
              help='Problem that will be solved')
@click.option('-b', '--benchmark_file', prompt='Select a benchmark file',
              help='Benchmark file on which problem will be run')
@click.option('-a', '--algorithm', prompt='Select an algorithm: ',
              type=click.Choice(
                  list(Algorithm.algorithms.keys()), case_sensitive=True),
              autocompletion=list(Algorithm.algorithms.keys()),
              help='Algorithm with which problem will be solved')
@click.option('-v', '--visualization', is_flag=True)
def cli(problem_model, benchmark_file, algorithm, visualization):
    config = SolverConfig(time_limit=60)
    solver = LocalSearchSolver(config)
    problem_model = Model.problems[problem_model].from_benchmark(
        benchmark_file)
    algorithm = Algorithm.algorithms[algorithm]()
    if visualization:
        visualization_wrapper = VisualizationWrapper.visualizations[type(
            problem_model)]
        if visualization_wrapper:
            algorithm = visualization_wrapper(algorithm, config)
    solution = solver.solve(problem_model, algorithm)
    click.echo(solution)
