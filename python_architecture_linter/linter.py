import astroid
from typing import Iterable

from python_architecture_linter.domain_objects.validation_result import ValidationResult

from python_architecture_linter.tree_structure.structure import Structure


def lint(structure, target) -> Iterable[ValidationResult]:
    for must in structure._must: # fixme, private access
        yield must(target)

    for has in structure._has: # fixme, private access
        next_targets = structure._navigation[has._structure_type](target)
        for next_target in next_targets:
            yield from lint(has, next_target)
