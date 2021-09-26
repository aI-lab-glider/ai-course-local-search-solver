from genetic_algorithms.algorithm_wrappers.plot_cost_function_wrapper import CostPrinterWrapper
from genetic_algorithms.solvers.solver import SolverConfig
from genetic_algorithms.problems.graph_coloring_problem.problem_model import GraphColoringModel
from genetic_algorithms.problems.traveling_salesman_problem import TravelingSalesmanModel
from genetic_algorithms.problems.avatar_problem.problem_model import AvatarModel
from genetic_algorithms.solvers import LocalSearchSolver
from genetic_algorithms.algorithms.simulated_annealing import SimulatedAnnealingConfig
from genetic_algorithms.algorithms.hill_climbing import HillClimbing
from genetic_algorithms.algorithms.simulated_annealing import SimulatedAnnealing
from genetic_algorithms.algorithms.first_choice_hill_climbing import FirstChoiceHillClimbing
from functools import reduce

# TODO: create a module
# Run with flag -m. Example:
# python -m genetic_algorithms.main
if __name__ == '__main__':
    # model = TravelingSalesmanModel.from_benchmark('tsp_5_1')
    # algorithm = HillClimbing()
    # config = SolverConfig(time_limit=60)
    # solver = LocalSearchSolver(config)
    # wrappers = [CostPrinterWrapper]
    # solution = solver.solve(model, reduce(
    #     lambda alg, wrapper: wrapper(algorithm=alg), wrappers, algorithm))
    model = AvatarModel.from_benchmark('monalisa.jpg')
    algorithm = FirstChoiceHillClimbing()
    config = SolverConfig(time_limit=60)
    solver = LocalSearchSolver(config)
    solution = solver.solve(model, algorithm)
    solution.show_image()
    # model = GraphColoringModel.from_benchmark('gc_1')
    # algorithm = FirstChoiceHillClimbing()
    # config = SolverConfig(time_limit=60)
    # solver = LocalSearchSolver(config)
    # solution = solver.solve(model, algorithm)
    # print(solution)
