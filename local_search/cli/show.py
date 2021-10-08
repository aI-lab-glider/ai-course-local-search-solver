from pathlib import Path
from typing import Type
import click
from enum import IntEnum, auto
from local_search import problems
from local_search.algorithm_subscribers.visualization_subscribers.visualization_subscriber import StateDrawer, VisualizationSubscriber
from local_search.problems import Problem
from inspect import signature
from rich.console import Console
from enum import Enum
import sys
import pygame

from local_search.problems.base.state import State

console = Console()


@click.command('show', help='Shows solution for benchmark')
@click.option('-p', '--problem_name', type=click.Choice(list(Problem.problems.keys())), required=True, prompt=True)
@click.option('-s', '--solution_file', help='File with data for visualization', required=True, prompt=True)
def show(problem_name: str, solution_file: str):
    problem_type = Problem.problems[problem_name]
    state_type: State = signature(problem_type.random_state).return_annotation
    if state_type is State or state_type is None:
        console.print(
            f"Cannot show solution for problem {problem_name} because return type is invalid.")
    problem = problem_type.from_solution(solution_file)

    state_drawer = VisualizationSubscriber.visualizations[problem_type].create_state_drawer(
        problem)
    screen = create_screen()
    state_drawer.draw_state(screen, problem, problem.initial_solution)
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
