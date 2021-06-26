import os
from dataclasses import asdict
from typing import Any

import click
from modular_provider_architecture_definition.definition import (  # fixme, should not bind generic CLI which is provided a specific definition
    project,
)

from python_architecture_linter.linter import lint


@click.command()
@click.argument(
    "path",
    default=os.path.dirname(os.path.realpath(__file__))
    + "/../modular_provider_architecture_definition/tests/cases/modular_provider_architecture",  # noqa: E501
)
@click.option("--show-success", default=0, help="Show successful validation attempts too")
def hello(path: str, show_success: bool) -> Any:
    """Runs linter and reports results."""
    results = list(lint(project, path))

    def display(result):
        if result.is_valid:
            click.secho(result.validator, bg="green")
        else:
            click.secho(result.validator, bg="red")
        click.echo(result.location)
        click.echo(result.explanation)
        click.echo("")

    [display(result) for result in results if not result.is_valid or show_success]


if __name__ == "__main__":
    hello()
