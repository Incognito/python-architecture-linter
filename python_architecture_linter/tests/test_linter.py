from unittest.mock import Mock

import pytest

from python_architecture_linter import Linter, Structure, ValidationResult


def test_simple_construction():
    # Arrange
    structure = Structure("STRUCTURE", {})
    # Act
    linter = Linter(structure)

    # Assert
    assert linter._structure == structure


def test_complex_construction():
    # Arrange
    sub_structure = Structure("SUB_STRUCTURE", {})
    structure = Structure("STRUCTURE", {})
    structure.has([sub_structure])

    # Act
    linter = Linter(structure)

    # Assert
    assert linter._structure == structure


def test_navigation_missing():
    # Arrange
    sub_structure = Structure("SUB_STRUCTURE", {})
    structure = Structure("STRUCTURE", {})
    structure.has([sub_structure])
    linter = Linter(structure)

    # Assert
    with pytest.raises(Exception):
        # Act
        list(linter.lint("Any target"))


def test_must():
    # Arrange
    def must_check(target) -> ValidationResult:
        return ValidationResult(explanation="test", is_valid=True, location="test", validator="test")

    structure = Structure("STRUCTURE", {})
    structure.must([must_check])
    linter = Linter(structure)

    # Act
    results = list(linter.lint("Any Target"))

    # Assert
    assert len(results) == 1
    assert results[0].explanation == "test"


def test_has():
    # Arrange

    node_navigator = Mock()
    node_navigator.return_value = "post-navigated result"

    sub_node_navigator = Mock()
    sub_node_navigator.return_value = "post-navigated result"

    sub_sub_structure = Structure("SUB_SUB_STRUCTURE", {})
    sub_structure = Structure("SUB_STRUCTURE", {"SUB_SUB_STRUCTURE": sub_node_navigator})
    sub_structure.has([sub_sub_structure])
    structure = Structure("STRUCTURE", {"SUB_STRUCTURE": node_navigator})
    structure.has([sub_structure])

    # Act
    linter = Linter(structure)
    list(linter.lint("Any random target"))

    # Assert
    assert linter._structure == structure
    assert node_navigator.called
    assert sub_node_navigator.called


@pytest.mark.skip(reason="Incomplete, missing asserts")
def test_bredth_first_walking():

    # Arrange
    structure_1_1_1_1 = Structure("1_1_1_1")
    structure_1_1_1_2 = Structure("1_1_1_2")
    structure_1_1_1_3 = Structure("1_1_1_3")
    structure_1_1_1 = Structure("1_1_1")
    structure_1_1 = Structure("1_1")
    structure_1_2 = Structure("1_2")
    structure_1_3 = Structure("1_3")
    structure_1 = Structure("1")

    structure_1.has([structure_1_1, structure_1_2, structure_1_3])
    structure_1_1.has([structure_1_1_1])
    structure_1_1_1.has([structure_1_1_1_1, structure_1_1_1_2, structure_1_1_1_3])

    # Act
    Linter(structure_1)

    # Assert
    assert False
