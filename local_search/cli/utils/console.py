from rich.console import Console
from rich import pretty

pretty.install()


def create_console(**kwargs):
    return Console(**kwargs)


console = create_console(markup=True)


def print_section_name(section_name: str):
    console.print(section_name, style="bold blue")
