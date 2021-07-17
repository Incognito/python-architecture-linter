import os
import sys
from functools import partial
from typing import Callable, Iterable, List

import click

from python_architecture_linter import Linter, Structure, ValidationResult
from python_architecture_linter_cli.steps import (
    display_results,
    filter_out_excuses,
    filter_out_successes,
    identity,
    truncate_project_path_from_locations,
    write_excuses_to_file,
)


def get_lint_results(project_definition, path) -> Iterable[ValidationResult]:
    linter = Linter(project_definition)
    yield from linter.lint(path)


def determine_exit_code(is_valid_flags: Iterable[bool]) -> int:
    for is_valid in is_valid_flags:
        if not is_valid:
            return 1

    return 0


def lint_command_factory(project_definition: Structure) -> click.Command:
    """
    Used to inject a project definition structure into the CLI command
    """

    @click.command()
    @click.argument("path", default=os.getcwd())
    @click.option("--show-success", default=False, help="Show successful validation attempts too")
    @click.option("--with-excuses", default=False, help="Excuse results stored in excuses.yml")
    @click.option("--excuse-path", default="", help="path of excuses.yml")
    @click.option("--write-excuses-file", default=False, help="Replace the excuse file with all violations")
    def lint_command(
        path: str,
        show_success: bool,
        with_excuses: bool,
        excuse_path: str,
        write_excuses_file: bool,
    ):
        """Runs linter and reports results."""

        excuse_path = path + "/excuses.yml" if excuse_path == "" else excuse_path

        # Mypy cannot understand partials
        steps: List[Callable[[Iterable[ValidationResult]], Iterable[ValidationResult]]] = [
            partial(truncate_project_path_from_locations, path),  # type: ignore
            filter_out_successes if not show_success else identity,
            partial(filter_out_excuses, excuse_path) if with_excuses else identity,  # type: ignore
            display_results,
            partial(write_excuses_to_file, excuse_path) if write_excuses_file else identity,  # type: ignore
        ]

        results = get_lint_results(project_definition, path)
        for step in steps:
            # Mypy cannot understand partials
            results = step(results)  # type: ignore

        # Runs the generator over the entire data-set and reduces each dataclass to one boolean
        is_valid_flags = [result.is_valid for result in results]
        exit_code = determine_exit_code(is_valid_flags)

        sys.exit(exit_code)

    return lint_command
