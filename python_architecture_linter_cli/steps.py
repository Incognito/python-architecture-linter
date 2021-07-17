from dataclasses import asdict
from typing import Iterable

import click
from ruamel.yaml import YAML

from python_architecture_linter import ValidationResult


def truncate_project_path_from_locations(
    project_path: str, results: Iterable[ValidationResult]
) -> Iterable[ValidationResult]:
    for result in results:
        props = asdict(result)
        props["location"] = props["location"].replace(project_path, "./")
        yield ValidationResult(**props)


def filter_out_successes(results: Iterable[ValidationResult]) -> Iterable[ValidationResult]:
    yield from (result for result in results if not result.is_valid)


def filter_out_excuses(excuses_path: str, results: Iterable[ValidationResult]) -> Iterable[ValidationResult]:
    yaml = YAML()
    yaml.register_class(ValidationResult)
    try:
        with open(excuses_path, "r") as infile:
            saved_excuses = yaml.load(infile)
    except IOError:
        saved_excuses = []

    if results is None:
        saved_excuses = []

    yield from (result for result in results if result not in set(saved_excuses))


def display_result(result: ValidationResult) -> None:
    if result.is_valid:
        click.secho(result.validator, bg="green", bold=True)
        click.secho(result.location, bg="green")
    else:
        click.secho(result.validator, bg="red", bold=True)
        click.secho(result.location, bg="red")
    click.echo(result.explanation)
    click.echo("")
    click.echo("")


def display_results(results: Iterable[ValidationResult]) -> Iterable[ValidationResult]:
    for result in results:
        display_result(result)
        yield result


def write_excuses_to_file(target_file: str, results: Iterable[ValidationResult]) -> Iterable[ValidationResult]:
    yaml = YAML()
    yaml.register_class(ValidationResult)

    all_results = list(results)  # Not nice for memory, not sure how to make the yml writer stream changes either.
    with open(target_file, "w") as outfile:
        yaml.dump(all_results, outfile)

    yield from all_results


def identity(results: Iterable[ValidationResult]) -> Iterable[ValidationResult]:
    yield from results
