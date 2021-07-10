from python_architecture_linter import Structure, ValidationResult


def test_structure_is_constructable():
    # Arrange
    # Act
    sut = Structure("SUT", {})

    # Assert
    assert sut.get_structure_type() == "SUT"


def test_structure_can_have_structures():
    # Arrange
    sub_sut = Structure("SUB_SUT", {})
    sut = Structure("SUT", {})

    # Act
    sut.has([sub_sut])

    # Assert
    assert sut.get_has() == [sub_sut]


def test_structure_appends_new_has_call():
    # Arrange
    sub_sut = Structure("SUB_SUT", {})
    alt_sub_sut = Structure("ALT_SUB_SUT", {})
    sut = Structure("SUT", {})

    # Act
    sut.has([sub_sut])
    sut.has([alt_sub_sut])

    # Assert
    assert sut.get_has() == [sub_sut, alt_sub_sut]


def test_structure_appends_new_must_call():
    # Arrange
    def validator() -> ValidationResult:
        return ValidationResult(explanation="test", is_valid=True, location="test", validator="test")

    def alt_validator() -> ValidationResult:
        return ValidationResult(explanation="test", is_valid=True, location="test", validator="test")

    sut = Structure("SUT", {})
    sut.must([validator])

    # Act
    sut.must([alt_validator])

    # Assert
    assert sut.get_must() == [validator, alt_validator]


def test_structure_can_have_constraints():
    # Arrange
    def validator() -> ValidationResult:
        return ValidationResult(explanation="test", is_valid=True, location="test", validator="test")

    sut = Structure("SUT", {})

    # Act
    sut.must([validator])

    # Assert
    assert sut.get_must() == [validator]


def test_structure_can_be_navigated_from():
    # Arrange
    # Act
    def navigation():
        pass

    sut = Structure("SUT", {"SUB_SUT": navigation})

    # Assert
    assert sut.get_navigation() == {"SUB_SUT": navigation}
