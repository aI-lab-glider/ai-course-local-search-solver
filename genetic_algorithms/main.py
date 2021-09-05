from genetic_algorithms.problems.traveling_salesman_problem import TravelingSalesmanModel
from genetic_algorithms.solvers import LocalSearchSolver
from genetic_algorithms.algorithms.hillclimbing import HillClimbing

# TODO: create a module
# Run with flag -m. Example:
# python -m genetic_algorithms.main
if __name__ == '__main__':
    model = TravelingSalesmanModel.from_benchmark('tsp_5_1')
    algorithm = HillClimbing()
    solver = LocalSearchSolver(algorithm=algorithm)
    solution = solver.solve(model)
    print(solution)
