from genetic_algorithms.algorithm_wrappers.plot_cost_function_wrapper import CostPrinterWrapper
from genetic_algorithms.problems.traveling_salesman_problem.visualization import Visualization
from genetic_algorithms.problems.graph_coloring_problem.visualization import GraphColoringVisualization
from genetic_algorithms.solvers.solver import SolverConfig
from genetic_algorithms.problems.graph_coloring_problem.problem_model import GraphColoringModel
from genetic_algorithms.problems.traveling_salesman_problem import TravelingSalesmanModel
from genetic_algorithms.solvers import LocalSearchSolver
from genetic_algorithms.algorithms.hill_climbing import HillClimbing
from functools import reduce

# TODO: create a module
# Run with flag -m. Example:
# python -m genetic_algorithms.main
if __name__ == '__main__':
    #model = TravelingSalesmanModel.from_benchmark('tsp_for_visualization_1')
    #algorithm = HillClimbing()
    config = SolverConfig(time_limit=60)
    #solver = LocalSearchSolver(config)
    #wrappers = [CostPrinterWrapper, lambda algorithm: Visualization(config,algorithm = algorithm)]
    #solution = solver.solve(model, reduce(
    #    lambda alg, wrapper: wrapper(algorithm=alg), wrappers, algorithm))
    #print(solution)
    model = GraphColoringModel.from_benchmark('gc_1')
    algorithm = HillClimbing()
    solver = LocalSearchSolver(config)
    wrappers = [lambda algorithm: GraphColoringVisualization(config,algorithm = algorithm,model=model)]
    solution = solver.solve(model, reduce(
        lambda alg, wrapper: wrapper(algorithm=alg), wrappers, algorithm))
    print(solution)
