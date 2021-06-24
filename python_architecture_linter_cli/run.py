import click
from tabulate import tabulate
from dataclasses import asdict


from python_architecture_linter.project_linter import lint

@click.command()
@click.argument('path', default='/home/brian/python-architecture-linter/python_architecture_linter/tests/cases/modular_provider_architecture')  # noqa: E501
@click.option('--show-success', default=0, help='Show successful validation attempts too')
def hello(path, show_success):
    """Runs linter and reports results."""
    results = lint(path)

    table = [asdict(result) for result in results if result.is_valid == False ]
    headers = []
    print(tabulate(table, headers="keys", tablefmt="plain"))

if __name__ == '__main__':
    hello()
