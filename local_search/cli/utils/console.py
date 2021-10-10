from rich.console import Console
from rich import pretty

pretty.install()
console = Console()


def print_section_name(section_name: str):
    console.print(section_name, style="bold blue")
