from typing import Any

import click
from tabulate import tabulate
from dataclasses import asdict

from python_architecture_linter.linter import lint
from modular_provider_architecture_definition.definition import project  # fixme, should not bind generic CLI to any specific definition 


@click.command()
@click.argument(
    "path",
    default="/home/brian/python-architecture-linter/modular_provider_architecture_definition/tests/cases/modular_provider_architecture",  # noqa: E501
)
@click.option("--show-success", default=0, help="Show successful validation attempts too")
def hello(path: str, show_success: bool) -> Any:
    """Runs linter and reports results."""
    results = list(lint(project, path))

    table = [asdict(result) for result in results if not result.is_valid or show_success]
    print(tabulate(table, headers="keys", tablefmt="plain"))


if __name__ == "__main__":
    hello()
