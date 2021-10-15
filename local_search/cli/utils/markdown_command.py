
import click
from local_search.cli.utils.console import console
from rich.markdown import Markdown


class MarkdownCommand(click.Command):
    def format_help_text(self, *_):
        formatted_markdown = Markdown(self.help)
        console.print(formatted_markdown)
