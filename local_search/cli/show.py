from pathlib import Path
import sys

import click
from local_search.solvers.solution import Solution
import pygame
from local_search.algorithm_subscribers.visualization_subscribers.visualization_subscriber import VisualizationSubscriber


@click.command('show', help='Shows solution for benchmark')
@click.argument('path_to_solution', type=click.Path(exists=True, readable=True), required=True)
def show(path_to_solution: str):
    solution = Solution.from_json(Path(path_to_solution))
    state_drawer = VisualizationSubscriber.visualizations[type(solution.problem)].create_state_drawer(
        solution.problem)
    screen = create_screen()
    state_drawer.draw_state(screen, solution.problem, solution.state)
    pygame.display.flip()
    freeze()


def create_screen():
    pygame.init()
    return pygame.display.set_mode((800, 800))


def freeze():
    while True:
        handle_pygame_events()


def handle_pygame_events():
    exit_on = [pygame.QUIT, pygame.K_ESCAPE]
    for event in pygame.event.get():
        if event.type in exit_on:
            sys.exit(0)
