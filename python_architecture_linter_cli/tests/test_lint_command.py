from click.testing import CliRunner

from python_architecture_linter import Structure, ValidationResult
from python_architecture_linter_cli.lint_command import lint_command_factory


def test_command_success():
    # Arrange
    # Arrange
    def must_pass(subject) -> ValidationResult:
        return ValidationResult(
            explanation="test_explanation", is_valid=True, location="test_location", validator="test_validator"
        )

    structure = Structure("TEST", {})
    structure.must([must_pass])

    command = lint_command_factory(structure)

    # Act
    runner = CliRunner()
    result = runner.invoke(command, ["FakePath"])

    # Assert
    assert result.exit_code == 0
    assert result.output == ""


def test_command_failure():
    # Arrange
    def must_fail(subject) -> ValidationResult:
        return ValidationResult(
            explanation="test_explanation", is_valid=False, location="test_location", validator="test_validator"
        )

    structure = Structure("TEST", {})
    structure.must([must_fail])

    command = lint_command_factory(structure)

    # Act
    runner = CliRunner()
    result = runner.invoke(command, ["FakePath"])

    # Assert
    assert result.exit_code == 1
    assert result.output == "test_validator\ntest_location\ntest_explanation\n\n"
