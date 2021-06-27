import os
import sys

import click

from python_architecture_linter import Linter
from python_architecture_linter.tree_structure import Structure


def lint_command_factory(project_definition: Structure) -> click.Command:
    """
    Used to inject a project definition structure into the CLI command
    """

    @click.command()
    @click.argument("path", default=os.getcwd())
    @click.option("--show-success", default=0, help="Show successful validation attempts too")
    def lint_command(path: str, show_success: bool):
        """Runs linter and reports results."""
        linter = Linter(project_definition)
        results = linter.lint(path)

        def display(result):
            if result.is_valid:
                click.secho(result.validator, bg="green")
            else:
                click.secho(result.validator, bg="red")
            click.echo(result.location)
            click.echo(result.explanation)
            click.echo("")

        exit_code = 0
        for result in results:
            if not result.is_valid or show_success:
                display(result)
            if not result.is_valid:
                exit_code = 1

        sys.exit(exit_code)

    return lint_command
