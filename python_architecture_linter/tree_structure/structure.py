from __future__ import annotations


class Structure:
    # todo type these params
    def __init__(self, structure_type, navigation) -> None:
        self._structure_type = structure_type
        self._navigation = navigation
        self._must = []
        self._has = []

    def must(self, must) -> Structure:
        self._must = must

    def has(self, has) -> Structure:
        self._has = has
        return self
