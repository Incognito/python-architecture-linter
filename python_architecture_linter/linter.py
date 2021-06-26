from typing import Iterable

from python_architecture_linter.domain_objects.validation_result import ValidationResult
from python_architecture_linter.tree_structure import Structure
from python_architecture_linter.types import LintTargetGenericType


def lint(structure: Structure, target: LintTargetGenericType) -> Iterable[ValidationResult]:
    """
    Given a structure definition, evaluate a target
    """
    for must in structure._must:  # fixme, private access
        yield must(target)

    for has in structure._has:  # fixme, private access
        # todo do something when the target is missing navigation
        next_targets = structure._navigation[has._structure_type](target)
        for next_target in next_targets:
            yield from lint(has, next_target)
