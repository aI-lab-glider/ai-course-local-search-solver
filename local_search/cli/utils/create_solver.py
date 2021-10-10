
from local_search.cli.utils.console import print_section_name
from local_search.cli.utils.create_dataclass import create_dataclass
from local_search.solvers.local_search_solver import LocalSearchSolver
from local_search.solvers.solver_config import SolverConfig


def create_solver(options):
    config = options.setdefault('solver_config', {})
    print_section_name("Configuring solver")
    config = create_dataclass(config, SolverConfig)
    return LocalSearchSolver(config)
