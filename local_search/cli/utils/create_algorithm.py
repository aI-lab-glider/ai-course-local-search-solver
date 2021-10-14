
import click
from local_search.algorithm_subscribers.visualization_subscribers.visualization_subscriber import VisualizationSubscriber
from local_search.algorithms.hill_climbing.hill_climbing import HillClimbing
from local_search.algorithms.subscribable_algorithm import SubscribableAlgorithm
from local_search.cli.utils.console import print_section_name
from local_search.cli.utils.create_dataclass import create_dataclass
from local_search.cli.utils.prompt import get_or_prompt_if_not_exists_or_invalid
from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.helpers.get_type_for_param import get_type_for_param
from local_search.problems.avatar_problem.problem import AvatarProblem
from local_search.problems.base.problem import Problem


def create_algorithm(problem_model: Problem, options) -> SubscribableAlgorithm:
    config = options['algorithm']

    print_section_name("Configuring algorithm")

    algo_name = assure_problem_is_solvable_by_algo(
        config, 'name', problem_model)

    get_or_prompt_if_not_exists_or_invalid(config, 'name', {
        'type': click.Choice(list(SubscribableAlgorithm.algorithms.keys()), case_sensitive=True)
    })

    algorithm_type = SubscribableAlgorithm.algorithms[algo_name]
    config_type = get_type_for_param(algorithm_type, 'config')
    config = create_dataclass(config, config_type)
    algorithm = algorithm_type(config)
    add_algorithm_subscribers(
        options, problem_model, algorithm)
    return algorithm


def assure_problem_is_solvable_by_algo(config, key: str, problem_model: Problem):
    available_algorithms = set(SubscribableAlgorithm.algorithms.keys())
    if isinstance(problem_model, AvatarProblem):
        available_algorithms = available_algorithms - \
            {camel_to_snake(HillClimbing.__name__)}
    algo_name = get_or_prompt_if_not_exists_or_invalid(config, key, {
        'type': click.Choice(list(available_algorithms), case_sensitive=True)
    })
    return algo_name


def add_algorithm_subscribers(options, problem_model: Problem, algorithm: SubscribableAlgorithm):
    if options.setdefault('visualization', {}).setdefault('enabled', False):
        add_visualization_subscriber(
            options['visualization'], problem_model, algorithm)


def add_visualization_subscriber(options, problem_model: Problem, algorithm: SubscribableAlgorithm) -> None:
    print_section_name("Configuring visulization")
    visualization = VisualizationSubscriber.visualizations.setdefault(type(
        problem_model), None)
    if visualization:
        visualization_params = {
            'model': problem_model
        }
        config_type = get_type_for_param(visualization, 'config')
        if config_type:
            visualization_params['config'] = create_dataclass(
                options, config_type)
        visualization = visualization(**visualization_params)
        algorithm.subscribe(visualization)
