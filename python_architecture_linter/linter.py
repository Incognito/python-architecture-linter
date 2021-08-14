import copy
from typing import Iterable

from python_architecture_linter.domain_objects.validation_result import ValidationResult
from python_architecture_linter.tree_structure import Structure
from python_architecture_linter.types import LintTargetGenericType


class Linter:
    """
    Given a structure definition, evaluate a target
    """

    def __init__(self, structure: Structure) -> None:
        self._structure = structure

    def lint(self, target: LintTargetGenericType) -> Iterable[ValidationResult]:
        yield from self._evaluate_must(target)
        yield from self._evaluate_has(target)

    def _evaluate_must(self, target: LintTargetGenericType):
        for must in self._structure.get_must():
            yield must(copy.deepcopy(target))

    def _evaluate_has(self, target: LintTargetGenericType):
        from_navigation = self._structure.get_navigation()

        for has_structure in self._structure.get_has():
            to_structure_type = has_structure.get_structure_type()

            try:
                navigator = from_navigation[to_structure_type]
            except KeyError:
                raise Exception(
                    f"Did not find navigation in structure from {self._structure.get_structure_type()} to {to_structure_type}"
                )

            next_targets = navigator(target)

            linter = Linter(has_structure)
            for next_target in next_targets:
                yield from linter.lint(next_target)
