from __future__ import annotations

from typing import Dict, List, Callable, Any

from python_architecture_linter.domain_objects.validation_result import ValidationResult
from python_architecture_linter.types import LintTargetGenericType

NavigationCallable = Callable[[LintTargetGenericType], Any]
NavigationDict = Dict[str, NavigationCallable]

MustCallable=Callable[[LintTargetGenericType], ValidationResult]
MustList = List[MustCallable]

HasList = List[Structure]

class Structure:
    """
    A "Structure" is the abstract base node that describes individual parts of
    an entire architecture.
    """
    _must: MustList = []
    _has: HasList = []

    def __init__(self, structure_type: str, navigation: NavigationDict) -> None:
        self._structure_type = structure_type
        self._navigation = navigation

    def must(self, must: MustList) -> Structure:
        """
        What MUST prove to be true about a structure. Can be thought
        of as "Validators".
        """
        self._must = must
        return self

    def has(self, has: HasList) -> Structure:
        """
        These are sub-structures your structure MAY have. The default
        linter provided by this project expects navigating into these nodes by
        using mapping being injected via the _navigation argument in the
        constructor.
        """
        self._has = has
        return self
