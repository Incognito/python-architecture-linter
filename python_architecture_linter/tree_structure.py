from __future__ import annotations

from typing import Any, Callable, Dict, List

from python_architecture_linter.domain_objects.validation_result import ValidationResult
from python_architecture_linter.types import LintTargetGenericType

NavigationCallable = Callable[[LintTargetGenericType], Any]
NavigationDict = Dict[str, NavigationCallable]

MustCallable = Callable[[LintTargetGenericType], ValidationResult]
MustList = List[MustCallable]


class Structure:
    """
    A "Structure" is the abstract base node that describes individual parts of
    an entire architecture.
    """

    def __init__(self, structure_type: str, navigation: NavigationDict) -> None:
        self._structure_type = structure_type
        self._navigation = navigation
        self._must: MustList = []
        self._has: List[Structure] = []

    def must(self, must: MustList) -> Structure:
        """
        Adds requirements for what MUST prove to be true about a
        structure. Can be thought of as "Validators".

        Example: A router in a web application MUST define web API
        routes
        """
        self._must += must
        return self

    def has(self, has: List[Structure]) -> Structure:
        """
        Adds sub-structures to what your structure MAY have. The default
        linter provided by this project expects navigating into these
        nodes by using mapping being injected via the _navigation
        argument in the constructor.

        Example: a project MAY have files, it might also be empty, but
        you expect it to be there.
        """
        self._has += has
        return self

    def get_must(self) -> MustList:
        return self._must

    def get_has(self) -> List[Structure]:
        return self._has

    def get_navigation(self) -> NavigationDict:
        return self._navigation

    def get_structure_type(self) -> str:
        return self._structure_type
